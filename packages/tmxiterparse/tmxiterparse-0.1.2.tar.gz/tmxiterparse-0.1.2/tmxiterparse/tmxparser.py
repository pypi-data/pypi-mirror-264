import defusedxml.ElementTree as ET
import os

from typing import NamedTuple, Dict, Iterator, Tuple, Any, List


class Tuv(NamedTuple):
    properties:Dict[str,str]
    lang:str
    value:str

class Tu(NamedTuple):
    properties:Dict[str,str]
    tuid:str
    datatype:str
    values:List[Tuv]


class TmxParser(object):
    def __init__(self, path:str) -> None:
        self.path = path
        self.fp = None
        self.elem_iterparse = None
        self.opened = False
        self.header_dict = {}

    @property
    def header(self) -> Dict[str, str]:
        return self.header_dict
    
    def open(self) -> None:
        if self.opened:
            return
        self.fp = open(self.path, "r", encoding="utf-8")
        self.elem_iterparse = ET.iterparse(self.fp, events=["start", "end"])
        run = True
        while run and (n := self.elem_iterparse.__next__()):
            event, elem = n[0], n[1]
            if event == "start" and elem.tag == "header":
                self.header_dict = elem.attrib
            elif event == "start" and elem.tag == "body":
                run = False
            elem.clear()
        self.opened = True
        
    def close(self) ->None:
        self.elem_iterparse = None
        if self.fp is not None and not self.fp.closed:
            self.fp.close()
        self.opened = False

    def __enter__(self) -> 'TmxParser':
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.opened:
            self.close()

    def __iter__(self) -> 'TmxParser':
        self.open()
        return self

    def __next__(self) -> Tu:
        def parse_tuv(elem, iterator:Iterator[Tuple[str,Any]]) -> Tuv:
            properties = {}
            value = None
            lang = None
            for k,v in elem.attrib.items():
                if k in {"xml:lang", "{http://www.w3.org/XML/1998/namespace}lang"}:
                    lang = v
                else:
                    properties[k] = v
            run = True
            while run and (n := iterator.__next__()):
                event, elem = n[0], n[1]
                if event == "end" and elem.tag == "tuv":
                    run = False
                if event == "start" and elem.tag == "prop":
                    properties[elem.attrib["type"]] = elem.text
                elif event == "start" and elem.tag == "seg":
                    value = elem.text
                elem.clear()
            return Tuv(properties, lang, value)
        def parse_tu(elem, iterator:Iterator[Tuple[str,Any]]) -> Tu:
            properties = {}
            values = []
            tuid = None
            datatype = None
            for k,v in elem.attrib.items():
                if k == "tuid":
                    tuid = v
                elif k == "datatype":
                    datatype = v
                else:
                    properties[k] = v
            run = True
            while run and (n := iterator.__next__()):
                event, elem = n[0], n[1]
                if event == "end" and elem.tag == "tu":
                    run = False
                if event == "start" and elem.tag == "prop":
                    properties[elem.attrib["type"]] = elem.text
                elif event == "start" and elem.tag == "tuv":
                    values.append(parse_tuv(elem, iterator))
                elem.clear()
            return Tu(properties, tuid, datatype, values)

        while (n := self.elem_iterparse.__next__()):
            event, elem = n[0], n[1]
            if event == "start" and elem.tag == "tu":
                return parse_tu(elem, self.elem_iterparse)
            elem.clear()
        return None