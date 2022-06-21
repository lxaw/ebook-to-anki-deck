# Book-to-Anki 📚

### What is it? :question:
Converts various book files to Anki decks. At the moment it only reads the text and saves it to cards. You could improve this by adding TTS, but I didn't want to have so many files in my Anki.

### How does it work?
It's just a small command-line program. You input the file, delimiter, minimum length of text each line needs to contain, the deck name, and card type information.

### Dependencies
This script makes heavy use of Anki-Connect.
See here: https://foosoft.net/projects/anki-connect/

Anki needs to be running to use Anki-Connect. Anki-Connect runs on localhost:8765

This script requires the following downloadable libraries:
- EbookLib 0.17.1: https://pypi.org/project/EbookLib/
