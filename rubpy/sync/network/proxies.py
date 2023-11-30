import requests
from urllib.parse import urlparse


class Proxies:
    def __init__(self,
                 host: str,
                 port: int,
                 type: str = 'http',
                 resolver: bool = False,
                 username: str = None,
                 password: str = None):
        if isinstance(type, str):
            if type.lower() not in ['http', 'https', 'socks5', 'socks4']:
                raise ValueError('Proxy type must be `socks5`, `socks4`, `http`, or `https`')

        self._resolver = resolver
        self._proxy_host = host
        self._proxy_port = port
        self._proxy_type = type
        self._proxy_username = username
        self._proxy_password = password

    @property
    def proxy_url(self):
        pattern = '{scheme}://{host}:{port}'
        if self._proxy_username:
            pattern = '{scheme}://{username}:{password}@{host}:{port}'
        return urlparse(pattern.format(scheme=self._proxy_type,
                                       username=self._proxy_username,
                                       password=self._proxy_password,
                                       host=self._proxy_host,
                                       port=self._proxy_port))

    @classmethod
    def from_url(cls, url, **kwargs):
        parse = urlparse(url)
        return cls(
            type=parse.scheme, port=int(parse.port), host=parse.hostname,
            username=parse.username, password=parse.password, **kwargs)

    def connect(self, req, timeout):
        if self.proxy_url.scheme in ['http', 'https']:
            req.proxies = {
                'http': self.proxy_url.geturl(),
                'https': self.proxy_url.geturl()
            }
            req.auth = (self._proxy_username, self._proxy_password)
        return requests.request(req.method, req.url, headers=req.headers, data=req.body, timeout=timeout)

    def _wrap_create_connection(self, protocol_factory, host=None, port=None, *args, **kwargs):
        if self.proxy_url.scheme not in ['http', 'https']:
            raise NotImplementedError("Socks proxy connection is not supported in synchronous mode.")
        else:
            return requests.Session()

    def send(self, req, **kwargs):
        timeout = kwargs.get('timeout')
        return self.connect(req, timeout)