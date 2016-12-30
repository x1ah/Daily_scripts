#!/usr/bin/env python
# encoding: utf-8

import requests
import datetime
from multiprocessing.dummy import Pool

urls = [
    'http://github.com',
    'http://github.com',
    'http://github.com',
    'http://github.com',
    'http://github.com',
    'http://github.com',
    'http://github.com',
    'http://github.com'
    # etc..
]

# use multiprocessing.dummy
# Make the Pool of workers
pool = Pool(8)

# Open the urls in their own threads and return the results
start = datetime.datetime.now()
# call chain: dummy.Pool-ThreadPoo, pool.map-_map_async.get-ApplyResult.get
# MapResult(ApplyResult subclass) self._value = [None] * length, a list
results = pool.map(requests.get, urls)
# close the pool and wait for the work to finish
pool.close()
pool.join()
# todo: print httpresponse contents
print(results)

print("use {0} seconds".format(datetime.datetime.now() - start))


# compare
results = []
start = datetime.datetime.now()
for url in urls:
    results.append(requests.get(url))

print(results)
print("use {0} seconds".format(datetime.datetime.now() - start))
