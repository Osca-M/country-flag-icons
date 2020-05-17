#!/usr/bin/env python
# encoding: utf-8
import os
import codecs
import json

import requests
from bs4 import BeautifulSoup

WIKI_URL = u'http://en.wikipedia.org'
_here = os.path.dirname(__file__)
errors = []
countries = []


def main():
    r = requests.get('%s/wiki/ISO_3166-1' % WIKI_URL)
    soup = BeautifulSoup(r.text, 'html5lib')
    table_rows = soup.select('table > tbody > tr', {'class': 'wikitable sortable jquery-tablesorter'})
    for table_row in table_rows:
        try:
            raw_flag = table_row.select('td')[0].select('td > span > img')[0]['src']
            raw_flag = raw_flag.split('.svg')
            new_raw_flag = raw_flag[0] + '.svg'
            thumbnail_a = new_raw_flag.split('/thumb')[0]
            thumbnail_b = new_raw_flag.split('/thumb')[1]
            flag = ('http:' + thumbnail_a + thumbnail_b)
            alpha_2_code = table_row.select('td')[1].text
            alpha_3_code = table_row.select('td')[2].text
            numeric_code = table_row.select('td')[3].text
            raw_independent = table_row.select('td')[-1].text
            independent = raw_independent.split("\n")[0]
            country = {'flag': flag, 'alpha_2_code': alpha_2_code, 'alpha_3_code': alpha_3_code,
                       'numeric_code': numeric_code, 'independent': independent}
            countries.append(country)

        except Exception:
            pass
    for row in countries:
        download_flag(row)
    write_json(countries)
    print('Done with {} errors'.format(len(errors)))


def download_flag(country):
    file_name = os.path.basename('%s.svg' % country['alpha_3_code']).lower()
    path = os.path.join(_here, 'images', 'svg', file_name)
    # print(country['flag'], "country['flag']")
    r = requests.get(country['flag'])
    print("Saving file: \'%s\' for %s" % (file_name, country['alpha_3_code']))
    with open(path, 'wb') as f:
        for chunk in r.iter_content():
            f.write(chunk)


def write_json(countries):
    with codecs.open(os.path.join(_here, 'countries.json'), 'w', 'utf-8') as f:
        f.write(json.dumps(countries))


if __name__ == '__main__':
    main()
