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

from smart_env.decoders import BooleanDecoder
from smart_env.decoders import CollectionDecoder
from smart_env.decoders import IDecoder
from smart_env.decoders import JSONDecoder
from smart_env.decoders import SUPPORTED_DECODERS
from smart_env.exceptions import EncodeError


__all__ = ('DecoderTestCase',)


class FakeDecoder(IDecoder):
    """Fake decoder class to test IDecoder class"""

    @classmethod
    def decode(cls, value):
        """This method will simply call parent method"""
        return super(FakeDecoder, cls).decode(value)


class DecoderTestCase(unittest.TestCase):
    """Test cases for Decoder classes"""

    def test_decoder_interface(self):
        """Check that IDecoder is a true interface"""
        with self.assertRaises(NotImplementedError):
            FakeDecoder.decode(None)


class EncoderTestCase(unittest.TestCase):
    """Test cases for encoders"""

    def setUp(self):
        self.initial_data = [
            {
                'decoder': JSONDecoder,
                'values': [
                    {
                        'input': {"abc": True, "def": 10},
                        'output': [
                            '{"abc": true, "def": 10}',
                            '{"def": 10, "abc": true}'
                        ]
                    },
                    {
                        'input': [1, 2, 3, "asd", False],
                        'output': '[1, 2, 3, "asd", false]'
                    },
                    {
                        'input': [1, 2, 34, None],
                        'output': '[1, 2, 34, null]'
                    }
                ],
            },
            {
                'decoder': BooleanDecoder,
                'values': [
                    {
                        'input': True,
                        'output': 'true'
                    },
                    {
                        'input': False,
                        'output': 'false'
                    }
                ]
            },
            {
                'decoder': CollectionDecoder,
                'values': [
                    {
                        'input': {1, 3},
                        'output': [
                            '[1, 3]',
                            '[3, 1]'
                        ]
                    },
                    {
                        'input': frozenset({1, 2}),
                        'output': [
                            '[1, 2]',
                            '[2, 1]'
                        ]
                    },
                    {
                        'input': (1, 2, 3.14),
                        'output': '[1, 2, 3.14]'
                    }
                ]
            }
        ]

    def test_encoding_mechanism(self):
        """Check if all supported decoders can encode data"""

        for context in self.initial_data:
            for input_data in context['values']:
                output = context['decoder'].encode(input_data['input'])
                if isinstance(input_data['output'], list):
                    self.assertIn(output, input_data['output'])
                else:
                    self.assertEqual(output, input_data['output'])
