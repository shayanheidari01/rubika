import struct
import socket
import asyncio
from ..gadgets import exceptions
from aiohttp import TCPConnector
from urllib.parse import urlparse
from aiohttp.abc import AbstractResolver


class BaseSocketWrapper(object):
    def __init__(self, loop, host, port, family=socket.AF_INET):
        self._loop = loop
        self._socket = None
        self._family = family
        self._dest_host = None
        self._dest_port = None
        self._socks_host = host
        self._socks_port = port

    async def _send(self, request):
        data = bytearray()
        for item in request:
            if isinstance(item, int):
                data.append(item)
            elif isinstance(item, (bytearray, bytes)):
                data += item
            else:
                raise ValueError('Unsupported item')
        await self._loop.sock_sendall(self._socket, data)

    async def _receive(self, n):
        data = b''
        while len(data) < n:
            packet = await self._loop.sock_recv(self._socket, n - len(data))
            if not packet:
                raise exceptions.InvalidServerReply('Not all data available')
            data += packet
        return bytearray(data)

    async def _resolve_addr(self, host, port):
        addresses = await self._loop.getaddrinfo(host=host, port=port,
                                                 family=socket.AF_UNSPEC,
                                                 type=socket.SOCK_STREAM,
                                                 proto=socket.IPPROTO_TCP,
                                                 flags=socket.AI_ADDRCONFIG)
        if not addresses:
            raise OSError(f'Can`t resolve address {host}:{host}')
        return addresses[0][0], addresses[0][4][0]

    async def negotiate(self):
        raise NotImplementedError

    async def connect(self, address):
        self._dest_host = address[0]
        self._dest_port = address[1]
        self._socket = socket.socket(family=self._family,
                                     type=socket.SOCK_STREAM)
        self._socket.setblocking(False)

        try:
            await self._loop.sock_connect(sock=self._socket,
                                          address=(self._socks_host,
                                                   self._socks_port))
        except OSError as x:
            self.close()
            raise exceptions.SocksConnectionError(
                x.errno,
                'Can not connect to proxy'
                f'{self._socks_host}:{self._socks_port} [{x.strerror}]'
            ) from x
        except asyncio.CancelledError:
            self.close()

        try:
            await self.negotiate()
        except exceptions.SocksError:
            self.close()

        except asyncio.CancelledError:
            if isinstance(self._loop, asyncio.ProactorEventLoop):
                self.close()

    def close(self):
        self._socket.close()

    async def sendall(self, data):
        await self._loop.sock_sendall(self._socket, data)

    async def recv(self, nbytes):
        return await self._loop.sock_recv(self._socket, nbytes)

    @property
    def socket(self):
        return self._socket


class Socks4SocketWrapper(BaseSocketWrapper):
    def __init__(self, loop, host, port, user_id=None, resolver=False):
        BaseSocketWrapper.__init__(self, loop=loop, host=host,
                                   port=port, family=socket.AF_INET)
        self._user_id = user_id
        self._resolver = resolver

    async def _socks_connect(self):
        host = self._dest_host
        include_hostname = False
        try:
            host_bytes = socket.inet_aton(self._dest_host)
        except socket.error:
            if self._resolver:
                host_bytes = bytes([0x00, 0x00, 0x00, 0x01])
                include_hostname = True
            else:
                _, host = await self._resolve_addr(self._dest_host,
                                                   self._dest_port)
                host_bytes = socket.inet_aton(self._dest_host)

        request = [0x04, 0x01, struct.pack('>H', self._dest_port), host_bytes]

        if self._user_id:
            request.append(self._user_id.encode())

        request.append(0x00)

        if include_hostname:
            request += [host.encode('idna'), 0x00]

        await self._send(request)

        respond = await self._receive(8)

        if respond[0] != 0x00:
            raise exceptions.InvalidServerReply(
                'SOCKS4 proxy server sent invalid data')

        if respond[1] == 0x5B:
            raise exceptions.SocksError('Request rejected or failed')

        elif respond[1] == 0x5C:
            raise exceptions.SocksError('Request rejected because SOCKS server')

        elif respond[1] == 0x5D:
            raise exceptions.SocksError(
                'Request rejected because the client program')

        elif respond[1] != 0x5A:
            raise exceptions.SocksError('Unknown error')

        return ((host, self._dest_port),
                socket.inet_ntoa(respond[4:]),
                struct.unpack('>H', respond[2:4])[0])

    async def negotiate(self):
        await self._socks_connect()


