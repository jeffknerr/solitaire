"""
deck of cards class

Default order is Ace234...TenJackQueenKing of Clubs, then 
Diamonds, Hearts, Spades, and two Jokers (Big, then Little).

Can optionally specify an order to the deck (full or partial):
  mydeck = Deck("5DAS3SKHTSAHQC")
The above would make a deck with the following order:
  5 of Diamonds, Ace of Spades, 3 of Spades, King of Hearts, etc

J. Knerr
Fall 2016
"""

from card import *
from random import shuffle
from collections import deque

class Deck(object):
  """deck of 52 playing cards plus 2 jokers"""

  def __init__(self, order=""):
    """create all 54 cards (use specified order if given)"""
    self.cards = deque()
    if order == "":
      for suit in "CDHS":
        for rank in "A23456789TJQK":
          c = Card(rank,suit)
          self.cards.append(c)
      bigjoker = Card("B","J")
      littlejoker = Card("L","J")
      self.cards.append(bigjoker)
      self.cards.append(littlejoker)
    else:
      # use given order to set the deck
      for i in range(0,len(order),2):
        rank = order[i]
        suit = order[i+1]
        c = Card(rank,suit)
        self.cards.append(c)

  def __len__(self): 
    return len(self.cards)

  def __str__(self):
    """return string representation of deck of cards"""
    s = ""
    i = 0
    for card in self.cards:
      rank = card.getRank()
      suit = card.getSuit()
      s = s + rank + suit + " "
      i = i + 1
      if i%13 == 0:
        s = s + "\n"
    return s

  def __getitem__(self, index):
    """support indexing of the deck of cards"""
    return self.cards[index]

  def getOrder(self):
    """return one long string to show current order of cards"""
    s = ""
    for card in self.cards:
      rank = card.getRank()
      suit = card.getSuit()
      s = s + rank + suit 
    return s

  def shuffle(self):
    """shuffle the deck"""
    shuffle(self.cards) 

  def dealCard(self):
    """deal one card from the deck"""
    if len(self.cards) > 0:
      card = self.cards.popleft() 
      return card
    else:
      raise Exception("Tried to deal from empty deck...")

  def isEmpty(self):
    """return True if deck is empty"""
    return len(self.cards) == 0

# ---------------------------------------------- #

def main():
  """some simple examples"""
  d = Deck()
  print("full initial deck:")
  print(d)
  assert(d.isEmpty() == False)
  assert(len(d) == 54)
  print("top card dealt:")
  topcard = d.dealCard()
  print(topcard)
  assert(len(d) == 53)
  order = "AS2HJCTS3C6D9C7CACAH"
  print("partial deck with specified order: %s" % order)
  newdeck = Deck(order)
  print(newdeck)

if __name__ == "__main__":
  main()
