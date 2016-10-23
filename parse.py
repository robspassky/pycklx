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
# import sys
import io


def parse(input):
    context = [{}]
    iterator = xml.etree.ElementTree.iterparse(input, ['start', 'end'])
    for event, element in iterator:
        if event == "start":
            context.append({})
        elif event == "end":
            x = context.pop()
            if element.tag in context[-1]:
                context[-1][element.tag].append(x)
            else:
                context[-1][element.tag] = [x]
            if len(context) == 1:
                return context[0]

simpledoc = """<?xml version="1.0" encoding="UTF-8" ?>
<on>
  <header></header>
</on>"""

complexdoc = """<?xml version="1.0" encoding="UTF-8" ?>
<on>
  <header><inner>abc</inner><inner>def</inner><inner2></inner2></header>
  <body></body>
  <footer>
    <links></links>
  </footer>
</on>"""


if __name__ == "__main__":
    # parse(sys.argv[1])
    doc = parse(io.StringIO(simpledoc))
    print(doc)
    doc = parse(io.StringIO(complexdoc))
    print(doc)
