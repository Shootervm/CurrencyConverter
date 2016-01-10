#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import shutil
import csv
from pprint import pprint
from urllib import request
from urllib.parse import urlencode
import xml.etree.ElementTree as ET

__author__ = 'Vojtech Mašek'


def parse_currencies():
    currencies = set()
    with open('currencies.csv', 'r') as csv_file:
        for row in csv.DictReader(csv_file, delimiter=','):
            col = row['currency_alphabetic_code']
            if col:
                currencies.add(col)
    return currencies


def download_rates(url):
    try:
        get_request = request.Request(url, method='GET', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
                                                                  'Accept-Charset': 'utf-8', 'Accept-Language': '*',
                                                                  'Connection': '*'})
        response = request.urlopen(get_request)

        if response.getcode() is not 200:
            print(response.getcode(), file=sys.stderr)

        return response.read()

    except Exception as e:
        print('Exception\n\n' + str(e), file=sys.stderr)
        exit(1)


def parse_rates(input_cur, output_cur):
    query = 'select%20*%20from%20yahoo.finance.xchange%20where%20pair%20in%20("' + input_cur + output_cur + '")'
    url = "http://query.yahooapis.com/v1/public/yql?q=" + query + "&env=store://datatables.org/alltableswithkeys"

    rates_xml = ET.fromstring(download_rates(url))

    for cube in rates_xml.findall('./results/rate/Rate'):
        pprint(cube.text)


def start():
    parse_currencies()
    parse_rates("EUR", "CZK")


if __name__ == '__main__':

    try:
        start()
    except KeyboardInterrupt:
        print('Script will be terminated!')
        exit(0)
