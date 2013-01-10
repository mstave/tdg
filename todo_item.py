'''
Created on Dec 17, 2012

@author: lb
'''

import re
import datetime


class TodoItem(object):  # pylint: disable-msg=R0902
    '''
    Represents just one td item in a portable format
    '''

    def __init__(self, raw_text=None):
        self.creation_date = None
        self.completion_date = None
        self.task = None
        self.project = None
        self._priority = None
        self.context = None
        self.gui_index = None
        self.done = None
        #self.todo_txt_line = raw_text
        if raw_text is not None:
            self.parse_done(raw_text)
            self.parse_creation_date(raw_text)
            self.parse_priority(raw_text)
            self.parse_context(raw_text)
            self.parse_task(raw_text)
            self.parse_project(raw_text)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return self.todo_txt_line
    
    def __len__(self):
        return len(self.todo_txt_line)
    
    def get_todo_dot_txt_line(self):
        ret_str = ""
        if self.done:
            ret_str = "x "
            if self.completion_date is not None:
                ret_str += self.completion_date + " "
        elif self.priority is not None:
            ret_str = "(" + self.priority + ") "
        if self.creation_date is not None:
            ret_str += self.creation_date + " "
        if self.task is not None:
            ret_str += self.task + " "
        if self.context is not None:
            ret_str += "@" + self.context
        ret_str = ret_str.strip()
        if ret_str == "":
            ret_str = None
        return ret_str

    # don't really need a property for this one, but making
    # it consistent with the others
    @property
    def todo_txt_line(self):
        return self.get_todo_dot_txt_line()

    @todo_txt_line.setter
    def todo_txt_line(self, line):
        self.todo_txt_line = line

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, new_pri):
        if new_pri is not None:
            new_pri = new_pri.upper()
        self._priority = new_pri

    @property
    def done(self):
        return self._done

    @done.setter
    def done(self, newdone):
        self._done = newdone
        if newdone:
            self.completion_date = self.curr_date_str()

    def parse_project(self, raw_text):
        project_pattern = re.compile(r'\+(\w+)')
        match = project_pattern.search(raw_text)
        if match is not None:
            self.project = match.group(1)

    def parse_context(self, raw_text):
        context_pattern = re.compile(r'@(\w+)')
        match = context_pattern.search(raw_text)
        if match is not None:
            self.context = match.group(1)

    def parse_done(self, raw_text):
        self.completion_date = None
        if raw_text is not None:
            self.done = raw_text.startswith("x ")
            if self.done:
                date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}).*')
                donematch = date_pattern.match(raw_text[2:])
                if donematch is not None:
                    self.completion_date = donematch.group(1)

    def parse_priority(self, raw_text):
        self.priority = None
        if raw_text[0] == "(" and raw_text[2] == ")":
            self.priority = raw_text[1]
        else:
            if self.done:
                pass
                # may want to investigate supporting this
                # but the file format seems to forid it
                #if raw_text[24] == "(" and raw_text[26] == ")":
                #    self.priority = raw_text[25]

    def parse_creation_date(self, raw_text):
        date_pattern = re.compile(r'(\d{4}\-\d{2}\-\d{2}).*')
        temp_line = raw_text
        self.creation_date = None
        if self.done:
            temp_line = temp_line[13:]
        if self.priority is None:
            self.parse_priority(raw_text)
        if self.priority is not None:
            temp_line = raw_text[4:]
        match = date_pattern.match(temp_line)
        if match is not None:
            self.creation_date = match.group(1)

    def parse_task(self, raw_text):
        self.task = raw_text
        self.parse_context(raw_text)
        self.parse_done(raw_text)

        if self.done:
            self.task = self.task[2:]
        if self.priority is not None:
            self.task = self.task[4:]
        if self.creation_date is not None:
            self.task = self.task[11:]
        if self.completion_date is not None:
            self.task = self.task[10:]
        if self.context is not None:
            self.task = self.task.replace("@" + self.context, "")
        if self.task == "":
            self.task = None
        if self.task is not None:
            self.task = self.task.strip()

    @classmethod
    def curr_date_str(cls):
        '''
        return current date in ISO format
        :param cls: implicit param
        '''
        temp_date = datetime.date.today()
        return temp_date.isoformat()
