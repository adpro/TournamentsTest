# coding=UTF-8
# vim: set fileencoding=UTF-8 :
'''
DESCRIPTION
    CoreView is module for displaying main objects.
'''


class CoreView():
    '''
    Basic methods for output into the terminal window.
    '''
    @staticmethod
    def show_text(text):
        print(text)


class CompetitorView():
    '''
    View for competitor object
    '''

    @staticmethod
    def get_name(competitor):
        '''
        @param competitor: Competitor object
        @return: string representation of competitor for terminal
        '''
        return competitor.name

    @staticmethod
    def show_name(competitor):
        '''
        Prints competitor name

        @param competitor: Competitor object
        '''
        CoreView.show_text(CompetitorView.get_name(competitor))


class ScoreView():
    '''
    View class for Score object.
    '''
    @staticmethod
    def get_score_string(score):
        '''
        @param score: Score object
        @return: string representation of score object
        '''
        return "{0}:{1}".format(score.score_competitor1,
                               score.score_competitor2)

    @staticmethod
    def show_score(score):
        '''
        Prints score object into the terminal

        @param score: Score object
        '''
        CoreView.show_text(ScoreView.get_score_string(score))

    @staticmethod
    def show_home_score(score):
        CoreView.show_text(score.score_competitor1)

    @staticmethod
    def show_away_score(score):
        CoreView.show_text(score.score_competitor2)


class MatchView():
    '''
    View for Match
    '''
    @staticmethod
    def get_match_competitors(match):
        '''
        @param match: Match object
        @return: competitors string for terminal
        '''
        return "{0} - {1}".format(
              CompetitorView.get_name(match.competitor1),
              CompetitorView.get_name(match.competitor2))

    @staticmethod
    def show_match_competitors(match):
        CoreView.show_text(MatchView.get_match_competitors(match))

    @staticmethod
    def get_match_competitors_w_results(match):
        '''
        @param match: Match object
        @return: Match result with info about competitors
        '''
        return "{0}\t{1}".format(
                MatchView.get_match_competitors(match),
                ScoreView.get_score_string(match.info.score)
                                 )

    @staticmethod
    def show_match_competitors_w_results(match):
        CoreView.show_text(MatchView.get_match_competitors_w_results(match))
