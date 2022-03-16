#!/usr/bin/env python3

import subprocess
import os
import string
import sys
import argparse

def main(argv):
  parser = argparse.ArgumentParser()
  parser.add_argument('-g', '--grey_letters', help= "Known grey letters that are defenitely not in the word", default="")
  parser.add_argument('-y', '--yellow_letters', help="Known yellow letters that are definitely in the word", default="")
  parser.add_argument('-l', '--language', help="Language: en|de", default="en")
  parser.add_argument('-w', '--wordl', help="Wordle word with known greens and _ for unknowns", required=True)
  args = vars(parser.parse_args())
  iterate(args["wordl"], args["yellow_letters"], args["grey_letters"], args["language"])
  
def iterate(word, y, g, l):
  for i in word:
    if i == "_":
      for j in string.ascii_lowercase:
        newword = word.split("_", 1)[0] + j + word.split("_", 1)[1]
        iterate(newword, y, g, l)
        check(newword, y, g, l)
      break

def check(word, y, g, l):
  valid = False
  for i in y:
    if i in word:
      valid = True
  if y == "":
    valid = True
  for i in word:
    if i in g:
      valid = False
  if "_" in word:
    valid = False
  if valid:
    ret = subprocess.getoutput("echo " + word + " | aspell -d " + l + " pipe")
    if ret.find("*") > 0:
      print("Valid word: " + word)
    if l is not "en":
      ret = subprocess.getoutput("echo " + word.title() + " | aspell -d " + l + " pipe")
      if ret.find("*") > 0:
        print("Valid word: " + word)

if __name__ == "__main__":
   main(sys.argv[1:])
