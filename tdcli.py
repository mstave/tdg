#!/usr/bin/env python
'''
Created on Sep 18, 2012

@author: mstave
'''
import argparse
import unittest
import todo_file
from todo_item import TodoItem
import logging as log


class TDCli(object):
    '''
    classdocs
    '''
    tdFilename = "todo.txt"
    td_file = None
    cmd = None
    addargs = None

    def __init__(self):
        '''
        Constructor
        '''
        self.parse()
        self.td_file = todo_file.TodoFile(self.tdFilename, True)
        self.td_file.be_quiet = True
        if self.cmd is not None:
            self.run()
        self.parser = None

    def cmd_lsgrep(self):
        print self.td_file.ls_grep(self.addargs)

    def cmd_ls(self, ls_str=None):
        if ls_str is None:
            ls_str = self.addargs
        print self.td_file.list_todos(ls_str, True)

    def cmd_lspri(self):
        print self.td_file.ls_pri(self.addargs.upper())

    def cmd_default(self):
        print self.parser.print_help()

    def cmd_add(self):
        priarg = self.cmd.replace("add", "")
        new_td = TodoItem(self.addargs)
        new_td.priority = priarg
        new_td.create_today()
        #print "Adding " + str(new_td)
        self.td_file.append(new_td)
        self.save()
        self.cmd_ls()

    def save(self):
        self.td_file.update_todo_txt_arr()
        self.td_file.write_file()

    def cmd_rm(self):
        self.td_file.delete_task(int(self.addargs))
        self.save()

    def cmd_do(self):
        temp_td = self.td_file.get_task(int(self.addargs))
        temp_td.done = True
        self.td_file.update_task(int(self.addargs), temp_td)
        self.save()
        self.cmd_ls(temp_td.task)

    def cmd_undo(self):
        temp_td = self.td_file.get_task(int(self.addargs))
        temp_td.done = False
        self.td_file.update_task(int(self.addargs), temp_td)
        self.save()
        self.cmd_ls(temp_td.task)

    def run(self):
        '''
        handle the command
        '''
        {
            'lsgrep':   self.cmd_lsgrep,
            'ls':       self.cmd_ls,
            'adda':     self.cmd_add,
            'addb':     self.cmd_add,
            'addc':     self.cmd_add,
            'addd':     self.cmd_add,
            'add':      self.cmd_add,
            'lspri':      self.cmd_lspri,
            'del':      self.cmd_rm,
            'rm':       self.cmd_rm,
            'do':       self.cmd_do,
            'undo':     self.cmd_undo
        }.get(self.cmd, self.cmd_default)()

    def parse(self):
        '''
        handle command-line attributes
        :param argv:
        '''
        self.parser = argparse.ArgumentParser(
                    description="todo.txt modification app")
        self.parser.add_argument("--test", action="store_true",
                    help="run built-in unit tests")
        self.parser.add_argument("-f", "--file", nargs=1,
                    help="specify name of todo.txt file")
        self.parser.add_argument("--cmdhelp", action="store_true",
                    help="show additional help for all commands")
        self.parser.add_argument("command", nargs='*',
                    help="list_todos, addp, etc., see --cmdhelp for more info")

        args = self.parser.parse_args()

        if args.cmdhelp:
            print TDCli.show_commands()

        if args.test:
            print "Executing tests for todo_py"
            suite = unittest.TestLoader().loadTestsFromName("todo_py")
            unittest.TextTestRunner().run(suite)
            # todo add tests for CLI

        if len(args.command) >= 1:
            self.cmd = args.command[0]
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
    CLI = TDCli()
