#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from json import JSONDecoder, JSONEncoder
from typing import Any, Callable

from tunit.core import TimeUnit, TimeUnitTypeError


class _TUnitJsonEncoderProxy(JSONEncoder):

    def default(self: JSONEncoder, o: Any) -> Any:
        if isinstance(o, TimeUnit):
            return o.serialize()

        return _TUnitJsonConfig._DEFAULT_SERIALIZER(self, o)


class _TUnitJsonDecoderProxy(JSONDecoder):

    def decode(self: JSONDecoder, s: str, _w: Callable[..., Any] = lambda *args, **kwargs: None) -> Any:

        decodedObj = _TUnitJsonConfig._DEFAULT_DESERIALIZER(self, s)
        if isinstance(decodedObj, str):
            return _TUnitJsonDecoderProxy._tryDecode(value=decodedObj)
        if isinstance(decodedObj, list):
            return [_TUnitJsonDecoderProxy._tryDecode(value=item) for item in decodedObj]
        if isinstance(decodedObj, dict):
            for key, value in decodedObj.items():
                decodedObj[key] = _TUnitJsonDecoderProxy._tryDecode(value=value)

        return decodedObj

    @staticmethod
    def _tryDecode(value: Any) -> Any:
        if not isinstance(value, str):
            return value

        for timeUnit in TimeUnit.__subclasses__():
            try:
                return timeUnit.deserialize(valueStr=value)
            except TimeUnitTypeError:
                pass

        return value


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
