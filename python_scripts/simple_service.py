"""
    simple_service.py
    Combine results from GA4GH and ExAC API to build
    a simple web service.
"""

# Our web service will listen on an HTTP port for
# requests and uses the Flask (http://flask.pocoo.org)
# python module to handle communication.

import flask
app = flask.Flask(__name__)

# We'll also include requests and the ga4gh client for
# communicating with other web services.

import ga4gh.client as client
import requests

# This is an endpoint for our web service. When the script
# runs we can point a web browser at these endpoints
# and the underlying code will be executed.

@app.route('/')
def hello_world():
    return 'Hello World!'

# This slightly more complicated route will read an argument,
# `echostring` from the URL and passes it to the gene_route
# function, echoing back our input. Try it by browsing to
# http://localhost:5000/echo/hello.

@app.route('/echo/<echostring>')
def echo_route(echostring):
    return echostring

# Now we'll generalize the combination of results from
# `combine_apis.py`.

EXAC_BASE_URL = "http://exac.hms.harvard.edu/rest/"
GA4GH_BASE_URL = "http://1kgenomes.ga4gh.org/"

@app.route('/gene/<gene_name>')
def gene_route(gene_name):

    # First, let's request variants in the gene from ExAC.

    # Note that we aren't handling cases when the gene isn't found. The ExAC
    # API uses redirects to locate the gene of interest. Better error handling
    # is left as an exercise.

    print("Looking for " + str(gene_name))

    print("If this hangs forever ctrl-c to quit :)")

    response = requests.get(
        EXAC_BASE_URL + "awesome?query=" + gene_name + "&service=variants_in_gene")

    exac_variants = response.json()

    # Now we'll check to make sure we got something back.

    print("Found " + str(len(exac_variants)) + " variants in " + gene_name)

    # As in `combine_apis` we'll get all the variants from the GA4GH
    # variant set.

    # We can refine our search by getting the range of positions
    # from the ExAC variants.

    min_start = 2**32
    max_start = 0
    chrom = "1"

    for variant in exac_variants:
        if variant['pos'] > max_start:
            max_start = variant['pos']
        if variant['pos'] < min_start:
            min_start = variant['pos']
        chrom = variant['chrom']


    print("Range: " + str(min_start) + ":" + str(max_start) + " on chrom " + chrom)

    c = client.HttpClient(GA4GH_BASE_URL)

    ga4gh_variants = [v for v in c.searchVariants(
        c.searchVariantSets(c.searchDatasets().next().id).next().id,
        start=min_start,
        end=max_start,
        referenceName=chrom)]

    # We'll find if there are any matches and return them.
    # Matches is a list of tuples, the first of each tuple
    # being the GA4GH variant, and the second being the ExAC
    # variant.

    matches = []

    for exac_variant in exac_variants:
        for ga4gh_variant in ga4gh_variants:
            # Note that GA4GH positions are 0-based so we add
            # 1 to line it up with ExAC.
            if (ga4gh_variant.start + 1) == exac_variant['pos']:
                matches.append((ga4gh_variant.toJsonDict(), exac_variant))

    print("Found " + str(len(matches)) + " matches.")

    # You can point a web browser at this address to see some results:
    # http://localhost:5000/gene/or4f5

    # Now that we have a web service synthesizing the results
    # from ExAC and GA4GH, you may use this web service in the same
    # way we used ExAC or GA4GH in the hello_ examples.

    # response = requests.get("http://localhost:5000/gene/or4f5")
    # response_data = response.json()
    # for result in response_data['matches']:
    #   print result

    return flask.jsonify({"gene_name": gene_name, "matches": matches})

if __name__ == '__main__':
    app.debug = True  # helps us figure out if something went wrong
    app.run()         # starts the server and keeps it running
