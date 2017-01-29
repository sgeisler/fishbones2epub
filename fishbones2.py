#!/usr/bin/python3

import argparse
import requests
from lxml import html
from lxml.html import tostring
from ebooklib import epub
import sys
import os
import operator

FISHBONES_INDEX_URL = "http://www.fishbonescomic.com/novel/book02/"

COVER_TEMPLATE = '''
  <div style="text-align: center; padding: 0pt; margin: 0pt;">
    <img src="{}" >
  </div>
'''

def fetch_index():
    index_page = requests.get(FISHBONES_INDEX_URL)
    index_links = html.fromstring(index_page.content).xpath("//*[@id=\"post-184\"]/div/blockquote/p/a")
    # the filter is needed bc of a broken and doubled link to chapter 7
    return {chapter.text: chapter.attrib['href'] for chapter in filter(lambda link: link.text is not None, index_links)}

def fetch_chapter_content(chapter_url):
    chapter_page = requests.get(chapter_url)
    raw_paragraphs = html.document_fromstring(chapter_page.content).xpath(
        "//*[contains(concat(\" \", normalize-space(@class), \" \"), \" entry-content \")]/p"
    )
    return [tostring(p).decode("utf-8") for p in raw_paragraphs]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch all chapters from Fishbones II and produce an epub file')
    parser.add_argument('filename', metavar="file", type=str, help="output file")
    parser.add_argument('--cover', metavar="cover-image", type=str, help="cover image to use for the ebook")

    args = parser.parse_args()

    book = epub.EpubBook()

    book.set_title("Fishbones II")
    book.set_language('en')
    book.add_author("Jisuk Cho")
    book.spine.append('cover')

    if args.cover is not None:
        try:
            cover_image = open(args.cover, "rb")
        except (OSError, IOError) as e:
            print("ERROR: can't opem file '{}': {}".format(args.cover, str(e)), file=sys.stderr)
            exit(e.errno)
        image_name = os.path.basename(args.cover)
        book.set_cover(image_name, cover_image.read(), create_page=False)

        cover_page = epub.EpubHtml(file_name="cover.xhtml")
        cover_page.content = COVER_TEMPLATE.format(image_name)
        book.add_item(cover_page)
        book.spine.append(cover_page)

    print("fetching index ...")
    index = fetch_index()
    print("found {} chapters".format(len(index)))

    for progress, (chapter_title, chapter_url) in enumerate(sorted(index.items(), key=operator.itemgetter(0))):
        print("fetching {} ... ({} of {})".format(chapter_title, progress + 1, len(index)))
        chapter_paragraphs = fetch_chapter_content(chapter_url)
        print("{} has {} paragraphs".format(chapter_title, len(chapter_paragraphs)))
        chapter_html = "<h1>" + \
                       chapter_title + \
                       "</h1>" + \
                       "\n".join(chapter_paragraphs)
        chappter = epub.EpubHtml(title=chapter_title, file_name=(chapter_title.replace(" ", "_") + ".xhtml"))
        chappter.content = chapter_html

        book.add_item(chappter)
        book.toc.append(chappter)
        book.spine.append(chappter)

    book.add_item(epub.EpubNcx())

    epub.write_epub(args.filename, book)
    pass