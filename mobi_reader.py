import mobi
# for reading epubs
import ebooklib
from ebooklib import epub
from ebooklib.utils import debug

# for parsing epubs
from bs4 import BeautifulSoup

def chapter_to_str(chapter):
    soup = BeautifulSoup(chapter.get_body_content(),'html.parser')
    text = [para.get_text() for para in soup.find_all('p')]
    return ' '.join(text)


book_dir = "books/hoshi.mobi"

tempdir,filepath = mobi.extract(book_dir)
print(tempdir,filepath)

book = epub.read_epub(filepath)

items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

lines = []
for i in items:
    chapter_lines = chapter_to_str(i).split('。')
    for line in chapter_lines:
        # dont need duplicate sentences
        if len(line) > 0 and line not in lines:
            lines.append(line)
print(lines)