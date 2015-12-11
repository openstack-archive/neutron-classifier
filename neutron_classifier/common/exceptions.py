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
neutron-classifier exception handling.
"""

from neutron.common import exceptions as exc


class InvalidEthernetClassifier(exc.NeutronException):
    message = ('Invalid ethernet classifier value for %(eth_type)s')


class IpAddressConflict(exc.NeutronException):
    message = ("Invalid input - IP addresses do not agree with IP Version")


class InvalidICMPParameter(exc.NeutronException):
    message = ("%(param)s are not allowed when protocol is set to ICMP.")


class EthertypeConflictWithProtocol(exc.NeutronException):
    message = ("Invalid ethertype %(ethertype)s for protocol %(protocol)s.")


class InvalidPortValue(exc.NeutronException):
    message = ("Invalid value for port %(port)s.")
