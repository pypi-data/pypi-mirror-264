from lxml import etree
from functools import cached_property

from .entrez_bio_object import FetchableBioObject
from .sra_library import SRALibrary

html_ns = {
    "x": "http://www.w3.org/1999/xhtml"
}

class BioProject(FetchableBioObject):
    db = "bioproject"

    @cached_property
    def _archive_id(self):
        arch_id_l = self.xml.xpath("//ArchiveID")
        assert len(arch_id_l) == 1
        return arch_id_l[0]
    
    def get_entrez_id(self):
        return self._archive_id.attrib["id"]
    
    def get_accession(self):
        return self._archive_id.attrib["accession"]

    @cached_property
    def samples(self):
        return [
            BioSample(self._man, entrez_id=elem.text) 
            for elem in self.links(
                "biosample"
            ).xpath(
                ("//LinkSetDb/LinkName[text() = 'bioproject_biosample_all']/../"
                "Link/Id")
            )
        ]

    @cached_property
    def experiments(self):
        return [
            SRAExperiment(self._man, entrez_id=elem.text)
            for elem in self.links(
                "sra"
            ).xpath(
                ("//LinkSetDb/LinkName[text() = 'bioproject_sra_all']/../"
                "Link/Id")
            )
        ]
            

class BioSample(FetchableBioObject):
    db = "biosample"
    object_root = "//BioSample"

    @cached_property
    def _ids(self):
        return self.xml.xpath("//Ids")[0]
    
    def _get_id(self, **kwargs):
        ids = self._ids.xpath(
            "./Id[{}]".format(
                " and ".join(f"@{k}='{v}'" for (k, v) in kwargs.items())
            )
        )
        assert len(ids) == 1
        return ids[0].text
    
    def get_entrez_id(self):
        return self.xml.xpath("//BioSample")[0].attrib["id"]

    def get_accession(self):
        return self._get_id(db="BioSample")
    
    @property
    def sample_name(self):
        return self._get_id(db_label="Sample name")
    
    @property
    def sra_id(self):
        return self._get_id(db="SRA")
    
    @cached_property
    def experiments(self):
        return [
            SRAExperiment(self._man, entrez_id=elem.text)
            for elem in self.links(
                "sra"
            ).xpath(
                ("//LinkSetDb/LinkName[text() = 'biosample_sra']/../"
                "Link/Id")
            )
        ]

    @cached_property
    def projects(self):
        return [
            BioProject(self._man, entrez_id=elem.text)
            for elem in self.links(
                "biosample"
            ).xpath(
                ("//LinkSetDb/LinkName[text() = 'biosample_bioproject_all']/../"
                 "Link/Id")
            )
        ]
    
    @cached_property
    def sample_attributes(self):
        return {
            el.attrib["attribute_name"]: el.text 
            for el in self.xml.xpath(f"//Attribute")
        }

    @classmethod
    def from_sra_accessions(cls, man, accs):
        res = man.esearch_paged(
            cls.db,
            " OR ".join(accs),
            field="accn",
            keep="Id"
        )
        from IPython import embed
        #embed()
        assert len(res) == len(accs)
        return [cls(man, entrez_id=elem.text) for elem in res]
    
    # def get_sample_attribute(self, attr):
    #     return self.xml.xpath(f"//Attribute[@attribute_name='{attr}']")[0].text
    
    @property
    def title(self):
        return self.xml.xpath("//Title")[0].text

class SRAObject(FetchableBioObject):
    db = "sra"
    
    @cached_property
    def experiment(self):
        return SRAExperiment.from_xml(
            self._man,
            self._man.efetch(self.db, id=self._lookup_id)
        )

class SRAExperiment(SRAObject):
    entrez_id_cache = {}
    object_root = "//EXPERIMENT_PACKAGE"

    def get_accession(self):
        return self.xml.xpath("//EXPERIMENT/IDENTIFIERS/PRIMARY_ID")[0].text

    def get_entrez_id(self):
        #parser = etree.HTMLParser()
        try:
            return type(self).entrez_id_cache[self.accession]
        except KeyError:
            pass
        resp = self._man.get(
            self.url
        )
        tree = etree.fromstring(resp.content)
        entrez_id = tree.xpath(
            "//x:dl[@class='rprtid']/x:dd",
            namespaces=html_ns
        )[0].text
        type(self).entrez_id_cache[self.accession] = entrez_id
        return entrez_id
    
    @cached_property
    def runs(self):
        res = []
        for elem in self.xml.xpath("//RUN"):
            run = SRARun.from_xml(etree.ElementTree(self._man), elem)
            run.experiment = self
            res.append(run)
        return res

    @cached_property
    def samples(self):
        return [
            BioSample(self._man, entrez_id=elem.text)
            for elem in self.links(
                "biosample"
            ).xpath(
                ("//LinkSetDb/LinkName[text() = 'sra_biosample']/../"
                "Link/Id")
            )
        ]

    @property
    def projects(self):
        return [
            BioProject(self._man, entrez_id=elem.text)
            for elem in self.links(
                "bioproject"
            ).xpath(
                ("//LinkSetDb/LinkName[text() = 'sra_bioproject_all']/../"
                "Link/Id")
            )
        ]

    @cached_property
    def library(self):
        return SRALibrary(self.xml.xpath("//LIBRARY_DESCRIPTOR")[0])

    @cached_property
    def title(self):
        return self.xml.xpath("//TITLE")[0].text   

class SRARun(SRAObject):
    @cached_property
    def xml(self):
        xml = super().xml
        res =  xml.xpath("//RUN[@accession='{}']".format(self.accession))
        assert len(res) == 1
        return res[0]
    
    def get_ids(self):
        return [self.accession]
    
    def get_accession(self):
        return self.xml.xpath("./IDENTIFIERS/PRIMARY_ID")[0].text
    
    @cached_property
    def download_link(self):
        res = self.xml.xpath(
            ("./SRAFiles/SRAFile[@semantic_name='SRA Normalized']/"
             "Alternatives[@access_type='anonymous']")
        )
        assert len(res) == 1
        return res[0].attrib["url"]
