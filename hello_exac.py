"""
    hello_exac.py

    A simple example usage of the PIC-SURE ExAC API.
    http://exac.hms.harvard.edu
"""

import requests

BASE_URL = "http://exac.hms.harvard.edu/rest/"

def main():
    # The ExAC API allows you to perform queries using a
    # specially formatted `region-id`.

    chrom = "1"
    start = "13000"
    stop = "20000"
    region_id = chrom + "-" + start + "-" + stop

    # Let's find all the variants in this region.

    response = requests.get(
        BASE_URL + "region/variants_in_region/" + region_id)

    variants = response.json()

    print("Variant allele frequencies: ")
    for variant in variants:
        print(variant['allele_count'])

    # Let's sort the variants by their allele_count.

    sorted_variants = sorted(variants,
                             reverse=True,
                             key=lambda x: x['allele_count'])

    print("Highest allele frequency variant: ")
    print("Position:" + str(sorted_variants[0]['pos']))
    print("Allele frequency:" + str(sorted_variants[0]['allele_count']))
    print(sorted_variants[0]['ref'] + " > " + sorted_variants[0]['alt'])

    # The ExAC API gives us several ways of finding variants.
    # Let's do another search that will return variants
    # for a given gene name.

    GENE_NAME = "BRCA1"

    response = requests.get(
        BASE_URL + "awesome?query=" + GENE_NAME + "&service=variants_in_gene")

    # Note that the ExAC API redirects the request we just made by
    # matching identifiers to the gene name we provided.

    print(response.url)
    variants = response.json()

    # As we did with the GA4GH example, let's construct a dictionary
    # to keep count of the variety of reference base lengths.

    reference_base_counts = {}

    for variant in variants:
        reference_base_length = len(variant['ref'])
        if reference_base_length not in reference_base_counts:
            reference_base_counts[reference_base_length] = 1
        else:
            reference_base_counts[reference_base_length] += 1

    print(reference_base_counts)

if __name__ == "__main__":
    main()