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

import itertools
import json
import os

from six import with_metaclass

from .decoders import SUPPORTED_DECODERS
from .exceptions import DecodeError
from .exceptions import EncodeError
from .iterator import EnvIterator


__all__ = ('ENV',)


class ClassProperty(type):
    """Metaclass for enabling properties on class"""

    __immutable_fields__ = ('enable_automatic_type_cast',
                          'disable_automatic_type_cast')
    __mutable_fields__ = ('_auto_type_cast',)

    __own_fields__ = __immutable_fields__ + __mutable_fields__

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

    def __encode(cls, value):
        """Encodes data as text"""

        if isinstance(value, str):
            return value

        for decoder in SUPPORTED_DECODERS:
            try:
                return decoder.encode(value)
            except EncodeError:
                pass
        else:
            raise ValueError("'{}' value is not serializable".format(value))

    def __getattr__(cls, item):
        if item in cls.__own_fields__:
            return cls.__dict__[item]
        if cls._auto_type_cast:
            return cls.__decode(os.environ.get(item, None))
        return os.environ.get(item, None)

    def __delattr__(cls, item):
        """Unset environment variable"""
        if item in cls.__own_fields__:
            raise AttributeError(
                "Own attribute '{}' cannot be deleted".format(item))
        # NOTE(albartash): If environment variable is not set,
        #                  it can be safely unset more times.
        #                  This behaviour is different from native
        #                  del os.environ[k] which would raise KeyError
        try:
            del os.environ[item]
        except KeyError:
            pass

    def __setattr__(cls, key, value):
        if key in cls.__immutable_fields__:
            raise AttributeError(
                "Own attribute '{}' cannot be reinitialized".format(key))

        if key in cls.__mutable_fields__:
            super(ClassProperty, cls).__setattr__(key, value)

        if value is None:  # means - unset variable
            delattr(cls, key)
            return

        os.environ[key] = cls.__encode(value)

    def __contains__(cls, item):
        """Check if environment variable is set"""

        # Class' own fields should not appear as existing
        # environment variables
        if item in cls.__own_fields__:
            return False

        return os.environ.get(item, None) is not None

    def __str__(cls):
        """Returns a string representation of os.environ object.

        In this case, values are not decoded from their string equivalents
        in the OS environment. For convenience, json.dumps() is used.
        """

        return json.dumps(dict(os.environ))

    def __repr__(cls):
        """Returns a string with sorted list of environment variables"""

        return str(sorted(os.environ.keys()))

    def __iter__(self):
        return EnvIterator(sorted(os.environ.keys()))

    def __dir__(self):
        """Returns list of environment variables + own fields"""

        return sorted(
            itertools.chain(self.__own_fields__,
                            os.environ.keys()
            )
        )


class ENV(with_metaclass(ClassProperty)):
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
