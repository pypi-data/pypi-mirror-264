#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import Optional

from json_handler_registry.decoder import IJsonDecoder
from json_handler_registry.encoder import EncodingResult, IJsonEncoder
from json_handler_registry.registry import JsonHandlerRegistry

from tunit.core import TimeUnit, TimeUnitTypeError


class TUnitJsonEncoder(IJsonEncoder):

    def encodeObject(self, obj: object) -> Optional[EncodingResult]:
        return obj.serialize() if isinstance(obj, TimeUnit)\
            else None


class TUnitJsonDecoder(IJsonDecoder):

    def decodeDict(self, dct: dict) -> Optional[object]:
        return None

    def decodeStr(self, valueStr: str) -> Optional[object]:
        for timeUnit in TimeUnit.__subclasses__():
            try:
                return timeUnit.deserialize(valueStr=valueStr)
            except TimeUnitTypeError:
                pass

        return None


class _TUnitJsonConfig:

    @staticmethod
    def registerJsonHandler(enableRegistry: bool = True) -> None:
        if enableRegistry:
            JsonHandlerRegistry.enable()
        JsonHandlerRegistry.registerEncoder(TUnitJsonEncoder)
        JsonHandlerRegistry.registerDecoder(TUnitJsonDecoder)

    @staticmethod
    def unregisterJsonHandler(disableRegistry: bool = False) -> None:
        if disableRegistry:
            JsonHandlerRegistry.disable()
        JsonHandlerRegistry.unregisterEncoder(TUnitJsonEncoder)
        JsonHandlerRegistry.unregisterDecoder(TUnitJsonDecoder)
