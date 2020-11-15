# coding=UTF-8
# vim: set fileencoding=UTF-8 :
'''
DESCRIPTION
    TennisView is sample module of classes for simulating tennis tournaments.
    Contains terminal view of tennis Single Elimination Tournaments.
'''
import examples.TennisTournament.tennis_model as tm


class TennisPlayerView():
    @staticmethod
    def print_player(player):
        print("TennisPlayer> {0} Stats:{1} {2} {3} ({4})".format(
                player.name,
                player.ability,
                player.forehand,
                player.backhend,
                player.ability + player.forehand + player.backhend
                ))


class TennisMatchView():
    '''
    View for Match class in Tennis example
    '''

    @staticmethod
    def print_match(match):
        set_scores = "["
        for score in match.info.score.set_scores:
            set_scores += str(score)
        set_scores += "]"
        print("{0} vs {1}\t{2} {3}".format(
              match.competitor1,
              match.competitor2,
              match.info.score,
              set_scores
              ))


class TennisSingleEliminationTournamentView():
    '''
    View from MVC for TournamentTest in TennisTournament example.
    '''

    def print_SET_header(self):
        print("*** Tennis Single Elimination Tournament Example ***")

    def print_players(self, players):
        print("* Players *")
        for player in players:
            assert isinstance(player, tm.TennisPlayer)
            TennisPlayerView.print_player(player)

    def print_round_header(self, info):
        print("* {0} *".format(info))

    def print_round_results(self, matches):
        print("* Round results *")
        for match in matches:
            TennisMatchView.print_match(match)
