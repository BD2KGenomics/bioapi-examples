"""
    combine_apis.py
    An example of combining the results of interacting with
    both the ExAC and GA4GH APIs.
"""

# We'll need both the requests module and the GA4GH client.

import ga4gh.client as client
import requests

EXAC_BASE_URL = "http://exac.hms.harvard.edu/rest/"
GA4GH_BASE_URL = "http://ga4gh-a1.westus.cloudapp.azure.com/ga4gh-example-data/"

def main():
    # Let's instantiate the GA4GH client first
    c = client.HttpClient(GA4GH_BASE_URL)

    # Since we've done it before, getting variants can be done
    # in a one-liner. We're picking up the first variant set
    # for the first dataset returned.

    ga4gh_variants = [v for v in c.searchVariants(
        c.searchVariantSets(c.searchDatasets().next().id).next().id,
        start=0,
        end=2**32,
        referenceName="1")]

    print(str(len(ga4gh_variants)) + " GA4GH variants.")

    # Now we'll access the ExAC API in search of variants on
    # the BRCA1 gene. See `hello_exac.py`

    GENE_NAME = "OR4F5"

    response = requests.get(
        EXAC_BASE_URL + "awesome?query=" + GENE_NAME + "&service=variants_in_gene")

    OR4F5_variants = response.json()

    print(str(len(OR4F5_variants)) + " ExAC variants.")

    # Let's find out if we have any matches on position.

    matches = []

    for OR4F5_variant in OR4F5_variants:
        for ga4gh_variant in ga4gh_variants:
            # Note that GA4GH positions are 0-based so we add
            # 1 to line it up with ExAC.
            if (ga4gh_variant.start + 1) == OR4F5_variant['pos']:
                print(OR4F5_variant['pos'])
                print(ga4gh_variant.start)
                matches.append((ga4gh_variant, OR4F5_variant))

    print("Found " + str(len(matches)) + " matches.")

    for match in matches:
        print(match[0].names)
        print(match[1]['rsid'])
        print(match[0].referenceBases, match[1]['ref'])
        print(match[0].alternateBases, match[1]['alt'])

if __name__ == "__main__":
    main()