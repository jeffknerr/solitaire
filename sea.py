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
# Still TODO:
#  - input: pad with X if not in groups of 5
#  - output in groups of 5 letters
#  - add more tests

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
  msgnums = letters2numbers(msg)
  kstnums = letters2numbers(keystream)
  if encrypt:
    newnums = add(msgnums,kstnums)
  else:
    newnums = subtract(msgnums,kstnums)
  output(newnums, outfile)

# ------------------------------------------------- #
# better way using % operator??? but nums need to be 1-26...
def add(L1, L2):
  """add two lists of integers (1-26), mod 26"""
  newL = []
  for i in range(len(L1)):
    sum = L1[i] + L2[i]
    if sum > 26: sum -= 26
    newL.append(sum)
  return newL

def subtract(L1, L2):
  """subtract (L1-L2) two lists of integers (1-26), mod 26"""
  newL = []
  for i in range(len(L1)):
    diff = L1[i] + L2[i]
    if diff < 1: diff += 26
    newL.append(diff)
  return newL

def output(numlist, outfile):
  """convert numlist back to letters, send to outfile/stdout"""
  letters = []
  for n in numlist:
    letters.append(chr(n-1+ord("A")))
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
    d.moveDown1(index+1)                    #              two
    first,second = d.findJokers()           # find location of jokers 
    d.tripleCut(first, second)              # triple cut on those locations
    d.countCut()                            # now do the count cut
    outputcard = d.outputCard()             # find the output card
    if outputcard != None:                  # go back to step 1 if it's a joker
      rn = outputcard.rankNum()             # convert it to 1-26, where
      sn = outputcard.suitNum()             # Clubs are 1-13, Diamonds 14-26
      if sn > 1:                            # Hearts 1-13, Spades 14-26
        sn -= 2                             # AC=1, AD=14, AH=1, AS=14
      letter = chr(ord('A') + (rn-1)+(sn*13))
      kstrm.append(letter)
      i += 1
  return "".join(kstrm)

def letters2numbers(s):
  """given a string of uppercase letters, convert to numbers 1 to 26"""
  nums = []
  for ch in s:
    num = ord(ch) - ord("A") + 1
    nums.append(num)
  return nums

# --------------------------------------- #

if __name__ == "__main__":
  main()
