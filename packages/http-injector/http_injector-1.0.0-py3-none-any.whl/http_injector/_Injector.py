from enum import Enum, auto
from typing import Dict, Optional, Union

from httpx import Client
from requests import Session

from ._Requests import Adapter as _RAdapter
from ._Httpx import Adapter as _HAdapter

class TypeInjector(Enum):

    requests = auto()
    httpx = auto()

class HTTPInjector(_HAdapter, _RAdapter):

    def __new__(cls, typeInjector: TypeInjector, timeout: int = 30, headers: Dict[str, str] = dict(), proxy_url: Optional[str] = None) -> Union[Client, Session]:
        #return super().__new__(cls, timeout, headers, proxy_url)
        if typeInjector == TypeInjector.requests:
            return _RAdapter.__new__(cls, timeout, headers, proxy_url)
        elif typeInjector == TypeInjector.httpx:
            return _HAdapter.__new__(cls, timeout, headers, proxy_url)