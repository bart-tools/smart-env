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

import unittest

from smart_env.iterator import EnvIterator


__all__ = ('EnvIteratorTestCase',)


class EnvIteratorTestCase(unittest.TestCase):
    """Test case for utils"""

    def test_iterator_with_valid_parameter(self):
        """Check that iterator can be created with valid parameter"""

        for value in ({'a': 'b'},
                      [1, 2],
                      {3, 4},
                      frozenset(),
                      (i for i in range(5))
                      ):
            for _ in EnvIterator(value):
                pass

    def test_iterator_with_invalid_parameter(self):
        """Check that iterator can't be created with invalid parameter"""

        for value in (object(), 'value', 1, 1.2, True):
            with self.assertRaises(TypeError):
                for _ in EnvIterator(value):
                    pass
