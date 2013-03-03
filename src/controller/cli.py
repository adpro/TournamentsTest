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


class Cli():
    '''
    Main class for command-line interface for tournaments.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def run(self):
        '''
        This method will be deleted or reimplemented into MVC-like code
        '''

        #
        # Some not MVC like code
        #

        seeded_competitors = [tmt.Competitor('As'),
                   tmt.Competitor('Bs'),
                   tmt.Competitor('Cs')]
        other_competitors = [tmt.Competitor('D'),
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
        frenchopen = \
            tmt.SingleEliminationTournament(seeded_competitors, \
                                        other_competitors, True)
        # test print
        print('---tmt.Competitors---')
        for item in frenchopen.competitors:
            print(item)
        print('---Selected competitor---')
        first = frenchopen.tournament_tree[0][0]
        match = first.previous_match2.previous_match2.previous_match2
        print('final.prev2.prev2.prev2.comp2', \
              match.competitor2)

        print('---Play Round---')
        for _ in range(int(math.log2(frenchopen.competitors_count))):
            frenchopen.play_round()
