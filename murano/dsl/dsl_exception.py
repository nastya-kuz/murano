#    Copyright (c) 2014 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import murano.dsl.yaql_functions as yaql_functions


class MuranoPlException(Exception):
    def __init__(self, names, message, stacktrace, extra=None, cause=None):
        super(MuranoPlException, self).__init__(
            '{0}: {1}'.format(names, message))
        if not isinstance(names, list):
            names = [names]
        self._names = names
        self._message = message
        self._stacktrace = stacktrace
        self._extra = extra or {}
        self._cause = cause

    @property
    def names(self):
        return self._names

    @property
    def message(self):
        return self._message

    @property
    def stacktrace(self):
        return self._stacktrace

    @property
    def extra(self):
        return self._extra

    @property
    def cause(self):
        return self._cause

    @staticmethod
    def from_python_exception(exception, context):
        stacktrace = yaql_functions.new('io.murano.StackTrace', context)
        exception_type = type(exception)
        names = ['{0}.{1}'.format(exception_type.__module__,
                                  exception_type.__name__)]

        return MuranoPlException(
            names, exception.message, stacktrace)

    def _format_name(self):
        if not self._names:
            return ''
        elif len(self._names) == 1:
            return self._names[0]
        else:
            return self._names

    def format(self, prefix='  '):
        text = '\n{3}{0}: {1}\n' \
               '{3}Traceback (most recent call last):\n' \
               '{2}'.format(self._format_name(), self.message,
                            self.stacktrace.toString(prefix + '  '), prefix)
        if self._cause is not None:
            text += '\n\n{0} Caused by {1}'.format(
                prefix, self._cause.format(prefix + ' ').lstrip())
        return text
