'''
Created on Dec 17, 2012

@author: mstave
'''
import unittest
from todo_item import TodoItem


class TestToDoItem(unittest.TestCase):  # pylint: disable-msg=R0904
    def test_parse_pri(self):
        test_str = "(B) 2012-08-27 @home Xbox repair"
        test_item = TodoItem(test_str)
        self.assertIsNotNone(test_item.priority)
        self.assertEqual(test_item.priority, "B")

    def test_parse_date(self):
        test_str = "(B) 2012-08-27 @home Xbox repair"
        test_item = TodoItem(test_str)
        self.assertIsNotNone(test_item.creation_date)
        self.assertEqual(test_item.creation_date, '2012-08-27')

    def test_parse_context(self):
        test_str = "(B) 2012-08-27 @home Xbox repair"
        test_item = TodoItem(test_str)
        self.assertIsNotNone(test_item.context)
        self.assertEqual(test_item.context, "home")

    def test_parse_no_pri(self):
        test_str = "2012-08-27 @home Xbox repair"
        test_item = TodoItem(test_str)
        self.assertIsNone(test_item.priority)
        self.assertEqual(test_item.creation_date, '2012-08-27')

    def test_parse_no_date(self):
        test_str = "@home Xbox repair"
        test_item = TodoItem(test_str)
        self.assertIsNone(test_item.creation_date)
        self.assertIsNotNone(test_item.context)
        self.assertEqual(test_item.context, "home")

    def test_parse_task_with_context(self):
        test_str = "@foo task"
        test_item = TodoItem(test_str)
        self.assertEqual("task", test_item.task)

    def test_parse_with_context_and_pri(self):
        test_str = "(B) @foo task"
        test_item = TodoItem(test_str)
        self.assertEqual("task", test_item.task)

    def test_parse_no_task(self):
        test_str = "(B) 2012-08-27"
        test_item = TodoItem(test_str)
        self.assertIsNone(test_item.task)

    def test_parse_no_context(self):
        test_str = "Xbox repair"
        test_item = TodoItem(test_str)
        self.assertIsNone(test_item.priority)
        self.assertIsNotNone(test_item.task)
        self.assertEqual(test_item.task, test_str)

    def test_set_context_existing(self):
        test_str = "(B) 2012-08-27 Xbox repair @home"
        test_item = TodoItem(test_str)
        self.assertIsNotNone(test_item.context)
        self.assertEqual(test_item.context, "home")
        test_item.context = "work"
        self.assertIsNotNone(test_item.context)
        self.assertEqual("work", test_item.context)
        self.assertEqual(test_str.replace("home", "work"),
                         test_item.todo_txt_line)

    def test_del_priority(self):
        test_str = "(B) 2012-08-27 @home Xbox repair"
        test_item = TodoItem(test_str)
        test_item.priority = None
        self.assertIsNone(test_item.priority)
        self.assertEqual("2012-08-27 Xbox repair @home",
                         test_item.todo_txt_line)

    def test_done(self):
        test_str = "(B) 2012-08-27 Xbox repair @home"
        done_str = "x 2012-09-23 2012-02-12 XBox repair @home"
        done_item = TodoItem(done_str)
        not_done_item = TodoItem(test_str)
        self.assertFalse(not_done_item.done)
        self.assertTrue(done_item.done)
        self.assertEqual("home", done_item.context)
        self.assertEqual("2012-02-12", done_item.creation_date) 
        self.assertEqual(str(done_item), done_str)
        print done_str, str(done_item)
        
    def test_done_2(self):
        test_str = "x 2012-09-27 approve 8194"
        test_item = TodoItem(test_str)
        self.assertEqual("approve 8194", test_item.task)
        
    def test_mark_done(self):
        test_str = "(B) 2012-08-27 @home Xbox repair"
        done_item = TodoItem("x " + TodoItem.curr_date_str() +
                            " 2012-08-27 @home Xbox repair")
        test_item = TodoItem(test_str)
        test_item.done = True
        test_item.priority = None
        self.assertEqual(test_item.__dict__, done_item.__dict__)

    def test_set_context_from_scratch(self):
        test_str = "(B) 2012-08-27 Xbox repair"
        test_item = TodoItem(test_str)
        self.assertIsNone(test_item.context)
        test_item.context = "work"
        self.assertIsNotNone(test_item.context)
        self.assertEqual("work", test_item.context)
        self.assertEqual("Xbox repair", test_item.task)
        self.assertEqual("(B) 2012-08-27 Xbox repair @work",
                         test_item.todo_txt_line)

    def test_set_task_existing(self):
        test_str = "(B) 2012-08-27 Xbox repair"
        test_item = TodoItem(test_str)
        self.assertIsNotNone(test_item.task)
        test_item.task = "ps3 polish"
        self.assertEqual("ps3 polish", test_item.task)
        self.assertEqual("(B) 2012-08-27 ps3 polish", test_item.todo_txt_line)

    def test_set_date_from_scratch(self):
        test_str = "(B) @home Xbox repair"
        test_item = TodoItem(test_str)
        self.assertIsNone(test_item.creation_date)
        test_item.creation_date = "2012-01-04"
        self.assertIsNotNone(test_item.creation_date)
        self.assertEquals("2012-01-04", test_item.creation_date)
        self.assertEquals("(B) 2012-01-04 Xbox repair @home",
                          test_item.todo_txt_line)

    def test_set_date_existing_date(self):
        test_str = "(B) 2012-02-05 @home Xbox repair"
        test_item = TodoItem(test_str)
        self.assertIsNotNone(test_item.creation_date)
        test_item.creation_date = "2012-01-04"
        self.assertIsNotNone(test_item.creation_date)
        self.assertEquals("(B) 2012-01-04 Xbox repair @home",
            test_item.todo_txt_line)

    def test_set_task_from_scratch(self):
        test_str = "(B) 2012-08-27"
        test_item = TodoItem(test_str)
        self.assertIsNone(test_item.task)
        test_item.task = "foo bar"
        self.assertIsNotNone(test_item.task)
        self.assertEquals("foo bar", test_item.task)
        self.assertEquals(test_str + " " + "foo bar", test_item.todo_txt_line)

        test_str = "(B)"
        test_item = TodoItem(test_str)
        test_item.task = "foo bar"
        self.assertIsNotNone(test_item.task)
        self.assertEquals("foo bar", test_item.task)
        self.assertEquals(test_str + " " + "foo bar", test_item.todo_txt_line)

    def test_set_priority_from_scratch(self):
        test_str = "2012-09-15 bar baz @home"
        test_item = TodoItem(test_str)
        self.assertIsNone(test_item.priority)
        test_item.priority = "D"
        self.assertIsNotNone(test_item.priority)
        self.assertEquals("(D) " + test_str, test_item.todo_txt_line)

    def test_set_priority_exists(self):
        test_str = "(A) 2012-09-15 bar baz @home"
        test_item = TodoItem(test_str)
        self.assertIsNotNone(test_item.priority)
        test_item.priority = "D"
        self.assertIsNotNone(test_item.priority)
        self.assertEquals("D", test_item.priority)
        self.assertEquals("(D) 2012-09-15 bar baz @home",
                          test_item.todo_txt_line)

if __name__ == "__main__":
    print "This module is not generally intended to run stand-alone"
    print "Running unit tests."
    unittest.main()
