# coding=UTF-8
# vim: set fileencoding=UTF-8 :
'''
DESCRIPTION
    Main file for unit tests for Tournaments.
LICENSE
    TournamentsTest by Aleš Daniel is licensed under a Creative Commons
    Attribution-NonCommercial 3.0 Unported License.
    http://creativecommons.org/licenses/by-nc/3.0/
AUTHOR
    adpro (Ales Daniel)
HOW TO RUN TESTS
    python3 -m tests.main_test
    python3 -m unittest discover tests '*_test.py' -v
'''

import unittest
import tests.core_test as core_test

'''
suite = unittest.TestLoader().loadTestsFromTestCase(
        core_test.CompetitorTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)
runner = unittest.TextTestRunner()
print(runner.run(suite))
'''