"""
playing card class

J. Knerr
Fall 2016
"""

class Card(object):
  """card object for playing cards"""

  def __init__(self, rank, suit):
    """create playing card, given rank and suit"""
    rank = rank.upper()
    suit = suit.upper()
    ranks = list("A23456789TJQKBL")
    suits = list("CDHSJ")
    if (rank in ranks) and (suit in suits):
      if suit=="J":
        if (rank!="B") and (rank!="L"):
          raise Exception("Joker rank (%s) must be Big (B) or Little (L)..." % (rank))
      else:
        if (rank=="B") or (rank=="L"):
          raise Exception("Non-joker rank (%s) must be A23..TJQK." % (rank))
      self.rank = rank
      self.suit = suit
    else:
      raise Exception("Odd rank (%s) or suit (%s)..." % (rank,suit))

  def __str__(self):
    """return string representation of playing card"""
    return self.rank+self.suit

  def __repr__(self):
    return "%s(%s,%s)" % (self.__class__.__name__, self.rank, self.suit)

  def __hash__(self):
    """to help with comparing cards"""
    return hash((self.rank, self.suit))

  def __eq__(self, other):
    """to allow comparing cards to see if equal"""
    return hash(self) == hash(other)

  def getRank(self):
    """getter for card rank"""
    return self.rank

  def getSuit(self):
    """getter for card suit"""
    return self.suit

  def rankNum(self):
    """convert card rank to number 1-13 (A->K)"""
    ranks = list("A23456789TJQK")
    if self.rank in ranks:
      number = ranks.index(self.rank) + 1
      return number
    raise Exception("Card rank (%s) not valid (1-13)..." % self.rank)

  def suitNum(self):
    """convert card suit to number: C=0,D=1,H=2,S=3"""
    suits = list("CDHS")
    if self.suit in suits:
      number = suits.index(self.suit)
      return number
    raise Exception("Card suit (%s) not valid (CDHS)..." % self.suit)

  def __lt__(self, oc):
    """allow comparing cards...all clubs, then D, H, S, Jokers"""
    ranks = list("A23456789TJQKBL")
    suits = list("CDHSJ")
    if self.suit == oc.suit:
      return ranks.index(self.rank) < ranks.index(oc.rank)
    else:
      return suits.index(self.suit) < suits.index(oc.suit)

  def __gt__(self, oc):
    """allow comparing cards...all clubs, then D, H, S, Jokers"""
    ranks = list("A23456789TJQKBL")
    suits = list("CDHSJ")
    if self.suit == oc.suit:
      return ranks.index(self.rank) > ranks.index(oc.rank)
    else:
      return suits.index(self.suit) > suits.index(oc.suit)

  def __le__(self, oc):
    """allow comparing cards...all clubs, then D, H, S, Jokers"""
    ranks = list("A23456789TJQKBL")
    suits = list("CDHSJ")
    if self.suit == oc.suit:
      return ranks.index(self.rank) <= ranks.index(oc.rank)
    else:
      return suits.index(self.suit) <= suits.index(oc.suit)

  def __gt__(self, oc):
    """allow comparing cards...all clubs, then D, H, S, Jokers"""
    ranks = list("A23456789TJQKBL")
    suits = list("CDHSJ")
    if self.suit == oc.suit:
      return ranks.index(self.rank) >= ranks.index(oc.rank)
    else:
      return suits.index(self.suit) >= suits.index(oc.suit)

  def __eq__(self, oc):
    """allow comparing cards...all clubs, then D, H, S, Jokers"""
    if oc == None:
      return False
    return self.suit == oc.suit and self.rank == oc.rank

  def __ne__(self, oc):
    """allow comparing cards...all clubs, then D, H, S, Jokers"""
    if oc == None:
      return True
    return self.suit != oc.suit or self.rank != oc.rank

# ---------------------------------------- #

from random import choice

def main():
  print("random suits, Ace through King:")
  suits = list("CDHS")
  for rank in "A23456789TJQK":
    c = Card(rank,choice(suits))  
    print(c)

if __name__ == "__main__":
  main()
