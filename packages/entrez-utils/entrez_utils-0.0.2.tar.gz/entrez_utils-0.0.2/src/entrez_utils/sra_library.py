import functools
from lxml import etree
from typing import Union

class SRALibrary:
    def __init__(
            self,
            xml: Union[etree._Element, etree._ElementTree],
            name=None,
            strategy=None,
            source=None,
            selection=None
        ):
        self.xml = xml
        self._name = name
        self._strategy = strategy
        self._source = source
        self._selection = selection

    def _xpath_prop(self, xpath, prop_name):
        if getattr(self, f"_{prop_name}") is None:
            setattr(self, f"_{prop_name}", self.xml.xpath(xpath)[0].text)
        return getattr(self, f"_{prop_name}")

for prop in ("name", "strategy", "source", "selection"):
    setattr(
        SRALibrary,
        prop,
        property(
            functools.partial(
                SRALibrary._xpath_prop,
                xpath="//LIBRARY_{}".format(prop.upper()),
                prop_name=prop
            )
        )
    )