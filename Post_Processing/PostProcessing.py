import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import os
from parse.material_parser import MaterialParser


class DataProcessor:
    def __init__(self, model=None, path=None, open_access=False):

        self.path = path
        self.model = model
        self.records = []
        self.blacklist = [
            "UFG",
            "oxygen",
            "magnesium",
            "scandium",
            "silicon",
            "hydrogen",
            "Hydrogen",
            "Magnesium",
            "Oxygen",
            "UTS",
            "Mg",
            "HEAs",
            "Hall-Petch",
            "Hall Petch",
            "Hall–Petch",
            "vanadium",
            "Vanadium",
            "nickel",
            "Nickel",
            "Zn",
            "zinc",
            "Zinc",
            "OBSERVED",
            "MPa",
            "boron",
            "YS",
            "H",
            "hydrogen",
            "Gas",
            "nitrogen",
            "Nb",
            "oxide",
            "His",
            "chloride",
            "Ca",
            "σCYS",
            "manganese",
            "nitrogen",
            "Nitrogen",
            "Ga",
            "–",
            "argon",
            "oxide",
            "helium",
            "Helium",
            "vanadium",
            "MMCs",
            "stress-strain",
            "Stress-Strain",
            "His",
            "Li",
            "Na",
            "Gd",
        ]
        self.preprocessed_data = None
        self.filtered_database = pd.DataFrame()
        self.open_access = open_access

    def readOutput(self):
        if not self.path:
            print("Warning: path to records has not been specified!\n")

        for cde_output in os.listdir(self.path):
            for line in open(self.path + cde_output, "r"):
                self.records.append(json.loads(line))

    def recordReader(self):
        if not self.model:
            print("Warning: model has not been specified!\n")

        data = []

        for entry in self.records:

            if self.model in entry:
                try:
                    value = entry[self.model]["value"]
                    units = entry[self.model]["units"]
                    raw_value = entry[self.model]["raw_value"]
                    raw_units = entry[self.model]["raw_units"]
                except:
                    pass

                try:
                    compound = entry[self.model]["compound"]["Compound"]["names"]
                    # print(compound)
                    if any(i in compound for i in self.blacklist):
                        blacklisted = "True"
                    else:
                        blacklisted = "False"
                except KeyError:
                    compound = "Not Found"
                    blacklisted = "True"

                article_metadata = entry["metadata"]["MetaData"]
                try:
                    article_doi = article_metadata["doi"]
                except KeyError:
                    article_doi = entry["file_name"][:-4]

                try:
                    article_title = article_metadata["title"]
                    article_author = article_metadata["authors"]
                    article_journal = article_metadata["journal"]
                    article_date = article_metadata["date"]
                except KeyError:
                    article_title = (
                        article_author
                    ) = article_journal = article_date = "Null"

                parsing_method = entry["parsing_method"]

                data.append(
                    [
                        compound,
                        blacklisted,
                        value,
                        units,
                        raw_value,
                        raw_units,
                        parsing_method,
                        article_doi,
                        article_title,
                        article_author,
                        article_journal,
                        article_date,
                        self.open_access,
                    ]
                )

        self.preprocessed_data = pd.DataFrame(
            data,
            columns=[
                "Compound",
                "Blacklisted Compound?",
                "Value",
                "Units",
                "Raw Value",
                "Raw Units",
                "Parsing Method",
                "DOI",
                "Article Title",
                "Author",
                "Journal",
                "Date",
                "Open Access",
            ],
        )

        self.preprocessed_data = self.preprocessed_data.loc[
            self.preprocessed_data["Compound"] != "Not Found"
        ].reset_index(drop=True)
        print(
            str(len(self.preprocessed_data))
            + " Records have been read for: "
            + str(self.model)
            + " Model."
        )

    def filterDict(self):
        # add regex?
        dict_phrases = [
            "AISI 1020",
            "AISI 1045",
            "AISI 201",
            "AISI 202",
            "AISI 301",
            "AISI 302",
            "AISI 304",
            "AISI 304L",
            "AISI 316",
            "AISI 316L",
            "AISI 405",
            "AISI 410",
            "AISI 430",
            "AISI 446",
            "15-5PH",
            "17-4PH",
            "17-7PH",
            "A-286",
            "Alloy 2205",
            "Ferrallium 255",
            "ASTM A159",
            "ASTM A536",
            "Al 2014",
            "Al 2024",
            "Al 5052",
            "Al 5083",
            "Al 6061",
            "Al 7075",
            "Hastelloy",
            "C-276",
            "Inconel 625",
            "Inconel 686",
            "Inconel 718",
            "Inconel 725",
            "Monel 400",
            "Monel K-500",
            "70/30 Copper-Nickel",
            "90/10 Copper-Nickel",
            "Aluminum Bronze",
            "Beryllium Copper",
            "Nickel Aluminum",
            "Bronze 632",
            "Steel 316",
            "Steel 304",
            "Steel",
            "316L austenitic stainless steel",
            "316L",
            "AJ62",
            "AZ31",
            "AZ31B",
            "AZ31B-H24" "AZ91",
            "AZ91D",
            "AZ31C",
            "AZ61",
            "IN200",
            "Udimet 720",
            "Udimet720",
            "Waspaloy",
            "C263",
            "IN100",
            "NC-silver",
            "NC-aluminium",
            "Nimonic",
            "NiTinol",
            "P91 Steel",
            "EUROFER Steel",
            "TZF6",
            "TZ74",
            "TZF8",
            "CP-Ti",
            "AA7075-T651",
            "Q890D steel" "ZK60",
            "DP600",
            "DP800",
            "Ti5111",
            "Ti-5111",
            "GS16Mn5",
            "RZ5",
            "CADZ",
            "GW123",
            "steel",
            "ZK60 alloy",
        ]

        self.dict_filtered_data = pd.DataFrame(columns=self.preprocessed_data.columns)
        for i in dict_phrases:
            mask = self.preprocessed_data["Compound"].apply(
                lambda x: i.casefold() in (y.casefold() for y in x)
            )
            self.dict_filtered_data = self.dict_filtered_data.append(
                self.preprocessed_data[mask]
            )

        self.preprocessed_data = self.preprocessed_data.drop(
            self.dict_filtered_data.index
        )
        self.filtered_database = self.filtered_database.append(
            self.dict_filtered_data, ignore_index=True
        )

    def filterMatParser(self):

        filtered_entries = []
        mat_parser = MaterialParser(verbose=False, pubchem_lookup=True, fails_log=False)
        for index, row in self.preprocessed_data.iterrows():
            compound = str(row["Compound"][0])

            try:
                parser_output = mat_parser.parse_material(compound)
                if (
                    parser_output["material_name"] or parser_output["material_formula"]
                ) and parser_output["composition"]:
                    filtered_entries.append(row)
                else:
                    pass
            except:
                pass

        self.mat_parsed_database = pd.DataFrame(filtered_entries)

        self.preprocessed_data = self.preprocessed_data.drop(
            self.mat_parsed_database.index
        )
        self.filtered_database = self.filtered_database.append(
            self.mat_parsed_database, ignore_index=True
        )

    def exportDatabase(self, save_path, save=True):
        self.filtered_database = self.mat_parsed_database.append(
            self.dict_filtered_data
        ).reset_index(drop=True)
        if save:
            self.filtered_database.to_csv(save_path + ".csv")
            self.filtered_database.to_json(save_path + ".json")
            self.filtered_database.to_pickle(save_path + ".pkl")
        else:
            pass
        return self.filtered_database
