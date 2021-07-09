#!/usr/bin/env python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import re

from lxml import etree
from .cem import (
    cem,
    chemical_label,
    lenient_chemical_label,
)
from .common import lbrct, dt, rbrct
from ..utils import first
from .actions import merge, join
from .quantity import value_element
from .elements import W, I, R, Optional, Any, OneOrMore, Not, ZeroOrMore, Group
from .template import MultiQuantityModelTemplateParser, QuantityModelTemplateParser

log = logging.getLogger(__name__)


class TensileStrengthParser(QuantityModelTemplateParser):
    pass


class MultiTensileStrengthParser(MultiQuantityModelTemplateParser):
    @property
    def multi_entity_phrase_3d(self):
        # Phrases of type grain size of CEM 1, CEM 2 and CEM 3 is Val 1, Val 2 and Val 3
        return Group(
            self.prefix
            + self.list_of_cems
            + OneOrMore(
                Not(self.single_cem | self.specifier_phrase | self.value_phrase)
                + Any().hide()
            )
            + self.list_of_values
        )("multi_entity_phrase_3")

    @property
    def multi_entity_phrase_3(self):
        """Combined phrases of type 3"""
        return Group(
            self.multi_entity_phrase_3a
            | self.multi_entity_phrase_3b
            | self.multi_entity_phrase_3c
            | self.multi_entity_phrase_3d
        )
