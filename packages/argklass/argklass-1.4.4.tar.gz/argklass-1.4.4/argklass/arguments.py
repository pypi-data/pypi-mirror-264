"""Simplified SimpleParsing because it was not simple"""
from __future__ import annotations

import argparse
import dataclasses
import enum
import typing
from copy import deepcopy
from dataclasses import MISSING, fields, is_dataclass
from typing import get_type_hints

from .cache import wait_cache_update
from .docstring import DocstringIterator

forward_refs_to_types = {
    "tuple": typing.Tuple,
    "set": typing.Set,
    "dict": typing.Dict,
    "list": typing.List,
    "type": typing.Type,
}


class Subparser:
    pass


def argument(
    default=MISSING,
    default_factory=MISSING,
    init=True,
    repr=True,
    hash=None,
    compare=True,
    metadata=None,
    action=None,
    **kwargs,
):
    """
    Build a field that store argparse argument metadata

    Examples
    --------

    .. code-block:: python

       @dataclass
       class MyParser:
           arg = argument("--args", type=int, default=20, help="My argument")

    """
    # argparse.ArgumentParser().add_argument
    if metadata is not None:
        kwargs.update(metadata)

    if isinstance(default, (list, dict)):
        default_value = default

        def default_factory():
            return deepcopy(default_value)

        default = MISSING

    kwargs["_kind"] = "argument"

    if action == "store_true":
        default = False

    if action == "store_false":
        default = True

    if action is not None:
        kwargs["action"] = action

    if default is not MISSING:
        kwargs["default"] = default

    if default_factory is not MISSING:
        kwargs["default"] = default_factory()

    return dataclasses.field(  #
        default=default,  #
        default_factory=default_factory,  #
        init=init,  #
        repr=repr,  #
        hash=hash,  #
        compare=compare,  #
        metadata=kwargs,  #
    )


def deduceable(default, vtype=None, required=True, **kwargs):
    kwargs["_kind"] = "argument"

    value = default()
    if value is not None:
        kwargs["default"] = value
        kwargs["type"] = vtype or type(value)
    else:
        kwargs["required"] = required

    return dataclasses.field(default=value, metadata=kwargs)


def group(default, help=None, **kwargs):
    # argparse.ArgumentParser().add_argument_group()
    kwargs["_kind"] = "group"
    if help is not None:
        kwargs["description"] = help

    return dataclasses.field(default_factory=default, metadata=kwargs)


def subparsers(**kwargs):
    kwargs["_kind"] = "subparsers"
    return dataclasses.field(default=None, metadata=kwargs)


def field(*args, choices=None, type=None, **kwargs):
    metadata = kwargs.pop("metadata", dict())
    if choices:
        metadata["choices"] = choices

    if type is not None:
        metadata["type"] = type

    return dataclasses.field(*args, metadata=metadata, **kwargs)


def choice(*args, default=MISSING, **kwargs):
    return argument(default=default, choices=args, **kwargs)


def _get_type_hint(hint, value):
    local_ns = {
        "typing": typing,
        **vars(typing),
    }
    local_ns.update(forward_refs_to_types)

    class Temp_:
        pass

    Temp_.__annotations__ = {"a": cvt_type(hint)}
    annotations_dict = get_type_hints(Temp_, localns=local_ns)
    return annotations_dict["a"]


def cvt_type(hint):
    try:
        if "| None" in hint:
            return "Optional[" + hint.replace("| None", "") + "]"
        return hint
    except Exception:
        return hint


def _add_flag(group, field, name, docstring):
    default = False
    action = "store_true"

    if field.default is True:
        default = True
        action = "store_false"

    group.add_argument(
        "--" + name,
        action=action,
        default=default,
        help=docstring,
    )


def is_optional(type_hint, value):
    try:
        return type_hint.__origin__ is typing.Optional or (
            type_hint.__origin__ is typing.Union
            and len(type_hint.__args__) == 2
            and type_hint.__args__[1] is type(None)
        )
    except Exception:
        return False


def is_list(type_hint, value):
    try:
        return (
            type_hint is typing.List
            or type_hint.__origin__ is typing.List
            or type_hint.__origin__ is list
        )
    except Exception:
        return False


def is_enum(type_hint, value):
    try:
        return issubclass(type_hint, enum.Enum)
    except Exception:
        return False


def is_tuple(type_hint, value):
    try:
        return type_hint.__origin__ is tuple
    except Exception:
        pass
    return 0


def leaf_type(type_hint):
    try:
        return type_hint.__args__[0]
    except Exception:
        return type_hint


