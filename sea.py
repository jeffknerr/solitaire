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
  """get message, get deck of cards, then encrypt/decrypt the message"""
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
    # add them
    result = [(ciphertext[i]+cipherkeystream[i])%26 for i in range(len(ciphertext))]
  else:
    # subtract them
    result = [(ciphertext[i]-cipherkeystream[i])%26 for i in range(len(ciphertext))]
  output(result, outfile)

# ------------------------------------------------- #

def output(result, outfile):
  """convert result back to letters, send to outfile/stdout"""
  letters = []
  for ch in result:
    letters.append(chr(ch+ord("A")))
  outstr = "".join(letters)
  if outfile=='':
    print(outstr)
  else:
    ofile = open(outfile, "w")
    ofile.write(outstr + "\n")
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
  """
  given deck of cards and number of letters (n), generate 
  n keystream letters, return as a string
  """
  kstrm = []
  i = 0
  while i < n:
    index = d.getIndex("LJ")                # find the little joker
    d.moveDown1(index)                      # move it down one
    index = d.getIndex("BJ")                # find big joker
    d.moveDown1(index)                      # move it down 
    d.moveDown1(index)                      #              two
    first,second = d.findJokers()           # find location of jokers 
    d.tripleCut(first, second)              # triple cut on those locations
    d.countCut()                            # now do the count cut
    outputcard = d.outputCard()             # find the output card
    if outputcard != None:                  # go back to step 1 if it's a joker
      rn = outputcard.rankNum()             # convert it to 1-26, where
      sn = outputcard.suitNum()             # Clubs are 1-13, Diamonds 14-26
      if sn > 1:                            # Hearts 1-13, Spades 14-26
        sn -= 2                             # AC=1, AD=14, AH=1, AS=14
      letter = chr(ord('A') + rn-1+(sn*13))
      kstrm.append(letter)
      i += 1
  return "".join(kstrm)

def letters2numbers(s):
  """given a string of letters, convert to numbers 0 to 25"""
  nums = []
  for ch in s:
    num = ord(ch) - ord("A")
    nums.append(num)
  return nums

# --------------------------------------- #

if __name__ == "__main__":
  main()
