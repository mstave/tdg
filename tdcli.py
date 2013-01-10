'''
Created on Sep 18, 2012

@author: mstave
'''
import argparse
import unittest
import sys
import todo_file


class TDCli(object):
    '''
    classdocs
    '''
    tdFilename = "todo.txt"
    td_file = None
    cmd = None
    addargs = None

    def __init__(self, args):
        '''
        Constructor
        '''
        self.parse(args)
        self.td_file = todo_file.TodoFile(self.tdFilename)
        self.run()
        self.parser = None

    def run(self):
        '''
        handle the command
        '''
        if self.cmd is None:
            print self.parser.print_help()
        elif self.cmd == "list_todos":
            print self.td_file.list_todos(self.addargs)
        elif self.cmd == "lsgrep":
            self.td_file.ls_grep(self.addargs)

    def parse(self, argv):
        '''
        handle command-line attributes
        :param argv:
        '''
        self.parser = argparse.ArgumentParser(
                    description="todo.txt modification app")
        self.parser.add_argument("--test", action="store_true",
                    help="run built-in unit tests")
        self.parser.add_argument("--file", nargs=1,
                    help="specify name of todo.txt file")
        self.parser.add_argument("--cmdhelp", action="store_true",
                    help="show additional help for all commands")
        self.parser.add_argument("command", nargs='*',
                    help="list_todos, addp, etc., see --cmdhelp for more info")

        args = self.parser.parse_args(argv)

        if args.cmdhelp:
            print TDCli.show_commands()

        if args.test:
            print "Executing tests for todo_py"
            suite = unittest.TestLoader().loadTestsFromName("todo_py")
            unittest.TextTestRunner().run(suite)
            # todo add tests for CLI

        self.cmd = args.command[0]
        if len(args.command) > 1:
            self.addargs = " ".join(args.command[1:])

    @classmethod
    def show_commands(cls):
        '''
        help
        :param cls:
        '''
        cmd_str = "TDCli commands:\n"
        cmd_str += "\tls \t\t: list all todos\n"
        cmd_str += "\tlsgrep [regex] \t: list todos containing that reg expr "
        cmd_str += "(ex: lsgrep [Hh]ello)"
        return cmd_str

    def list_cmd(self, arg):
        '''

        :param arg:
        '''
        print self.td_file.list_todos(arg)

if __name__ == "__main__":
    CLI = TDCli(sys.argv[1:])
