'''
DESCRIPTION
    Tournaments is module of classes for simulating tournaments (tennis,
    football, hockey, etc.)
LICENSE
    What licence is provided?
AUTHOR
    adpro (Ales Daniel)
'''


import math
import random


class Competitor():
    '''
    Class representing match competitor - player or team
    '''
    def __init__(self, name=''):
        self.name = name

    def __str__(self):
        return 'Competitor:' + self.name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        assert isinstance(name, str), "Name must be string."
        self.__name = name


class Score():
    '''
    Class for representing score for match between two competitors
    '''
    def __init__(self, score1=None, score2=None):
        '''
        Constructor

        @param score1: initial score (points, goals, and so on) for first
            competitor
        @param score2: initial score (points, goals, and so on) for second
            competitor
        '''
        self.score_competitor1 = score1
        self.score_competitor2 = score2

    def __verify_score(self, score):
        assert isinstance(score, int) or isinstance(score, float), \
            "Part of score can be Int or Float value."

    @property
    def score_competitor1(self):
        '''Score (points, goals) for first competitor'''
        return self.__score_competitor1

    @score_competitor1.setter
    def score_competitor1(self, value):
        self.__verify_score(value)
        self.__score_competitor1 = value

    @property
    def score_competitor2(self):
        '''Score (points, goals) for second competitor'''
        return self.__score_competitor2

    @score_competitor2.setter
    def score_competitor2(self, value):
        self.__verify_score(value)
        self.__score_competitor2 = value


class MatchInfo():
    '''
    Class for storing information about match
    '''
    def __init__(self, score=None, can_draw=False):
        '''
        Constructor

        @param score: initial score; if not set, is used default (zero) point
        @param can_draw: flag, whether match can end with draw; default False
        '''
        self.score = score
        self.__can_draw = can_draw
        self.draw = False
        self.winner = None
        self.loser = None

    @property
    def score(self):
        '''Property for storing score in this match.'''
        return self.__score

    @score.setter
    def score(self, value):
        if value is None:
            value = Score(0, 0)
        assert isinstance(value, Score), \
            'Score can contains only Score objects.'
        self.__score = value

    @property
    def can_draw(self):
        '''Getter for can_draw property. Stores bool value, whether it is
            possible to end match with draw
        '''
        return self.__can_draw


class Match():
    '''
    Class representing main entities of match
    '''
    def __init__(self, competitor1=None, competitor2=None,
                 next_round=None, info=None):
        '''
        Constructor

        @param competitor1: stores pointer to the first competitor
        @param competitor2: stores pointer to the second competitor
        @param next_round: stores pointer to the next match in next round
        @param info: stores pointer to the MatchInfo object
        '''
        self.competitor1 = competitor1
        self.competitor2 = competitor2
        self.next_round = next_round
        self.previous_match1 = None
        self.previous_match2 = None
        self.info = info

    def __test_competitors(self, value):
        '''
        Private method to testing, whether value is Competitor object

        @param value: object to test whether it is instance of Competitor class
        @return: True if value is Competitor class instance otherwise raise
            AssertionError
        '''
        if value is not None:
            assert isinstance(value, Competitor), \
                'Object is not Competitor object.'
        return True

    def __test_previous_match(self, value):
        '''
        Private method to testing, whether value is Match object

        @param value: object to test whether it is instance of Match class
        @return: True if value is Match class instance otherwise raise
            AssertionError
        '''
        if value is not None:
            assert isinstance(value, Match), \
                'Previous match must be Match object.'
        return None

    @property
    def competitor1(self):
        '''Pointer to first Competitor object'''
        return self.__competitor1

    @competitor1.setter
    def competitor1(self, value):
        assert self.__test_competitors(value)
        self.__competitor1 = value

    @property
    def competitor2(self):
        '''Pointer to the second Competitor object.'''
        return self.__competitor2

    @competitor2.setter
    def competitor2(self, value):
        assert self.__test_competitors(value)
        self.__competitor2 = value

    @property
    def previous_match1(self):
        '''Store pointer to the previous match'''
        return self.__previous_match1

    @previous_match1.setter
    def previous_match1(self, value):
        self.__test_previous_match(value)
        self.__previous_match1 = value

    @property
    def previous_match2(self):
        '''Store pointer to the previous match'''
        return self.__previous_match2

    @previous_match2.setter
    def previous_match2(self, value):
        self.__test_previous_match(value)
        self.__previous_match2 = value

    @property
    def next_round(self):
        '''A pointer to the next round match. Only Final match has no one.
        '''
        return self.__next_round

    @next_round.setter
    def next_round(self, value):
        if value is not None:
            assert isinstance(value, Match), \
                'Object is not instance of Match class.'
        self.__next_round = value

    @property
    def info(self):
        '''Pointer to MatchInfo object'''
        return self.__info

    @info.setter
    def info(self, value):
        if value is not None:
            assert isinstance(value, MatchInfo), \
                'Object must be a MatchInfo object.'
        self.__info = value

    def play_match(self):
        raise NotImplementedError()


