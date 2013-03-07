# coding=UTF-8
# vim: set fileencoding=UTF-8 :
'''
DESCRIPTION
    Tournaments is module of classes for simulating tournaments (tennis,
    football, hockey, etc.)
LICENSE
    TournamentsTest by Aleš Daniel is licensed under a Creative Commons
    Attribution-NonCommercial 3.0 Unported License.
    http://creativecommons.org/licenses/by-nc/3.0/
AUTHOR
    adpro (Ales Daniel)
'''
import math
import model.tournaments as tmt
import view.core_view as cview
import view.SET_view as setview


class Cli():
    '''
    Main class for command-line interface for tournaments.
    '''

    def run(self):
        '''
        This method is example how to use other modules
        '''

        seeded_competitors = [tmt.Competitor('As'),
                   tmt.Competitor('Bs'),
                   tmt.Competitor('Cs')]
        other_competitors = [tmt.Competitor('D'),
                       tmt.Competitor('E'), tmt.Competitor('F'),
                       tmt.Competitor('G'), tmt.Competitor('H'),
                       tmt.Competitor('I'), tmt.Competitor('J'),
                       tmt.Competitor('K'), tmt.Competitor('L'),
                       tmt.Competitor('M'), tmt.Competitor('N'),
                       tmt.Competitor('O'), tmt.Competitor('P'),
                       tmt.Competitor('D2'), tmt.Competitor('E2'),
                       tmt.Competitor('F2'), tmt.Competitor('G2'),
                       tmt.Competitor('H2'), tmt.Competitor('I2'),
                       tmt.Competitor('J2'), tmt.Competitor('K2'),
                       tmt.Competitor('L2'), tmt.Competitor('M2'),
                       tmt.Competitor('N2'), tmt.Competitor('O2'),
                       tmt.Competitor('P2'), tmt.Competitor('Q2'),
                       tmt.Competitor('R2'), tmt.Competitor('S2'),
                       tmt.Competitor('D3'), tmt.Competitor('E3'),
                       tmt.Competitor('F3'), tmt.Competitor('G3'),
                       tmt.Competitor('H3'), tmt.Competitor('I3'),
                       tmt.Competitor('J3'), tmt.Competitor('K3'),
                       tmt.Competitor('L3'), tmt.Competitor('M3'),
                       tmt.Competitor('N3'), tmt.Competitor('O3'),
                       tmt.Competitor('P3'), tmt.Competitor('Q3'),
                       tmt.Competitor('R3'), tmt.Competitor('S3'),
                       tmt.Competitor('D4'), tmt.Competitor('E4'),
                       tmt.Competitor('F4'), tmt.Competitor('G4'),
                       tmt.Competitor('H4'), tmt.Competitor('I4'),
                       tmt.Competitor('J4'), tmt.Competitor('K4'),
                       tmt.Competitor('L4'), tmt.Competitor('M4'),
                       tmt.Competitor('N4'), tmt.Competitor('O4'),
                       tmt.Competitor('P4'), tmt.Competitor('Q4'),
                       tmt.Competitor('R4'), tmt.Competitor('S4')
                       ]
        frenchopen = \
            tmt.SingleEliminationTournament(seeded_competitors, \
                                        other_competitors, True)
        setview.SETView.show_SET_header()
        setview.SETView.show_not_seeded_competitors(
                    frenchopen.seeded_players,
                    True)
        setview.SETView.show_not_seeded_competitors(
                    frenchopen.other_players)

        cview.CoreView.show_text('---Selected competitors---')
        first = frenchopen.tournament_tree[0][0]
        match = first.previous_match2.previous_match2.previous_match2
        match = match.previous_match2.previous_match2
        cview.CoreView.show_text("final.prev2.prev2.prev2.prev2.prev2.comp2")
        cview.CompetitorView.show_name(match.competitor2)

        match = first.previous_match2.previous_match1.previous_match2
        match = match.previous_match1.previous_match2
        cview.CoreView.show_text("final.prev2.prev1.prev2.prev1.prev2.comp2")
        cview.CompetitorView.show_name(match.competitor2)

        for i in range(int(math.log2(frenchopen.competitors_count))):
            setview.SETView.show_round_header(
                frenchopen.get_current_fraction_info())
            frenchopen.play_round()
            for match in frenchopen.tournament_tree[-1 - i]:
                cview.MatchView.show_match_competitors_w_results(match)
