import unittest, io, sys
from card import *
from deck import *
from random import randrange, choice, shuffle
from operator import itemgetter

class TestCards(unittest.TestCase):

  def setUp(self):
    """create cards and deck"""
    self.queenhearts = Card("Q","H")  # off with their heads
    self.tenclubs = Card("T","C")     # ten of clubs
    self.bigjoker = Card("B","J")     # big joker
    self.littlejoker = Card("L","J")  # little joker
    self.cards = Deck()

  def test_cards(self):
    """test basic card properties"""
    self.assertEqual(self.queenhearts.getRank(), "Q")
    self.assertEqual(self.queenhearts.getSuit(), "H")
    self.assertEqual(self.tenclubs.getRank(), "T")
    self.assertEqual(self.tenclubs.getSuit(), "C")
    self.assertEqual(self.bigjoker.getRank(), "B")
    self.assertEqual(self.bigjoker.getSuit(), "J")
    self.assertEqual(self.littlejoker.getRank(), "L")
    self.assertEqual(self.littlejoker.getSuit(), "J")
    self.assertEqual(len(self.cards), 54)
    self.assertFalse(self.cards.isEmpty())
    firstcard = self.cards.dealCard()
    self.assertEqual(len(self.cards), 53)
    self.assertEqual(firstcard.getRank(), "A")
    self.assertEqual(firstcard.getSuit(), "C")

  def test_badCards(self):
    """test illegal card properties"""
    #                                 rank suit
    self.assertRaises(Exception, Card, "R", "X")  # rank A23456789TJQK
    self.assertRaises(Exception, Card, "T", "X")  # suit CDHS
    self.assertRaises(Exception, Card, "Z", "C")  # joker rank BL
    self.assertRaises(Exception, Card, "Z", "C")  # joker suit J
    self.assertRaises(Exception, Card, "B", "C")  
    self.assertRaises(Exception, Card, "L", "C")  
    self.assertRaises(Exception, Card, "L", "5")  
    self.assertRaises(Exception, Card, "5", "J")  
    self.assertRaises(Exception, Card, "Z", "J")  

  def test_equality(self):
    """test card equality"""
    newcard = Card("Q","H")
    self.assertTrue(newcard == self.queenhearts)
    newcard = Card("Q","S")
    self.assertFalse(newcard == self.queenhearts)

  def test_deck(self):
    """test deck creation and dealing out cards"""
    i = 0
    while not self.cards.isEmpty():
      c = self.cards.dealCard()
      rank = i % 13
      i += 1
      if c.getSuit() != "J":
        if rank == 0:
          self.assertEqual(c.getRank(), "A")
        elif rank == 9:
          self.assertEqual(c.getRank(), "T")
        elif rank == 10:
          self.assertEqual(c.getRank(), "J")
        elif rank == 11:
          self.assertEqual(c.getRank(), "Q")
        elif rank == 12:
          self.assertEqual(c.getRank(), "K")
        else:
          self.assertEqual(c.getRank(), str(rank+1))
        self.assertEqual(len(self.cards), 54-i)

  def test_deckorder(self):
    """test deck creation with specific order"""
    self.cards.shuffle()
    randomorder = self.cards.getOrder()
    newdeck = Deck(randomorder)
    for i in range(len(self.cards)):
       self.assertEqual(self.cards[i], newdeck[i])

if __name__ == '__main__':
  unittest.main()