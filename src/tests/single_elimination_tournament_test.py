# coding=UTF-8
# vim: set fileencoding=UTF-8 :
'''
DESCRIPTION
    Tournaments game main file.
LICENSE
    What licence is provided?
AUTHOR
    adpro  (Ales Daniel)
'''
import unittest
from model import tournaments as tmt
import math


class SingleEliminationTestCase(unittest.TestCase):

    def setUp(self):
        #unittest.TestCase.setUp(self)
        self.seeded_competitors = [tmt.Competitor('As'),
                   tmt.Competitor('Bs'),
                   tmt.Competitor('Cs')]
        self.other_competitors = [tmt.Competitor('D'),
                   tmt.Competitor('E'),
                   tmt.Competitor('F'),
                   tmt.Competitor('G'),
                   tmt.Competitor('H'),
                   tmt.Competitor('I'),
                   tmt.Competitor('J'),
                   tmt.Competitor('K'),
                   tmt.Competitor('L'),
                   tmt.Competitor('M'),
                   tmt.Competitor('N'),
                   tmt.Competitor('O'),
                   tmt.Competitor('P'),
                   ]
        self.set = tmt.SingleEliminationTournament(
                            self.seeded_competitors,
                            self.other_competitors,
                            shuffle=False)

    def tearDown(self):
        #unittest.TestCase.tearDown(self)
        self.seeded_competitors = None
        self.other_competitors = None
        self.set = None

    def test_single_elimination_position_in_tree(self):
        final = self.set.tournament_tree[0][0]
        # second seeded player is on opposite side of tree
        self.assertEqual(
            final.previous_match2.previous_match2.previous_match2.competitor2,
            self.set.competitors[1])
        # second seeded player plays against 14th player
        self.assertEqual(
            final.previous_match2.previous_match2.previous_match2.competitor1,
            self.set.competitors[14])
        self.assertEqual(self.set.competitors[14], \
                         self.other_competitors[11])
        self.assertEqual(
            final.previous_match1.previous_match2.previous_match2.competitor1,
            self.set.competitors[4])
        self.assertEqual(
            final.previous_match1.previous_match2.previous_match1.competitor1,
            self.set.competitors[3])
        self.assertEqual(
            final.previous_match1.previous_match1.previous_match2.competitor1,
            self.set.competitors[7])

    def test_single_elimination_winner(self):
        for _ in range(int(math.log2(self.set.competitors_count))):
            self.set.play_round()
        final = self.set.tournament_tree[0][0]
        winner = final.info.winner
        # winner is Competitor class instance
        self.assertIsInstance(winner, tmt.Competitor)
        if final.competitor1 == winner:
            self.assertEqual(winner, \
                             final.previous_match1.info.winner)
        else:
            self.assertEqual(winner, \
                             final.previous_match2.info.winner)
