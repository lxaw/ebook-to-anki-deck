# for reading epubs
import ebooklib
from ebooklib import epub
from ebooklib.utils import debug

# for parsing epubs
from bs4 import BeautifulSoup
# for json
import json

from anki_commands import invoke, request

class BookToAnki():
    """
    Note that cards are generated to the "Default" note type as it is
    difficult to program for each card type.
    """
    def __init__(self):
        self.kPOSSIBLE_EXTENSIONS = ['.epub','.txt','.mobi']
        self.kMODEL_NAME= "Default"
        self.kFRONT_FIELD = "Front"
        self.kBACK_FIELD = "Back"
    
    def listChapterToStr(self,chapter):
        soup = BeautifulSoup(chapter.get_body_content(),'html.parser')
        text = [para.get_text() for para in soup.find_all('p')]
        return ' '.join(text)
    
    def fromTxt(self,strTextFile,strOutDeckName,strDelim = '。'):
        pass
    
    def fromMobi(self,strMobi,strOutDeckName,strDelim = '。'):
        pass
    
    def fromEpub(self,strEpubFile,strOutDeckName,strDelim = '。'):
        """
        Creates an anki deck from EPUB file.
        """
        book = epub.read_epub(strEpubFile)
        items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

        lines = []
        for i in items:
            chapter_lines = self.listChapterToStr(i).split(strDelim)
            for line in chapter_lines:
                if len(line) > 0 and line not in lines:
                    lines.append(line)
        
        # make deck if not present
        if strOutDeckName not in invoke('deckNames'):
            invoke('createDeck',deck=strOutDeckName)
        
        for line in lines:
            note = {
                'deckName':strOutDeckName,
                'modelName':self.kMODEL_NAME,
                'fields':{
                    self.kFRONT_FIELD:line,
                    self.kBACK_FIELD: '',
                },
                'options':{
                    'allowDuplicate':True,
                }
            }
            invoke('addNote',note=note)

    def makeDeck(self, strSrcFile, strOutDeckName,strDelim = '。')
        """
        Finds what types of book file you have and converts it to anki deck.
        """
        strFileExtension = strSrcFile.split('.')[-1]
        
        if strFileExtension = "txt":
            pass
        elif strFileExtension = "mobi"
            pass
        elif strFileExtension = "epub":
            pass
        else:
            print('file extension: {} is not supported.'.format(strFileExtension))
            print('please use one of the below file types: ')
            for e in self.kPOSSIBLE_EXTENSIONS:
                print(e)
            print()

        pass