# coding=UTF-8
# vim: set fileencoding=UTF-8 :
'''
DESCRIPTION
    Unit test file for unit tests for core classes in Tournaments.
LICENSE
    TournamentsTest by Aleš Daniel is licensed under a Creative Commons
    Attribution-NonCommercial 3.0 Unported License.
    http://creativecommons.org/licenses/by-nc/3.0/
AUTHOR
    adpro (Ales Daniel)
'''
import unittest
from model import tournaments as tmt


class CompetitorTestCase(unittest.TestCase):

    def setUp(self):
        #unittest.TestCase.setUp(self)
        self.people = ['Alfons', None, "Cyril", 'Dalimil']
        self.competitors = []

    def tearDown(self):
        #unittest.TestCase.tearDown(self)
        self.people = None
        self.competitors = None

    def test_competitor(self):
        for man in self.people:
            self.competitors.append(tmt.Competitor(man))
        self.competitors.append(tmt.Competitor())

        self.assertEqual(self.people[0], self.competitors[0].name)
        self.assertEqual('', self.competitors[1].name)
        self.assertEqual('Cyril', self.competitors[2].name)
        self.assertEqual('Dalimil', self.competitors[3].name)
        self.assertEqual('', self.competitors[4].name)
        self.competitors.pop()
        self.assertEqual(len(self.people), len(self.competitors))


class ScoreTestCase(unittest.TestCase):

    def test_score(self):
        self.assertFalse(True)


class MatchInfoTestCase(unittest.TestCase):

    def test_matchinfo(self):
        self.assertFalse(True)


class MatchTestCase(unittest.TestCase):

    def test_match(self):
        self.assertFalse(True)


class CoreTestCase(unittest.TestCase):
    '''Tests for whole core classes'''
    def test_core(self):
        self.assertFalse(True)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
