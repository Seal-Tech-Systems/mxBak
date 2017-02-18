import ssl
import re
import os
from urllib import request


def get_html(url, login, password):
    html = ''
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
    html = result.read()
    return html, fn


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


def create_file(html, fn, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.join(folder, fn)
    with open(path, mode='wb') as f:
        f.write(html)


def generate_backup(item, folder):
    html, fn = get_html(item['url'], item['login'], item['password'])
    result = {
        'url': item['url'],
    }
    if not html:
        return result
    create_file(html, fn, folder)
    result['status'] = 'OK'
    return result
