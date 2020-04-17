# unpywall - Interfacing the Unpaywall API with Python

[![Build Status](https://travis-ci.org/unpywall/unpywall.svg?branch=master)](https://travis-ci.org/github/unpywall/unpywall)
[![codecov.io](https://codecov.io/gh/unpywall/unpywall/branch/master/graph/badge.svg)](https://codecov.io/gh/unpywall/unpywall?branch=master)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/unpywall)](https://pypi.org/project/unpywall/)
[![License](https://img.shields.io/github/license/unpywall/unpywall)](https://github.com/unpywall/unpywall/blob/master/LICENSE.txt)
[![PyPI - Version](https://img.shields.io/pypi/v/unpywall)](https://pypi.org/project/unpywall/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/unpywall)](https://pypi.org/project/unpywall/)

## Introduction

unpywall is a Python client that utilizes the [Unpaywall REST API](https://unpaywall.org/products/api) for scholarly analysis with [pandas](https://pandas.pydata.org/). This package is influenced by [roadoi](https://github.com/ropensci/roadoi), a R client that interacts with the Unpaywall API.

You can find more about the Unpaywall service here: https://unpaywall.org/.

The documentation about the Unpaywall REST API is located here: https://unpaywall.org/products/api.


## Install

Install from [pypi](https://pypi.org/project/unpywall/) using pip:
```python
pip install unpywall
```

## Use

### Authentication

To use the Unpaywall Service, you need to authenticate yourself. For that, unpywall offers multiple ways for authorizing the client. You can either import `UnpywallCredentials` which generates an environment variable or you can set the environment variable by yourself. Both methods require an email.

```python
from unpywall.utils import UnpywallCredentials

UnpywallCredentials('nick.haupka@gmail.com')
```

Notice that the environment variable for authentication needs to be called `UNPAYWALL_EMAIL`.

```bash
export UNPAYWALL_EMAIL=nick.haupka@gmail.com
```

### Pandas Integration

unpywall uses the data analysis tool [pandas](https://pandas.pydata.org/) for evaluating information from Unpaywall. By default, the Unpaywall API returns a JSON data structure. However, by using `get_df`, you can transform that into a pandas DataFrame. This also works with multiple DOIs.

```python
from unpywall import Unpywall

Unpywall.get_df(dois=['10.1038/nature12373', '10.1093/nar/gkr1047'])

#   data_standard  ... best_oa_location.version
#0              2  ...         publishedVersion
#0              2  ...         publishedVersion

#[2 rows x 32 columns]
```

You can track the progress of your API call by setting the parameter `progress` to True. This is especially useful for estimating the time required.

```python
Unpywall.get_df(dois=['10.1038/nature12373', '10.1093/nar/gkr1047'],
                progress=True)

#|=========================                        | 50%
```

The method also allows two options for catching errors (`raise` and `ignore`)

```python
Unpywall.get_df(dois=['10.1038/nature12373', '10.1093/nar/gkr1047'],
                errors='ignore')
```

### Conveniently obtain full text

If you are using Unpaywall to obtain full-text copies of papers for literature mining, you may benefit from the following functions:

You can use the `download_pdf_handle` method to return a PDF handle for the given DOI.

```python
Unpywall.download_pdf_handle(doi='10.1038/nature12373')
```

To return an URL to a PDF for the given DOI, use `get_pdf_link`.

```python
Unpywall.get_pdf_link(doi='10.1038/nature12373')

#'https://dash.harvard.edu/bitstream/1/12285462/1/Nanometer-Scale%20Thermometry.pdf'
```

To return an URL to the best available OA copy, regardless of the format, use `get_doc_link`.

```python
Unpywall.get_doc_link(doi='10.1038/nature12373')
```

To return a list of all URLS to OA copies, use `get_all_links`.

```python
Unpywall.get_all_links(doi='10.1038/nature12373')
```

You can also directly access all data provided by unpaywall in json format using `get_json`.

```python
Unpywall.get_json(doi='10.1038/nature12373')
```

## Develop

To install unpywall, along with dev tools, run:

```python
pip install -e '.[dev]'
```
