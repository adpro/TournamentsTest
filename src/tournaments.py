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




# simple test
players = ['A','B','C','D','E','F','G','H']
wimbledon = SingleEliminationTournament(players)
# prints F
print(str(
        wimbledon.champion.competitor2.competitor1.competitor1.winner_object))






