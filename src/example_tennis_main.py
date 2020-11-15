#!/usr/bin/python3
'''
DESCRIPTION
    Tournaments is module of classes for simulating tournaments (tennis,
    football, hockey, etc.)
'''
import examples.TennisTournament.tennis_controller as cli


if __name__ == '__main__':
    cmd = cli.TennisCli()
    cmd.run()
