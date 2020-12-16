# unpywall - Interfacing the Unpaywall API with Python

[![Build Status](https://travis-ci.org/unpywall/unpywall.svg?branch=master)](https://travis-ci.org/github/unpywall/unpywall)
[![codecov.io](https://codecov.io/gh/unpywall/unpywall/branch/master/graph/badge.svg)](https://codecov.io/gh/unpywall/unpywall?branch=master)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/unpywall)](https://pypi.org/project/unpywall/)
[![License](https://img.shields.io/github/license/unpywall/unpywall)](https://github.com/unpywall/unpywall/blob/master/LICENSE.txt)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4085415.svg)](https://doi.org/10.5281/zenodo.4085415)
[![PyPI - Version](https://img.shields.io/pypi/v/unpywall)](https://pypi.org/project/unpywall/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/unpywall)](https://pypi.org/project/unpywall/)
[![Documentation Status](https://readthedocs.org/projects/unpywall/badge/?version=latest)](https://unpywall.readthedocs.io/en/latest/?badge=latest)

## Introduction

unpywall is a Python client that utilizes the [Unpaywall REST API](https://unpaywall.org/products/api) for scholarly analysis with [pandas](https://pandas.pydata.org/). This package is influenced by [roadoi](https://github.com/ropensci/roadoi), a R client that interacts with the Unpaywall API.

You can find more about the Unpaywall service here: https://unpaywall.org/.

The documentation about the Unpaywall REST API is located here: https://unpaywall.org/products/api.


## Install

Install from [pypi](https://pypi.org/project/unpywall/) using pip:
```bash
pip install unpywall
```

## Use

### Authentication

An authentification is required to use the Unpaywall Service. For that, unpywall offers two options for authorizing the client. You can either import `UnpywallCredentials` which generates an environment variable or you can set the environment variable by yourself. Both methods require an email.

```python
from unpywall.utils import UnpywallCredentials

UnpywallCredentials('nick.haupka@gmail.com')
```

Notice that the environment variable for authentication needs to be called `UNPAYWALL_EMAIL`.

```bash
export UNPAYWALL_EMAIL=nick.haupka@gmail.com
```

### Query Unpaywall by DOI

If you want to search articles by a given DOI use the method `doi`. The result is a [pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html).

```python
from unpywall import Unpywall

Unpywall.doi(dois=['10.1038/nature12373', '10.1093/nar/gkr1047'])

#   data_standard  ... best_oa_location.version
#0              2  ...         publishedVersion
#1              2  ...         publishedVersion

#[2 rows x 32 columns]
```

You can track the progress of your API call by setting the parameter `progress` to True. This is especially useful for estimating the time required.

```python
Unpywall.doi(dois=['10.1038/nature12373', '10.1093/nar/gkr1047'],
             progress=True)

#|=========================                        | 50%
```

This method also allows two options for catching errors (`raise` and `ignore`)

```python
Unpywall.doi(dois=['10.1038/nature12373', '10.1093/nar/gkr1047'],
             errors='ignore')
```

### Query Unpaywall by text search

If you want to search articles by a given term use the method `query`. The result is a [pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)

```python
Unpywall.query(query='sea lion',
               is_oa=True)
#   data_standard  ... first_oa_location.version
#0              2  ...          publishedVersion
#1              2  ...          publishedVersion
#2              2  ...          publishedVersion
```

### Conveniently obtain full text

If you are using Unpaywall to obtain full-text copies of papers for literature mining, you may benefit from the following functions:

You can use the `download_pdf_handle` method to return a PDF handle for the given DOI.

```python
Unpywall.download_pdf_handle(doi='10.1038/nature12373')

#<http.client.HTTPResponse object at 0x7fd08ef677c0>
```

To return an URL to a PDF for the given DOI, use `get_pdf_link`.

```python
Unpywall.get_pdf_link(doi='10.1038/nature12373')

#'https://dash.harvard.edu/bitstream/1/12285462/1/Nanometer-Scale%20Thermometry.pdf'
```

To return an URL to the best available OA copy, regardless of the format, use `get_doc_link`.

```python
Unpywall.get_doc_link(doi='10.1016/j.envint.2020.105730')

#'https://doi.org/10.1016/j.envint.2020.105730'
```
To return a list of all URLS to OA copies, use `get_all_links`.

```python
Unpywall.get_all_links(doi='10.1038/nature12373')

#['https://dash.harvard.edu/bitstream/1/12285462/1/Nanometer-Scale%20Thermometry.pdf']
```

You can also directly access all data provided by unpaywall in json format using `get_json`.

```python
Unpywall.get_json(doi='10.1038/nature12373')

#{'best_oa_location': {'endpoint_id': '8c9d8ba370a84253deb', 'evidence': 'oa repository (via OAI-PMH doi match)', 'host_type': ...
```

## Command-Line-Interface

unpywall comes with a command-line-interface that can be used to quickly look up a PDF or to download free full-text articles to your device.

### Obtain a PDF URL

Retrieve the URL of a PDF for a given DOI with the following command.

```bash
unpywall link 10.1038/nature12373
```

### View a PDF

If you want to view a PDF in your Browser or on your system use `view`.

```bash
unpywall view 10.1038/nature12373 -m browser
```

### PDF Download

Use `download` if you want to store a PDF on your machine.

```bash
unpywall download 10.1038/nature12373 -f article.pdf -p ./documents
```

### Help

You can always use `help` to open a description for the provided functions.

```bash
unpywall -h
```

## Documentation

Full documentation is available at https://unpywall.readthedocs.io/.

## Develop

To install unpywall, along with dev tools, run:

```bash
pip install -e '.[dev]'
```
