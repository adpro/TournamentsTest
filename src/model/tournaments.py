# coding=UTF-8
# vim: set fileencoding=UTF-8 :
'''
DESCRIPTION
    Tournaments is module of classes for simulating tournaments (tennis,
    football, hockey, etc.)
'''


import math
import random


class MatchInfoError(LookupError):
    '''
    Error indicates problem, that MatchInfo object is not exists.
    '''
    pass


class MatchError(Exception):
    pass


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
        if name is None:
            name = ''
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

    def __str__(self):
        return ''.join(('(', str(self.score_competitor1), ':',
                         str(self.score_competitor2), ')'))

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

    def add_home_score(self, value):
        '''
        Adds value to home competitor score.

        @param value: value to increase the home competitor score
        '''
        if value is None:
            raise ValueError('Increment value for score is not set.')
        self.__verify_score(value)
        self.score_competitor1 += value

    def add_away_score(self, value):
        '''
        Adds value to away competitor score.

        @param value: value to increase the away competitor score
        '''
        if value is None:
            raise ValueError('Increment value for score is not set.')
        self.__verify_score(value)
        self.score_competitor2 += value

    def evaluate_score(self):
        '''
        Evaluate who is winner

        @return: 1 if Home wins, -1 if Away wins, 0 if draw
        '''
        if self.score_competitor1 > self.score_competitor2:
            return 1
        elif self.score_competitor1 == self.score_competitor2:
            return 0
        else:
            return -1

    def get_max_score(self):
        '''
        Return bigger score value of the competitors score
        Example: Score(3, 5) returns 5.

        @return: maximum number from score numbers
        '''
        return max((self.score_competitor1, self.score_competitor2))


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

    def set_score(self, score):
        '''
        Sets new Score object
        '''
        self.score = score

    def evaluate(self, competitor1, competitor2):
        '''
        Evaluates score and sets pointers to the winner and the loser
        '''
        if not isinstance(competitor1, Competitor) and \
            not isinstance(competitor2, Competitor):
            raise ValueError(competitor1, \
                        'Competitors must be instances of Competitor class.')
        result = self.score.evaluate_score()
        if result == 1:
            # home wins
            self.winner = competitor1
            self.loser = competitor2
            self.draw = False
        elif result == 0:
            # draw
            self.winner = None
            self.loser = None
            self.draw = True
        else:
            # away wins
            self.winner = competitor2
            self.loser = competitor1
            self.draw = False


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
        '''
        Runs current match - compare competitors objects
        '''
        if self.info is None:
            raise MatchInfoError('Pointer is not set to MatchInfo object.')

        while True:
            home = random.randrange(0, 5)
            away = random.randrange(0, 5)
            # result of the match can be any - draw is possible
            if self.info.can_draw:
                break
            else:
                # one competitor must win - if draw, repeat
                if not home == away:
                    break
        self.info.score = Score(home, away)
        self.info.evaluate(self.competitor1, self.competitor2)

    def add_competitor(self, competitor):
        '''
        Adds competitor (from previous round) into current match
        '''
        if not isinstance(competitor, Competitor):
            raise ValueError(competitor, \
                                'It must be instance of Competitor class.')
        if self.competitor1 == None:
            self.competitor1 = competitor
        elif self.competitor1 is not None and self.competitor2 == None:
            self.competitor2 = competitor
        else:
            raise MatchError('Too much competitors in one match.')


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
        assert math.modf(math.log(players_count,2))[0] == 0.0, \
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

        # set fraction info (final, semifinal, ..)
        self.__fraction_info = []
        self._init_fraction_info()

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

    def _init_round_list(self, i):
        return [Match(info=MatchInfo()) for _ in range(2 ** i)]

    def __create_tournament_tree(self):
        '''
        Creates list for every rounds. Connects every list item between other
        items, that connections makes tournament tree.

        @return: list of interconnected list items
        '''
        tournament_rounds = []
        # create lists for every round
        for i in range(int(math.log(self.competitors_count,2))):
            round_list = self._init_round_list(i)
            tournament_rounds.append(round_list)
        # make interconnections between rounds - tournament tree
        for i in range(int(math.log(self.competitors_count - 1,2))):
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
        # set current round variable to index for the first round
        self.__current_round = len(tournament_rounds) - 1
        # return all rounds
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

    def _init_fraction_info(self):
        '''
        Initialize list with name of tournament round name
        '''
        rounds_count = int(math.log(self.competitors_count,2))
        default = ["Final", "Semi-Final", "Quarter-Final"]

        self.fraction_info = default[0:rounds_count]
        if rounds_count > 3:
            next_rounds = []
            for i in range(rounds_count - 3):
                if i % 10 == 0:
                    next_rounds.append("{0}st Round".format(i + 1))
                elif i % 10 == 1:
                    next_rounds.append("{0}nd Round".format(i + 1))
                elif i % 10 == 2:
                    next_rounds.append("{0}rd Round".format(i + 1))
                else:
                    next_rounds.append("{0}th Round".format(i + 1))
        self.fraction_info = next_rounds[::-1]
        #self.__fraction_info = self.__fraction_info[::-1]

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

    @property
    def fraction_info(self):
        '''Info about fraction of tournament'''
        return self.__fraction_info

    @fraction_info.setter
    def fraction_info(self, value):
        assert isinstance(value, tuple) or isinstance(value, list), \
            'Fraction info must be a list or a tuple object.'
        self.__fraction_info.extend(value)

    def get_current_fraction_info(self):
        '''
        Get name of fraction of tournament.

        @return: string with name of fraction like 'Final' or 'Quarter-Final'
        '''
        return self.fraction_info[self.current_round]

    def play_round(self):
        '''
        Runs all games in the current round.
        '''
        #print('---play round method---')
        for match in self.tournament_tree[self.__current_round]:
            match.play_match()

            #print(len(self.tournament_tree[self.__current_round]))
            #print('*', match.competitor1, match.competitor2, \
            #      match.info.score, '> wins', match.info.winner)

            # if not final match
            if self.__current_round > 0:
                ## add winner to the next round
                match.next_round.add_competitor(match.info.winner)
        # prepare next round index / decrease index
        if self.__current_round > 0:
            self.__current_round -= 1
