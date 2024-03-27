import multiprocessing
import threading
import time
import io
import math
from lxml import etree

from . import url_path
from .url_path import URLPath

entrez_base = URLPath.from_str("https://eutils.ncbi.nlm.nih.gov/entrez/eutils")

req_lock = multiprocessing.Lock()
req_rate = 1/3

def delayed_unlock(l, t):
    def inner():
        time.sleep(t)
        l.release()
    threading.Thread(target=inner).start()

def entrez_request(req_type, email, *args, **kwargs):
    #assert "data" not in kwargs
    req = getattr(url_path, req_type)
    req_lock.acquire()
    kwargs.setdefault("params", {})
    #kwargs["json"]["email"] = email
    kwargs["params"]["email"] = email
    res = req(*args, **kwargs)
    delayed_unlock(req_lock, req_rate)
    return res

class EntrezManager:
    def __init__(self, email):
        self.email = email
        self.extra_args = {}

    def send_request(self, req_type, *args, **kwargs):
        kwargs.setdefault("params", {})
        kwargs["params"] |= self.extra_args
        return entrez_request(req_type, self.email, *args, **kwargs)
    
    def _xml_parsed(self, endpoint, **kwargs):
        resp = self.get(
            endpoint,
            params=kwargs
        )
        return etree.parse(io.BytesIO(resp.content))
    
    def einfo(self, **kwargs):
        return self._xml_parsed(entrez_base / "einfo.fcgi", **kwargs)
    
    def efetch(self, db, **kwargs):
        kwargs["db"] = db
        return self._xml_parsed(entrez_base / "efetch.fcgi", **kwargs)
    
    def elinks(self, dbfrom, db, **kwargs):
        kwargs["dbfrom"] = dbfrom
        kwargs["db"] = db
        return self._xml_parsed(entrez_base / "elink.fcgi", **kwargs)

    def esearch(self, db, term, **kwargs):
        kwargs["db"] = db
        kwargs["term"] = term
        return self._xml_parsed(entrez_base / "esearch.fcgi", **kwargs)

    def esearch_paged(self, db, term, keep, page_size=20, **kwargs):
        ret_start = 0
        count = math.inf
        kwargs["RetMax"] = page_size
        res = []
        while ret_start < count:            
            resp = self.esearch(db, term, RetStart=ret_start, **kwargs)
            count = int(resp.xpath("//Count")[0].text)
            new = resp.xpath(f"//{keep}")
            res = res + new
            ret_start += len(new)
        return res
            

for req_type in ("get", "post"):
    setattr(
        EntrezManager,
        req_type, 
        lambda self, *a, **k: self.send_request(req_type, *a, **k)
    )
