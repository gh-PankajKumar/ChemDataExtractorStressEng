#!/usr/bin/env python3
from chemdataextractor import Document
from chemdataextractor.model import (
    StressModel,
    LengthModel,
    ModelType,
    StringType,
    Compound,
)
from chemdataextractor.parse.elements import W, I, R, Optional, Not
from chemdataextractor.reader.elsevier import ElsevierXmlReader
from chemdataextractor.parse.auto import AutoTableParser
from chemdataextractor.parse.actions import join
from chemdataextractor.parse.yield_strength import (
    YieldStrengthParser,
    MultiYieldStrengthParser,
)
from chemdataextractor.parse.grain_size import (
    GrainSizeParser,
    MultiGrainSizeParser,
)
from chemdataextractor.model.model import (
    GrainSize,
    TableGrainSize,
    YieldStrength,
    TableYieldStrength,
)
import os


def extractYS(self, file):

    models = [YieldStrength]
    records = []
    for model in models:
        f = open(file, "rb")
        d = Document.from_file(f, readers=[ElsevierXmlReader()])
        try:
            d.models = [model]
            try:
                meta_data = d.metadata.serialize()
            except:
                meta_data = "empty"
            print("parsing " + file + " with model " + str(model))

            rough = d.records.serialize()
            for dic in rough:
                if "Compound" in dic:
                    continue
                dic["metadata"] = meta_data
                file_name = os.path.basename(file).replace("10.1016-", "10.1016/")
                dic["file_name"] = file_name
                dic["extraction_model"] = str(model)
                dic["parsing_method"] = "Text Parsing"
                count += 1
                records.append(dic)
            # print(str(count) + " records have been extracted. \n-------")
            f.close()
        except:
            print("Error")
            f.close()
            pass
    return records


def extractGS(self, file):

    models = [GrainSize]

    records = []
    for model in models:
        f = open(file, "rb")
        d = Document.from_file(f, readers=[ElsevierXmlReader()])
        try:
            d.models = [model]
            try:
                meta_data = d.metadata.serialize()
            except:
                meta_data = "empty"
            print("parsing " + file + " with model " + str(model))

            rough = d.records.serialize()
            for dic in rough:
                if "Compound" in dic:
                    continue
                dic["metadata"] = meta_data
                file_name = os.path.basename(file).replace("10.1016-", "10.1016/")
                dic["file_name"] = file_name
                dic["extraction_model"] = str(model)
                dic["parsing_method"] = "Text Parsing"
                count += 1
                records.append(dic)
            # print(str(count) + " records have been extracted. \n-------")
            f.close()
        except:
            print("Error")
            f.close()
            pass
    return records


def extractYSTable(self, file):

    models = [TableYieldStrength]
    records = []
    for model in models:
        f = open(file, "rb")
        d = Document.from_file(f, readers=[ElsevierXmlReader()])
        try:
            d.models = [model]
            try:
                meta_data = d.metadata.serialize()
            except:
                meta_data = "empty"
            print("parsing " + file + " with model " + str(model))

            rough = d.records.serialize()
            for dic in rough:
                if "Compound" in dic:
                    continue
                dic["metadata"] = meta_data
                file_name = os.path.basename(file).replace("10.1016-", "10.1016/")
                dic["file_name"] = file_name
                dic["extraction_model"] = str(model)
                dic["parsing_method"] = "Table Parsing"
                count += 1
                records.append(dic)
            # print(str(count) + " records have been extracted. \n-------")
            f.close()
        except:
            print("Error")
            f.close()
            pass
    return records


def extractGSTable(self, file):

    models = [TableGrainSize]

    records = []
    for model in models:
        f = open(file, "rb")
        d = Document.from_file(f, readers=[ElsevierXmlReader()])
        try:
            d.models = [model]
            try:
                meta_data = d.metadata.serialize()
            except:
                meta_data = "empty"
            print("parsing " + file + " with model " + str(model))

            rough = d.records.serialize()
            for dic in rough:
                if "Compound" in dic:
                    continue
                dic["metadata"] = meta_data
                file_name = os.path.basename(file).replace("10.1016-", "10.1016/")
                dic["file_name"] = file_name
                dic["extraction_model"] = str(model)
                dic["parsing_method"] = "Table Parsing"
                count += 1
                records.append(dic)
            # print(str(count) + " records have been extracted. \n-------")
            f.close()
        except:
            print("Error")
            f.close()
            pass
    return records
