# Wordle helper
A little python script that helps to find possible valid wordle solutions to your input.

## Prerequisites: 
 - python3
 - spelchecker

## Usage

    wordle.py [-h] [-g GREY_LETTERS] [-y YELLOW_LETTERS] [-l LANGUAGE] -w WORDL

    arguments:
     -h, --help             show this help message and exit
     -g GREY_LETTERS, --grey_letters GREY_LETTERS
                            Known grey letters that are defenitely not in the word
     -y YELLOW_LETTERS, --yellow_letters YELLOW_LETTERS
                            Known yellow letters that are definitely in the word
     -l LANGUAGE, --language LANGUAGE
                            Language: en|de
     -w WORDL, --wordl WORDL
                            Wordle word with known greens and _ for unknowns

## Example

    $ ./wordle.py -w cra_e -g vt -l en
    Valid word: crane
    Valid word: crape
    Valid word: craze
    
    $ 
