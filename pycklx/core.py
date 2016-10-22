import xml.etree.ElementTree


def incr(d, k):
    if k in d:
        d[k] += 1
    else:
        d[k] = 1


def topickle(input, cb):
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

if __name__ == "__main__":
    import sys
    topickle(sys.argv[1], None)
