"""
    hello_ga4gh.py

    This script shows the basics of accessing a remote web service.

"""

# The requests module handles the HTTP layer so that our script
# can communicate with a distant web server.

import requests

# JavaScript Object Notation (JSON) is how the data passed
# between the client and server is described. This module
# will handle the conversion between python dictionaries
# and the JSON the server expects to receive.

import json

# Here we set a global variable for the base of the URL the
# remote server. It allows us to compose more complicated
# requests by adding to the end of the string.

BASE_URL = "http://ga4gh-a1.westus.cloudapp.azure.com/ga4gh-count1-data/"

# This global points the specific "endpoint" that will
# handle our request.

DATASETS_SEARCH_URL = BASE_URL + "datasets/search"

# We also set the variable `headers` here so that when
# we perform requests the server knows what kind of data
# to expect.

headers = {'Content-type': 'application/json'}

def main():
    # GA4GH collects data together in a dataset. Here we ask
    # the server which datasets it hosts and save the response
    # into the `response` variable.

    response = requests.post(
        DATASETS_SEARCH_URL,  # Where we want our data to post to
        headers=headers,      # Metadata the server needs to know
        data=json.dumps({"pageToken": None}))

    # We expect a list of Dataset objects in JSON to be returned.
    # Here we use the member function to convert the raw
    # response data into a python dictionary.

    response_data = response.json()

    # If you are able to communicate with the server and there
    # are datasets being hosted by it there will be a key
    # called `datasets`. Let's save the list to a variable.

    datasets = response_data['datasets']

    # Now we can iterate through the result as it is a
    # python list of dictionaries.

    print("Datasets")
    for dataset in datasets:
        print(dataset['name'])

    # Let's discover all the variant sets hosted by the server.

    VARIANT_SETS_SEARCH_URL = BASE_URL + "variantsets/search"

    # This endpoint allows you to search for variantsets.
    # Variant sets are similar to VCF files and are the container
    # for variants, calls, and callsets.

    # To find all of the hosted variantsets we will search
    # for all variant sets that match the datasetIds we have.

    variant_sets = []

    for dataset in datasets:
        datasetId = dataset['id']
        payload = {"datasetId": datasetId}
        response = requests.post(
            VARIANT_SETS_SEARCH_URL,
            headers=headers,
            data=json.dumps(payload))  # convert the payload to a JSON string

        response_data = response.json()

        # Each individual variant set is appended to our list of
        # variant sets so we can iterate over them later.

        for variant_set in response_data['variantSets']:
            variant_sets.append(variant_set)

    # We now have a list of all of the variant sets hosted
    # by the server.

    print(str(len(variant_sets)) + " variant set(s)")

    # Let's get some variants from one of those variant sets
    # and start an analysis.

    # Let's select the first variant set.

    variant_set = variant_sets[1]

    # Then we build a GA4GH query of variants over a range.
    # Don't worry if the range seems large, we just want to
    # make sure we get some results.

    payload = {
        "variantSetId": variant_set['id'],
        "start": 41196312,             # genomic position
        "end": 41196400,           # genomic position
        "referenceName": "17",    # the contig we want to search on
        "pageToken": None,       # start at the first page
    }

    # Let's take a look at the payload.

    print(payload)

    # Now we post our query to the variants/search endpoint.

    response = requests.post(
        BASE_URL + "variants/search",
        headers=headers,
        data=json.dumps(payload))

    # And parse out the response data.

    response_data = response.json()
    variants = response_data['variants']

    # If there are many results for a query, an API will often split
    # the results into multiple pages. Here we test to see if there is
    # another page and if so, we request it and add the results
    # to our list if variants.

    # As long as there is a nextPageToken we will keep requesting
    # more variants.

    while response_data['nextPageToken']:
        payload['pageToken'] = response_data['nextPageToken']
        print(payload['pageToken'])
        response = requests.post(
            BASE_URL + "variants/search",
            headers=headers,
            data=json.dumps(payload))
        response_data = response.json()
        for variant in response_data['variants']:
            variants.append(variant)


    # Let's take just the first variant, and obtain the 
    # non-reference samples:

    variant = variants[0]
    rbases = variant['referenceBases']
    vbases = [rbases] + variant['alternateBases']  # array of all allele bases
    print("Reference is: {}".format(rbases))
    for call in variant['calls']:
        gt = call['genotype']
        if gt[0] != 0 or gt[1] != 0:
            print("callset: {} has non-reference genotype: {}|{}".format(
                call['callSetName'], vbases[gt[0]], vbases[gt[1]]))


if __name__ == "__main__":
    main()