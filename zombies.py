#!/usr/bin/env python3

from collections import namedtuple
import json
from itertools import chain, repeat
import os
from time import sleep
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen
import xml.etree.ElementTree as etree

import options


Status = namedtuple('Status', 'action survivors zombies dead')


def call(**kwds):
    query = ('?' + urlencode(kwds)) if kwds else ''
    url = 'https://www.nationstates.net/cgi-bin/api.cgi' + query
    for backoff in chain([1, 2, 4, 8, 15, 30], repeat(60)):
        try:
            handle = urlopen(url)
            return etree.parse(handle).getroot()
        except URLError as e:
            delay = backoff * options.delay
            print()
            print('** ERROR: {}'.format(e))
            print('Retrying in {} seconds...'.format(delay))
            sleep(delay)


def get_nations():
    root = call(region=options.region, q='nations')
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
            sleep(options.delay)

        print_progress(len(nations))
        print()


def main():
    filename = 'cache.json'
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


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nAu revoir~!')
