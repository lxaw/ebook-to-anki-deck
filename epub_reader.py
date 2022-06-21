# for reading epubs
import ebooklib
from ebooklib import epub
from ebooklib.utils import debug

# for parsing epubs
from bs4 import BeautifulSoup
# for json
import json

from anki_commands import invoke, request

# delimiter for lines
kDELIM = '。'
# the shortest allowable size for text
kLINE_THRESHOLD_SIZE = 10
# name of new deck
kDECK_NAME = 'yougishax'
# name of card type
kMODEL_NAME = 'Japanese Card'

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
    for line in chapter_lines:
        if len(line) >= kLINE_THRESHOLD_SIZE:
            lines.append(line)

# make a deck if not present
#
# if kDECK_NAME not in invoke('deckNames'):
# invoke('createDeck',deck=kDECK_NAME)

dFields = {
    'Front':'',
    'Expression':'',
    'Japanese Example Sentence':'',
    'Japanese Definition':'',
    'Pronunciation (Kana/Pinyin)':'',
    'Test Word Alone?':'',
    'Recording':'',
    'Test final Kanji/Hanzi (combo)?':'',
    'Stroke Order Diagram 1':'',
    'Pronunciation (Pitch)':''
}

# add cards
#
for index,line in enumerate(lines):
    # put in fields
    dFields['Front'] = line

    note = {
        'deckName':kDECK_NAME,
        'modelName':kMODEL_NAME,
        'fields':dFields,
        }
    

    invoke('addNote',note=note)