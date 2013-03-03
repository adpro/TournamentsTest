# coding=UTF-8
# vim: set fileencoding=UTF-8 :
'''
DESCRIPTION
    TennisController is sample module of classes for simulating tennis
    tournaments. Contains terminal controller of tennis Single Elimination
    Tournaments.
LICENSE
    TournamentsTest by Aleš Daniel is licensed under a Creative Commons
    Attribution-NonCommercial 3.0 Unported License.
    http://creativecommons.org/licenses/by-nc/3.0/
AUTHOR
    adpro (Ales Daniel)
'''
import math
import model.tournaments as tmt
import examples.TennisTournament.tennis_model as tm


class TennisCli():
    '''
    classdocs
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

        seeded_competitors = [tm.TennisPlayer('As'),
                   tm.TennisPlayer('Bs'),
                   tm.TennisPlayer('Cs')]
        other_competitors = [tm.TennisPlayer('D'),
                       tm.TennisPlayer('E'),
                       tm.TennisPlayer('F'),
                       tm.TennisPlayer('G'),
                       tm.TennisPlayer('H'),
                       tm.TennisPlayer('I'),
                       tm.TennisPlayer('J'),
                       tm.TennisPlayer('K'),
                       tm.TennisPlayer('L'),
                       tm.TennisPlayer('M'),
                       tm.TennisPlayer('N'),
                       tm.TennisPlayer('O'),
                       tm.TennisPlayer('P'),
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
