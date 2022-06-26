#!/usr/bin/python

from lib.BookToAnki import BookToAnki

import sys

def run(listArgs):
    if len(listArgs) < 3:
        print('usage: python kindle_to_anki.py [BOOK_FILE_PATH] [ANKI_DECK_NAME] [OPTIONAL DELIMITER]')
        return
    
    bTa = BookToAnki()
    bTa.createDefaultModel()

    return

    strBookFilePath = listArgs[1]
    strAnkiDeckName = listArgs[2]
    if len(listArgs) == 4:
        strDelim = listArgs[3]
        try:
            bTa.makeDeck(strBookFilePath,strAnkiDeckName,strDelim)

        except Exception as e:
            print('error:\n{}'.format(e))
        return
    try:
        bTa.makeDeck(strBookFilePath,strAnkiDeckName)

    except Exception as e:
        print('error:\n{}'.format(e))
    return

if __name__ == "__main__":
    run(sys.argv)
    print('\nThank you for using this program!\nIf you would like to contribute, find the repo at:\n{}\n'.format('https://github.com/lxaw/kindle-to-anki-deck'))