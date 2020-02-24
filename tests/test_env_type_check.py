"""
MIT License

Copyright (c) 2020 Alex Sokolov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import json
import os
import sys
import time
import unittest

from smart_env import ENV
from smart_env.util import is_python2_running


__all__ = ('EnvWithTypeCastTestCase',)


class EnvWithTypeCastTestCase(unittest.TestCase):
    """Test case for ENV with automatic type cast enabled"""

    KEY = "VALUE_WITH_TYPE"

    @classmethod
    def setUpClass(cls):
        super(EnvWithTypeCastTestCase, cls).setUpClass()
        ENV.enable_automatic_type_cast()

    def setup_value(self, value):
        """Set up environment variable with passed value"""
        os.environ[self.KEY] = json.dumps(value) \
            if not isinstance(value, str) else value

    def test_001_retrieve_text_value(self):
        value = "Text"
        self.setup_value(value)
        self.assertEqual(getattr(ENV, self.KEY), value)

    def test_002_retrieve_float_value(self):
        value = 3.14
        self.setup_value(value)
        self.assertEqual(getattr(ENV, self.KEY), value)

    def test_003_retrieve_bool_value(self):
        for value in (True, "true", "True"):
            self.setup_value(value)
            self.assertEqual(getattr(ENV, self.KEY), True)

        for value in (False, "false", "False"):
            self.setup_value(value)
            self.assertEqual(getattr(ENV, self.KEY), False)

    def test_004_retrieve_integer_value(self):
        for value in (0, -1, 100500, "-20", "10"):
            self.setup_value(value)
            self.assertEqual(getattr(ENV, self.KEY), int(value))

    def test_005_retrieve_list(self):
        value = ["Hello", "Smart", "Env", ["with", "nested", "list"]]
        self.setup_value(value)
        self.assertEqual(getattr(ENV, self.KEY), value)

        # additional test for single quotes

        value = "['Hello', ['world']]"
        self.setup_value(value)
        self.assertEqual(getattr(ENV, self.KEY), ['Hello', ['world']])

    def test_006_retrieve_dict_with_double_quotes(self):
        value = {"key": "value",
                 "another_key": ["value", "value2", {"key1": "value1"}]}
        self.setup_value(value)
        self.assertEqual(getattr(ENV, self.KEY), value)

    def test_007_retrieve_tuple(self):
        value = '("1", "2", "3")'
        self.setup_value(value)
        self.assertEqual(getattr(ENV, self.KEY), ("1", "2", "3"))

    @unittest.skipIf(is_python2_running(),
                     "Set are not supported for Python 2")
    def test_008_retrieve_set(self):
        value = '{"1", "2", "3"}'
        self.setup_value(value)
        self.assertEqual(getattr(ENV, self.KEY), {"1", "2", "3"})

    def test_009_retrieve_variable_not_set(self):
        self.assertIsNone(
            getattr(ENV, "YET_ANOTHER_VAR_{}".format(int(time.time()))))

    def test_010_retrieve_dict_with_single_quotes(self):
        value = "{'key': 'value', \"key2\": \"value\"}"
        self.setup_value(value)
        self.assertEqual(getattr(ENV, self.KEY),
                         {'key': 'value', "key2": "value"})
