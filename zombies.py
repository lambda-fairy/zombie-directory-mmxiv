#!/usr/bin/env python3

from collections import namedtuple
import json
import os
from time import sleep
from urllib.request import urlopen
import xml.etree.ElementTree as etree


Status = namedtuple('Status', 'action survivors zombies dead')


def call(**kwds):
    query = ('?' + '&'.join(str(k) + '=' + str(v) for k, v in kwds.items())) if kwds else ''
    handle = urlopen('https://www.nationstates.net/cgi-bin/api.cgi'+query)
    return etree.parse(handle).getroot()


def get_nations():
    root = call(region='pony_lands', q='nations')
    return frozenset(root[0].text.split(':'))


def get_status(nation):
    root = call(nation=nation, q='zombie')
    zombie = root[0]
    return Status(
            action=zombie[0].text,
            survivors=int(zombie[1].text),
            zombies=int(zombie[2].text),
            dead=int(zombie[3].text))


def loop(cache):
    while True:
        nations = get_nations()

        def print_progress(i):
            percent = i / len(nations)
            print('\rRetrieving data for {} nations... {:7.2%}'.format(len(nations), percent), end='')

        print_progress(0)

        for i, nation in enumerate(nations):
            status = get_status(nation)
            print_progress(i)
            cache[nation] = status
            yield {nation: cache.setdefault(nation, None) for nation in nations}
            sleep(0.7)  # Just below 50 requests per 30 seconds

        print_progress(len(nations))
        print()


if __name__ == '__main__':
    filename = 'zombies.json'
    tempname = filename + '.part'

    # Load initial data
    try:
        with open(filename) as infile:
            cache = {k: (Status(**v) if v else None) for k, v in json.load(infile).items()}
    except FileNotFoundError:
        cache = {}

    # Loop
    for output in loop(cache):
        with open(tempname, 'w') as outfile:
            json.dump({k: (v._asdict() if v else None) for k, v in output.items()}, outfile, sort_keys=True)
        os.rename(tempname, filename)
