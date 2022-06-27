# Book-to-Anki 📚

### What is it?
Converts various book files to Anki decks. At the moment it only reads the text and saves it to cards. You could improve this by adding TTS, but I didn't want to have so many files in my Anki.

### How does it work?
It's just a small command-line program. You input the file, name of the output deck and the delimiter type. The delimiter defaults to the Japanese period if nothing is inputted. The program automatically generates a model type of "default_bta". This is essentially the "Default" model, but to ensure that a card can be generated this model type is created upon run. Feel free to delete it after.

### Dependencies
This script makes heavy use of Anki-Connect.
See here: https://foosoft.net/projects/anki-connect/

Anki needs to be running to use Anki-Connect. Anki-Connect runs on localhost:8765

This script requires the following downloadable libraries:
- EbookLib 0.17.1: https://pypi.org/project/EbookLib/
- bs4: https://pypi.org/project/bs4/
- mobi: https://pypi.org/project/mobi/

I would create a virtual environment to download these, and run the program
within the virtual environment. However, this is not strictly necessary, just good practice.

# How to run
To run you call:

`python bta.py [PATH TO BOOK FILE] [NAME OF OUTPUT DECK] [OPTIONAL DELIMITER]`

##### Note
The optional delimiter defaults to the Japanese period, '。'.

# Examples:
Included are some example book files (for each supported type).

Example 1: epub file
`python bta.py books/moby.epub "Moby Dick" "."`

Example 2: mobi file
`python bta.py books/hoshi.mobi "hoshi"`
###### NOTE: 
Here we do not pass a delimiter because we know that the Japanese period is the separator. This will be the same case in the next example as well.

Example 2: text file
`python bta.py books/tokyowiki.txt" "Tokyo"`


# Note on speed
Sometimes it takes a while to make decks. It appears that the actual action of creating a card takes a bit of time, so if more cards are needed, more time should be expected. I have attempted to thread it, but I am not sure if Anki / Anki Connect makes it such that you cannot attempt to create multiple cards at once.
