#!/usr/bin/python3
#
# parse.py
#
# XML Analyzer written in python. On reading an XML file, pycklx will extract a
# set of classes to describe it.
#
# SPECS
#
# Parse the XML files generically.

import xml.etree.ElementTree
import sys
import io


context = [{}]


def startElement(element):
    elem = {}
    if len(element.attrib):
        elem["__ATTR__"] = {}
        for key, value in element.attrib.items():
            elem["__ATTR__"][key] = value
    context.append(elem)


def endElement(element):
    x = context.pop()
    if len(list(element)) == 0:
        if element.text is not None and len(element.text) > 0:
            x["__TEXT__"] = element.text
    if element.tag in context[-1]:
        if not isinstance(context[-1][element.tag], list):
            y = context[-1][element.tag]
            context[-1][element.tag] = [y]
        context[-1][element.tag].append(x)
    else:
        context[-1][element.tag] = x


def parse(input):
    iterator = xml.etree.ElementTree.iterparse(input, ['start', 'end'])
    for event, element in iterator:
        if event == "start":
            startElement(element)
        elif event == "end":
            endElement(element)
            if len(context) == 1:
                return context[0]


simpledoc = """<?xml version="1.0" encoding="UTF-8" ?>
<on>
  <header></header>
</on>"""

complexdoc = """<?xml version="1.0" encoding="UTF-8" ?>
<on>
  <header><inner>abc</inner><inner2></inner2></header>
  <body></body>
  <footer>
    <links></links>
  </footer>
</on>"""

siblingdoc = """<?xml version="1.0" encoding="UTF-8" ?>
<on>
  <header><inner>abc</inner><inner>def</inner></header>
</on>"""

attrdoc = """<?xml version="1.0" encoding="UTF-8" ?>
<on>
  <header one="1" two="2" three="three">abcdefghi</header>
  <body>hello there</body>
</on>"""


def test():
    doc = parse(io.StringIO(simpledoc))
    print(doc)
    doc = parse(io.StringIO(complexdoc))
    print(doc)
    doc = parse(io.StringIO(siblingdoc))
    print(doc)
    doc = parse(io.StringIO(attrdoc))
    print(doc)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        test()
    else:
        parse(sys.argv[1])
