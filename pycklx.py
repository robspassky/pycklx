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
import re
import json


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


#
# read xml, extract classes
#
klasses = {}
fields = {}


class Klass:
    def __init__(self):
        self.contexts = set()
        self.fields = {}
        self.name = ""

    def add(self, context, element):
        self.name = element.tag.capitalize()
        self.contexts.add(context)
        counts = {}
        for i in list(element):
            incr(counts, element.tag)
        for i in counts.keys():
            ftype = fields[i]
            if counts[i] > 1:
                self.fields[i] = "Array<{}>".format(ftype)
            else:
                self.fields[i] = ftype

    def __repr__(self):
        return """
-------------
Class: {}
Fields: {}
-------------
""".format(self.name, self.fields)


pinteger = re.compile('^[0-9]+$')
pfloat = re.compile('^[0-9]+\.[0-9]*$')


def do_branch(context, element):
    fields[element.tag] = element.tag.capitalize()
    klass = Klass()
    if element.tag in klasses:
        klass = klasses[element.tag]
    else:
        klasses[element.tag] = klass
    klass.add(context, element)


def do_leaf(context, element):
    fieldkey = "{}/{}".format(context, element.tag)
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


def analyze(input):
    stack = []

    iterator = xml.etree.ElementTree.iterparse(input, ['start', 'end'])
    for event, element in iterator:
        if event == "start":
            stack.append(element.tag)
        elif event == "end":
            stack.pop()
            if len(list(element)) > 0:
                do_branch(".".join(stack), element)
            else:
                do_leaf(".".join(stack), element)

    json.dumps(fields, sort_keys=True, indent=4)
    json.dumps(klasses, sort_keys=True, indent=4)


if __name__ == "__main__":
    analyze(sys.argv[1])
