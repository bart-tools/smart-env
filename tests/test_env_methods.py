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

import datetime
import itertools
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

    def test_007_try_reinitialize_own_immutable_fields(self):
        """Check immutability of __immutable_fields__ in ENV"""

        for field in ENV.__immutable_fields__:
            with self.assertRaises(AttributeError):
                setattr(ENV, field, 'value')

    def test_008_get_own_fields(self):
        """Check getting __own__fields__ items"""

        for field in ENV.__own_fields__:
            self.assertIsNotNone(getattr(ENV, field))

    def test_009_try_delete_own_attribute(self):
        """Check deletion of __own_fields__ in ENV"""

        for field in ENV.__own_fields__:
            with self.assertRaises(AttributeError):
                delattr(ENV, field)

    def test_010_serialize_invalid_value(self):
        """Check that invalid value cannot be serialized"""

        ENV.enable_automatic_type_cast()

        for value in (datetime.datetime.now(), object()):
            with self.assertRaises(ValueError):
                setattr(ENV, 'SOMEVAR', value)

    def test_011_smoke_test_decode(self):
        """Check method __decode() in ENV"""

        with self.assertRaises(TypeError):
            ENV._ENV__decode(object())


class ENVRepresentationTestCase(unittest.TestCase):
    """Test cases for representations of ENV class"""

    def setUp(self):
        """Erase environment before running tests"""

        for var in ENV:
            setattr(ENV, var, None)

    def test_001_test_str_method(self):
        """Check __str__() method of ENV class"""

        variable_name = "STR_VAR_{}".format(int(time()))
        variable_value = str(time())

        setattr(ENV, variable_name, variable_value)

        env_string = '{"%s": "%s"}' % (variable_name, variable_value)
        self.assertEqual(str(ENV), env_string)

    def test_002_repr_method(self):
        """Check __repr__() method of ENV class"""

        variable_name_1 = "STR_VAR_1"
        variable_name_2 = "STR_VAR_2"
        variable_value = "Something"

        setattr(ENV, variable_name_2, variable_value)
        setattr(ENV, variable_name_1, variable_value)

        env_string = "['{}', '{}']".format(
            variable_name_1, variable_name_2
        )
        self.assertEqual(repr(ENV), env_string)

    def test_003_iterate_environment(self):
        """Check iteration of environment variables"""

        var_names = ["VAR_{}".format(i) for i in range(5)]
        for var in var_names:
            setattr(ENV, var, 'value')

        var_names_cmp = [name for name in ENV]

        self.assertEqual(var_names, var_names_cmp)

    def test_004_list_variables(self):
        variable_name = "STR_VAR_{}".format(int(time()))
        setattr(ENV, variable_name, 'value')
        dir_list = sorted(
            itertools.chain(
                ENV.__own_fields__, [variable_name]
            )
        )

        self.assertEqual(dir(ENV), dir_list)
