#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import sys
import xml.etree.ElementTree as ET
from pprint import pprint
from urllib import request

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
        get_request = request.Request(url, method='GET')
        response = request.urlopen(get_request)

        if response.getcode() is not 200:
            print(response.getcode(), file=sys.stderr)

        return response.read()

    except Exception as e:
        print('Exception\n\n' + str(e), file=sys.stderr)
        exit(1)


def get_rates(input_cur, output_cur):
    query = 'select%20*%20from%20yahoo.finance.xchange%20where%20pair%20in%20('
    if type(output_cur) is list:
        for cur in output_cur:
            query += '"' + input_cur + cur + '",' if input_cur != cur else ''
    else:
        query += '"' + input_cur + output_cur + '",'
    query = query[:-1] + ')'
    url = "http://query.yahooapis.com/v1/public/yql?q=" + query + "&env=store://datatables.org/alltableswithkeys"

    rates_xml = ET.fromstring(download_rates(url))

    rates = {}
    for rate in rates_xml.findall('./results/rate'):
        rates[rate.attrib['id']] = rate.find("./Rate").text

    return rates


def get_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument("--amount", "-a", type=float, required=True,
                        help="Amount of imputed currency, that will be calculated by conversion rate/rates")
    parser.add_argument("--input_currency", "-i", type=str, required=True,
                        help="")
    parser.add_argument("--output_currency", "-o", nargs='+', type=str, default='',
                        help="")

    return parser.parse_args()


def start():
    parse_currencies()

    args = get_parameters()
    pprint(args)

    pprint(get_rates("EUR", list(parse_currencies())))
    # get_rates("EUR", ["AUD", "USD"])
    # get_rates("EUR", "CZK")

    ret = {"input": {}, "output": {}}
    pprint(ret)


if __name__ == '__main__':

    try:
        start()
    except KeyboardInterrupt:
        print('Script will be terminated!')
        exit(0)
