from enum import Enum, auto
from typing import Dict, Optional, Union

from httpx import Client
from requests import Session

from ._Requests import Adapter as _RAdapter
from ._Httpx import Adapter as _HAdapter

class TypeInjector(Enum):

    requests = auto()
    httpx = auto()

class ProxyType(Enum):
    
    socks5  = auto()
    http    = auto()

class ProxyParams:
    
    def __init__(self, type: ProxyType, IP: str, PORT: int, USERNAME: Optional[str] = None, PASSWORD: Optional[str] = None) -> None:
        self.proxy_url = None
        if USERNAME is not None and PASSWORD is not None:
            build = f'{USERNAME}:{PASSWORD}@{IP}:{PORT}'
        else:
            build = f'{IP}:{PORT}'
        if type == ProxyType.http:
            self.proxy_url = f'http://{build}'
        elif type == ProxyType.socks5:
            self.proxy_url = f'socks5://{build}'

class HTTPInjector(_HAdapter, _RAdapter):

    def __new__(cls, typeInjector: TypeInjector, timeout: int = 30, headers: Dict[str, str] = dict(), proxyParams: Optional[ProxyParams] = None) -> Union[Client, Session]:
        if not proxyParams:
            proxy_url = None
        else:
            proxy_url = proxyParams.proxy_url
        if typeInjector == TypeInjector.requests:
            return _RAdapter.__new__(cls, timeout, headers, proxy_url)
        elif typeInjector == TypeInjector.httpx:
            return _HAdapter.__new__(cls, timeout, headers, proxy_url)