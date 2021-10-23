from sfpd.words import count_words
from sfpd.words import top_words_llr, top_words_sfpd, top_words_chi2

def textiter(filename, maxln = -1):
    with open(filename) as f:
        for ln, line in enumerate(f, 1):
            yield line.strip()
            if maxln > 0 and ln == maxln:
                return

background = textiter("./data/enwiki-20211001-pages-articles-multistream1.xml-p1p41242.extracted", 10000)
target = textiter("./data/sample")

background_counts = count_words(background, min_count = 4, language = "en_core_web_sm")
target_counts = count_words(target, min_count = 4, language = "en_core_web_sm")

words = top_words_sfpd(target_counts, background_counts)

print(words)
