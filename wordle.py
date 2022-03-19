#!/usr/bin/env python3

import subprocess
import os
import string
import sys
import argparse
from spellchecker import SpellChecker

possibles = []

def main(argv):
  # Get all necesary arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('-g', '--grey_letters', help= "Known grey letters that are defenitely not in the word", default="")
  parser.add_argument('-y', '--yellow_letters', help="Known yellow letters that are definitely in the word", default="")
  parser.add_argument('-l', '--language', help="Language: en|de", default="en")
  parser.add_argument('-w', '--wordl', help="Wordle word with known greens and _ for unknowns", required=True)
  args = vars(parser.parse_args())

  spell = SpellChecker(language=args["language"])
  iterate(args["wordl"], args["yellow_letters"], args["grey_letters"])
  for i in possibles:
    isaword(i, spell)
  
# Make a list of all posssible letter combinations
def iterate(word, y, g):
  for i in word:
    if i == "_":
      for j in string.ascii_lowercase:
        newword = word.split("_", 1)[0] + j + word.split("_", 1)[1]
        iterate(newword, y, g)
        if check(newword, y, g):
          possibles.append(newword)
      break

# Check if word complies with grey and yellow letters
def check(word, y, g):
  valid = False
  # Word has all yellow letters
  if set(y).issubset(word): 
    valid = True
  # Word contains not one of the grey letters
  for i in word:
    if i in g:
      valid = False
  # Word is from final iteration without any blanks
  if "_" in word:
    valid = False
  return valid

# Check with aspell if word exists (Old, slow, depricated)
def isaword_aspell(word, l):
  ret = subprocess.getoutput("echo " + word + " | aspell -d " + l + " pipe")
  if ret.find("*") > 0:
    print("Valid word: " + word)
  if l is not "en":
    ret = subprocess.getoutput("echo " + word.title() + " | aspell -d " + l + " pipe")
    if ret.find("*") > 0:
      print("Valid word: " + word)

# Check with dict if word exists
def isaword(word, spell):
  if spell.known([word]):
    print("Valid word: " + word)
 
if __name__ == "__main__":
   main(sys.argv[1:])
