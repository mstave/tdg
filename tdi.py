#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tdi: interacive todo
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

import curses  # may not work on Windows without cygwin
import traceback
import os
import shutil
import datetime
import re

todoarr = []  # array to hold contents of todo list, initially from todo.txt
currow = 0  # current selected row
offset = 0  # used to map what's seen on the screen to the full array
debug = 0  # set to 1 to enable diagnostics
currMaxRows = 0  # handle screen resizes
tddir = '.'  # directory containing todo.txt


def init_colors():
    # 0 defaults to white (foreground), black

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)


def colorize(outstr, attr):
    if outstr.startswith('(A)'):
        attr |= curses.color_pair(1)
        attr |= curses.A_BOLD
    if outstr.startswith('(B)'):
        attr |= curses.color_pair(2)
    if outstr.startswith('(C)'):
        attr |= curses.color_pair(3)
    if outstr.startswith('(D)'):
        attr |= curses.color_pair(4)
    if outstr.startswith('(E)'):
        attr |= curses.color_pair(5)
    return attr


def draw_row(scr, row, outstr, attr):
    attr = colorize(outstr, attr)
    if debug == 1:
        outstr += ' cr = ' + str(currow) + ' offset = ' + str(offset)
        outstr = 'R: ' + str(row) + ' of ' + str(scr.getmaxyx()[0]) \
                 + ' ' + outstr
    outstr = outstr.ljust(scr.getmaxyx()[1] - 1)
    # noinspection PyBroadException
    try:
        scr.addstr(row, 0, outstr, attr)
    except:
        err_str = '\nError attempting to print ' + outstr
        err_str += '\nrow: ' + str(row)
        err_str += '\ncurrow: ' + str(currow)
        err_str += '\noffset: ' + str(offset)
        err_str += traceback.format_exc()
        print(err_str)


def repaint(scr):
    (maxy, maxx) = scr.getmaxyx()
    scr.erase()
    for row in range(0, maxy - 3):  # status bar height 3
        if row >= len(todoarr):
            break
        draw_row(scr, row, todoarr[row + offset], curses.A_NORMAL)
    scr.addch(maxy - 3, 0, curses.ACS_ULCORNER)
    for col in range(1, maxx - 2):
        scr.addch(maxy - 3, col, curses.ACS_HLINE)
    scr.addch(maxy - 3, maxx - 2, curses.ACS_URCORNER)
    scr.addch(maxy - 2, 0, curses.ACS_VLINE)
    scr.addch(maxy - 2, maxx - 2, curses.ACS_VLINE)
    scr.addch(maxy - 1, 0, curses.ACS_LLCORNER)
    for col in range(1, maxx - 2):
        scr.addch(maxy - 1, col, curses.ACS_HLINE)

    # scr.addch(maxy-1,maxx-1,curses.ACS_LRCORNER)

    scr.addch(maxy - 1, maxx - 2, curses.ACS_LRCORNER)
    status_str = 'Commands: q: quit, r: reload(lose changes), a-e: set priority, s:sort,' + \
                 ' w: write, i: insert, x: complete, h:@home'

    # centered? scr.addstr(maxy-2, (maxx/2) - (len(status_str)/2), status_str)

    scr.addstr(maxy - 2, 2, status_str)
    draw_row(scr, currow, todoarr[currow + offset],
             curses.A_REVERSE)
    scr.refresh()


def loadfile():
    global tddir
    global todoarr
    try:
        tddir = os.environ['TODO_DIR']
    except KeyError:
        tddir = os.getcwd()

    try:
        getlines = open(os.path.join(tddir, 'todo.txt')).readlines()
        todoarr = [line.strip() for line in getlines]
    except IOError:
        error_exit("Error: couldn't find todo.txt at " + tddir
                   + ' please run from todo directory, or set env var TODO_DIR'
                   )


