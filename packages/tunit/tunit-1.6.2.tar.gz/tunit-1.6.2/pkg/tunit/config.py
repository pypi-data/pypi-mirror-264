#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from tunit.core import _TUnitSerializationConfig
from tunit.json import _TUnitJsonConfig


class TUnitConfig(_TUnitSerializationConfig, _TUnitJsonConfig):
    pass
