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

from six import with_metaclass

from .decoders import SUPPORTED_DECODERS
from .exceptions import DecodeError


__all__ = ('ENV',)


class __ClassProperty(type):
    """Metaclass for enabling properties on class"""

    __own_fields__ = ('enable_automatic_type_cast',
                      'disable_automatic_type_cast',
                      'is_auto_type_cast')

    @staticmethod
    def __decode(value):
        """Decodes data from environment variable if possible,
        or return the source value otherwise"""
        if value is None:  # Variable was not set in environment
            return value

        if not isinstance(value, str):
            raise TypeError("Value {} must be str, not {}".format(value,
                                                                  type(value)))

        for decoder in SUPPORTED_DECODERS:
            try:
                return decoder.decode(value)
            except DecodeError:
                pass
        else:
            return value

    def __getattr__(cls, item):
        if item in cls.__own_fields__:
            return cls.__dict__[item]
        if cls._auto_type_cast:
            return cls.__decode(os.environ.get(item, None))
        return os.environ.get(item, None)


class ENV(with_metaclass(__ClassProperty)):
    """Environment wrapper"""

    _auto_type_cast = False

    @classmethod
    def enable_automatic_type_cast(cls):
        """Enable automatic type cast"""
        cls._auto_type_cast = True

    @classmethod
    def disable_automatic_type_cast(cls):
        """Disable automatic type cast"""
        cls._auto_type_cast = False

    @classmethod
    def is_auto_type_cast(cls):
        """Shows if automatic type cast is enabled"""
        return cls._auto_type_cast
