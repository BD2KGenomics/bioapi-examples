import requests
import json

import sys


from ga4gh.client import client
c = client.HttpClient("http://brcaexchange.org/backend/data/ga4gh/v0.6.0a7/")

dataset = c.get_dataset(dataset_id="brca")

variant_sets = [i for i in c.search_variant_sets(dataset_id="brca")]

def beacon_query(todo, done):
  mine = todo.get()
  while mine != 'STOP':
    variant = mine[1]
    id_ = mine[0]
    url = "https://beacon-network.org/api/responses/{}?chrom={}&pos={}&allele={}&ref=GRCh37".format(
                         id_,variant.reference_name, variant.start, variant.alternate_bases[0])
    r = requests.get(url)
    rdata = json.loads(r.content)
    if rdata['response'] is None:
      sys.stdout.write('-')
    elif rdata['response'] is True:
      sys.stdout.write('Y')
    else:
      sys.stdout.write('n')
    done.put(rdata)
    mine = todo.get()
  return True

beacons = json.loads(requests.get("https://beacon-network.org/api/beacons").content)
ids = [b['id'] for b in beacons]
references = [b['supportedReferences'] for b in beacons]
print("Found {} beacons".format(len(beacons)))
print('\n'.join(ids))

from multiprocessing import Queue, Process

todo = Queue()
done = Queue()

workers = 500
processes = []

for variant in c.search_variants(reference_name="chr17", variant_set_id="brca-hg37", start=41244980, end=41255981):
  print("searching for {}:{} {}".format(variant.reference_name, variant.start, variant.alternate_bases[0]))
  q = Queue()
  for id_ in ids:
    if id_ != 'bob':
      todo.put((id_, variant),)
  for w in xrange(workers):
    p = Process(target=beacon_query, args=(todo, done))
    p.start()
    processes.append(p)
    todo.put('STOP')
  for p in processes:
    p.join()
  done.put('STOP')
  print("")
  x = done.get()
  while x != 'STOP':
    if x['response']:
      print(x['beacon']['id'])
    x = done.get()
