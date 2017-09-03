from __future__ import print_function

import argparse
import sys

from .squirrel import Squirrel


class SquirrelTerm(object):

    def __init__(self):
        self.baseparser()
        parser = argparse.ArgumentParser(
            description='Data Squirrel Command line interface',
            usage='''squirrel <command> [<args>]

The most commonly used squirrel commands are:
    newborn     Start a new collection
    forrage     Continue with an existing collection
''')
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def newborn(self):
        parser = argparse.ArgumentParser(
            prog='squirrel newborn', parents=[self.parser],
            description='New collection')
        parser.add_argument(
            '-s', '--start',
            help='The starting time in second since EPOCH. If none is ' +
            'supplied the default of 7 prior to today will be used',
            metavar='\b', default=None, type=int)
        args = parser.parse_args(sys.argv[2:])
        squirrel = Squirrel(args.wanted_nuts,
                            data_dir=args.dir, auth_file=args.auth)
        squirrel.newborn(args.start)

    def forrage(self):
        parser = argparse.ArgumentParser(
            prog='squirrel forrage', parents=[self.parser],
            description='Continue with existing collection')
        args = parser.parse_args(sys.argv[2:])
        squirrel = Squirrel(args.wanted_nuts,
                            data_dir=args.dir, auth_file=args.auth)
        squirrel.forrage()

    def baseparser(self):
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument(
            '-d', '--dir',
            help='The directory where the data should be stored. If none is ' +
            'supplied the default auth.json will be used.',
            metavar='\b', default=None)
        self.parser.add_argument(
            '-a', '--auth',
            help='The full file path of the auth.json file. If none is ' +
            'supplied the default auth.json will be used.',
            metavar='\b', default=None)
        self.parser.add_argument(
            'wanted_nuts',
            help='The data you want to be collected. Options inclue: luno ' +
            'btcc and any google finance ticker, e.g. usdzar. Space separated',
            nargs='*', default=None)



def main():
    SquirrelTerm()
