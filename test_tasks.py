import os
import tempfile
import unittest

import tasks


class TaskTests(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.remove(self.path)
        os.environ["TASKS_FILE"] = self.path

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_add_and_ids(self):
        self.assertEqual(tasks.add("a")["id"], 1)
        self.assertEqual(tasks.add("b")["id"], 2)

    def test_done(self):
        tasks.add("a")
        self.assertTrue(tasks.mark_done(1))
        self.assertTrue(tasks.load()[0]["done"])
        self.assertFalse(tasks.mark_done(99))

    def test_delete(self):
        tasks.add("a")
        self.assertTrue(tasks.delete(1))
        self.assertEqual(tasks.load(), [])
        self.assertFalse(tasks.delete(1))


if __name__ == "__main__":
    unittest.main()
