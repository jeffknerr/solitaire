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

# ---------------------------------------- #

from random import choice

def main():
  print("random cards, Ace through King:")
  suits = list("CDHS")
  for rank in "A23456789TJQK":
    c = Card(rank,choice(suits))  
    print(c)

if __name__ == "__main__":
  main()
