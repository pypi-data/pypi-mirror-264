from urllib.parse import urlparse, ParseResult
from pathlib import PurePosixPath as Path
import requests
import functools
from typing import Union

class URLPath(ParseResult):
    @property
    def _path(self):
        return Path(self.path)

    def __truediv__(self, other):
        return self._replace(path=str(self._path / other))
    
    @classmethod
    def from_str(cls, url):
        return cls(*urlparse(url))
    
def url_request(request_type, url: Union[URLPath, str], *args, **kwargs):
    try:
        url = url.geturl()
    except AttributeError:
        pass
    return getattr(requests, request_type)(url, *args, **kwargs)

for req_type in ("get", "post"):
    globals()[req_type] = functools.partial(url_request, req_type)