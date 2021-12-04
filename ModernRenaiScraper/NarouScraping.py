from NarouScraper2 import get_page
from NarouIndexScraper import get_index, get_indexes

def main():
    ncodes = get_indexes()
    for hrefs in get_index():
        for href in hrefs:
            get_page(href, ncodes)

if __name__=='__main__':
    main()