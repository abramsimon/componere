# Copyright 2o18 Premise Data
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from unittest import TestCase
from componere.load_input import load_objects


class LoadInputTest(TestCase):
    def setUp(self):
        self.areas = {}
        self.components = {}
        self.levels = {}
        self.teams = {}
        self.types = {}

    def test_single_file_load(self):
        path = "./tests/test_file1.comp"
        load_objects(path, self.areas, self.components, self.levels, self.teams, self.types)
        self.assertEqual(len(self.areas), 3)
        self.assertEqual(len(self.components), 1)
        self.assertEqual(len(self.levels), 2)
        self.assertEqual(len(self.teams), 1)
        self.assertEqual(len(self.types), 1)

    def test_directory_load(self):
        path = "./tests"
        load_objects(path, self.areas, self.components, self.levels, self.teams, self.types)
        self.assertEqual(len(self.areas), 10)
        self.assertEqual(len(self.components), 7)
        self.assertEqual(len(self.levels), 4)
        self.assertEqual(len(self.teams), 4)
        self.assertEqual(len(self.types), 4)

    def test_nested_directory_load(self):
        path = "./tests/nested_folder"
        load_objects(path, self.areas, self.components, self.levels, self.teams, self.types)
        self.assertEqual(len(self.areas), 0)
        self.assertEqual(len(self.components), 0)
        self.assertEqual(len(self.levels), 0)
        self.assertEqual(len(self.teams), 2)
        self.assertEqual(len(self.types), 0)
