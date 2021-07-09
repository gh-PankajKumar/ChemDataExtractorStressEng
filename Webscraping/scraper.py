"""
Webscrapers for article retrieval. 
Scraper targets Elsevier but also has functionality to search Crossref for DOIs.

:code author: Pankaj Kumar (pk503@cam.ac.uk)
"""

import sys
import os
import requests
from crossref.restful import Works, Journals



class BaseDownloader:
    def __init__(self, pub_prefix=None):
        self.pub_prefix = pub_prefix
        self.dois = []

    def querySearch(self, query):
        # search for DOI using query
        works = Works()
        filters = {
            "has_full_text": "true",
            "has_license": "true",
            "full_text__type": "text/xml",
        }

        if self.pub_prefix is not None:
            filters["prefix"] = self.pub_prefix

        search_results = works.query(query).filter(**filters)

        print(
            f"{search_results.count()} results found using '{query}' as search query.\nResult URL: {search_results.url}"
        )

        for i, search_result in enumerate(search_results):
            doi = search_result["DOI"]
            self.dois.append(doi)

        return search_results

    def journalSearch(self, issn, query):
        # search for DOI using journal issn and query
        journals = Journals()
        filters = {
            "has_full_text": "true",
            "has_license": "true",
            "full_text__type": "text/xml",
        }

        if self.pub_prefix is not None:
            filters["prefix"] = self.pub_prefix

        if journals.journal_exists(issn):
            search_results = journals.works(issn).query(query).filter(**filters)

        elif not journals.journal_exists(issn):
            print(
                f"Journal with ISSN: {issn} cannot be found. Check if journal exists."
            )
            sys.exit()

        for i, search_result in enumerate(search_results):
            doi = search_result["DOI"]
            self.dois.append(doi)

        return search_results

    def storeDOI(self, save_dir):
        if not self.dois:
            print("DOIs list is empty!")
            sys.exit()

        if not os.path.exists(save_dir):
            print(
                f"{save_dir} directory does not exists.\nCreating directory {save_dir}"
            )
            os.makedirs(save_dir)

        with open(save_dir + "doi.txt", "a", encoding="utf-8") as save_file:
            for doi in self.dois:
                save_file.write(doi + "\n")

    def clearDOI(self):
        self.dois = []


class ElsevierDownloader(BaseDownloader):
    def __init__(self, search_data=None, api_key):
        super().__init__(pub_prefix="10.1016")
        self.api_key = api_key
        self.search_data = search_data

    def searchElsevier(self, query=None, offset=0):
        if query:
            self.search_data = {"qs": query, "show": 100}
        if not query and not self.search_data:
            print(
                "Search query and search data are empty!\nCall function with a query or assign a search request body to object."
            )
            sys.exit()
        if not self.search_data:
            print("Search data empty!")
            sys.exit()
        search_url = "https://api.elsevier.com/content/search/sciencedirect"

        search_results = requests.put(
            search_url, json=self.search_data, headers={"X-ELS-APIkey": self.api_key}
        ).json()
        # print(
        #     f"{search_results['resultsFound']} number of articles matched search criteria!"
        # )
        for search_result in search_results["results"]:
            doi = search_result["doi"]
            self.dois.append(doi)

        return search_results

    def downloadElsevier(self, dois, save_dir):
        if not os.path.exists(save_dir):
            print(
                f"{save_dir} directory does not exists.\nCreating directory {save_dir}"
            )
            os.makedirs(save_dir)

        for doi in dois:
            #print(doi)
            #print("This is save dir:" + save_dir + doi.replace("/", "-"))
            article_url = "https://api.elsevier.com/content/article/doi/" + doi
            article = requests.get(
                article_url,
                headers={
                    "x-els-apikey": self.api_key,
                    "Content-Type": "application/json",
                },
            ).text
            if doi:
                with open(
                    save_dir + doi.replace("/", "-"), "w+", encoding="utf-8"
                ) as save_file:
                    save_file.write(article)
            else:
                print("Empty DOI!")

