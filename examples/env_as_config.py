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

# Imagine you have a web application written with popular frameworks
# (Django, Flask, etc). If so, your settings.py would look like this.

from smart_env import ENV


ENV.enable_automatic_type_cast()


# This variable now can be checked as-is, without
# Copy-pasting checks like "var in ('true', 1, etc)".

DEBUG = ENV.DEBUG

# These configs might had been stored in a separate Shell or JSON file,
# and brought to environment just before running your application.
DATABASES = ENV.DATABASE_CONFIG
SENTRY_CONFIG = ENV.SENTRY_CONFIG

# This value now can be passed directly into loggin.config.dictConfig()
LOGGING_CONFIG = ENV.LOGGING_CONFIG
