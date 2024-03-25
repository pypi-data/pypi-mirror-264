#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from json import JSONDecoder, JSONEncoder
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

from tunit.core import TimeUnit, TimeUnitTypeError

_K = TypeVar('_K')
_V = TypeVar('_V')
_Node = Union[Dict[_K, _V], List[_V]]


class _TUnitJsonSerializer:

    @staticmethod
    def serialize(obj: Any) -> Optional[str]:
        return obj.serialize() if isinstance(obj, TimeUnit)\
            else None


class _TUnitJsonDeserializer:

    @classmethod
    def deserialize(cls, obj: Any) -> Any:
        if isinstance(obj, str):
            return cls._tryDeserialize(value=obj)
        if isinstance(obj, (list, dict)):
            cls.deepUpdate(rootNode=obj)

        return obj

    @classmethod
    def deepUpdate(cls, rootNode: _Node[_K, _V]) -> None:
        nodesToWalk: List[_Node[_K, _V]] = [rootNode]
        while len(nodesToWalk) > 0:
            node = nodesToWalk.pop()
            nodeIterator = node.items() if isinstance(node, dict) else enumerate(node)
            for key, value in nodeIterator:
                if isinstance(value, (list, dict)):
                    nodesToWalk.append(value)
                    continue

                if not isinstance(value, str):
                    continue

                node[key] = cls._tryDeserialize(value=value)

    @staticmethod
    def _tryDeserialize(value: str) -> Union[TimeUnit, str]:
        for timeUnit in TimeUnit.__subclasses__():
            try:
                return timeUnit.deserialize(valueStr=value)
            except TimeUnitTypeError:
                pass

        return value


class _TUnitJsonEncoderProxy(JSONEncoder):

    def default(self: JSONEncoder, o: Any) -> Any:
        timeUnitOpt = _TUnitJsonSerializer.serialize(obj=o)
        return timeUnitOpt if timeUnitOpt is not None\
            else _TUnitJsonConfig._DEFAULT_SERIALIZER(self, o)


class _TUnitJsonDecoderProxy(JSONDecoder):

    def decode(self: JSONDecoder, s: str, _w: Callable[..., Any] = lambda *args, **kwargs: None) -> Any:
        decodedObj = _TUnitJsonConfig._DEFAULT_DESERIALIZER(self, s)
        return _TUnitJsonDeserializer.deserialize(obj=decodedObj)


class _TUnitJsonConfig:

    _DEFAULT_SERIALIZER: Callable = JSONEncoder.default
    _DEFAULT_DESERIALIZER: Callable = JSONDecoder.decode

    @classmethod
    def registerJsonHandler(cls) -> None:
        cls._DEFAULT_SERIALIZER = JSONEncoder.default
        JSONEncoder.default = _TUnitJsonEncoderProxy.default  # type: ignore

        cls._DEFAULT_DESERIALIZER = JSONDecoder.decode
        JSONDecoder.decode = _TUnitJsonDecoderProxy.decode  # type: ignore

    @classmethod
    def unregisterJsonHandler(cls) -> None:
        JSONEncoder.default = cls._DEFAULT_SERIALIZER  # type: ignore
        JSONDecoder.decode = cls._DEFAULT_DESERIALIZER  # type: ignore