class Socks5SocketWrapper(BaseSocketWrapper):
    def __init__(self, loop, host, port, username=None,
                 password=None, resolver=True, family=socket.AF_INET):
        BaseSocketWrapper.__init__(self, loop=loop, host=host,
                                   port=port, family=family)
        self._resolver = resolver
        self._username = username
        self._password = password

    async def _socks_auth(self):
        auth_methods = [0x00]
        if self._username and self._password:
            auth_methods = [0x02, 0x00]

        await self._send([0x05, len(auth_methods)] + auth_methods)
        respond = await self._receive(2)
        if respond[0] != 0x05:
            raise exceptions.InvalidServerVersion(
                f'Unexpected SOCKS version number: {respond[0]}')

        if respond[1] == 0xFF:
            raise exceptions.NoAcceptableAuthMethods(
                'No acceptable authentication methods were offered')

        if respond[1] not in auth_methods:
            raise exceptions.UnknownAuthMethod(
                f'Unexpected SOCKS authentication method: {respond[1]}')

        if respond[1] == 0x02:
            await self._send([0x01,
                              chr(len(self._username)).encode(),
                              self._username.encode(),
                              chr(len(self._password)).encode(),
                              self._password.encode()])

            respond = await self._receive(2)
            if respond[0] != 0x01:
                raise exceptions.InvalidServerReply(
                    'Invalid authentication response')

            if respond[1] != 0x00:
                raise exceptions.LoginAuthenticationFailed(
                    'Username and password authentication failure')

    async def _socks_connect(self):
        req_addr, resolved_addr = await self._build_dest_address()
        await self._send([0x05, 0x01, 0x00] + req_addr)
        respond = await self._receive(3)
        if respond[0] != 0x05:
            raise exceptions.InvalidServerVersion(
                f'Unexpected SOCKS version number: {respond[0]}')

        if respond[1] == 0x01:
            raise exceptions.SocksError('General SOCKS server failure')

        elif respond[1] == 0x02:
            raise exceptions.SocksError('Connection not allowed by ruleset')

        elif respond[1] == 0x03:
            raise exceptions.SocksError('Network unreachable')

        elif respond[1] == 0x04:
            raise exceptions.SocksError('Host unreachable')

        elif respond[1] == 0x05:
            raise exceptions.SocksError('Connection refused')

        elif respond[1] == 0x06:
            raise exceptions.SocksError('TTL expired')

        elif respond[1] == 0x07:
            raise exceptions.SocksError('Command not supported, or protocol error')

        elif respond[1] == 0x08:
            raise exceptions.SocksError('Address type not supported')

        elif respond[1] != 0x00:
            raise exceptions.SocksError('Unknown error')

        if respond[2] != 0x00:
            raise exceptions.InvalidServerReply('The reserved byte must be 0x00')

        return resolved_addr, await self._read_binded_address()

    async def _build_dest_address(self):
        port_bytes = struct.pack('>H', self._dest_port)
        for family in (socket.AF_INET, socket.AF_INET6):
            try:
                host_bytes = socket.inet_pton(family, self._dest_host)
                return (
                    [0x01 if family == socket.AF_INET else 0x04,
                     host_bytes, port_bytes],
                    (self._dest_host, self._dest_port)
                )

            except socket.error:
                pass

        if self._resolver:
            host_bytes = self._dest_host.encode('idna')
            return [0x03, chr(len(host_bytes)).encode(),
                    host_bytes, port_bytes], (self._dest_host, self._dest_port)

        family, _ = await self._resolve_addr(host=self._dest_host,
                                             port=self._dest_port)
        return (
            [0x01 if family == socket.AF_INET else 0x04,
             host_bytes, port_bytes],
            (socket.inet_ntop(family, host_bytes), self._dest_port)
        )

    async def _read_binded_address(self):
        atype = (await self._receive(1))[0]
        if atype == 0x01:
            addr = await self._receive(4)
            addr = socket.inet_ntoa(addr)
        elif atype == 0x03:
            length = await self._receive(1)
            addr = await self._receive(ord(length))
        elif atype == 0x04:
            addr = await self._receive(16)
            addr = socket.inet_ntop(socket.AF_INET6, addr)
        else:
            raise exceptions.InvalidServerReply(
                'SOCKS5 proxy server sent invalid data')
        port = await self._receive(2)
        return addr, struct.unpack('>H', port)[0]

    async def negotiate(self):
        await self._socks_auth()
        await self._socks_connect()


