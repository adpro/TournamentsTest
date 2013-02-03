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
        pass

    def test_constructor(self):
        player = tmt.Competitor()
        player
        pass

    def test_competitor(self):
        pass


class ScoreTestCase(unittest.TestCase):

    def test_constructor(self):
        pass

    def test_score(self):
        pass


class MatchInfoTestCase(unittest.TestCase):
    pass


class MatchTestCase(unittest.TestCase):
    pass


class CoreTestCase(unittest.TestCase):
    '''Tests for whole core classes'''
    pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
