import sys
import re
import html

fo = open("enwiki-20211001-pages-articles-multistream1.xml-p1p41242")

def extract(line):

    # filtering

    if not line:
        return
    if line[0] == "*":
        return
    if line.startswith("File:"):
        return
    if line.startswith("#REDIRECT"):
        return
    if re.match("^[!|]", line):
        return
    if line.startswith("&lt;"):
        return
    if line[:2] in ("[[", "{{", "}}", "=="):
        return

    # refining

    line = html.unescape(line)
    line = re.sub("'{2,}", "'", line)
    line = re.sub("\(.+?\)", "", line)
    line = re.sub("\{\{.+?\}\}", "", line)
    line = re.sub("\[\[(.+?)\]\]", "\\1", line)
    line = re.sub("</?.+?>", " ", line)
    line = re.sub("\s+", " ", line)
    line = line.strip()

    print(line)

flag = False

for line in fo:
    line = line.strip()

    if line.count("<text"):
        line = re.sub(".*<text.+?>", "", line)
        flag = True

    if line.count("</text>"):
        line = re.sub("</text.+?>.*", "", line)
        extract(line)
        flag = False

    if not flag:
        continue

    extract(line)


fo.close()
