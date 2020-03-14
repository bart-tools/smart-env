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

from time import time
import unittest

from smart_env import ENV


__all__ = ('EnvTestCase',)


class EnvTestCase(unittest.TestCase):
    """Tests for ENV class itself"""

    def setUp(self):
        """Auto reset settings"""
        ENV.disable_automatic_type_cast()

    def test_001_own_fields(self):
        """Check if all own fields work"""

        for name in ('enable_automatic_type_cast',
                     'disable_automatic_type_cast',
                     'is_auto_type_cast'):
            getattr(ENV, name)

    def test_002_changing_type_cast(self):
        """Check if enabling type cast works"""

        self.assertFalse(ENV.__dict__['_auto_type_cast'])
        self.assertFalse(ENV.is_auto_type_cast())

        ENV.enable_automatic_type_cast()

        self.assertTrue(ENV.__dict__['_auto_type_cast'])
        self.assertTrue(ENV.is_auto_type_cast())

        ENV.disable_automatic_type_cast()

        self.assertFalse(ENV.__dict__['_auto_type_cast'])
        self.assertFalse(ENV.is_auto_type_cast())

    def test_003_contains_variable(self):
        """Check "in" operator for Environment class"""

        variable_name = "NO_VAR_{}".format(int(time()))
        self.assertFalse(variable_name in ENV)

        setattr(ENV, variable_name, "somevalue")
        self.assertTrue(variable_name in ENV)

        setattr(ENV, variable_name, None)
        self.assertFalse(variable_name in ENV)

    def test_004_contains_own_field(self):
        """Check "in" operator for own fields of ENV class"""

        for key in ENV.__own_fields__:
            self.assertFalse(key in ENV)

    def test_005_unset_env_variable(self):
        """Check unsetting environment variable"""

        variable_name = "NO_VAR_{}".format(int(time()))
        variable_value = str(time())

        setattr(ENV, variable_name, variable_value)
        delattr(ENV, variable_name)
        self.assertFalse(variable_name in ENV)

    def test_006_set_env_variable(self):
        """Check setting environment variable"""

        variable_name = "NO_VAR_{}".format(int(time()))
        variable_value = str(time())

        setattr(ENV, variable_name, variable_value)
        self.assertEqual(getattr(ENV, variable_name), variable_value)
