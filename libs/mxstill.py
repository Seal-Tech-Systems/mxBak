import os
import ssl
from urllib import request


def get_img(url, login, password, x, y, q):
    url += '/cgi-bin/image.jpg?size=%sx%s&quality=%s'.format(x, y, q)
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
    data = result.read()
    return data


def get_fn(url, login, password):
    url += '/control/rcontrol?action=gettext&message=%24(ID.NAM)'
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
    data = result.read()
    return data.decode()


def create_file(binary, fn, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.join(folder, fn)
    with open(path, mode='wb') as f:
        f.write(binary)


def generate_still(item, folder, x, y, q):
    img = get_img(item['url'], item['login'], item['password'], x, y, q)
    result = {
        'url': item['url'],
    }
    if not img:
        return result
    create_file(img, get_fn(item['url'], item['login'], item['password']) + '.jpg', folder)
    result['status'] = 'OK'
    return result
