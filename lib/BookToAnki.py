#
# BookToAnki
#
# Written by Lex Whalen, 06/26/22
#
# A simple program to create Anki decks from common book file types.
# At the moment of release (06/26/22), only three types are supported:
# .txt, .epub, and .mobi
#

import mobi
# for reading epubs
import ebooklib
from ebooklib import epub
from ebooklib.utils import debug

# for parsing epubs
from bs4 import BeautifulSoup
# for json
import json

# threading
from multiprocessing import cpu_count
from threading import Thread

# anki commands
from .anki_commands import invoke, request

#
# BookToAnki
#
# This class manages all functions related to creation of Anki decks from books.
#
class BookToAnki():
    """
    Note that cards are generated to the "default_bta" model type as it is
    difficult to program for each card type.
    """
    def __init__(self):
        # the model type cards will be generated to
        self.kMODEL_NAME= "default_bta"

        # number of cpus
        self.kCPU_COUNT = cpu_count()

        # always create the model type we will be using if not present
        self.createDefaultModel()

    def voidWorkerProcess(self, listFragment,strOutDeckName):
        # worker process to create cards
        for line in listFragment:
            if len(line.strip()) > 0:
                self.createNote(line,'',strOutDeckName)
    
    def listSplitList(self, listContent, intDivisions):
        # splits a list of content into some number of lists
        intLineCount = len(listContent)

        listRet = [[]] * intDivisions

        intRegularSectionLineWidth = intLineCount // intDivisions

        # prepare the lists
        for i in range(0,intDivisions):
            if (i == intDivisions- 1):
                listRet[i] = [0] * (
                    intRegularSectionLineWidth + (intLineCount % intDivisions) 
                )
            else:
                listRet[i] = [0]*intRegularSectionLineWidth
        # populate the lists
        intListIndex = 0
        intListInnerIndex = 0

        for line in listContent:
            listRet[intListIndex][intListInnerIndex] = line

            intListInnerIndex +=1
            
            if (intListInnerIndex != 0) and (intListInnerIndex % intRegularSectionLineWidth == 0):
                if intListIndex != intDivisions - 1:
                    # next list
                    intListIndex += 1
                    # restart inner
                    intListInnerIndex = 0

        return listRet 
    
    def listChapterToStr(self,chapter):
        """
        Inputs: epub chapter (essentially similar to html)
        Outputs: list of text from the chapter
        Function: get the text from a chapter
        """
        soup = BeautifulSoup(chapter.get_body_content(),'html.parser')
        text = [para.get_text() for para in soup.find_all('p')]

        return ' '.join(text)
    
    def runThreads(self, listContent,strOutDeckName):
        """
        Runs the threads to do work
        """
        listSplit = self.listSplitList(listContent,self.kCPU_COUNT)
        listThreads = [Thread(target=self.voidWorkerProcess,args=(listSplit[i],strOutDeckName)) for i in range(0,self.kCPU_COUNT)]

        for i in range(0, self.kCPU_COUNT):
            listThreads[i].start()
        
        for i in range(0, self.kCPU_COUNT):
            listThreads[i].join()
    
    def createDefaultModel(self):
        """
        Inputs: void
        Outputs: void
        Function: Creates the model 'default_bta' for
        use in creation of notes.
        """
        # if already created, do nothing
        if self.kMODEL_NAME in invoke('modelNames'):
            return
        # else create
        inOrderFields = ['Front','Back']
        cardTemplates = [
            {
                'Name':'Card 1',
                'Front': "{{Front}}",
                'Back':"{{Back}}"
            }
        ]

        invoke('createModel',modelName = self.kMODEL_NAME,
        inOrderFields = inOrderFields,cardTemplates=cardTemplates) 


    
    def fromTxt(self,strTextPath,strOutDeckName,strDelim = '。'):
        """
        Inputs: path of text file, name of deck to export to, delimiter to parse the text file with
        Outputs: void
        Function: creates an Anki deck from a text file.
        """
        # read the text file, then create notes

        with open(strTextPath,'r') as f:
            # create deck if not present
            if strOutDeckName not in invoke('deckNames'):
                invoke('createDeck',deck=strOutDeckName)
            data = f.read().split(strDelim)

            self.runThreads(data,strOutDeckName)


    def fromMobi(self,strMobiPath,strOutDeckName,strDelim = '。'):
        """
        Inputs: path of mobi file, name of deck to export to, delimiter to parse the mobi file with
        Outputs: void
        Function: creates an Anki deck from a mobi file.
        """
        tempdir,filepath = mobi.extract(strMobiPath)
        book = epub.read_epub(filepath)

        items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
        lines = []
        for i in items:
            chapter_lines = self.listChapterToStr(i).split(strDelim)
            for line in chapter_lines:
                if len(line.strip()) > 0:
                    lines.append(line)
        # make deck if not present
        if strOutDeckName not in invoke('deckNames'):
            invoke('createDeck',deck=strOutDeckName)

        self.runThreads(lines,strOutDeckName)

    def fromEpub(self,strEpubFile,strOutDeckName,strDelim = '。'):
        """
        Inputs: path of epub file, name of deck to export to, delimiter to parse the epub file with
        Outputs: void
        Function: creates an Anki deck from a epub file.
        """
        book = epub.read_epub(strEpubFile)
        items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

        lines = []
        for i in items:
            chapter_lines = self.listChapterToStr(i).split(strDelim)
            for line in chapter_lines:
                if len(line.strip()) > 0:
                    lines.append(line)
        
        # make deck if not present
        if strOutDeckName not in invoke('deckNames'):
            invoke('createDeck',deck=strOutDeckName)
        
        self.runThreads(lines,strOutDeckName)
    
    def createNote(self, strFrontData, strBackData,strDeckName):
        """
        Inputs: data to show on front of card, data to show on back of card, name of deck to put card in
        Outputs: void
        Function: creates a flash card with data in a deck
        """
        note = {
            'deckName':strDeckName,
            'modelName':self.kMODEL_NAME,
            'fields':{
                "Front":strFrontData,
                "Back": strBackData,
            },
            'options':{
                'allowDuplicate':True,
            }
        }
        invoke('addNote',note=note)

    def makeDeck(self, strSrcFile, strOutDeckName,strDelim = '。'):
        """
        Inputs: path of source file, name of out deck, delimiter
        Outputs: void
        Function: creates an anki deck
        """
        strFileExtension = strSrcFile.split('.')[-1]
        
        if strFileExtension == "txt":
            self.fromTxt(strSrcFile,strOutDeckName,strDelim)
        elif strFileExtension == "mobi":
            self.fromMobi(strSrcFile,strOutDeckName,strDelim) 
        elif strFileExtension == "epub":
            self.fromEpub(strSrcFile,strOutDeckName,strDelim)
        else:
            print()
            print('file extension: {} is not supported.'.format(strFileExtension))
            print('please use one of the below file types: ')
            for e in self.kPOSSIBLE_EXTENSIONS:
                print(e)
            print()
        