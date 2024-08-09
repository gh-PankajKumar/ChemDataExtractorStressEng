# Auto-generating databases of Yield Strength and Grain Size using ChemDataExtractor: Code Repository 

This repository contains code that was used to automatically-extract stress engineering material properties from the literature which has been organised into folders for each step.

Related paper: https://doi.org/10.1038/s41597-022-01301-w
```
@article{Kumar2022,
  title = {Auto-generating databases of Yield Strength and Grain Size using ChemDataExtractor},
  volume = {9},
  ISSN = {2052-4463},
  url = {http://dx.doi.org/10.1038/s41597-022-01301-w},
  DOI = {10.1038/s41597-022-01301-w},
  number = {1},
  journal = {Scientific Data},
  publisher = {Springer Science and Business Media LLC},
  author = {Kumar,  Pankaj and Kabra,  Saurabh and Cole,  Jacqueline M.},
  year = {2022},
  month = jun 
}
```

## ChemDataExtractorStressEng

In this folder, a bespoke version of ChemDataExtractor for stress engineering is contained and can be installed. Included is TableDataExtractor which needs to be installed for the extraction of information contained in tables. 

For further information on installation and usage, please refer to the [ChemDataExtractor documentation](http://chemdataextractor.org/docs/intro)[[1]](#1).

## Webscraping

Python code to download and filter papers from Elsevier. To use the search and download functions, an API key is required from [Elsevier's Developer Portal](https://dev.elsevier.com/)

## Post_Processing

Post processing functions designed to filter the extracted records and organise them into database. Contained is a iPython notebook detailing the steps to process the extracted records. The [MaterialParser](https://github.com/CederGroupHub/MaterialParser) was used in some stages in post processing and is code developed by the Ceder Group [[2]](#2).

## propertyExtractor.py

An example of how the newly defined property models can be used to automatically-extract yield strength and grain size from the downloaded literature.

For a walkthrough demonstration see `propertyExtractor_Example.ipynb` which gives an example of extracting Yield Strength from a previously downloaded Elsevier article. 

## References

<a id="1">[1]</a>
Swain, M. C., & Cole, J. M. "ChemDataExtractor: A Toolkit for Automated Extraction of Chemical Information from the Scientific Literature", J. Chem. Inf. Model. 2016, 56 (10), pp 1894–1904 10.1021/acs.jcim.6b00207


<a id="2">[2]</a>
Kononova et. al
"Text-mined dataset of inorganic materials synthesis recipes",
Scientific Data 6 (1), 1-11 (2019)
10.1038/s41597-019-0224-1

