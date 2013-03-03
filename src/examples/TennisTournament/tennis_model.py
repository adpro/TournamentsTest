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

import random

import model.tournaments as tmt


def is_in_interval(value):
    '''Helper function to test, whether value is in ou interval'''
    assert isinstance(value, int)
    if 0 <= value < 10:
        return True
    return False


class TennisPlayer(tmt.Competitor):
    '''
    Sample implementation of tennis player
    '''

    def __init__(self, name='', ability=0, fh=0, bh=0):
        '''
        Constructor
        '''
        super.__init__(name)
        self.forehand = fh
        self.backhend = bh

    @property
    def ability(self):
        '''Tennis player ability from 0 to 9. More is better.'''
        return self.__ability

    @ability.setter
    def ability(self, value):
        assert isinstance(value, int) and is_in_interval(value), \
            'Value must be int between 0 and 9.'
        self.__ability = value

    @property
    def forehand(self):
        '''Tennis player property for forehand'''
        return self.__forehand

    @forehand.setter
    def forehand(self, value):
        assert isinstance(value, int) and is_in_interval(value), \
            'Forehand must be int between 0-9.'
        self.__forehand = value

    @property
    def backhend(self):
        '''Tennis player property for backhand'''
        return self.__backhend

    @backhend.setter
    def backhend(self, value):
        assert isinstance(value, int) and is_in_interval(value), \
            'Backhand must be int between 0-9.'
        self.__backhend = value


class TennisGameScore(tmt.Score):
    '''
    Sample implementation of tennis score for a game in one set.
    '''
    def evaluate_score(self):
        first = max((self.score_competitor1, self.score_competitor2))
        second = min((self.score_competitor1, self.score_competitor2))

        if first < 6:
            # no one is set winner
            return 0
        elif (first >= 6 and first - second >= 2) or \
            (first == 7 and second == 6):
            # somebody wins the set
            if self.score_competitor1 > self.score_competitor2:
                return 1
            elif self.score_competitor1 < self.score_competitor2:
                return -1
        else:
            print("*** Some change in tennis game eval", first, second)


class TennisMatch(tmt.Match):
    '''
    Custom implementation of tennis match
    '''

    def __play_game(self):
        '''
        Evaluates duel between competitors for game in set - who wins the game

        @return: 1 if game winner is home player, 2 if winner is away player
        '''
        while True:
            home = random.randrange(0, 5)
            away = random.randrange(0, 5)
            if home != away:
                break
        if home > away:
            return 1
        else:
            return 2

    def play_match(self, sets=3):
        '''
        Custom implementation of tennis match

        @param sets: number of sets to win a match
        '''
        if self.info is None:
            raise tmt.MatchInfoError('Pointer is not set to MatchInfo object.')

        ''' change this code '''
        # make new score with MatchInfo
        # for every set:
        # for every game evaluate players properties and change set score
        # after every set change score object
        # something else ?
        match_score = tmt.Score(0, 0)
        while True:
            set_score = TennisGameScore(0, 0)
            while True:
                game_winner = self.__play_game()
                if game_winner == 1:
                    set_score.add_home_score(1)
                elif game_winner == 2:
                    set_score.add_away_score(1)
                state = set_score.evaluate_score()
                if state != 0:
                    if state == 1:
                        match_score.add_home_score(1)
                    elif state == -1:
                        match_score.add_away_score(1)
                    break
            if match_score.get_max_score() == sets:
                # match ended
                self.info.score = match_score
                self.info.evaluate(self.competitor1, self.competitor2)
