import glob
import importlib
import os
import pkgutil
import traceback
from contextlib import contextmanager
from typing import Any

from .cache import cache_to_local
from .parallel import as_completed, submit


def discover_plugins_simple(module):
    """Discover uetools plugins"""
    path = module.__path__
    name = module.__name__

    plugins = {}

    for _, name, _ in pkgutil.iter_modules(path, name + "."):
        plugins[name] = importlib.import_module(name)

    return plugins


def discover_plugins_parallel(module):
    """Discover uetools plugins"""
    path = module.__path__
    name = module.__name__

    plugins = {}

    futures = dict()
    for _, name, _ in pkgutil.iter_modules(path, name + "."):
        f = submit(importlib.import_module, name)
        futures[f] = name

    for future in as_completed(futures):
        name = futures[future]
        module = future.result()
        plugins[name] = module

    return plugins


def discover_plugins(module):
    """Discover uetools plugins"""
    return discover_plugins_parallel(module)


def discover_plugin_commands_no_cache(module):
    modules = discover_plugins(module)
    all_commands = []

    for _, module in modules.items():
        if hasattr(module, "COMMANDS"):
            commands = getattr(module, "COMMANDS")

            if not isinstance(commands, list):
                _norm_name(commands, module.__file__)
                commands = [commands]

            all_commands.extend(commands)

    return all_commands


def _norm_name(cls, module_path):
    _, tail = os.path.split(module_path)
    cmd = tail.replace(".py", "")

    if isinstance(cls, list):
        return cls

    if not hasattr(cls, "name"):
        cls.name = cmd

    return cls


def _resolve_factory_module(base_file_name, base_module, function_name, module_path):
    module_file = module_path.split(os.sep)[-1]

    # module_file is not always a file, it can be a folder
    if module_file == base_file_name:
        return

    module_name = module_file.split(".py")[0]
    try:
        path = ".".join([base_module, module_name])

        module = __import__(path, fromlist=[""])

        if hasattr(module, function_name):
            return _norm_name(getattr(module, function_name), module_path)
        elif not module.endswith(".data"):
            print(f"Found no commands in {path}")
    except ImportError:
        print(traceback.format_exc())
        return


def fetch_factories_parallel(
    registry, base_module, base_file_name, function_name="COMMANDS"
):
    """Loads all the defined commands"""

    module_path = os.path.dirname(os.path.abspath(base_file_name))
    paths = list(glob.glob(os.path.join(module_path, "[A-Za-z]*"), recursive=True))

    futures = []
    for path in paths:
        args = (base_file_name, base_module, function_name, path)
        futures.append(submit(_resolve_factory_module, *args))

    for future in as_completed(futures):
        cmd = future.result()

        if cmd is not None:
            registry.insert_commands(cmd)


def fetch_factories_single(
    registry, base_module, base_file_name, function_name="COMMANDS"
):
    """Loads all the defined commands"""
    module_path = os.path.dirname(os.path.abspath(base_file_name))

    for module_path in glob.glob(
        os.path.join(module_path, "[A-Za-z]*"), recursive=False
    ):
        cmd = _resolve_factory_module(
            base_file_name, base_module, function_name, module_path
        )
        if cmd is not None:
            registry.insert_commands(cmd)


def fetch_factories(registry, base_module, base_file_name, function_name="COMMANDS"):
    fetch_factories_parallel(registry, base_module, base_file_name, function_name)
    # fetch_factories_single(registry, base_module, base_file_name, function_name)


def discover_from_plugins_commands(registry, module, function_name="COMMANDS"):
    """Imports all commands for the plugins we found"""
    plugins = discover_plugins(module)

    for _, plugin in plugins.items():
        if hasattr(plugin, function_name):
            plugin_commands = getattr(plugin, function_name)

            registry.insert_commands(plugin_commands)


# pylint: disable=too-few-public-methods
class CommandRegistry:
    """Simple class to keep track of all the commands we find"""

    def __init__(self):
        self.found_commands = {}

    def insert_commands(self, cmds):
        """Insert a command into the registry makes sure it is unique"""
        if not isinstance(cmds, list):
            cmds = [cmds]

        for cmdcls in cmds:
            cmd = cmdcls()

            if cmd.name != cmd.name.strip():
                print(f"Warning: {cmd.name} has white space before or after the name")

            assert (
                cmd.name not in self.found_commands
            ), f"Duplicate command name: {cmd.name}"
            self.found_commands[cmd.name] = cmd

    def fix_nondeterminism(self):
        data = self.__getstate__()
        self.__setstate__(data)

    def __getstate__(self):
        return sorted(self.found_commands.items(), key=lambda x: x[0])

    def __setstate__(self, d):
        self.found_commands = {k: v for k, v in d}


def discover_module_commands_no_cache(module, plugin_module=None):
    """Discover all the commands we can find (plugins and built-in)"""
    registry = CommandRegistry()

    fetch_factories(registry, module.__name__, module.__file__)

    if plugin_module is not None:
        discover_from_plugins_commands(registry, plugin_module)

    registry.fix_nondeterminism()
    return registry


def discover_plugin(location=None):
    def _(module):
        nonlocal location

        if location is None:
            location = module.__name__

        cached_call = cache_to_local(module.__name__, location)(
            discover_plugin_commands_no_cache
        )
        return cached_call(module)

    return _


def discover_module(location=None):
    def _(module, plugin_module=None):
        nonlocal location

        if location is None:
            location = module.__name__

        cached_call = cache_to_local("commands", location)(
            discover_module_commands_no_cache
        )
        return cached_call(module, plugin_module)

    return _


class CallRef:
    def __init__(self, original) -> None:
        self.call = original

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.call(*args, *kwds)


discover_plugin_commands = CallRef(discover_plugin())
discover_module_commands = CallRef(discover_module())


@contextmanager
def with_cache_location(location):
    global discover_plugin_commands, discover_module_commands
    old_plugin = discover_plugin_commands.call
    old_module = discover_module_commands.call

    discover_plugin_commands.call = discover_plugin(location)
    discover_module_commands.call = discover_module(location)

    yield

    discover_plugin_commands.call = old_plugin
    discover_module_commands.call = old_module
