#!/usr/bin/python3
#
# pycklx
#
# XML Analyzer written in python. On reading an XML file, pycklx will extract a
# set of classes to describe it.
#
# SPECS
#
# For every branch node, create a class with a capitalized name based on the
# tag. This class will have members, one per unique child seen. Children that
# are present at every instance of the branch node will be marked as required.
# A type will be assigned for each field based on the observed values --
# "float", "int", "string" or "date" for leaf children, and "array" and
# "object" will also be detected. "object" children will be a reference to
# another class.

import xml.etree.ElementTree
import dateutil.parser
import sys
import io
import re


def incr(d, k):
    if k in d:
        d[k] += 1
    else:
        d[k] = 1


def uniqkids(element):
    kids = set()
    for i in list(element):
        kids.add(i)
    return kids


def analyze(input, cb):
    counts = {}
    attrcounts = {}

    stack = []
    iterator = xml.etree.ElementTree.iterparse(input, ['start', 'end'])
    for event, element in iterator:
        if event == "start":
            e = {}
            e["tag"] = element.tag
            e["attribs"] = list(sorted(element.attrib.keys()))
            stack.append(e)
            key = ".".join(map(lambda x: x["tag"], stack))
            incr(counts, key)
        elif event == "end":
            if len(list(element)) > 0:
                key = ".".join(map(lambda x: x["tag"], stack))
                print("{}: {} children".format(key, len(list(element))))
            e = stack.pop()
            e["text"] = element.text
            if len(e) > 0:
                key = ",".join(e["attribs"])
                incr(attrcounts, key)
        # print("Event {}, Element {}".format(event, element))

    print("Element counts")
    for i in list(sorted(counts.keys())):
        print("{}: {}".format(i, counts[i]))

    print("Attribute counts")
    for i in list(sorted(attrcounts.keys())):
        print("{}: {}".format(i, attrcounts[i]))


def analyze2(input):
    counts = {}
    stack = []
    iterator = xml.etree.ElementTree.iterparse(input, ['end'])
    for event, element in iterator:
        if event == "start":
            stack.append(element.tag)
        elif event == "end":
            if len(stack) > 0:
                stack.pop()
            children = set(map(lambda x: x.tag, list(element)))
            text = element.text.strip()
            if len(children) > 0 and len(text) > 0:
                print("MIXED NODE: {} with {} children and text: {}".format(element.tag, len(children), text))
            else:
                key = ".".join(stack)
                childrenkey = ".".join(list(sorted(children)))
                if key not in counts:
                    counts[key] = {}
                incr(counts[key], childrenkey)
                incr(counts, "{}:PARENT".format(element.tag))
    print(counts)


class Klass:
    def __init__(self):
        self.contexts = set()
        self.fields = {}

    def add(self, context, element):
        self.contexts.add(context)



#
# read xml, extract classes
#
classes = {}
stack = []
fields = {}


pinteger = re.compile('^[0-9]+$')
pfloat = re.compile('^[0-9]+\.[0-9]*$')


def do_branch(element):
    obj = {}
    children = set(element)
    for k in children:
        if k in fields:
            obj[k] = fields[k]
        else:
            obj[k] = 'Unknown'
    classes[element.tag] = obj
    fields[element.tag] = element.tag.capitalize()


def do_leaf(element):
    fieldkey = "{}/{}".format(".".join(stack), element.tag)
    if pinteger.match(element.text):
        fields[fieldkey] = 'integer'
    elif pfloat.match(element.text):
        fields[fieldkey] = 'float'
    else:
        try:
            dateutil.parser.parse(element.text)
            fields[fieldkey] = 'date'
        except Exception:
            fields[fieldkey] = 'string'


def analyze3(input):
    iterator = xml.etree.ElementTree.iterparse(input, ['start', 'end'])
    for event, element in iterator:
        if event == "start":
            stack.append(element.tag)
        elif event == "end":
            stack.pop()
            children = set(element)
            if len(children) > 0:
                do_branch(element)
            else:
                do_leaf(element)
    print(fields)
    print(classes)


def test(file=None):
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<root>
  <object>
    <intfld>12345</intfld>
    <fltfld>13.234</fltfld>
    <strfld>These are the 123 times that try 5.5 men&quot;s souls.</strfld>
    <dtfld>2016-10-08</dtfld>
  </object>
</root>"""
    if file == None:
        analyze3(io.StringIO(xml))

if __name__ == "__main__":
    test(sys.argv[1])
    # import sys
    # analyze(sys.argv[1], None)
    # analyze2(sys.argv[1])
