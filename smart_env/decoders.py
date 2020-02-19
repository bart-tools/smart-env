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

import abc
import ast
import json

from six import with_metaclass

from .exceptions import DecodeError


__all__ = ('IDecoder',
           'JSONDecoder',
           'BooleanDecoder',
           'CollectionDecoder',
           'SUPPORTED_DECODERS')


class IDecoder(with_metaclass(abc.ABCMeta)):
    """Interface for defining all decoder classes"""

    @classmethod
    @abc.abstractmethod
    def decode(cls, value):
        """Decode value using specified algorithm"""
        raise NotImplementedError


class JSONDecoder(IDecoder):
    """JSON-based decoder"""

    @classmethod
    def decode(cls, value):
        """Try to decode value assuming it's a JSON-like string

        Supported values:
            - int
            - float
            - str
            - list (of JSON-compatible values)
            - dict (with double quotes used for strings)
            - "null" string (means None)
            - "true" string (means True)
            - "false" string (means False)
        """

        try:
            return json.loads(value)
        except ValueError:  # To cover exceptions in all Python versions
            raise DecodeError


class BooleanDecoder(IDecoder):
    """Decoder for boolean-like values"""

    @classmethod
    def decode(cls, value):
        """Try to decode value assuming it's boolean-like string

        Supported values:
            - "True"
            - "False"
            - "true"
            - "false"
        """

        if value in ("True", "true"):
            return True
        if value in ("False", "false"):
            return False
        raise DecodeError


class CollectionDecoder(IDecoder):
    """Decoder for collection-like values"""

    @classmethod
    def decode(cls, value):
        """Try to decode value assuming it's list-like string

        Supported values:
            - list-like string
            - set-like string
            - tuple-like string
            - dict-like string
        """
        try:
            return ast.literal_eval(value)
        except ValueError:
            raise DecodeError


SUPPORTED_DECODERS = (
    JSONDecoder,
    BooleanDecoder,
    CollectionDecoder,
)
