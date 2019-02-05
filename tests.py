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
    self.doc = Deck()                 # deck of cards
    self.assertTrue(self.doc._valid())

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
    self.assertEqual(len(self.doc), 54)
    self.assertFalse(self.doc.isEmpty())
    firstcard = self.doc.dealCard()
    self.assertEqual(len(self.doc), 53)
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
    while not self.doc.isEmpty():
      c = self.doc.dealCard()
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
        self.assertEqual(len(self.doc), 54-i)

  def test_deckorder(self):
    """test deck creation with specific order"""
    self.doc.shuffle()
    self.assertTrue(self.doc._valid())
    randomorder = self.doc.getOrder()
    newdeck = Deck(randomorder)
    for i in range(len(self.doc)):
       self.assertEqual(self.doc[i], newdeck[i])

  def test_movedown(self):
    """test the moveDown1 method"""
    cstr = "6D"
    for i in range(55):
      index = self.doc.getIndex(cstr)
      if index == len(self.doc) - 1:
        newindex = 1
        beforecard = self.doc[0]
      else:
        newindex = index + 1
        beforecard = self.doc[index+1]
      self.doc.moveDown1(index)
      self.assertEqual(self.doc[newindex].getRank(), cstr[0])
      self.assertEqual(self.doc[newindex].getSuit(), cstr[1])
      self.assertEqual(self.doc[newindex-1].getRank(), beforecard.getRank())
      self.assertEqual(self.doc[newindex-1].getSuit(), beforecard.getSuit())
    self.assertTrue(self.doc._valid())

  def test_findjokers(self):
    """test the findJokers method"""
    first, second = self.doc.findJokers()
    self.assertEqual(first,52)
    self.assertEqual(second,53)
    nojokers = Deck("ASAHADAC")
    self.assertRaises(Exception, nojokers.findJokers)
    onejokers = Deck("ASAHBJADAC")
    self.assertRaises(Exception, onejokers.findJokers)

  def test_triplecut(self):
    """test the tripleCut method"""
    listorder = ["AS","BJ","AC","LJ","AD"]
    order = "".join(listorder)
    mydeck = Deck(order)
    first, second = mydeck.findJokers()
    mydeck.tripleCut(first, second)
    self.assertEqual(mydeck.getOrder(), "ADBJACLJAS")
    listorder = ["BJ","AC","LJ","AD"]
    order = "".join(listorder)
    mydeck = Deck(order)
    first, second = mydeck.findJokers()
    mydeck.tripleCut(first, second)
    self.assertEqual(mydeck.getOrder(), "ADBJACLJ")
    listorder = ["AS","BJ","LJ","AD"]
    order = "".join(listorder)
    mydeck = Deck(order)
    first, second = mydeck.findJokers()
    mydeck.tripleCut(first, second)
    self.assertEqual(mydeck.getOrder(), "ADBJLJAS")
    listorder = ["AS","BJ","AC","LJ"]
    order = "".join(listorder)
    mydeck = Deck(order)
    first, second = mydeck.findJokers()
    mydeck.tripleCut(first, second)
    self.assertEqual(mydeck.getOrder(), "BJACLJAS")
    listorder = ["AS","LJ","AC","BJ","AD"]
    order = "".join(listorder)
    mydeck = Deck(order)
    first, second = mydeck.findJokers()
    mydeck.tripleCut(first, second)
    self.assertEqual(mydeck.getOrder(), "ADLJACBJAS")
    listorder = ["2S","3S","4S","AS","LJ","AC","BJ","AD"]
    order = "".join(listorder)
    mydeck = Deck(order)
    first, second = mydeck.findJokers()
    mydeck.tripleCut(first, second)
    self.assertEqual(mydeck.getOrder(), "ADLJACBJ2S3S4SAS")
    # now test full deck is still OK
    self.doc.shuffle()
    first, second = self.doc.findJokers()
    self.doc.tripleCut(first, second)
    self.assertTrue(self.doc._valid())

  def test_countcut(self):
    """test the countCut method"""
    # joker on bottom means do nothing
    order = self.doc.getOrder()
    self.doc.countCut()
    self.assertEqual(self.doc.getOrder(), order)
    self.assertTrue(self.doc._valid())
    for i in range(10):
      while self.doc[-1].getSuit() == "J":
        self.doc.shuffle()
      order = self.doc.getOrder()
      lastcard = self.doc[-1]
      index = lastcard.rankNum() + lastcard.suitNum()*13
      self.doc.countCut()
      neworder = self.doc.getOrder()
      self.assertEqual(order[:2*index], neworder[2*(53-index):2*53])  # old first = new second
      self.assertEqual(order[2*index:2*53], neworder[:2*(53-index)])  # old second = new first
      self.assertTrue(self.doc._valid())

  def test_outputcard(self):
    """test the outputCard method"""
    for i in range(30):
      self.doc.shuffle()
      top = self.doc[0]
      if top.getSuit() != "J":    # don't test for jokers
        outcard = self.doc.outputCard()
        count = top.rankNum() + top.suitNum()*13
        self.assertEqual(self.doc[count], outcard)
      self.assertTrue(self.doc._valid())

if __name__ == '__main__':
  unittest.main()
