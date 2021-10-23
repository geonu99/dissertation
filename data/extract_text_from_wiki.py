import sys
import re
import html
from lxml import objectify

def extract_text_from_wiki_xml(filename):
    xml_data = objectify.parse(filename)
    root = xml_data.getroot()
    for child in root.getchildren():
        for node in child.getchildren()[-1].getchildren():
            yield node.text

def normalize(text):

    # filtering

    if not text:
        return
    if not text.count(" "):
        return
    if text.startswith("#REDIRECT"):
        return

    # refining

    text = html.unescape(text)
    text = re.sub("\[\[(.+?)\]\]", "\\1", text)
    text = re.sub("'{2,}", "'", text)
    text = re.sub("</?.+?>", " ", text)
    text = re.sub("\{\{.+?\}\}", " ", text)
    text = re.sub("\((.+?)\)", "\\1", text)
    text = re.sub("\s+", " ", text)
    text = text.strip()

    return text

if __name__ == "__main__":

    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        filename = "enwiki-20211001-pages-articles-multistream1.xml-p1p41242"

    dataiter = extract_text_from_wiki_xml(filename)
    outfile = open(sys.argv[1] + ".extracted", "w")

    for ln, text in enumerate(dataiter, 1):
        text = normalize(text)
        if not text:
            continue
        print(text, file = outfile)

        if ln % 100000 == 0:
            print("%d lines" % ln, file = sys.stder)

    outfile.close()