class Resolver(AbstractResolver):
    async def resolve(self, host, port=0, family=socket.AF_INET):
        return [{
                'proto': 0, 'flags': 0,
                'host': host, 'port': port,
                'family': family, 'hostname': host}]

    async def close(self):
        pass


class Proxies(TCPConnector):

    def __init__(self,
                 host: str,
                 port: int,
                 type: str = 'http',
                 resolver: bool = False,
                 username: str = None,
                 password: str = None,
                 family=socket.AF_INET, *args, **kwargs):
    
        if isinstance(type, str):
            if type.lower() not in ['http', 'https', 'socks5', 'socks4']:
                raise ValueError(
                    'proxy type must be'
                    '(`socks5` | `socks4` | `http` | `https` )')
        if resolver:
            kwargs['resolver'] = Resolver()

        TCPConnector.__init__(self, **kwargs)
        self._resolver = resolver
        self._proxy_host = host
        self._proxy_port = port
        self._proxy_type = type
        self._proxy_family = family
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
        """_from_url_

        Args:
            url (str): proxy url
                http exmaple: http://login:password@127.0.0.1:1080
                https exmaple: https://login:password@127.0.0.1:1080
                socks4 exmaple: socks4://username:password@127.0.0.1:1080
                socks5 exmaple: socks5://username:password@127.0.0.1:1080
        """        
        parse = urlparse(url)
        return cls(
            type=parse.scheme, port=int(parse.port), host=parse.hostname,
            username=parse.username, password=parse.password, **kwargs)

    async def connect(self, req, traces, timeout):
        if self.proxy_url.scheme in ['http', 'https']:
            req.update_proxy(self.proxy_url._replace(scheme='https').geturl(),
                             None, req.proxy_headers)
        return await TCPConnector.connect(
            self, req=req, traces=traces, timeout=timeout)

    async def _wrap_create_connection(self, protocol_factory, host=None,
                                    port=None, *args, **kwargs):
        if self.proxy_url.scheme not in ['http', 'https']:
            if self.proxy_url.scheme == 'socks5':
                sock = Socks5SocketWrapper(resolver=self._resolver,
                                            loop=self._loop,
                                            host=self._proxy_host,
                                            port=self._proxy_port,
                                            family=self._proxy_family,
                                            username=self._proxy_username,
                                            password=self._proxy_password)
            else:
                sock = Socks4SocketWrapper(resolver=self._resolver,
                                            loop=self._loop,
                                            host=self._proxy_host,
                                            port=self._proxy_port,
                                            user_id=self._proxy_username)
            await sock.connect((host, port))
            return await TCPConnector._wrap_create_connection(
                self, protocol_factory, None, None,
                *args, sock=sock.socket, **kwargs)
        else:
            return await TCPConnector._wrap_create_connection(
                self, protocol_factory, host, port,
                *args, **kwargs)
