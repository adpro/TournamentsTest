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
from random import randrange
import examples.TennisTournament.tennis_model as tm
import examples.TennisTournament.tennis_view as tv


class TennisCli():
    '''
    Main class for command-line interface for tennis tournaments example.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.view_SET = tv.TennisSingleEliminationTournamentView()

    def run(self):
        '''
        Runs all method for tournaments to show, how we can use it.
        '''

        #
        # Some not MVC like code
        #

        seeded_competitors = [tm.TennisPlayer('As', 7, 9, 8),
                   tm.TennisPlayer('Bs', 8, 8, 8),
                   tm.TennisPlayer('Cs', 9, 7, 9)]
        other_competitors = [tm.TennisPlayer('D', 6, 8, 9),
                       tm.TennisPlayer('E', 9, 7, 7),
                       tm.TennisPlayer('F', 7, 9, 7),
                       tm.TennisPlayer('G', 8, 8, 7),
                       tm.TennisPlayer('H', 5, 9, 9),
                       tm.TennisPlayer('I', 6, 8, 7),
                       tm.TennisPlayer('J', 7, 7, 6),
                       tm.TennisPlayer('K', 1, 1, 1),
                       tm.TennisPlayer('L', randrange(1, 10), \
                                            randrange(1, 10),
                                            randrange(1, 10)),
                       tm.TennisPlayer('M', randrange(1, 10), \
                                            randrange(1, 10),
                                            randrange(1, 10)),
                       tm.TennisPlayer('N', randrange(1, 10), \
                                            randrange(1, 10),
                                            randrange(1, 10)),
                       tm.TennisPlayer('O', randrange(1, 10), \
                                            randrange(1, 10),
                                            randrange(1, 10)),
                       tm.TennisPlayer('P', randrange(1, 10), \
                                            randrange(1, 10),
                                            randrange(1, 10))
                       ]
        frenchopen = \
            tm.TennisSET(seeded_competitors, \
                        other_competitors, \
                        True)
        assert isinstance(frenchopen, tm.TennisSET)

        # test print
        self.view_SET.print_SET_header()
        self.view_SET.print_players(frenchopen.competitors)

        for i in range(int(math.log2(frenchopen.competitors_count))):
            self.view_SET.print_round_header(i)
            frenchopen.play_round()
            self.view_SET.print_round_results(\
                                frenchopen.tournament_tree[-1 - i])
