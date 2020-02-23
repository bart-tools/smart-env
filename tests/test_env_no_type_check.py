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

import os
import time
from unittest import TestCase

from smart_env import ENV


__all__ = ('EnvGeneralTestCase',)


class EnvGeneralTestCase(TestCase):
    """Test case for basic tests of ENV class"""

    @staticmethod
    def generate_param_name():
        """Generates param name using current timestamp value"""
        return 'PARAM_{}'.format(int(time.time()))

    @staticmethod
    def generate_param_value():
        """Generates param value using current timestamp value"""
        return 'VALUE_{}'.format(int(time.time()))

    def test_001_retrieve_value(self):
        """Check that it's possible to retrieve value
        from environment variables"""

        param_name = self.generate_param_name()
        param_value = self.generate_param_value()
        os.environ[param_name] = param_value

        self.assertEqual(getattr(ENV, param_name), param_value)
        del os.environ[param_name]

    def test_002_value_not_set(self):
        """Check that value which was not set in environment variables
        is None in ENV"""

        param_name = self.generate_param_name()
        self.assertEqual(getattr(ENV, param_name), None)
