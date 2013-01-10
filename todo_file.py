#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111
# todo_py :
# Copyright (C) 2012 Matt Stave
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import shutil
import time
from todo_item import TodoItem


class TodoFile(object):
    todo_txt_arr = []
    # array to hold contents of to do list, initially from "todo.txt"
    todo_item_arr = []
    todo_file_name = None
    ENV_TD_DIR = 'TODO_DIR'  # pylint: disable-msg=W0511

    def __init__(self, f_name="todo.txt"):
        try:
            tddir = os.environ[self.ENV_TD_DIR]
        except KeyError:
            tddir = os.getcwd()
        self.todo_file_name = os.path.join(tddir, f_name)
        self.load_file(self.todo_file_name)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return '\n'.join(self.todo_txt_arr) + "\n"

    def get_gui_index(self, query):
        index = 0
        for item in self.todo_item_arr:
            if item.gui_index == query:
                return index
            index += 1

    def get_priorities(self):
        pris = []
        for item in self.todo_item_arr:
            if not item.priority in pris:
                pris.append(item.priority)
        pris.sort()
        return pris

    def update_todo_item_arr(self):
        self.todo_item_arr = []
        for txt_item in self.todo_txt_arr:
            if txt_item is not None and (len(txt_item.strip()) > 0 ):
                self.todo_item_arr.append(TodoItem(txt_item))

    def update_todo_txt_arr(self):
        self.todo_txt_arr = []

        for todo_item in self.todo_item_arr:
            self.todo_txt_arr.append(todo_item.todo_txt_line)

    def append(self, new_item):
        self.todo_item_arr.append(new_item)
        self.update_todo_txt_arr()

    def load_file(self, f_name=None):
        if f_name is not None:
            self.todo_file_name = f_name
        t_file = open(self.todo_file_name, "r")
        getlines = open(self.todo_file_name).readlines()
        self.todo_txt_arr = [line.strip() for line in getlines]
        self.update_todo_item_arr()

    def write_file(self):
        self.update_todo_txt_arr()
        shutil.copy(self.todo_file_name, self.todo_file_name + ".bak")
        t_file = open(self.todo_file_name, 'w')
        t_file.write('\n'.join(self.todo_txt_arr))
        t_file.write('\n')
        t_file.close()

    def delete_task(self, index):
        self.todo_txt_arr.pop(index)
        item = self.todo_item_arr.pop(index)
        self.update_todo_txt_arr()
        return item

    def list_todos(self, arg):
        if arg is None:
            return str(self)
        temp_arr = []
        for todo in self.todo_txt_arr:
            if todo.find(arg) >= 0:
                temp_arr.append(todo)
        return '\n'.join(temp_arr) + "\n"

    def ls_grep(self, rex):

        #temp_arr = self.todo_txt_arr
        temp_arr = []
        for todo in self.todo_txt_arr:
            if re.search(rex, todo):
                temp_arr.append(todo)

        return '\n'.join(temp_arr) + "\n"
