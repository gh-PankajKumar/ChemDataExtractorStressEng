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
from .base import BaseSentenceParser
from .quantity import value_element, value_element_plain
from .elements import W, I, R, Optional, Any, OneOrMore, Not, ZeroOrMore, Group, SkipTo
from .template import MultiQuantityModelTemplateParser, QuantityModelTemplateParser


log = logging.getLogger(__name__)

delim = R("^[:;\.,]$")

gs_expression = (
    Optional(R(("[Av]erage(s?)"))) + R("^grain$") + R("^size(s?)")
).add_action(join)("specifier")

prefix = (
    Optional(I("a")).hide()
    + gs_expression.hide()
    + Optional(delim).hide()
    + Optional(
        I("of")
        | W("=")
        | I("was")
        | I("is")
        | I("had")
        | I("are")
        | Optional(I("of")) + I("about")
    ).hide()
)

units = R("(m(eter(s)?)?(?!ile(s)?))|(Meter(s)?(?!ile(s)?))")("raw_units")
value_unit = value_element(units)
value_opt_unit = Group(value_element_plain() + Optional(units))


# single grain size value
gs = (prefix + Optional(delim).hide() + value_unit)("gs")

# multiple grain size values
multi_gs = (
    Optional(delim).hide()
    + (value_unit | value_opt_unit)
    + ZeroOrMore((I("and") | delim) + value_unit)
)("gs")

bracket_any = lbrct + OneOrMore(Not(gs) + Not(rbrct) + Any()) + rbrct
multi_cem = cem + ZeroOrMore((I("and").hide()) | delim) + cem
cem_gs_phrase = (
    Optional(cem)
    + Optional(I("having")).hide()
    + Optional(delim).hide()
    + Optional(bracket_any).hide()
    + Optional(delim).hide()
    + Optional(lbrct)
    + gs
    + Optional(rbrct)
)("gs_phrase")

to_give_gs_phrase = (
    (
        I("to") + (I("give") | I("afford") | I("yield") | I("obtain"))
        | I("affording")
        | I("afforded")
        | I("gave")
        | I("yielded")
    ).hide()
    + Optional(dt).hide()
    + (cem | chemical_label | lenient_chemical_label)
    + ZeroOrMore(Not(gs) + Not(cem) + Any()).hide()
    + gs
)("gs_phrase")
obtained_gs_phrase = (
    (cem | chemical_label)
    + (I("is") | I("are") | I("was")).hide()
    + (I("afforded") | I("obtained") | I("yielded")).hide()
    + ZeroOrMore(Not(gs) + Not(cem) + Any()).hide()
    + gs
)("gs_phrase")

multi_gs_phrase = (gs_expression + multi_cem + SkipTo(multi_gs).hide() + multi_gs)(
    "gs_phrase"
)
gs_phrase = (
    cem_gs_phrase
    | to_give_gs_phrase
    | obtained_gs_phrase
    | multi_gs_phrase
    | OneOrMore(gs_expression)("gs_phrase")
)


delim = R("^[:;\.,]$")


class GrainSizeParser(QuantityModelTemplateParser):
    pass


class MultiGrainSizeParser(MultiQuantityModelTemplateParser):
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


# class GrainSizeParser(BaseSentenceParser):
#     """
#     MpParser rewritten to extract values and errors.
#     """

#     root = gs_phrase

#     def interpret(self, result, start, end):
#         log.debug(etree.tostring(result))
#         try:
#             compound = self.model.fields["compound"].model_class()
#             raw_value = first(result.xpath("./gs/raw_value/text()"))
#             raw_units = first(result.xpath("./gs/raw_units/text()"))
#             grain_size = self.model(
#                 raw_value=raw_value,
#                 raw_units=raw_units,
#                 value=self.extract_value(raw_value),
#                 error=self.extract_error(raw_value),
#                 units=self.extract_units(raw_units, strict=True),
#             )
#             cem_el = first(result.xpath("./compound"))
#             if cem_el is not None:
#                 log.debug(etree.tostring(cem_el))
#                 grain_size.compound = compound
#                 grain_size.compound.names = cem_el.xpath("./names/text()")
#                 grain_size.compound.labels = cem_el.xpath("./labels/text()")
#             log.debug(grain_size.serialize())
#             yield grain_size
#         except TypeError as e:
#             log.debug(e)