def to_enum(enum_type):
    elems = list(enum_type)

    elem = elems[0]
    name_t = type(elem.name)

    def cvt(value):
        try:
            return enum_type[name_t(value)]
        except Exception:
            pass

        try:
            return elems[int(value)]
        except Exception:
            pass

        for elem in elems:
            if elem.name == value:
                return elem

            if elem.value == value:
                return elem

    return cvt


def tuple_action(ftype):
    def _(*args, **kwargs):
        return _TupleStoreAction(*args, ttype=ftype, **kwargs)

    return _


class _TupleStoreAction(argparse._StoreAction):
    def __init__(self, *args, ttype=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ttype = ttype

    def __call__(self, parser, namespace, values, option_string=None):
        elems = []
        if isinstance(values, str):
            values = values.split(",")

        if isinstance(values[0], str) and len(values) == 1 and "," in values[0]:
            values = values[0].split(",")

        for value_t, value in zip(self.ttype.__args__, values):
            elems.append(value_t(value))

        setattr(namespace, self.dest, tuple(elems))


def deduce_add_arguments(field, docstring):
    ftype = _get_type_hint(field.type, field.default)
    required = True
    action = field.metadata.get("action")
    nargs = None

    if is_optional(ftype, field.default):
        nargs = "?"
        ftype = leaf_type(ftype)
        required = False

    if is_list(ftype, field.default):
        nargs = "+"
        ftype = leaf_type(ftype)

    if is_tuple(ftype, field.default):
        nargs = "*"
        action = tuple_action(field.type)

    if is_enum(ftype, field.default):
        ftype = to_enum(field.type)

    # Optional + List = nargs=*
    default = MISSING
    if field.default is not MISSING:
        default = field.default
        required = False

    if field.default_factory is not MISSING:
        default = field.default_factory()
        required = False

    choices = None
    if field.metadata:
        choices = field.metadata.get("choices")
        required = False

    positional = False
    if default is MISSING:
        positional = True
        default = None

    kwargs = dict(
        default=default,
        help=docstring,
        action=action,
        choices=choices,
        nargs=nargs,
    )

    if action is None:
        kwargs.update(
            dict(
                const=None,
                type=ftype,
                metavar=None,
            )
        )

    return positional, required, kwargs


def _flag(name, positional=False):
    if positional:
        return name
    return "--" + name


def _add_argument(
    group: argparse._ArgumentGroup, field, name, docstring
) -> argparse.Action:
    positional, required, kwargs = deduce_add_arguments(field, docstring)

    if "." in name and positional:
        required = True
        positional = False

    # name = name.replace("_", "-")

    if positional:
        return group.add_argument(
            name,
            **kwargs,
        )
    else:
        return group.add_argument(
            "--" + name,  # Option Strings
            dest=name,  # dest
            required=not positional and required,
            **kwargs,
        )


def _group(dataclass, title=None, dest=None):
    if dest:
        return dest

    if title:
        return title

    return dataclass.__name__


def add_arguments(
    parser: argparse.ArgumentParser,
    dataclass,
    title=None,
    pathname=False,
    create_group=True,
    dest=None,
):
    """Traverse the dataclass hierarchy and build a parser tree"""
    docstr = DocstringIterator(dataclass)

    if not create_group and (parser.description is None or parser.description == ""):
        parser.description = docstr.get_dataclass_docstring()

    group = parser
    subparser = None
    if create_group:
        group = parser.add_argument_group(
            title=title or dataclass.__name__,
            description="",
            # description=docstr.get_dataclass_docstring(),
            # description=dataclass.__doc__ <= this is ugly AF
        )
        setattr(group, "_dataclass", dataclass)
        setattr(group, "_dest", dest)

    for field in fields(dataclass):
        name = field.name
        if pathname:
            name = f"{dest}.{name}"

        meta = dict(field.metadata)
        special_argument = meta.pop("_kind", None)
        docstring = docstr.find_field(field)

        if special_argument == "group":
            meta.setdefault("title", name)
            meta.setdefault("description", docstring)

            newgroup = group.add_argument_group(**meta)
            add_arguments(newgroup, field.type, create_group=False)
            continue

        if special_argument == "subparsers":
            subparser = parser.add_subparsers(dest=field.name)

            for k, argcls in meta.items():
                parser = subparser.add_parser(k)
                parser.add_arguments(argcls, create_group=True)

        if special_argument == "subparser":
            meta.setdefault("title", name)
            meta.setdefault("description", docstring)
            meta.setdefault("dest", name)

            if subparser is None:
                subparser = group.add_subparsers(**meta)
            continue

        if special_argument == "parser":
            meta.setdefault("name", name)
            meta.setdefault("description", docstring)

            group = subparser.add_parser(**meta)
            add_arguments(group, field.type, create_group=False)
            continue

        if special_argument == "argument":
            positional, _, deduced = deduce_add_arguments(field, docstring)

            for k, v in deduced.items():
                if v is not None:
                    meta.setdefault(k, v)

            group.add_argument(_flag(field.name, positional), **meta)
            continue

        if is_dataclass(field.type):
            add_arguments(
                group,
                field.type,
                dest=name,
                pathname=pathname,
                create_group=create_group,
            )
            continue

        if field.type == "bool" or field.type is bool:
            _add_flag(group, field, name, docstring)
        else:
            _add_argument(group, field, name, docstring)

    return group


class ArgumentParsingError(Exception):
    def __init__(self, parser, message):
        self.parser = parser
        self.message = message

    def fail(self):
        argparse.ArgumentParser.error(self.parser, self.message)


class ArgumentParser(argparse.ArgumentParser):
    def __init__(
        self,
        *args,
        group_by_parser: bool = False,
        group_by_dataclass: bool = False,
        dataclass: type = argparse.Namespace,
        use_exception: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(
            *args,
            **kwargs,
        )
        self.group_by_parser: bool = group_by_parser
        self.group_by_dataclass: bool = group_by_dataclass
        self.dataclass = dataclass
        self.use_exception = use_exception
        self.rebuild_parser = None

        if self.dataclass is not argparse.Namespace:
            self.add_arguments(self.dataclass, create_group=False)

    def add_arguments(self, dataclass, dest=None, pathname=False, create_group=False):
        add_arguments(
            self, dataclass, dest=dest, pathname=pathname, create_group=create_group
        )

    def add_subparsers(self, *args, **kwargs):
        kwargs.setdefault("parser_class", type(self))
        return super().add_subparsers(*args, **kwargs)

    def set_defaults(self, config):
        from .config import ArgumentConfig

        transform = ArgumentConfig(config)
        transform(self)

    def save_defaults(self, config):
        from .config import ArgumentConfig

        config = dict()

        transform = ArgumentConfig(config)
        transform(self)

        return config

    def parse_args(self, *args, config=None, **kwargs):
        return parse_args(self, *args, config=None, **kwargs)

    def error(self, message):
        if self.use_exception:
            raise ArgumentParsingError(self, message)
        else:
            super().error(message)


def argument_parser(dataclass, *args, title=None, dest=None, **kwargs):
    parser = ArgumentParser(*args, **kwargs, group_by_dataclass=True)
    parser.add_arguments(dataclass, create_group=True)
    return parser


def parse(dataclass, *args, title=None, dest=None, **kwargs):
    p = argument_parser(dataclass, *args, title=None, dest=None, **kwargs)

    gp = _group(dataclass, title=title, dest=dest)

    return getattr(p.parse_args(), gp)


def parse_known_args(dataclass, *args, title=None, dest=None, **kwargs):
    p = argument_parser(dataclass, *args, title=None, dest=None, **kwargs)

    gp = _group(dataclass, title=title, dest=dest)

    args, others = p.parse_known_args()

    return getattr(args, gp), others


def parse_args(parser, *args, config=None, **kwargs):
    from .config import ArgumentConfig
    from .groupargs import group_by_dataclass

    args, parser = cache_aware_parse_args(
        parser, *args, **kwargs, rebuild_parser=parser.rebuild_parser
    )

    grouped = group_by_dataclass(
        parser,
        args,
        parser.group_by_parser,
        parser.group_by_dataclass,
        parser.dataclass,
    )

    # Apply a config on top of the command line
    #   Command line takes precedence
    if config:
        transform = ArgumentConfig(config, grouped)
        transform(parser)

    return grouped


def cache_aware_parse_args(parser, *argv, rebuild_parser=None, **kwargs):
    """Parse arguments, on failure wait for the async cache update and try again"""
    try:
        return argparse.ArgumentParser.parse_args(parser, *argv, **kwargs), parser

    except ArgumentParsingError as err:
        # Argument parsing failed once
        # maybe the command cache is outdated
        was_updated = wait_cache_update()

        if was_updated:
            # cache was updated try again
            # we need to rebuild the parser
            if rebuild_parser is not None:
                parser = rebuild_parser()
                try:
                    return (
                        argparse.ArgumentParser.parse_args(parser, *argv, **kwargs),
                        parser,
                    )
                except ArgumentParsingError:
                    # Argument parsing failed after update
                    # just fail
                    err.fail()

        err.fail()
