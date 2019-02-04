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
    msg = input("msg: ")
  else:
    msg = readFile(msgfile)
  print(msg)
  if encrypt:
    print("enscrypting...")
  else:
    print("decrypting...")
  if outfile=='':
    print("writing to stdout...")
  else:
    print("writing to %s..." % (outfile))
  print("reading key from %s..." % (keyfile))

def readFile(fn):
  """read message from given filename"""
  return "do not use pc"

# --------------------------------------- #

if __name__ == "__main__":
  main()
