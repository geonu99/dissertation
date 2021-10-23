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

    if len(sys.argv) != 2:
        sys.exit("Usage: %s wiki_xml_file" % sys.argv[0])

    filename = sys.argv[1]
    dataiter = extract_text_from_wiki_xml(filename)
    outfile = open(sys.argv[1] + ".extracted", "w")

    for text in dataiter:
        text = normalize(text)
        if not text:
            continue
        print(text, file = outfile)

    outfile.close()
