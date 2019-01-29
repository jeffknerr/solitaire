"""
deck of cards class

J. Knerr
Fall 2016
"""

from card import *
from random import shuffle

class Deck(object):
  """deck of 52 playing cards plus 2 jokers"""

  def __init__(self, order=""):
    """create all 52 cards"""
    self.cards = []
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
    card = self.cards.pop(0)              # should use deque???
    return card

  def isEmpty(self):
    """return True if deck is empty"""
    return len(self.cards) == 0

if __name__ == "__main__":

  d = Deck()
  assert(d.isEmpty() == False)
  assert(len(d) == 54)
  print(d)
  print(d.getOrder())
  d.shuffle()
  print(d.getOrder())
  while not d.isEmpty():
    print(d.dealCard())
  assert(d.isEmpty() == True)
  assert(len(d) == 0)
  print("-"*30)
  newdeck = Deck("AS2HJCTS3C6D9C7CACAH")
  while not newdeck.isEmpty():
    print(newdeck.dealCard())
