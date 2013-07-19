#!python
'''
Created on Oct 7, 2012

@author: Matt Stave
'''

import Tkinter as tk
import tkFont
import ttk
import todo_file
from todo_item import TodoItem


class TDTk(object):
    '''
   GUI for TodoFile
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.root = tk.Tk()
        self.status_strvar = ttk.Tkinter.StringVar()
        self.status_bar = None
        self.help_bar = None
        self.tabs = None

	#mapping of which tab (frame) maps to which todo_file
	self.tab_file = {}

        # window for inserting new tasks
        self.add_win = None

        # todo file contents
        self.td_file = None
	self.td_file1 = None
	self.td_file2 = None

        # used for creating new tasks
        self.new_task = tk.StringVar()
        self.new_context = tk.StringVar()
        self.new_priority = tk.StringVar()
        self.new_date = tk.StringVar()

        # for restoring active tab after a reload
        self.active_tab_idx = 0

        self.pri_map = {"A": "Do TODAY (A)", "B": "Next (B)", "C": "Soon (C)",
                        "D": "Someday (D)", None: "NEEDS PRIORITY"}
        self.load()

    def load(self):
        self.td_file = None
	self.td_file1 = todo_file.TodoFile()
	self.td_file2 = todo_file.TodoFile("c:\\dropbox\\todo\\todo.txt")

    def reload(self, event):
        self.load()
        self.reset_ui()

    def active_td_file(self):
	return self.tab_file[str(self.tabs.select())]

    def save(self):
        self.set_status("Adding new item: ")
        new_item = TodoItem()
        new_item.priority = self.new_priority.get()
        if new_item.priority == "":
            new_item.priority = None
        new_item.context = self.new_context.get()
        if new_item.context == "" or new_item.context == "None":
            new_item.context = None
        new_item.task = self.new_task.get()
        new_item.creation_date = self.new_date.get()
        if new_item.creation_date == "":
            new_item.creation_date = None
        self.set_status("Adding new item: " + str(new_item))
        self.active_td_file().append(new_item)
        self.set_status(
            "Adding new item: " + str(new_item) + " ... save complete")
        self.reset_ui()

    def add_attr(self, win, display_str, store_var, g_row):
        tk.Label(win, text=display_str).grid(row=g_row, column=1)
        ent = tk.Entry(win, width=80, textvariable=store_var)
        ent.grid(row=g_row, column=2, columnspan=2)
        return ent

    def add_task(self, event):
        self.add_win = tk.Toplevel(takefocus=True)
        self.add_win.title = "Add a new to do"
        self.add_attr(self.add_win, "Task: ", self.new_task, 1).focus()
        self.add_attr(self.add_win, "Pri: ", self.new_priority, 2)
        self.add_attr(self.add_win, "Context: ", self.new_context, 3)
        self.add_attr(self.add_win, "Creation Date: ", self.new_date, 4)
        button_frame = tk.Frame(self.add_win)
        button_frame.grid(row=5, columnspan=2, column=2)
        tk.Button(button_frame, text="Close", command=lambda:
                  self.add_win.destroy()).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Add this task",
                  command=lambda: self.save()).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Add and close",
                  command=lambda: self.commit_close()).pack(side=tk.LEFT)
        self.new_date.set(TodoItem.curr_date_str())
        self.add_win.focus_set()
        self.add_win.bind("<Return>", lambda event: self.commit_close())
        self.add_win.bind("<Escape>", lambda event: self.add_win.destroy())

    def commit_close(self):
        self.save()
        self.add_win.destroy()

    # methods for determining which items to display
    def includeAll(self, arg):
        return True

    def excludeDone(self, arg):
        return not arg.done

    def list_ui(self, td_file, root_frame=None, include_func=None):
        '''
        add lists for each priority to root_frame
        include_func is called on each item to determine if it should be shown
        '''
        if include_func is None:
            include_func = self.includeAll
        if root_frame is None:
            root_frame = self.frame
        # add panes
        # container for 2 sub-containers (high and low priority)
        lbox_panes = tk.PanedWindow(root_frame, orient=tk.VERTICAL, height=800)
        lbox_panes.pack(fill=tk.BOTH, expand=1)

        high_pri_pane = tk.PanedWindow(lbox_panes, orient=tk.HORIZONTAL, sashwidth=10)
        high_pri_pane.pack(fill=tk.BOTH, expand=1)
        lbox_panes.add(high_pri_pane)
        low_pri_pane = tk.PanedWindow(lbox_panes, orient=tk.HORIZONTAL)
        low_pri_pane.pack(fill=tk.BOTH, expand=1)
        lbox_panes.add(low_pri_pane)

        pri_lists = {}
        # Pri A listbox
        aLabelFont = tkFont.Font(weight='bold')
        pri_lists["A"] = tk.LabelFrame(
            high_pri_pane, text=self.pri_map["A"], font=aLabelFont)
        pri_lists["A"].pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.add_listbox(
            pri_lists["A"], "A", tkFont.Font(size=11), include_func, td_file)
        high_pri_pane.add(pri_lists["A"], stretch="always")

        # Pri <None> listbox
        pri_lists["B"] = tk.LabelFrame(
            high_pri_pane, text=self.pri_map["B"], font=aLabelFont)
        pri_lists["B"].pack(fill=tk.BOTH, expand=1)
        self.add_listbox(
            pri_lists["B"], "B", tkFont.Font(size=9), include_func, td_file)
        high_pri_pane.add(pri_lists["B"], stretch="always")
        for pri in ["C", "D", None]:
        # for pri in self.active_td_file().get_priorities():
            pri_lists[pri] = tk.LabelFrame(low_pri_pane,
                                           text=self.pri_map[pri])
            pri_lists[pri].pack(fill=tk.BOTH, expand=1)
            self.add_listbox(
                pri_lists[pri], pri, tkFont.Font(size=9), include_func, td_file)
            low_pri_pane.add(pri_lists[pri], stretch="always")

    def add_listbox(self, parent, priority, thefont, include_func, td_file):
        vscroll = tk.Scrollbar(parent, orient=tk.VERTICAL)
        hscroll = tk.Scrollbar(parent, orient=tk.HORIZONTAL)
        lbox = tk.Listbox(parent,
                          width=0,  # size of largest item
                          font=thefont,
                          xscrollcommand=hscroll.set,
                          yscrollcommand=vscroll.set)

        vscroll.config(command=lbox.yview)
        vscroll.pack(side=tk.RIGHT, fill=tk.Y)
        hscroll.config(command=lbox.xview)
        hscroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.populate_listbox(lbox, priority, include_func, td_file)
        lbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.bind_list_commands(lbox)

        return lbox

    def populate_listbox(self, lbox, priority, include_func, td_file):
        trow = 0
        for row_itr in td_file.todo_item_arr:
            if row_itr.priority == priority:
                if include_func(row_itr):
                    lbox.insert(trow, row_itr)
                    trow += 1
        lbox.master["text"] = "[" + str(trow) + "] " + lbox.master["text"]

    def set_status(self, status_str):
        self.status_strvar.set(status_str)

    def list_selected(self, event):
        # ignore clicks on empty listboxes
        if event.widget.curselection() != ():
            self.set_status(self.active_td_file().todo_item_arr[self.active_td_file().todo_txt_arr.index(event.widget.get(event.widget.curselection()[0]))])

    def set_priority(self, event):
        pri = event.char
        if pri == "n":
            pri = None
        self.active_td_file().todo_item_arr[self.get_td_array_index(
            self.get_selected_text(event))].priority = pri
        self.active_td_file().update_todo_txt_arr()
        self.reset_ui()

    def modify_task(self, event):
        temp_td = self.get_selected_td(event)
        self.set_status("Deleting " + self.get_selected_text(event))
        self.delete_task(event)
        self.new_context.set(temp_td.context)
        if self.new_context.get() == "None":
            self.new_context.set("")
        self.new_task.set(temp_td.task)
        if temp_td.priority is not None:
            self.new_priority.set(temp_td.priority)
        self.set_status("adding new task")
        self.add_task(None)

    def toggle_complete(self, event):
        cur_done = self.get_selected_td(event).done
        self.active_td_file().todo_item_arr[self.get_td_array_index(
            self.get_selected_text(event))].done = not cur_done
        self.active_td_file().update_todo_txt_arr()
        self.reset_ui()

    def delete_task(self, event):
        self.active_td_file.delete_task(
            self.get_td_array_index(self.get_selected_text(event)))
        self.reset_ui()

    def get_selected_text(self, event):
        return event.widget.get(event.widget.curselection()[0])

    def get_selected_td(self, event):
        return self.active_td_file().todo_item_arr[self.get_td_array_index(self.get_selected_text(event))]

    def get_td_array_index(self, idx_str):
        return self.active_td_file().todo_txt_arr.index(idx_str)

    def save_active_tab(self):
        self.active_tab_idx = self.tabs.index(self.tabs.select())

    def restore_active_tab(self):
        self.tabs.select(self.active_tab_idx)
        self.tabs.focus_set()

    def reset_ui(self):
        self.save_active_tab()
        self.tabs.destroy()
        self.add_all_tabs()
        self.restore_active_tab()

    def write_file(self, event):
        self.td_file1.write_file()
	self.td_file2.write_file()
        self.set_status(self.td_file1.todo_file_name + " and " + self.td_file2.todo_file_name + " have been saved")

    def debug2(self, event):	
	self.set_status("Tab info: " + str(self.tabs.select()) + " " + str(self.tabs.index(self.tabs.select())))

    def bind_list_commands(self, lbox):
        lbox.bind("<<ListboxSelect>>", self.list_selected)
        lbox.bind("<Delete>", self.delete_task)
        lbox.bind("a", self.set_priority)
        lbox.bind("b", self.set_priority)
        lbox.bind("c", self.set_priority)
        lbox.bind("d", self.set_priority)
        lbox.bind("e", self.set_priority)
        lbox.bind("n", self.set_priority)
        lbox.bind("x", self.toggle_complete)
        lbox.bind("i", self.add_task)
        lbox.bind("m", self.modify_task)
        self.global_binds(lbox)

    def global_binds(self, widget):
	widget.bind("X", self.debug2)
        widget.bind("w", self.write_file)
        widget.bind("s", self.write_file)
        widget.bind("i", self.add_task)
        widget.bind("r", self.reload)
        widget.bind("q", lambda event: self.root.destroy())

    def command_help(self):
        return "[a-e (or n for none)]: set priority\
            \t x: toggle complete\
            \t i: insert new task\
            \t s or w:save\
            \t <Delete>: delete task\
            \t m: modify task\
            \t r: reload file\
            \t q: quit"

    def add_tab(self, root, func, label_text, td_file):
        new_frame = ttk.Frame(root)
	self.tab_file[str(new_frame)] = td_file
        self.list_ui(td_file,new_frame, func)
        new_frame.pack(fill=tk.BOTH, expand=1)
        root.add(new_frame, text=label_text)
	return new_frame

    def add_all_tabs(self):
        self.tabs = ttk.Notebook(self.frame)
        self.add_tab(self.tabs, lambda arg: (
            not arg.done), "Open: Work", self.td_file1)
        self.add_tab(self.tabs, lambda arg: (
            arg.done ), "Complete: Work", self.td_file1)
        self.add_tab(
            #self.tabs, lambda arg: arg.context != "home", "All: Work")
            self.tabs, lambda arg: True, "All: Work", self.td_file1)
        self.add_tab(self.tabs, lambda arg: (
            not arg.done), "Open: Dropbox", self.td_file2)
        self.add_tab(self.tabs, lambda arg: (
            arg.done ), "Complete: Dropbox", self.td_file2)
        self.add_tab(
            self.tabs, lambda arg: True, "All: Home", self.td_file2)
        self.tabs.pack(fill=tk.BOTH, expand=1)
        self.global_binds(self.tabs)

    def run(self):
        '''
        kick off everything
        '''
        self.frame = tk.Frame(self.root)
        self.global_binds(self.frame)
        self.frame.pack(fill=tk.BOTH, expand=1)
        self.add_all_tabs()
        self.help_bar = tk.Label(self.frame, text=self.command_help())
        self.help_bar.pack(side=tk.BOTTOM, fill=tk.X)
        if self.status_bar is None:
            self.status_bar = tk.Label(self.frame, anchor=tk.W, justify="left",
                                       textvar=self.status_strvar)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.frame.master.title("To do GUI")
        self.restore_active_tab()
        self.root.mainloop()

if __name__ == "__main__":
    app = TDTk()
    app.run()
