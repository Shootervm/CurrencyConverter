#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import json
from json import encoder
import sys
import xml.etree.ElementTree as ET
from urllib import request

__email__ = 'shooter.vm@gmail.com'
__author__ = 'Vojtech Mašek'


def parse_currencies():
    currencies = set()
    with open('currencies.csv', 'r') as csv_file:
        for row in csv.DictReader(csv_file, delimiter=','):
            col = row['currency_alphabetic_code']
            if col:
                currencies.add(col)
    return list(currencies)


def parse_symbols():
    currencies = {}
    with open('symbols.csv', 'r') as csv_file:
        for row in csv.DictReader(csv_file, delimiter='\t'):
            col2 = row['Symbol']
            if len(col2) == 1:
                currencies[col2] = row['Code ISO 4217']
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
            query += '"' + input_cur + cur + '",' if input_cur != cur else ''  # TODO: '.format()'? Or at least %s?
    else:
        query += '"' + input_cur + output_cur + '",'  # TODO: '.format()' or at least %s
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
                        help="Input currency (3 letters [Code ISO 4217] or currency symbol)")
    parser.add_argument("--output_currency", "-o", nargs='+', type=str, default=[],
                        help="Requested/Output currency (3 letters [Code ISO 4217] or currency symbol), "
                             "if missing all know currencies will be outputted")

    return parser.parse_args()


def check_currency(curr, currencies, symbols):
    if len(curr) == 1:
        for sym in symbols:
            if sym == curr:
                return symbols[sym]
        print('Currency "' + curr + '" is not in wellknown symbols', file=sys.stderr)
        exit(2)
    elif len(curr) != 3:
        print('Currency "' + curr + '" does not fulfill three characters currency alphabetic code requirement',
              file=sys.stderr)
        exit(2)

    for cur in currencies:
        if cur == curr:
            return curr
    else:
        print('Currency "' + curr + '" is not supported.', file=sys.stderr)
        exit(2)


def check_currencies(args, currencies, symbols):
    args.input_currency = check_currency(args.input_currency, currencies, symbols)
    checked = set()
    for curr in args.output_currency:
        checked.add(check_currency(curr, currencies, symbols))
    args.output_currency = list(checked)


def start():
    # currencies = parse_currencies()
    # these currencies are pre-parsed from a csv file, to parse them runtime, uncomment the parser function
    currencies = ['AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN',
                  'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BWP', 'BYR', 'BZD', 'CAD', 'CHF', 'CLP', 'CNY',
                  'COP', 'CRC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD',
                  'FKP', 'GBP', 'GEL', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HUF', 'IDR',
                  'ILS', 'INR', 'IQD', 'IRR', 'ISK', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW',
                  'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT',
                  'MOP', 'MRO', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR',
                  'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR',
                  'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 'SOS', 'SRD', 'SSP', 'STD', 'SYP', 'SZL', 'THB', 'TJS', 'TMT',
                  'TND', 'TOP', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU', 'UZS', 'VEF', 'VND', 'VUV',
                  'WST', 'XAF', 'XCD', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMW', 'ZWL']
    # symbols = parse_symbols()
    # these are the well known currency symbols that can be used, to parse them uncomment the function call above
    symbols = {'$': 'USD', '¢': 'GHC', '£': 'GBP', '¥': 'CNY', 'ƒ': 'ANG', '؋': 'AFN', '฿': 'THB', '៛': 'KHR',
               '₡': 'CRC', '₤': 'TRL', '₦': 'NGN', '₨': 'PKR', '₩': 'KRW', '₪': 'ILS', '₫': 'VND', '€': 'EUR',
               '₭': 'LAK', '₮': 'MNT', '₱': 'CUP', '₴': 'UAH', '₹': 'INR', '﷼': 'IRR'}

    args = get_parameters()
    check_currencies(args, currencies, symbols)  # will perform check of validity and translate symbols to 3 chars sets

    conversion_rates = get_rates(args.input_currency,
                                 args.output_currency if args.output_currency else currencies)

    ret = {"input": {"amount": args.amount, "currency": args.input_currency}, "output": {}}
    for rate in conversion_rates:
        try:
            ret['output'][rate[3:]] = args.amount * float(conversion_rates[rate])
        except ValueError:
            ret['output'][rate[3:]] = ""  # if conversion rate is missing leave field empty with ""

    # This will set Float precision to 2 digits after the floating point
    encoder.FLOAT_REPR = lambda f: ("%.2f" % f)

    # pretty print dumped json structure (output of the script)
    print(json.dumps(ret, sort_keys=True, indent=4, separators=(',', ': ')))


if __name__ == '__main__':

    try:
        start()
    except KeyboardInterrupt:
        print('Script will be terminated!')
        exit(0)


# doc:10/10	code:8/10	 creativity_bonus:2/inf
# coefficients:
# doc:0.1	    code:0.7	creativity_bonus:0.2