def writefile():
    try:
        shutil.copy(os.path.join(tddir, 'todo.txt'),
                    os.path.join(tddir, 'todo.txt.bak'))
    except IOError:
        error_exit("Error couldn't backup todo.txt to todo.txt.bak in "
                   + tddir)
    try:
        f = open(os.path.join(tddir, 'todo.txt'), 'w')
        f.write('\n'.join(todoarr))
        f.write('\n')
    except IOError:
        curses.endwin()
        traceback.print_exc()
        error_exit("Error: couldn't find todo.txt at " + tddir
                   + ' please run from todo directory, or set env var TODO_DIR'
                   )


def error_exit(msg):
    curses.endwin()
    print(msg)
    exit()


def has_pri():
    return todoarr[currow + offset].startswith('(')


def has_date():
    date_pat = re.compile(r'\d{4}-\d{2}-\d{2}.*')
    if has_pri:
        temp_line = todoarr[currow + offset]
        temp_line = temp_line[4:]
        return date_pat.match(temp_line) is not None
    return date_pat.match(todoarr[currow + offset]) is not None


def change_context(context_str):
    global todoarr
    if has_date():
        pass


def change_pri(ch):
    global todoarr
    if has_pri():
        todoarr[currow + offset] = (todoarr[currow + offset])[4:]
    # chop off old priority
    todoarr[currow + offset] = '(' + chr(ch).upper() + ') ' \
                               + todoarr[currow + offset]


def delete_task():
    global todoarr
    if todoarr[currow + offset].startswith('('):
        todoarr[currow + offset] = (todoarr[currow + offset])[4:]
    todoarr[currow + offset] = 'x ' + curr_date_str() + " " + todoarr[currow + offset]


def curr_date_str():
    d = datetime.date.today()
    return d.isoformat()


def inserttask(scr):
    global todoarr
    edit_win = scr.derwin(5, 70, 10, 10)
    edit_win.erase()
    edit_win.addstr('Enter new task: ')
    curses.curs_set(1)
    curses.echo()
    edit_win.insstr(1, 2, curr_date_str())
    edit_win.box()
    answer = curr_date_str() + ' ' + edit_win.getstr(1, 13)
    curses.curs_set(0)
    todoarr.insert(currow, answer)
    repaint(scr)


def msgloop(scr):
    global currow
    global offset
    global currMaxRows
    # curses.curs_set(0)  # turn off the cursor
    while True:
        ch = scr.getch()
        currMaxRows = scr.getmaxyx()[0]
        if ch >= ord('a'):
            if ch <= ord('e'):
                change_pri(ch)
        if ch == ord('s'):
            todoarr.sort()
        if ch == ord('r'):
            loadfile()
        if ch == curses.KEY_UP:
            if currow == 0:
                if offset > 0:
                    offset -= 1
            elif currow > 0:
                if offset > 0:
                    currow -= 1
                else:
                    draw_row(scr, currow, todoarr[currow],
                             curses.A_NORMAL)
                    currow -= 1
                    draw_row(scr, currow, todoarr[currow],
                             curses.A_REVERSE)
        if ch == curses.KEY_DOWN:
            if currow < len(todoarr) - 1:
                if currow == currMaxRows - 4:
                    if offset < len(todoarr) - currMaxRows:
                        offset += 1
                else:
                    draw_row(scr, currow, todoarr[currow + offset],
                             curses.A_NORMAL)
                    currow += 1
                    draw_row(scr, currow, todoarr[currow + offset],
                             curses.A_REVERSE)
        if ch == ord('l'):
            loadfile()
        if ch == ord('w'):
            writefile()
        if ch == ord('i'):
            inserttask(scr)
        if ch == ord('x'):
            delete_task()
        if ch == ord('H'):
            change_context("@home")
        if ch == ord('q'):
            break
        repaint(scr)


def main(scr):
    global currMaxRows
    curses.start_color()
    init_colors()
    loadfile()
    currMaxRows = scr.getmaxyx()[0]
    repaint(scr)
    msgloop(scr)
    curses.endwin()


# noinspection PyCallingNonCallable
curses.wrapper(main)
