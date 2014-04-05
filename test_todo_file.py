'''
Created on Dec 17, 2012

@author: mstave
'''
import os
import unittest
import tempfile
from todo_item import TodoItem
from todo_file import TodoFile


class TestTodoFile(unittest.TestCase):  # pylint: disable-msg=R0904
    '''
        Unit tests for TodoFile
    '''
    test_item = None
    temp_file = None

    def setUp(self):  # pylint: disable-msg=C0103
        '''
        prepare items used by subsequent tests
        :param self: implicit param
        '''
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.write("(B) 2012-08-27 @home +games Xbox repair\n")
        self.temp_file.write("walk the dog\n")
        #temp.close()
        self.temp_file.flush()
        self.temp_file.close()
        self.test_item = TodoFile(self.temp_file.name)

    def test_basics(self):
        self.assertIsNotNone(self.test_item)
        self.assertEqual("B",
            self.test_item.todo_item_arr[0].priority)
        self.assertEqual("home",
            self.test_item.todo_item_arr[0].context)
        self.assertEqual("walk the dog",
            self.test_item.todo_item_arr[1].task)
        self.assertEqual("walk the dog",
            self.test_item.todo_item_arr[1].todo_txt_line)
        self.assertEqual("games",
            self.test_item.todo_item_arr[0].project)

    def test_ls_grep(self):
        self.assertEqual("walk the dog\n", self.test_item.ls_grep("dog"))
        self.assertEqual("walk the dog\n", self.test_item.ls_grep("d[ao]g"))
        self.assertNotEqual("walk the dog\n", self.test_item.ls_grep("cat"))

    def test_ls(self):
        self.assertEqual("walk the dog\n", self.test_item.list_todos("dog"))

    def test_str(self):
        getlines = open(self.temp_file.name).read()
        self.assertEqual(getlines, str(self.test_item))

    def test_eq(self):
        dup_item = TodoFile(self.temp_file.name)
        self.assertEqual(self.test_item, dup_item)

    def test_delete(self):
        new_item = TodoFile(self.temp_file.name)
        new_item.delete_task(0)
        self.assertEqual("walk the dog", new_item.todo_item_arr[0].task)

    def test_create_new(self):
        try:
            temp_file = tempfile.NamedTemporaryFile(mode="w",
                                                   delete=False)
            test_str_1 = "(B) 2012-02-05 Xbox repair @home"
            test_item_1 = TodoItem(test_str_1)
            test_str_2 = "(B) 2012-02-05 Xbox repair @work"
            test_item_2 = TodoItem(test_str_2)
            test_td_file = TodoFile(temp_file.name)
            test_td_file.append(test_item_1)
            test_td_file.write_file()
            test_td_file_2 = TodoFile(temp_file.name)
            self.assertIsNotNone(test_td_file_2)
            self.assertIsNotNone(test_td_file_2.todo_item_arr)
            self.assertEqual(1, len(test_td_file_2.todo_item_arr))
            self.assertEqual("home", test_td_file_2.todo_item_arr[0].context)
            self.assertEqual(test_item_1, test_td_file_2.todo_item_arr[0])
            test_td_file.append(test_item_2)
            test_td_file.write_file()
            test_td_file_3 = TodoFile(temp_file.name)
            self.assertIsNotNone(test_td_file_3)
            self.assertIsNotNone(test_td_file_3.todo_item_arr)
            self.assertEqual(2, len(test_td_file_3.todo_item_arr))
            self.assertEqual(test_item_1, test_td_file_3.todo_item_arr[0])
            self.assertEqual(test_item_2, test_td_file_3.todo_item_arr[1])
            self.assertEqual(test_str_1,
                             test_td_file_3.todo_item_arr[0].todo_txt_line)
            self.assertEqual(test_str_2,
                             test_td_file_3.todo_item_arr[1].todo_txt_line)
        finally:
            temp_file.close()
            os.unlink(temp_file.name)

    def test_nested(self):
        #   this doesn't really test anything yet
        try:
            temp_file = tempfile.NamedTemporaryFile(mode="w",
                                                    delete=False)
            data_to_nest = '''
(B) 2014-03-01 First B task @home
(B) 2014-03-01 Second B task @home
(A) 2014-04-02 Do today @home
(C) 2014-02-04 Third tier @work
'''
            visual = '''
filename
    (A Home)
        Do today
        (B Home)
            First B task
            Second B task
    (A Work)
        (B Work)
            (C Work)
                Third Tier
        '''
            correct = {"name": temp_file.name,
                       "children": [
                           {"name": "(A) @home",
                            "children": [
                                {"name": "Do today", "size": 100},
                                {"name": "(B) @home",
                                    "children": [
                                        {"name": "First B task", "size": 100},
                                        {"name": "Second B task", "size": 100}
                                    ]
                                 }
                            ],
                            },
                           {"name": "(A) @work",
                                    "children": [
                                        {"name": "(B) @work",
                                            "children": [
                                                {"name": "(C) @work",
                                                    "children": [
                                                        {"name": "Third Tier",
                                                            "size": 100}
                                                    ]
                                                 }
                                            ]
                                         }
                                    ]
                            }
                       ]
                       }
            temp_file.write(data_to_nest)
            test_td_file = TodoFile(temp_file.name)
            self.assertIsNotNone(test_td_file)
            self.assertIsNotNone(test_td_file.todo_item_arr)
        finally:
            temp_file.close()

    def tearDown(self):  # pylint: disable-msg=C0103
        '''

        '''
        os.unlink(self.temp_file.name)

if __name__ == "__main__":
    print "This module is not generally intended to run stand-alone"
    print "Running unit tests"
    unittest.main()
