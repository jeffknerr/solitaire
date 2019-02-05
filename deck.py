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

class Deck(object):
  """deck of 52 playing cards plus 2 jokers"""

  def __init__(self, order=""):
    """create all 54 cards (use specified order if given)"""
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
      card = self.cards.pop(0) 
      return card
    else:
      raise Exception("Tried to deal from empty deck...")

  def isEmpty(self):
    """return True if deck is empty"""
    return len(self.cards) == 0

  def getIndex(self, cardstr):
    """
    given a card string, such as "AS", or "3C", return it's 
    index in the deck (0=first, 1=second,...)
    """
    rank=cardstr[0].upper()
    suit=cardstr[1].upper()
    for i in range(len(self.cards)):
      c = self.cards[i]
      if c.getRank()==rank and c.getSuit()==suit:
        return i
    raise Exception("Card (%s) not found in deck..." % cardstr)

  def moveDown1(self, i):
    """
    move the card at index i down by 1.
    however, if card is last, don't swap with first. move it to second spot.
    """
    if i == len(self.cards)-1:
      # insert into position 1
      lastcard = self.cards.pop()
      self.cards.insert(1,lastcard)
    else:
      self.cards[i],self.cards[i+1] = self.cards[i+1],self.cards[i]

  def findJokers(self):
    """
    find the jokers in the deck, return index of each. 
    Doesn't matter which joker is which, just return index of 
    first joker found and index of second joker found
    """
    first = None
    second = None
    for i in range(len(self.cards)):
      rank = self.cards[i].getRank()
      suit = self.cards[i].getSuit()
      if suit=="J":
        if first==None:
          first = i
        else:
          second = i
    if first==None or second==None:
      raise Exception("There aren't two jokers in this deck...")
    return first, second

  def tripleCut(self, first, second):
    """
    triple cut the deck at the first and second indecies.
    everything before first swaps with everything after second.
    if deck is 26JKfirstQKAsecond58T3 before the triple cut, 
    it should be 58T3firstQKAsecond26JK after.
    """
    before = self.cards[:first]
    after = self.cards[second+1:]
    middle = self.cards[first:second+1]
    self.cards = after + middle + before

  def countCut(self):
    """
    count cut the deck: find *number* of last card, count down that
    many from the top, swap top cut with rest of the deck, leaving the
    last card as is. For example, suppose last card is 5 of Clubs:
    before: 2864JQT9....K5  so count down 5 from top (2864J) and cut
     after: QT9....K2864J5  but leave 5 of Clubs last. 
    If last card is 5D, would count down 5+13
    If last card is 5H, would count down 5+26
    If last card is 5S, would count down 5+39
    If last card is a joker, do nothing.
    """
    last = self.cards[len(self.cards) - 1]
    if last.getSuit() != "J":
      suits = list("CDHS")
      suitnum = suits.index(last.getSuit())
      count = last.rankNum() + (suitnum*13)
      before = self.cards[:count]
      after = self.cards[count:len(self.cards)-1]
      self.cards = after + before + [last]

  def outputCard(self):
    """
    get card number of top card, count down that many from top, 
    output the card. So if top card is 5C, count down 5 from the top
    (first card is 1), then output the next card.
    """
    topcard = self.cards[0]
    suit = topcard.getSuit()
    if suit == "J":
      return None
    topnum = topcard.rankNum() + (topcard.suitNum()*13)
    return self.cards[topnum]

  def _valid(self):
    """return True if deck has all 54 cards and no repeats"""
    if len(self.cards) < 54:
      return False
    dcp = list(self.cards)  # deck copy
    dcp.sort()              # should now be sorted
    ranks = list("A23456789TJQK")
    suits = list("CDHS")
    i = 0
    for s in suits:
      for r in ranks:
        c = dcp[i]
        if c.getRank()!=r or c.getSuit()!=s:
          return False
        i += 1
    if dcp[i].getRank()!="B" or dcp[i].getSuit()!= "J":
      return False
    i += 1
    if dcp[i].getRank()!="L" or dcp[i].getSuit()!= "J":
      return False
    # if we get here...all OK
    return True

# ---------------------------------------------- #

def main():
  """some simple examples"""
  print("-"*20)
  d = Deck()
  print("full initial deck:")
  print(d)
  assert(d.isEmpty() == False)
  assert(len(d) == 54)
  print("-"*20)
  print("top card dealt:")
  topcard = d.dealCard()
  print(topcard)
  assert(len(d) == 53)
  print("-"*20)
  order = "AS2HJCTS3C6D9C7CACAH"
  print("partial deck with specified order: %s" % order)
  newdeck = Deck(order)
  print(newdeck)
  print("-"*20)

if __name__ == "__main__":
  main()
