from urllib.parse import urlparse, parse_qsl, urlencode
import json
import msal
import os.path

try:
    import redis
    have_redis = True
except ImportError:
    have_redis = False


class FileCache(msal.TokenCache):

    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def exists(self):
        return os.path.exists(self.filename)

    def load(self):
        with open(self.filename, 'r') as fd:
            self._cache = json.load(fd)

    def save(self):
        with open(self.filename, 'w') as fd:
            json.dump(self._cache, fd)


class RedisCache(msal.TokenCache):

    def __init__(self, url, key):
        super().__init__()
        self.client = redis.from_url(url)
        self.key = key

    def exists(self):
        return self.client.get(self.key) is not None

    def load(self):
        self._cache = json.loads(self.client.get(self.key))

    def save(self):
        self.client.set(self.key, json.dumps(self._cache))


def from_url(url):
    parts = urlparse(url)
    if parts.scheme == 'file':
        return FileCache(parts.path)
    elif parts.scheme.startswith('redis'):
        if not have_redis:
            raise ValueError('Must install `redis` package')
        query = dict(parse_qsl(parts.query))
        key = query.pop('key')
        query = '?' + urlencode(query) if query else ''
        return RedisCache(
            '%s://%s%s%s' % (parts.scheme, parts.netloc, parts.path, query),
            key)
    raise ValueError('Unknown cache type %s')
