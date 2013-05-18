'''
Created on Oct 7, 2012

@author: mstave
'''

import Tkinter as tk
import tkFont
import ttk
import todo_file

class TDTk(object):
    '''
   GUI for TodoFile
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.ttree = None
        self.td_file = todo_file.TodoFile()
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root, width=1400)
        self.panes = None
        self.pri_open = {}
        self.status_strvar = ttk.Tkinter.StringVar()
        self.tdlabelframe = None
        self.bottom = None
        self.active_tab = None
        self.complete_tab = None
        self.all_tab = None
        self.tabs = None
        self.lbox = None
        self.low_pri_pane = None        # Paned window containing lists of each priority task
        self.high_pri_pane = None        # Paned window containing lists of each priority task
        self.pri_lists = {}                 # Hash of each list

        for pri in self.td_file.get_priorities():
            self.pri_open[pri] = True
        self.pri_open["<none>"] = False

    def list_ui(self):
        '''
        List all todos in a GUI
        '''
        # add panes
        pri_map = { "A" : "Do TODAY (A)", "B" : "Next (B)", "C" : "Soon (C)", "D" : "Someday (D)", None : "NEEDS PRIORITY" }
        self.frame.master.title("To do")
        self.frame.pack(fill=tk.BOTH, expand=1)
        all_pri = tk.PanedWindow(self.frame, orient=tk.VERTICAL, height=800, width=1424)
        all_pri.pack( fill=tk.BOTH, expand=1)        self.high_pri_pane = tk.PanedWindow(all_pri, orient=tk.HORIZONTAL)
        self.high_pri_pane.pack( fill=tk.BOTH, expand=1)        self.low_pri_pane = tk.PanedWindow(all_pri, orient=tk.HORIZONTAL)
        self.low_pri_pane.pack( expand=1)
        aLabelFont= tkFont.Font(weight='bold')
        self.pri_lists["A"] = tk.LabelFrame(self.high_pri_pane,  text=pri_map["A"], font=aLabelFont)
        self.pri_lists["A"].pack(fill=tk.BOTH, expand=1)
        aFont =tkFont.Font(size=11, weight=tk.NORMAL)
        self.add_listbox(self.pri_lists["A"],"A",aFont)
        self.high_pri_pane.add(self.pri_lists["A"])
        
        self.pri_lists[None] = tk.LabelFrame(self.high_pri_pane, text=pri_map[None], font=aLabelFont)
        self.pri_lists[None].pack( expand=1)
        self.add_listbox(self.pri_lists[None],None,tkFont.Font(size=9))
        self.high_pri_pane.add(self.pri_lists[None])
        for pri in [ "B","C", "D" ]:
        #for pri in self.td_file.get_priorities():
            self.pri_lists[pri] = tk.LabelFrame(self.low_pri_pane, text=pri_map[pri])
            self.pri_lists[pri].pack(fill=tk.BOTH, expand=1)
            self.add_listbox(self.pri_lists[pri], pri, tkFont.Font(size=8))
            self.low_pri_pane.add(self.pri_lists[pri])
        self.bottom = ttk.Label(self.frame, textvariable=self.status_strvar)
        self.bottom.pack()
        all_pri.add(self.high_pri_pane)
        all_pri.add(self.low_pri_pane)
        all_pri.pack(side=tk.TOP, fill=tk.BOTH, expand=1)        #self.panes.insert("end", self.bottom)
    
    def add_listbox(self,parent, priority, thefont):
        vscroll = tk.Scrollbar(parent, orient=tk.VERTICAL)
        hscroll = tk.Scrollbar(parent, orient=tk.HORIZONTAL)
        lbox = tk.Listbox(parent,
                          width=57,
                          font=thefont,
                          xscrollcommand=hscroll.set,
                          yscrollcommand=vscroll.set)

        trow = 0
        for row_itr in self.td_file.todo_item_arr:
            if row_itr.priority == priority:
                lbox.insert(trow, row_itr)
                trow += 1      
        vscroll.config(command=lbox.yview)
        vscroll.pack(side=tk.RIGHT, fill=tk.Y)
        hscroll.config(command=lbox.xview)
        hscroll.pack(side=tk.BOTTOM, fill=tk.X)
        lbox.pack(fill=tk.BOTH, expand=1)
        lbox.bind("q", exit)
        lbox.bind("<<ListboxSelect>>",self.list_selected)
        return lbox
        

    def list_selected(self, event):
        print event.widget.get(event.widget.curselection()[0])
 
    
    def bind_tree_keys(self):
        self.ttree.bind("q", exit)
        self.ttree.bind("s", self.print_selected_td)
        self.ttree.bind("<<TreeviewSelect>>", self.print_selected_td)
        self.ttree.bind("a", self.set_priority)
        self.ttree.bind("b", self.set_priority)
        self.ttree.bind("c", self.set_priority)
        self.ttree.bind("d", self.set_priority)
        self.ttree.bind("e", self.set_priority)
        self.ttree.bind("x", self.toggle_complete)
        self.ttree.bind("<<TreeviewOpen>>", self.handle_open)
        self.ttree.bind("<<TreeviewClose>>", self.handle_close)
        self.ttree.bind("w", self.write_file)

    def update_tree_data(self):
        index = 1
        for tditem in self.td_file.todo_item_arr:
            if (tditem.done is None) or (tditem.done is False):
                done_char = " "
            else:
                done_char = "x"
            if tditem.priority is not None:
                tditem.gui_index = self.ttree.insert(tditem.priority,
                    "end", index, values=(done_char,
                        tditem.priority, (" " if tditem.creation_date is
                            None else tditem.creation_date),
                        tditem.task))
            else:
                tditem.gui_index = self.ttree.insert("<none>", "end",
                    index, values=(done_char, "",
                        (" " if tditem.creation_date is None else
                            tditem.creation_date), tditem.task))
            index += 1

    def tree_td_ui(self):
        '''
        show todos in a tree gui element
        '''
        if self.tabs is None:
            self.tabs = ttk.Notebook(self.frame)
            self.active_tab = ttk.Frame(self.tabs)
            self.complete_tab = ttk.Frame(self.tabs)
            self.all_tab = ttk.Frame(self.tabs)
            self.tabs.add(self.active_tab,text="Active")
            self.tabs.add(self.complete_tab, text="Complete")
            self.tabs.add(self.all_tab, text="All")
            self.tabs.pack()
        if self.panes is None:
            self.panes = ttk.Panedwindow(self.all_tab,
                                         orient=ttk.Tkinter.VERTICAL)
            self.panes.pack(fill=ttk.Tkinter.BOTH, expand=1)
            self.tdlabelframe = ttk.LabelFrame(self.panes)
            self.bottom = ttk.Label(self.panes, textvariable=self.status_strvar)
            self.bottom.pack()
            self.panes.insert("end", self.bottom)

        if self.ttree is None:
            self.ttree = ttk.Treeview(self.tdlabelframe, height=40,
                  columns=("complete", "pri", "date", "task", "context"))
            self.panes.insert(0, self.tdlabelframe)
            self.ttree.column('#0', width=75)
            self.ttree.column('complete', width=45, anchor="center")
            self.ttree.column('pri', width=45, anchor="center")
            self.ttree.column('date', width=90)
            self.ttree.column("task", width=600)
            self.ttree.column("context", width=90)

            self.ttree.heading("complete", text="Done")
            self.ttree.heading("pri", text="Pri")
            self.ttree.heading('date', text="Date")
            self.ttree.heading("task", text="Task")
            self.ttree.heading("context", text="Context")

            self.ttree.insert("", "end", "priority", text="Priority",
                              open=True)
            self.ttree.insert("", "end", "context", text="Context")
            self.ttree.insert("", "end", "complete", text="Complete")

            # populate priorities
            for pri in self.td_file.get_priorities():
                if pri is not None:
                    self.ttree.insert("priority", "end", pri, text=pri,
                               open=self.pri_open[pri])
                else:
                    self.ttree.insert("priority", "end", "<none>",
                               text="<none>", open=self.pri_open["<none>"])
            self.update_tree_data()
            self.ttree.pack()
            self.bind_tree_keys()

    def write_file(self, dummy):
        self.td_file.update_todo_txt_arr()
        self.td_file.write_file()

    def handle_close(self, dummy):
        '''
        TK event handler for collapsing a subsection
        '''
        self.pri_open[self.ttree.focus()] = False

    def handle_open(self, dummy):
        '''
        TK event handler for expanding a subsection
        '''
        # save this state so it can be reconstructed
        self.pri_open[self.ttree.focus()] = True

    def toggle_complete(self, dummy):
        '''
        change completeness state
        '''
        temp_task = self.get_old_task()
        temp_task.done = not temp_task.done
        self.put_updated_task(temp_task)

    def get_old_task(self):
        source_index = int(self.ttree.focus()) - 1
        # the index into the array to tasks
        return self.td_file.delete_task(source_index)

    def put_updated_task(self, updated_task):
        new_selected = self.ttree.next(int(self.ttree.focus()))
        if new_selected == "":
            new_selected = self.ttree.prev(self.ttree.focus())
        self.td_file.append(updated_task)
        self.td_file.todo_item_arr.sort()
        self.ttree.destroy()
        self.ttree = None
        self.tree_td_ui()
        self.frame.pack()

        self.ttree.selection_set(new_selected)
        self.ttree.focus(new_selected)
        self.ttree.focus_force()

    def set_priority(self, pri):
        '''
        change the priority to pri
        find which item to have selected  post-move
        destroy and redraw the tree (which semms instantaneous
        :param pri: event with pri.char = a-e
        '''
        temp_todo = self.get_old_task()
        temp_todo.priority = pri.char.capitalize()
        self.put_updated_task(temp_todo)

    def print_selected_td(self, param):
        '''
        TK event handler to print to stout selected
        task, and it's index
        '''
        if self.get_selected_td(param) is not None:
            self.status_strvar.set("  " + str(self.get_selected_td(param)[0]))

    def get_selected_td(self, param=None):  # pylint: disable-msg=W0613
        '''
           callback method
        :param param:set implicitly in event handler
        '''
        focus_item_index = self.ttree.focus()
        #e.g I00C
        try:
            retIdx = int(focus_item_index) - 1
        except:
            # if it's a heading, not a to do item
            retIdx = None
            return 
        return self.td_file.todo_item_arr[retIdx], retIdx
   
    def run(self):
        '''
        do everything
        '''
        self.list_ui()
        #self.tree_td_ui()
        self.frame.pack()
        self.root.mainloop()

if __name__ == "__main__":
    APP = TDTk()
    APP.run()
