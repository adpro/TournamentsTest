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


class SETTreeNode():
    '''
    Represents tree structure of Single elim. tournament node.
    '''

    def __init__(self, competitor1=None,
                 competitor2=None,
                 next_round=None):
        '''
        Constructor with competitors and winner
        '''
        self.competitor1 = competitor1
        self.competitor2 = competitor2
        self.next_round = next_round
        self.winner_object = None

    def __str__(self):
        return str(self.winner_object)

    @property
    def competitor1(self):
        '''
        Contains the first match competitor.
        '''
        return self.__competitor1

    @competitor1.setter
    def competitor1(self, competitor):
        self.__competitor1 = competitor

    @property
    def competitor2(self):
        '''
        Contains the second match competitor.
        '''
        return self.__competitor2

    @competitor2.setter
    def competitor2(self, competitor):
        self.__competitor2 = competitor

    @property
    def next_round(self):
        '''
        Pointer to the next round
        '''
        return self.__next_round

    @next_round.setter
    def next_round(self, next_round):
        self.__next_round = next_round

    @property
    def winner_object(self):
        '''
        Data of tree node. Contains player object (winner of a previous round
        match).
        '''
        return self.__winner_object

    @winner_object.setter
    def winner_object(self, winner_obj):
        self.__winner_object = winner_obj


class SingleEliminationTournament():
    '''
    Represents Single elimination tournament and its structure
    '''

    def __init__(self, players=[], compare_func=None):
        '''
        Constructor
        '''
        self.no_competitors = len(players)
        self.champion = self.__create_tournament_tree()
        self.__assign_players_to_tree(self.no_competitors, players)
        self.__current_round = 0   # current round in tournament
        self.__comp_func = compare_func  # how to compare player's objects

    def __create_tournament_tree(self):
        '''
        Helper method for creating tournament tree

        @return: one item list for champion
        '''
        rounds_list = []
        # thru competitors makes node's object in rounds list
        for i in range(int(math.log2(self.no_competitors)) + 1):
            # make nodes list
            round_list = [SETTreeNode() \
                        for _ in range(self.no_competitors // (2 ** i))]
            rounds_list.append(round_list)
        # make interconnections between nodes (tree structure)
        for i in range(int(math.log2(self.no_competitors))):
            if len(rounds_list[i]) > 1:
                for j in range(len(rounds_list[i]) // 2):
                    k = (2 * j)
                    rounds_list[i][k].next_round = rounds_list[i + 1][j]
                    rounds_list[i][k + 1].next_round = rounds_list[i + 1][j]
                    rounds_list[i + 1][j].competitor1 = rounds_list[i][k]
                    rounds_list[i + 1][j].competitor2 = rounds_list[i][k + 1]
        self.tournament_tree = rounds_list
        # top list in two-dimensional list is champion
        return rounds_list[-1][0]

    def __set_first_round_ranking(self, count):
        '''
        Makes list of competitors sorted for tournament tree from left to right
        More info:
        http://codereview.stackexchange.com/questions/17703/
                using-python-to-model-a-single-elimination-tournament
        http://en.wikipedia.org/wiki/Single-elimination_tournament

        @param count: number of competitors

        @return: list of competitors sorted for tree
        '''
        first_round = list(range(count))
        left = []
        right = []
        if count > 2:
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

    def __assign_players_to_tree(self, players_count, players=[]):
        '''
        Assigns players to the tournament tree

        @param players_count: number of competitors in tournament
        @param players: list of SETTreeNodes with player's objects (sorted
            from the best one to the worst one

        '''
        ranking = self.__set_first_round_ranking(players_count)
        #seed player into the tournament
        for i in range(len(ranking)):
            self.tournament_tree[0][i].winner_object = players[ranking[i]]

    @property
    def no_competitors(self):
        '''
        Competitor count in the tournament. Must be a power of 2.
        '''
        return self.__competitors_count

    @no_competitors.setter
    def no_competitors(self, count):
        assert math.modf(math.log2(count))[0] == 0.0, \
            "Competitors count must be a power of 2."
        self.__competitors_count = count

    @property
    def champion(self):
        '''
        Root element of the tournament tree
        '''
        return self.__champion

    @champion.setter
    def champion(self, root):
        self.__champion = root

    @property
    def tournament_tree(self):
        '''Two-dimensional list of matches in tournament'''
        return self.__tournament_tree

    @tournament_tree.setter
    def tournament_tree(self, tree):
        assert len(tree) >= 0, "Tournament tree is two-dimensional list."
        self.__tournament_tree = tree

    def play_round_matches(self):
        '''
        Evaluates all the matches in current round.
        '''
        # TODO potrebuji vyhodnocovaci funkci, kdo je lepsi
        #      v promenne self.__comp_func
        pass


#-----------------------------------------------------------------------------


class Competitor():
    '''
    Class representing match competitor - player or team
    '''
    def __init__(self, name=''):
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
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

    @property
    def score_competitor1(self):
        '''Score (points, goals) for first competitor'''
        return self.__score_competitor1

    @score_competitor1.setter
    def score_competitor1(self, value):
        self.__score_competitor1 = value

    @property
    def score_competitor2(self):
        '''Score (points, goals) for second competitor'''
        return self.__score_competitor2

    @score_competitor2.setter
    def score_competitor2(self, value):
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
            value = 0
        assert isinstance(value, int) or isinstance(value, float), \
            'Score can contains Int or Float value.'
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


class SingleElimination():
    '''
    Represents Single elimination tournament and its structure
    '''
    pass


# simple test
players = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
wimbledon = SingleEliminationTournament(players)
# prints F
print(str(
        wimbledon.champion.competitor2.competitor1.competitor1.winner_object))
