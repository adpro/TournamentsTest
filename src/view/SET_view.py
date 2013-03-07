# coding=UTF-8
# vim: set fileencoding=UTF-8 :
'''
DESCRIPTION
    Class for interpreting Single Elimination Tournament to the terminal.
LICENSE
    TournamentsTest by Aleš Daniel is licensed under a Creative Commons
    Attribution-NonCommercial 3.0 Unported License.
    http://creativecommons.org/licenses/by-nc/3.0/
AUTHOR
    adpro (Ales Daniel)
'''

import view.core_view as cv


class SETView():
    '''
    Class for showing Single Elimination Tournament objects into terminal
    '''

    @staticmethod
    def get_SET_header():
        return "*** Single Elimination Tournament ***"

    @staticmethod
    def show_SET_header():
        cv.CoreView.show_text(SETView.get_SET_header())

    @staticmethod
    def get_round_header(info):
        return "* {0} *".format(info)

    @staticmethod
    def show_round_header(info):
        cv.CoreView.show_text(SETView.get_round_header(info))

    @staticmethod
    def show_round_matches(round_matches):
        '''
        Shows competitors in matches in current round

        @param round: matches in current round
        '''
        for match in round_matches:
            cv.CoreView.show_text(cv.MatchView.get_match_competitors(match))

    @staticmethod
    def show_not_seeded_competitors(competitors, seeded=False):
        '''
        Show competitors who are (not) seeded in the Single Elimination
        Tournament

        @param competitors: seeded competitors sequence
        @param seeded: boolean value, True if competitors are seeded,
                        other False
        '''
        if seeded:
            cv.CoreView.show_text("* Seeded competitors *")
        else:
            cv.CoreView.show_text("* Not seeded competitors *")

        for player in competitors:
            cv.CompetitorView.show_name(player)
