#!/usr/bin/python
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
import sys

todoarr = []  # array to hold contents of todo list, initially from todo.txt
currow = 0  # current selected row
offset = 0  # used to map what's seen on the screen to the full array
debug = 0  # set to 1 to enable diagnostics
currMaxRows = 0  # handle screen resizes
tddir = '.'  # directory containing todo.txt


def initColors():

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


def drawRow(scr, row, outstr, attr):
    attr = colorize(outstr, attr)
    if debug == 1:
        outstr += ' cr = ' + str(currow) + ' offset = ' + str(offset)
        outstr = 'R: ' + str(row) + ' of ' + str(scr.getmaxyx()[0]) \
            + ' ' + outstr
    outstr = outstr.ljust(scr.getmaxyx()[1] - 1)
    #noinspection PyBroadException
    try:
        scr.addstr(row, 0, outstr, attr)
    except:
        errStr = '\nError attempting to print ' + outstr
        errStr += '\nrow: ' + str(row)
        errStr += '\ncurrow: ' + str(currow)
        errStr += '\noffset: ' + str(offset) 
        errStr += traceback.format_exc()
        print errStr


def repaint(scr):
    (maxy, maxx) = scr.getmaxyx()
    scr.erase()
    for row in xrange(0, maxy - 3):  # status bar height 3
        if row >= len(todoarr):
            break
        drawRow(scr, row, todoarr[row + offset], curses.A_NORMAL)
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
    statusStr = 'Commands: q: quit, r: reload(lose changes), a-e: set priority, s:sort,' + \
            ' w: write, i: insert, x: complete, h:@home'

    # centered? scr.addstr(maxy-2, (maxx/2) - (len(statusStr)/2), statusStr)

    scr.addstr(maxy - 2, 2, statusStr)
    drawRow(scr, currow, todoarr[currow + offset],
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
        errorExit("Error: couldn't find todo.txt at " + tddir
                  + ' please run from todo directory, or set env var TODO_DIR'
                  )

def writefile():
    try:
        shutil.copy(os.path.join(tddir, 'todo.txt'),
                    os.path.join(tddir, 'todo.txt.bak'))
    except IOError:
        errorExit("Error couldn't backup todo.txt to todo.txt.bak in "
                  + tddir)
    try:
        f = open(os.path.join(tddir, 'todo.txt'), 'w')
        f.write('\n'.join(todoarr))
        f.write('\n')
    except IOError:
        curses.endwin()
        traceback.print_exc()
        errorExit("Error: couldn't find todo.txt at " + tddir
                  + ' please run from todo directory, or set env var TODO_DIR'
                  )


def errorExit(msg):
    curses.endwin()
    print msg
    exit()

def hasPri():
    return todoarr[currow + offset].startswith('(')

def hasDate():
    datePat = re.compile(r'\d{4}-\d{2}-\d{2}.*')
    if hasPri:
        tempLine = todoarr[currow + offset]
        tempLine = tempLine[4:]
        return datePat.match( tempLine) is not None
    return datePat.match(todoarr[currow + offset]) is not None

def changeContext(contextStr):
    global todoarr
    if hasDate():
        pass

def changePri(ch):
    global todoarr
    if hasPri():
        todoarr[currow + offset] = (todoarr[currow + offset])[4:]
    # chop off old priority
    todoarr[currow + offset] = '(' + chr(ch).upper() + ') ' \
        + todoarr[currow + offset]

def deleteTask():
    global todoarr
    if todoarr[currow + offset].startswith('('):
        todoarr[currow + offset] = (todoarr[currow + offset])[4:]
    todoarr[currow + offset] = 'x ' + currDateStr() + " " + todoarr[currow + offset]


def currDateStr():
    d = datetime.date.today()
    return d.isoformat()

def inserttask(scr):
    global todoarr
    editWin = scr.derwin(5, 70, 10, 10)
    editWin.erase()
    editWin.addstr('Enter new task: ')
    curses.curs_set(1)
    curses.echo()
    editWin.insstr( 1, 2, currDateStr())
    editWin.box()
    answer = currDateStr() + ' ' + editWin.getstr(1, 13)
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
                changePri(ch)
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
                    drawRow(scr, currow, todoarr[currow],
                            curses.A_NORMAL)
                    currow -= 1
                    drawRow(scr, currow, todoarr[currow],
                            curses.A_REVERSE)
        if ch == curses.KEY_DOWN:
            if currow < len(todoarr) - 1:
                if currow == currMaxRows - 4:
                    if offset < len(todoarr) - currMaxRows:
                        offset += 1
                else:
                    drawRow(scr, currow, todoarr[currow + offset],
                            curses.A_NORMAL)
                    currow += 1
                    drawRow(scr, currow, todoarr[currow + offset],
                            curses.A_REVERSE)
        if ch == ord('l'):
            loadfile()
        if ch == ord('w'):
            writefile()
        if ch == ord('i'):
            inserttask(scr)
        if ch == ord('x'):
            deleteTask()
        if ch == ord('H'):
            changeContext("@home")
        if ch == ord('q'):
            break
        repaint(scr)


def main(scr):
    global currMaxRows
    curses.start_color()
    initColors()
    loadfile()
    currMaxRows = scr.getmaxyx()[0]
    repaint(scr)
    msgloop(scr)
    curses.endwin()

#noinspection PyCallingNonCallable
curses.wrapper(main)
