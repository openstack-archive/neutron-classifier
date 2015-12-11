# Copyright (c) 2015 Huawei Technologies India Pvt Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
neutron-classifier base exception handling.
"""

from oslo_utils import excutils
import six


# Below code is copied from neutron/common/exceptions.py
class ClassifierException(Exception):
    """Base neutron-classifier Exception.

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """
    message = ("An unknown exception occurred.")

    def __init__(self, **kwargs):
        try:
            super(ClassifierException, self).__init__(self.message % kwargs)
            self.msg = self.message % kwargs
        except Exception:
            with excutils.save_and_reraise_exception() as ctxt:
                if not self.use_fatal_exceptions():
                    ctxt.reraise = False
                    # at least get the core message out if something happened
                    super(ClassifierException, self).__init__(self.message)

    if six.PY2:
        def __unicode__(self):
            return unicode(self.msg)

    def __str__(self):
        return self.msg

    def use_fatal_exceptions(self):
        return False


class InvalidEthernetClassifier(ClassifierException):
    message = ('Invalid ethernet classifier value for %(eth_type)s')


class IpAddressConflict(ClassifierException):
    message = ("Invalid input - IP addresses do not agree with IP Version")


class InvalidICMPParameter(ClassifierException):
    message = ("%(param)s are not allowed when protocol is set to ICMP.")


class EthertypeConflictWithProtocol(ClassifierException):
    message = ("Invalid ethertype %(ethertype)s for protocol %(protocol)s.")


class InvalidPortValue(ClassifierException):
    message = ("Invalid value for port %(port)s.")
