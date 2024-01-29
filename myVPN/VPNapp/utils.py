"""Additional functions"""


def change_tag(alias, my_site, attr):
    if attr.startswith('/'):
        attr = '/' + alias + '/' + attr
    elif attr.startswith(my_site.alias_url):
        attr = '/' + alias + '/' + attr[len(my_site.alias_url):]
    return attr


def get_headers(environ):
    headers = {}
    for key, value in environ.items():
        if key.startswith('HTTP_') and key != 'HTTP_HOST':
            headers[key[5:].replace('_', '-')] = value
        elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            headers[key.replace('_', '-')] = value
    return headers


def dict_len(dict_):
    length = 0
    for key in dict_:
        length += len(key) + len(dict_[key])
    return length
