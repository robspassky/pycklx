pycklx
======

This script will convert an xml file to a pickle file, and vice-versa.

$ pycklx input.xml -o output.p   # read from input.xml, write to output.p
$ pycklx -o output.p             # read from stdin, write to output.p
$ pycklx input.p -o output.xml   # read from input.p, write to output.xml
$ pycklx -t xml -o output        # read from stdin, write to output, convert from pickle *t*o xml

