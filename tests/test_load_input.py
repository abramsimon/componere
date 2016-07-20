from unittest import TestCase
from componere.load_input import load_objects

class LoadInputTest(TestCase):
    def setUp(self):
        self.areas = {}
        self.components = {}
        self.levels = {}
        self.teams = {}

    def test_single_file_load(self):
        path = "../componere/tests/test_file1.comp"
        load_objects(path, self.areas, self.components, self.levels, self.teams)
        self.assertEqual(len(self.areas), 3)
        self.assertEqual(len(self.components), 1)
        self.assertEqual(len(self.levels), 2)
        self.assertEqual(len(self.teams), 0)

    def test_directory_load(self):
        path = "../componere/tests"
        load_objects(path, self.areas, self.components, self.levels, self.teams)
        self.assertEqual(len(self.areas), 10)
        self.assertEqual(len(self.components), 7)
        self.assertEqual(len(self.levels), 4)
        self.assertEqual(len(self.teams), 4)

    def test_nested_directory_load(self):
        path = "../componere/tests/nested_folder"
        load_objects(path, self.areas, self.components, self.levels, self.teams)
        self.assertEqual(len(self.areas), 0)
        self.assertEqual(len(self.components), 0)
        self.assertEqual(len(self.levels), 0)
        self.assertEqual(len(self.teams), 2)
