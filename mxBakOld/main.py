#!/usr/bin/env python3
import csv
import re
from urllib import request
import ssl
import os
import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, help="specify name of input file, default: 'input.csv'",
                    default='input.csv')
args = parser.parse_args()
INPUT_FILENAME = args.input

now = datetime.datetime.now()

DIR = 'backups'
CURRENT_DATE = now.strftime("%m%d%Y")

LOGGING_ENABLED = False


def get_input_data():
    result = []
    with open(INPUT_FILENAME) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            r = {
                'url': row['url'],
                'login': row['login'],
                'password': row['password'],
            }
            result.append(r)
    return result


def _get_html(url, login, password):
    url = url + '/admin/m1cam.cfg'
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    p = request.HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, url, login, password)
    ssl_handler = request.HTTPSHandler(context=ctx)
    auth_handler = request.HTTPBasicAuthHandler(p)
    opener = request.build_opener(ssl_handler, auth_handler)
    request.install_opener(opener)
    result = opener.open(url)
    info = result.info()['Content-Disposition']
    pattern = r'attachment; filename=\"(.*)\"'
    m = re.findall(pattern, info)
    fn = m[0]
    return result, fn


def get_html(url, login, password):
    html = ''
    result, fn = _get_html(url, login, password)
    html = result.read()
    return html, fn


def create_file(html, fn):
    dir = os.path.join(DIR, CURRENT_DATE)
    if not os.path.exists(dir):
        os.makedirs(dir)
    path = os.path.join(dir, fn)
    with open(path, mode='wb') as f:
        f.write(html)


def process_item(item):
    html, fn = get_html(item['url'], item['login'], item['password'])
    result = {
        'url': item['url'],
    }
    if not html:
        return result
    create_file(html, fn)
    result['status'] = 'OK'
    return result


def process_list(l):
    result = []
    for item in l:
        print('Processing %s' % item['url'])
        try:
            r = process_item(item)
            if r:
                result.append(r)
                print("Success: %s" % item['url'])
        except IOError as e:
            print("IO error '%s' while trying to process URL: %s" % (e, item['url']))
            result.append({'url': item['url'], 'status': 'IO ERROR: %s' % e})
        except BaseException as e:
            print("Unknown error '%s' while trying to process URL: %s" % (e, item['url']))
            raise e
    return result


def main():
    result = process_list(get_input_data())


if __name__ == "__main__":
    main()
