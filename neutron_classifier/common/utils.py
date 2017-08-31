# Copyright 2011, VMware, Inc.
# All Rights Reserved.
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
#
# Borrowed from the Neutron code base, more utilities will be added/borrowed as
# and when needed.

import importlib
import os
import re
import sys

import neutron_classifier

_SEPARATOR_REGEX = re.compile(r'[/\\]+')


def import_modules_recursively(topdir):
    '''Import and return all modules below the topdir directory.'''
    topdir = _SEPARATOR_REGEX.sub('/', topdir)
    modules = []
    for root, dirs, files in os.walk(topdir):
        for file_ in files:
            if file_[-3:] != '.py':
                continue

            module = file_[:-3]
            if module == '__init__':
                continue

            import_base = _SEPARATOR_REGEX.sub('.', root)

            # NOTE(ihrachys): in Python3, or when we are not located in the
            # directory containing neutron code, __file__ is absolute, so we
            # should truncate it to exclude PYTHONPATH prefix

            prefixlen = len(os.path.dirname(neutron_classifier.__file__))
            import_base = 'neutron_classifier' + import_base[prefixlen:]

            module = '.'.join([import_base, module])
            if module not in sys.modules:
                importlib.import_module(module)
            modules.append(module)
    return modules
