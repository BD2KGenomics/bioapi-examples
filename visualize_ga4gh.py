"""
    visualize_ga4gh.py
    This example uses the GA4GH HTTP client and matplotlib
    to render a visualization.
"""

# In addition to the GA4GH client we need our plotting libraries.

import ga4gh.client as client
import numpy as np
import matplotlib.pyplot as plt

BASE_URL = "http://ga4gh-a1.westus.cloudapp.azure.com/ga4gh-example-data/"

def main():
    # First, instantiate an HTTP client using the BASE_URL.

    c = client.HttpClient(BASE_URL)

    # Now we'll get a variant set.

    # We can get the first item of an iterator using `.next()`.

    dataset = c.searchDatasets().next()

    variant_set = c.searchVariantSets(dataset.id).next()

    # We now collect the variants in that variant set.

    variants = c.searchVariants(
        variant_set.id,         # The ID of the variantSet
        start=0,                # Start position
        end=2**32,              # End position
        referenceName="1")      # chrom

    # And copy them into `variant_list`

    variant_list = []

    for variant in variants:
        variant_list.append(variant)

    # Our analysis will make counts of the reference and
    # alternate base lengths, so let's grab those from
    # each variant and make lists of the lengths.

    ref_lengths = []
    alt_lengths = []

    for variant in variant_list:
        ref_lengths.append(len(variant.referenceBases))
        for base in variant.alternateBases:
            alt_lengths.append(len(base))

    print(str(len(variant_list)) + " variants.")

    # Now we can create histograms for each of these lists.
    # see more examples http://matplotlib.org/1.2.1/examples/pylab_examples/histogram_demo.html

    plt.figure(1)

    binning = [x for x in range(1, np.max(ref_lengths) + 1)]

    n, bins, patches = plt.hist(ref_lengths, bins=binning, facecolor='red', alpha=0.75, log=True)
    plt.title("Frequency of reference base lengths")
    plt.xlabel('Length of reference')
    plt.ylabel('n variants of length (log)')
    plt.axis([0, len(n), 0, np.max(n)])

    plt.figure(2)

    binning = [x for x in range(1, np.max(alt_lengths) + 1)]

    m, binsm, patchesm = plt.hist(alt_lengths, bins=binning, facecolor='blue', alpha=0.75, log=True)
    plt.title("Frequency of alternate base lengths")
    plt.xlabel('Length of alts')
    plt.ylabel('n variants of length (log)')
    plt.axis([0, len(m), 0, np.max(m)])

    plt.show()


if __name__ == "__main__":
    main()