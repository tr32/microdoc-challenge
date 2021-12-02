#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
{Description}
{License}
"""

__author__ = "Masud M. Khan"
__copyright__ = "Copyright 2019"
__license__ = "Copyright"
__credits__ = []
__version__ = "1.0.1"
__maintainer__ = "Masud M. Khan"
__status__ = "Dev"

import argparse
import logging
import os
import sys
import csv
import json
import gzip
import mmap
import multiprocessing as mp
import random
from heapq import merge
from itertools import islice
from datetime import date, datetime, timedelta
from time import time as timer

logger = logging.getLogger(__name__)


def _make_gen(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)


def raw_gen_count(filename):
    f = open(filename, 'rb')
    f_gen = _make_gen(f.raw.read)
    return sum(buf.count(b'\n') for buf in f_gen)


def get_file_offsets(filepath, n_rows):
    offs = []
    _offset = 0
    with open(filepath, 'r') as _rf:
        for _ in range(0, n_rows):
            _offset += len(_rf.readline())
            offs.append(_offset)
    return offs


def get_min_max(items):
    return min(items), max(items)


def find_median(items):
    """
    Median: min. 50% <= und min. 50% >=
    - ungerade Anzahl: mittlerer Wert der sortierten Werte
    - gerade Anzahl: Mittelwert der beiden mittleren Werte
    --> Mittelwert: Summe Werte / Anzahl Werte
    """
    n = len(items)
    middle = (n - 1) // 2

    if n % 2 == 0:
        return (items[middle] + items[middle + 1]) / 2
    else:
        return items[middle]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", "-i", dest="input_file", default=None, required=True, help="Absolut path+filename+suffix to input file")
    parser.add_argument("--output-path", "-o", dest="output_path", default=None, help="Path where output files should be stored")
    args = parser.parse_args()
    start_timer = timer()

    base = os.path.basename(args.input_file)
    num_cores = mp.cpu_count()
    num_rows = raw_gen_count(args.input_file)
    items_per_page = 100
    pages = (0, 0)

    if items_per_page > num_rows:
        items_per_page = num_rows

    if num_rows > 0:
        pages = divmod(num_rows, items_per_page)
    else:
        raise ZeroDivisionError("Number of rows is zero. Maybe a empty file?")

    print("processing: {}\n".format(base))
    print("rows: {}\nitemsPerPage:{}\npages:{}\n".format(num_rows, items_per_page, pages))

    pool = mp.Pool(num_cores)

    result = []
    with open(args.input_file, 'r') as fr:
        # with open(args.output_path + '_sorted.log', 'w') as fw:
        chunks = []
        for page in range(0, pages[0] + (1 if pages[1] else 0)):
            print(10*'-' + '> page: ', page)
            chunk = []
            for x in range(0, items_per_page):
                line = fr.readline().strip().rstrip('\n')
                if len(line) > 0 and line.isdigit():
                    chunk.append(float(line))
            sorted_chunk = sorted(chunk)
            min_val, max_val = get_min_max(sorted_chunk)
            with open(os.path.join(args.output_path, str(page) + '_' + str(int(min_val)) + '_' + str(int(max_val)) + '.log'), 'a') as fw:
                fw.write('\n'.join(str(item) for item in sorted_chunk))
            chunks.append(sorted_chunk)
        result.append(merge(*chunks))

    for items in iter(result):
        nums = list(iter(items))
        mid = (len(nums) - 1) // 2
        if len(nums) % 2 != 0:
            print("Median: ", nums[mid])
        else:
            median = (nums[mid] + nums[mid + 1]) / 2
            print("Median: ", median)

    print("Total Elapsed Time: {}".format(str(round(timer() - start_timer, 3))))
