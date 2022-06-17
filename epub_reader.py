import ebooklib
from bs4 import BeautifulSoup

from ebooklib import epub
from ebooklib.utils import debug

kDELIM = '。'

def chapter_to_str(chapter):
    soup = BeautifulSoup(chapter.get_body_content(),'html.parser')
    text = [para.get_text() for para in soup.find_all('p')]
    return ' '.join(text)

strTestFile = './books/yougishax.epub'
book = epub.read_epub(strTestFile)

items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

lines = []
for i in items:
    chapter_lines = chapter_to_str(i).split(kDELIM)
    lines += chapter_lines

# make deck out of it!
#