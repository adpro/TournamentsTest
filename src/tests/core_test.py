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

    def test_score_constructor(self):
        def process1():
            _ = tmt.Score()

        def process2():
            _ = tmt.Score('a', 'b')

        self.assertRaises(AssertionError, process1)
        self.assertRaises(AssertionError, process2)

        score = tmt.Score(-1, -4)
        self.assertEqual(score.score_competitor1, -1)
        self.assertEqual(score.score_competitor2, -4)

        score = tmt.Score(54, 0.987654321)
        self.assertEqual(score.score_competitor1, 54)
        self.assertGreater(1, score.score_competitor2)
        self.assertIsInstance(score.score_competitor1, int)
        self.assertIsInstance(score.score_competitor2, float)

    def test_score_str(self):
        score = tmt.Score(3.32, 2.56)
        self.assertEqual('(3.32:2.56)', str(score))

    def test_score_add(self):
        def process_a():
            score.add_home_score('a')

        def process_b():
            score.add_away_score('a')

        def process_a2():
            score.add_home_score(None)

        def process_b2():
            score.add_away_score(None)

        score = tmt.Score(0, 0)
        score.add_home_score(1)
        score.add_away_score(0.5)
        self.assertEqual(1, score.score_competitor1)
        self.assertEqual(0.5, score.score_competitor2)
        score.add_home_score(-0.3456)
        score.add_away_score(956)
        self.assertEqual(0.6544, score.score_competitor1)
        self.assertEqual(956.5, score.score_competitor2)

        self.assertRaises(AssertionError, process_a)
        self.assertRaises(AssertionError, process_b)
        score = tmt.Score(0, 0)
        self.assertRaises(ValueError, process_a2)
        self.assertRaises(ValueError, process_b2)

    def test_score_eval(self):
        scores = [tmt.Score(3, 2),
                  tmt.Score(0, 0),
                  tmt.Score(-1, -1),
                  tmt.Score(-45.987, -8345.21980),
                  tmt.Score(4.321, 9.3245),
                  tmt.Score(456.789, 456.789),
                  tmt.Score(2, 4),
                  tmt.Score(10.00000000000001, 10.00000000000001),
                  tmt.Score(10.000000000000001, 10.000000000000001),
                  tmt.Score(10.00000000000001, 10.00000000000002),
                  tmt.Score(10.000000000000001, 10.000000000000002),
                  tmt.Score(10.000000000000001, 10.0000000000000011)
                  ]
        results = []

        for score in scores:
            results.append(score.evaluate_score())
        # last 2 scores are after precision of float to compare
        expected = [1, 0, 0, 1, -1, 0, -1, 0, 0, -1, 0, 0]
        self.assertListEqual(expected, results)


class MatchInfoTestCase(unittest.TestCase):

    def setUp(self):
        #unittest.TestCase.setUp(self)
        self.mi_list = [tmt.MatchInfo(),
                   tmt.MatchInfo(tmt.Score(0, 0)),
                   tmt.MatchInfo(tmt.Score(-1, 0)),
                   tmt.MatchInfo(tmt.Score(65.003, 65.003)),
                   tmt.MatchInfo(tmt.Score(65.003, 65.003), True),
                   tmt.MatchInfo(tmt.Score(2, 1), True)
                   ]

    def tearDown(self):
        #unittest.TestCase.tearDown(self)
        self.mi_list = None

    def test_matchinfo(self):
        def process():
            self.mi_list[0].evaluate(0, 0)

        self.assertEqual(self.mi_list[0].score.score_competitor1, 0)
        self.assertEqual(self.mi_list[1].score.score_competitor1, 0)
        self.assertEqual(self.mi_list[2].score.score_competitor1, -1)
        self.assertEqual(self.mi_list[3].score.score_competitor1, 65.003)
        self.assertEqual(self.mi_list[4].score.score_competitor1, 65.003)
        self.assertEqual(self.mi_list[5].score.score_competitor1, 2)
        for i in (0, 1, 3, 4):
            self.assertFalse(self.mi_list[i].draw)
            if i < 4:
                self.assertFalse(self.mi_list[i].can_draw)
            else:
                self.assertTrue(self.mi_list[i].can_draw)
            self.assertEqual(self.mi_list[i].winner, \
                             self.mi_list[i].loser)
            self.assertEqual(self.mi_list[i].winner, None)
            self.mi_list[i].evaluate(tmt.Competitor('a'), tmt.Competitor('b'))
            self.assertEqual(self.mi_list[i].winner, \
                             self.mi_list[i].loser)
            self.assertEqual(self.mi_list[i].winner, None)

        self.assertRaises(ValueError, process)
        self.assertEqual(self.mi_list[2].winner, \
                         self.mi_list[2].loser)
        self.assertEqual(self.mi_list[2].winner, None)
        self.mi_list[2].evaluate(tmt.Competitor('a'), tmt.Competitor('b'))
        self.assertNotEqual(self.mi_list[2].winner, \
                         self.mi_list[2].loser)
        self.assertNotEqual(self.mi_list[2].winner, None)
        self.assertNotEqual(self.mi_list[2].loser, None)
        self.assertIsInstance(self.mi_list[2].winner, tmt.Competitor)
        self.assertIsInstance(self.mi_list[2].loser, tmt.Competitor)


class MatchTestCase(unittest.TestCase):

    def setUp(self):
        #unittest.TestCase.setUp(self)
        self.players = [tmt.Competitor('A'),
                        tmt.Competitor('B'),
                        tmt.Competitor('C'),
                        tmt.Competitor('D')]
        self.mi = tmt.MatchInfo()

    def tearDown(self):
        #unittest.TestCase.tearDown(self)
        self.players = None

    def test_match(self):
        def process1():
            tmt.Match()
            return True

        def process2():
            tmt.Match('a', 'b')

        def process3():
            tmt.Match(None, None, None, self.mi)

        self.assertTrue(process1)
        self.assertRaises(AssertionError, process2)
        self.assertTrue(process3)

        match1 = tmt.Match(self.players[0], self.players[1], None, \
                           tmt.MatchInfo())
        match2 = tmt.Match(self.players[2], self.players[3], None, \
                           tmt.MatchInfo(can_draw=True))
        #match1.info.score.add_home_score(3)
        #match1.info.score.add_away_score(1)
        match1.play_match()
        self.assertIsInstance(match1.info.winner, tmt.Competitor)
        self.assertFalse(match1.info.draw)
        while not match2.info.draw:
            match2.play_match()
        self.assertEqual(match2.info.winner, match2.info.loser)
        match1.next_round = match2
        match2.previous_match2 = match1
        self.assertEqual(match1.next_round.previous_match2, match1)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
