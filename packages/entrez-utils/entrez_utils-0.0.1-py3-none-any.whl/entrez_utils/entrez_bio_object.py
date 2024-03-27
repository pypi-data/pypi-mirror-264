from functools import cached_property, lru_cache

from lxml import etree

from .ncbi import ncbi_base
from .entrez import EntrezManager

class EntrezBioObject:
    def __init__(self, accession=None):
        self._accession = accession

    @property
    def accession(self):
        return self._accession
    
def fetch_multi(objs):
    return type(objs[0]).fetch_multi(objs)

def fetched(objs):
    fetch_multi(objs)
    return objs
    
class FetchableBioObject(EntrezBioObject):
    xml_cache = {}

    def __init__(
        self,
        entrez_man: EntrezManager,
        *args,
        entrez_id = None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._man = entrez_man
        self._entrez_id = entrez_id
        self._xml = None

    @property
    def _lookup_id(self):
        if self._entrez_id is not None:
            return self._entrez_id
        return self._accession
    
    def get_xml(self):
        try:
            return type(self).xml_cache[str(self._lookup_id)]
        except KeyError:
            return self._man.efetch(self.db, id=self._lookup_id)
        
    def get_ids(self):
        return [self.accession, self.entrez_id]
    
    @property
    def xml(self):
        if self._xml is None:
            self.xml = self.get_xml()
        return self._xml
    
    @xml.setter
    def xml(self, xml):
        self._xml = xml
        for obj_id in self.get_ids():
            type(self).xml_cache[obj_id] = self.xml

    # @cached_property
    # def xml(self):
    #     xml = self._man.efetch(self.db, id=self._lookup_id)
    #     try:
    #         xml = xml.xpath(f"//{self.object_root}")[0]
    #     except AttributeError:
    #         pass
    #     return xml
    
    @lru_cache(None)
    def links(self, to):
        return self._man.elinks(self.db, to, id=self.entrez_id)
    
    @property
    def entrez_id(self):
        if self._entrez_id is None:
            self._entrez_id = self.get_entrez_id()
        return self._entrez_id

    @property
    def accession(self):
        if self._accession is None:
            self._accession  = self.get_accession()
        return self._accession
    
    @cached_property
    def url(self):
        return ncbi_base / self.db / self.accession
    
    @classmethod
    def from_xml(cls, man, xml):
        inst = cls(man)
        inst.xml = xml
        return inst
    
    @classmethod
    def fetch_multi(cls, objs):
        full_xml = objs[0]._man.efetch(cls.db, id=[x._lookup_id for x in objs])
        for obj, elem in zip(objs, full_xml.xpath(f"//{cls.object_root}")):
            obj.xml = etree.ElementTree(elem)
        return full_xml