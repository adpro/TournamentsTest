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
