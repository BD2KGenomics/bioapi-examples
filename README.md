# Biomedicine API Examples

## Introduction
Data sharing efforts and readily available computing resources are making bioinformatics over the Web possible. In the past, siloed data stores and obscure file formats made it difficult to synthesize and reproduce results between institutions. Some familiarity with python is expected.

There are 3 sections of example code in this repository.
1. Python Notebooks - collection of python notebooks that demonstrate GA4GH APIs
2. Python Scripts - A set of scripts that demonstrate biomedicine APIs that use GA4GH APIs
3. Variant Browser - An example visualization of variants that uses GA4GH APIs

## Python Notebooks

*Get Started!*

First install the ga4gh client module. It is best to do the install inside of a virtual environment.
```
virtualenv ga4gh-client
source ga4gh-client/bin/activate
pip install --no-cache-dir --pre ga4gh_client
```

This environment is suitable for running any of the python notebooks listed in the python_notebook directory. There is a directory of which GA4GH APIs are demonstrated by each example that can be found on the wiki https://github.com/BD2KGenomics/bioapi-examples/wiki


## Python Scripts
Examples of scripts that work against existing services.

*Get started!*

```
pip install -r requirements.txt
python hello_ga4gh.py
```

## GA4GH

[GA4GH](https://genomicsandhealth.org) aims to standardize how bioinformatics data are shared over the web. A reference server with a subset of publicly available test data from 1000 genomes has been made available for these examples.

The GA4GH reference server hosts bioinformatics data using an HTTP API. These data are backed by BAM and VCF files. For these examples we will only be accessing a GA4GH server, but it is open source and eager individuals can create their own server instance using [these instructions](http://ga4gh-reference-implementation.readthedocs.org/en/latest/demo.html).

## What is an HTTP API

HTTP APIs allow web browsers and command line clients to use the same communication layer to transmit data to a server. A client can `GET` a resource from a server, `POST` a resource on a server, or `DELETE` amongst other things.

The documents that servers and clients pass back and forth are often in JavaScript Object Notation (JSON), which can flexibly describe complex data structures. For example, a variant in GA4GH is returned as a document with the form:

    {
        "alternateBases": ["T"],
        "calls": [],
        "created": 1455236057000,
        "end": 4530,
        "id": "YnJjYTE6MWtnUGhhc2UzOnJlZl9icmNhMTo0NTI5OjllNjRkMDIzOTc5NzQ3M2MyNjk2NzFiNzczMjg1MWNj",
        "info": {},
        "referenceBases": "C",
        "referenceName": "ref_brca1",
        "start": 4529,
        "updated": 1455236057000,
        "variantSetId": "YnJjYTE6MWtnUGhhc2Uz"
    }

JSON uses strings as keys for values that could be strings, numbers, or arrays and maps of more complex objects.