class SingleEliminationTournament():
    '''
    Represents Single elimination tournament and its structure
    '''
    def __init__(self, seeded_players=[], other_players=[], shuffle=True):
        '''
        Constructor
        '''
        # competitors count verifications
        players_count = len(seeded_players) + len(other_players)
        assert players_count > 1, \
            "Competitors count must be 2 and more (power of 2)."
        assert math.modf(math.log2(players_count))[0] == 0.0, \
            "Competitors count must be a power of 2."
        self.__competitors_count = players_count
        # seeded competitors verifications
        self.__verify_competitors(seeded_players)
        self.__seeded_players = tuple(seeded_players)
        # other competitors verifications and shuffle they
        self.__verify_competitors(other_players)
        self.__other_players = \
            self.__shuffle_competitors(other_players, shuffle)
        # other actions
        self.__current_round = 0
        # assign players
        self.__competitors = tuple(self.seeded_players + \
                                   tuple(self.other_players))
        # create tournament tree
        self.__tournament_tree = self.__create_tournament_tree()
        # seed competitors into tree
        self.__seed_competitors()

    def __verify_competitors(self, players=[]):
        '''
        Verifies players, that everybody is instance of Competitor object

        @param players: list of players to verify
        @return: True, if all competitors is instances of Competitor class or
            if list is empty
        '''
        if len(players) > 0:
            for player in players:
                assert isinstance(player, Competitor), \
                    "Competitor must be instance of Competitor class."
        return True

    def __shuffle_competitors(self, players=[], shuffle=True):
        '''
        Shuffles list of competitors for random sequence of competitors

        @param players: list of competitors to shuffle
        @param shuffle: boolean value whether function do shuffle or not
        @return: shuffled list of competitors
        '''
        if shuffle:
            return random.sample(players, len(players))
        else:
            return players

    def __set_first_round_ranking(self):
        '''
        Makes list of competitors sorted for tournament tree from left to right
        More info:
        http://codereview.stackexchange.com/questions/17703/
                using-python-to-model-a-single-elimination-tournament
        http://en.wikipedia.org/wiki/Single-elimination_tournament

        @return: list of competitors sorted for tree
        '''
        first_round = list(range(self.competitors_count))
        left = []
        right = []
        if self.competitors_count > 2:
            left = first_round[0::4] + first_round[-1::-4]
            right = first_round[1::4] + first_round[-2::-4]
        else:
            left.append(first_round[0])
            right.append(first_round[1])
        left = sorted(left)
        right = sorted(right)
        half = len(left) // 2
        leftf = []
        rightf = []
        if half > 1:
            for i in range(half // 2):
                leftf.append(left[i])
                leftf.append(left[-1 - i])
                leftf.append(left[half - 1 - i])
                leftf.append(left[half + i])
                rightf.append(right[i])
                rightf.append(right[-1 - i])
                rightf.append(right[half - 1 - i])
                rightf.append(right[half + i])
        elif half == 1:
            # for competitors need special list joins (semifinal)
            leftf.append(left[0])
            leftf.append(left[-1])
            rightf.append(right[0])
            rightf.append(right[-1])
        else:
            # two competitors (final match)
            leftf = left[0]
            rightf = right[0]
        return leftf + rightf[::-1]

    def __create_tournament_tree(self):
        '''
        Creates list for every rounds. Connects every list item between other
        items, that connections makes tournament tree.

        @return: list of interconnected list items
        '''
        tournament_rounds = []
        # create lists for every round
        for i in range(int(math.log2(self.competitors_count))):
            round_list = [Match() for _ in range(2 ** i)]
            tournament_rounds.append(round_list)
        # make interconnections between rounds - tournament tree
        for i in range(int(math.log2(self.competitors_count - 1))):
            if len(tournament_rounds[- 1 - i]) > 1:
                for j in range(len(tournament_rounds[- 1 - i]) // 2):
                    k = (2 * j)
                    tournament_rounds[- 1 - i][k].next_round = \
                        tournament_rounds[- 1 - i - 1][j]
                    tournament_rounds[- 1 - i][k + 1].next_round = \
                        tournament_rounds[- 1 - i - 1][j]
                    tournament_rounds[- 1 - i - 1][j].previous_match1 = \
                        tournament_rounds[- 1 - i][k]
                    tournament_rounds[- 1 - i - 1][j].previous_match2 = \
                        tournament_rounds[- 1 - i][k + 1]
        return tournament_rounds

    def __seed_competitors(self):
        player_order = self.__set_first_round_ranking()
        # insert competitors into right place in the tournament tree
        # first list is last round, last list is first round
        for i in range(len(self.__competitors) // 2):
            self.__tournament_tree[-1][i].competitor1 = \
                self.competitors[player_order[2 * i]]
            self.__tournament_tree[-1][i].competitor2 = \
                self.competitors[player_order[(2 * i) + 1]]

    @property
    def competitors_count(self):
        '''Number of competitors in single elimination tournament'''
        return self.__competitors_count

    @property
    def seeded_players(self):
        '''Seeded competitors to the tournament'''
        return self.__seeded_players

    @property
    def other_players(self):
        '''List of not seeded competitors'''
        return self.__other_players

    @property
    def current_round(self):
        '''Current round of tournament from bottom to final match'''
        return self.__current_round

    @property
    def competitors(self):
        '''Tuple of all competitors in the tournament'''
        return self.__competitors

    @property
    def tournament_tree(self):
        return self.__tournament_tree

    def play_round(self):
        raise NotImplementedError()

#-----------------------------------------------------------------------------


# simple test of SE
seeded_competitors = [Competitor('As'),
               Competitor('Bs'),
               Competitor('Cs')]
other_competitors = [Competitor('D'),
               Competitor('E'),
               Competitor('F'),
               Competitor('G'),
               Competitor('H')]
frenchopen = \
    SingleEliminationTournament(seeded_competitors, other_competitors, False)
# test print
for item in frenchopen.competitors:
    print(item)
print('final.prev2.prev1.comp1', frenchopen.tournament_tree[0][0].previous_match2.previous_match1.competitor1)
