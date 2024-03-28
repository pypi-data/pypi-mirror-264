#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""regmapGen это Генератор Регистровой Карты.
Он позволяет автоматически создавать пригодный для синтеза SystemVerilog код и документацию.
"""

__title__ = "regmapGen"
__description__ = "Генератор Регистровой Карты."

try:
    from ._version import version as __version__
except (ImportError, ModuleNotFoundError) as e:
    __version__ = 'git-latest'

from . import config
from .enum import EnumValue
from .bitfield import BitField
from .reg import Register
from .regmap import RegisterMap
from . import generators
