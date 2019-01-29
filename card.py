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
          raise Exception("Non-joker rank (%s) must be A123..TJQK." % (rank))
      self.rank = rank
      self.suit = suit
    else:
      raise Exception("Odd rank (%s) or suit (%s)..." % (rank,suit))

  def __str__(self):
    """return string representation of playing card"""
    return self.rank+self.suit

  def getRank(self):
    """getter for card rank"""
    return self.rank

  def getSuit(self):
    """getter for card suit"""
    return self.suit

# ---------------------------------------- #

def main():
  for rank in "A23456789TJQK":
    c = Card(rank,"D")  
    print(c)
  c = Card("5","J")

if __name__ == "__main__":
  main()

