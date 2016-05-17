# Biomedicine API Examples

## Introduction
Data sharing efforts and readily available computing resources are making bioinformatics over the Web possible. In the past, siloed data stores and obscure file formats made it difficult to synthesize and reproduce results between institutions. Here we present two biomedicine APIs, currently under development, and provide example usage. Some familiarity with python is expected.

*Get started!*

```
pip install -r requirements.txt
python hello_ga4gh.py
```

## ExAC
> Building on the existing ExAC application we opened up direct data access through straight forward web services. These services enable a user to integrate ExAC services into their own tools, querying the variant information and returning the data in an easy to programmatically use JSON format.
https://github.com/hms-dbmi/exac_browser


> The Exome Aggregation Consortium (ExAC) is a coalition of investigators seeking to aggregate and harmonize exome sequencing data from a wide variety of large-scale sequencing projects, and to make summary data available for the wider scientific community.

> The data set provided on this website spans 60706 unrelated individuals sequenced as part of various disease-specific and population genetic studies.
http://exac.broadinstitute.org

The REST API for ExAC has been developed as part of Harvard’s Patient-centered Information Commons: Standardized Unification of Research Elements (PIC-SURE http://www.pic-sure.org/software). 

## GA4GH

[GA4GH](https://genomicsandhealth.org) aims to standardize how bioinformatics data are shared over the web. A reference server with a subset of publicly available test data from 1000 genomes has been made available for these examples.

The GA4GH reference server hosts bioinformatics data using an HTTP API. These data are backed by BAM and VCF files. For these examples we will only be accessing a GA4GH server, but it is open source and eager individuals can create their own server instance using [these instructions](http://ga4gh-reference-implementation.readthedocs.org/en/latest/demo.html).

## What is HTTP API

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

## Examples

Please view each file's source for more details on usage.

### python_notebooks

### `python_scripts`

#### hello_ga4gh.py

Access a GA4GH reference server hosting bioinformatics data and see the basics of building a query.

#### hello_exac.py

Access an API hosting population genomics data and a query service for finding variants in a gene.

#### hello_nhanes.py

A demonstration of using the IRCT PIC-SURE API for NHANES data. It gathers patient blood pressure data by demographic.

#### hello_ga4gh_client.py

Access a GA4GH reference server using a (provided) client, making some operations easier.

#### visualize_ga4gh.py

Get data from a remote web service and visualize it using matplotlib.

#### find_nonreference_samples_for_variant.py

TODO

#### hello_ga4gh_brca1.py

TODO

#### combine_apis.py

Use data from two web services to produce synthetic results.

#### simple_service.py

Make the results of combining two APIs available as its own web service.

### html

#### 1kgenomes.html

Visual demonstration of the variant calls matrix represented by a set of GA4GH variants.

#### hello_ga4gh_d3.html

Displays GA4GH sequence annotations as a force directed graph.

#### speedtest.html

