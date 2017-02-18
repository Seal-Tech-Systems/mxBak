#!/usr/bin/env python3
import csv
import ssl
from urllib import request
import os

from .htmlparser import HTMLTableParser
def get_camera_info(url, login, password):
    html = ''
    url = url + '/control/camerainfo'
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    p = request.HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, url, login, password)
    ssl_handler = request.HTTPSHandler(context=ctx)
    auth_handler = request.HTTPBasicAuthHandler(p)
    opener = request.build_opener(ssl_handler, auth_handler)
    request.install_opener(opener)
    html = opener.open(url).read()
    return html

def write_info(data, fn):
    if data:
        with open(fn, 'w', newline='', encoding='utf-8') as csvfile:
            keys = []
            for n in data:
                keys += list(n.keys())
            keys = list(set(keys))
            keys.pop(keys.index('url'))
            fieldnames = ['url', 'status'] + keys
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')

            writer.writeheader()
            for r in data:
                writer.writerow(r)

    else:
        print('No info data')

def generate_info(item):
    html = get_camera_info(item['url'], item['login'], item['password'])
    result = {
        'url': item['url'],
    }
    if not html:
        return result
    html = html.decode('utf-8')
    p = HTMLTableParser()
    p.feed(html)

    try:
        t = p.table
    except IndexError as e:
        print(html)
        raise e
    last_title = ''
    for r in t:
        title = r[0]
        if len(r) < 2:
            continue
        # hack 'Listening Ports'
        tmplt = '%s %s'
        if title == 'Listening Ports':
            if 'Listening Ports' not in result:
                result['Listening Ports'] = []
            result['Listening Ports'].append(tmplt % (r[1], r[2]))
        elif not title and last_title == 'Listening Ports':
            title = 'Listening Ports'
            result['Listening Ports'].append(tmplt % (r[1], r[2]))
        else:
            result[title] = r[1]
        last_title = title
    result['Listening Ports'] = '"%s"' % ', '.join(result['Listening Ports'])
    result['status'] = 'OK'
    return result

