#! /usr/bin/python3

"""
The Solitaire Encryption Algorithm.
Designed by Bruce Schneier
Featured in Neal Stephenson's Cryptonomicon
https://www.schneier.com/academic/solitaire/

J. Knerr
Spring 2019
"""

from card import *
from deck import *
import click

# ------------------------------------------------- #

@click.command()
@click.option('-m','--msgfile',
              default='', 
              help="message file containing msg to encrypt/decrypt")
@click.option('--encrypt/--decrypt','-e/-d',default=True,
              help="encrypt/decrypt the message (default=encrypt)")
@click.option('-o','--outfile',
              default='',
              help="output file for results of en/decryption")
@click.option('-k','--keyfile',required=True, type=str,
              help="keyfile containing initial deck of cards order")
def main(msgfile,encrypt,outfile,keyfile):
  """get message, deck of cards, encrypt/decrypt message"""
  if msgfile=='':
    msg = clean(input("msg: "))
  else:
    msg = clean(readFile(msgfile))
  deckofcards = readCards(keyfile)
  nletters = len(msg)
  keystream = generateKeystream(deckofcards,nletters)
  ciphertext= letters2numbers(msg)
  cipherkeystream= letters2numbers(keystream)
  if encrypt:
    difference = subtract(ciphertext, cipherkeystream)
  else:
    difference = subtract(cipherkeystream, ciphertext)
  output(difference, outfile)

# ------------------------------------------------- #

def output(difference, outfile):
  """convert difference back to letters, send to outfile/stdout"""
  if outfile=='':
    print(difference)
  else:
    ofile = open(outfile, "w")
    ofile.write(difference + "\n")
    ofile.close()

def readFile(fn):
  """read and return message from given filename"""
  while True:
    try:
      inf = open(fn, "r")
      break
    except FileNotFoundError:
      print("Message file (%s) not found." % (fn))
      fn = input("msgfile: ")
  orig = inf.readlines()
  inf.close()
  return "".join(orig)

def clean(orig):
  """given a string, clean it up (only uppercase letters)"""
  cleaned = ""
  for line in orig:
    for ch in line:
      if ch.isalpha():
        cleaned += ch.upper()
  return cleaned

def readCards(fn):
  """read deck of cards order from given filename, return deck"""
  while True:
    try:
      inf = open(fn, "r")
      break
    except FileNotFoundError:
      print("Keyfile (%s) not found." % (fn))
      fn = input("keyfile: ")
  order = inf.readline().strip()
  # skip the commented out lines and just grab first non-comment
  while order[0] == "#":
    order = inf.readline().strip()
  if len(order) != 54*2:
    raise Exception("keyfile not a valid deck of cards...")
  d = Deck(order)
  return d

def generateKeystream(d,n):
  """given deck of cards and number of letters, generate the keystream"""
  return "KDWUPONOWT"

def letters2numbers(s):
  """given a string of letters, convert to numbers 1 to 26"""
  return [15,19,11,10,10]

def subtract(str1, str2):
  """given two strings, return str1-str2 modulo 26"""
  return [4,15,14,15,20]

# --------------------------------------- #

if __name__ == "__main__":
  main()
