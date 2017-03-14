# Copyright (c) 2016 Huawei Technologies India Pvt Ltd.
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

from neutron_lib import exceptions as nexceptions


class InvalidEthernetClassifier(nexceptions.NeutronException):
    message = ('Invalid ethernet classifier value for %(eth_type)s.')


class EthertypeConflictWithProtocol(nexceptions.NeutronException):
    message = ("Invalid ethertype %(ethertype)s for protocol %(protocol)s.")


class IpAddressConflict(nexceptions.NeutronException):
    message = ("IP address do not agree with the given IP Version.")


class InvalidICMPParameter(nexceptions.NeutronException):
    message = ("%(param)s are not allowed when protocol is set to ICMP.")


class InvalidPortRange(nexceptions.NeutronException):
    message = ("Invalid port range %(port_range).")


class InvalidClassificationUuid(nexceptions.NeutronException):
    message = ("No classification matches ID %(uuid).")


class InvalidClassificationName(nexceptions.NeutronException):
    message = ("No classification matches name %(name).")


class InvalidParameterToType(nexceptions.NeutronException):
    message = ("%(parameter) is not valid for classification type %(type)")


class InvalidValueToParameter(nexceptions.NeutronException):
    message = ("%(value) is not a valid value for the %(parameter) field")


class InvalidClassificationResource(nexceptions.NeutronException):
    message = ("%(res) is not a valid classification resource")


class InvalidClassificationAction(nexceptions.NeutronException):
    message = ("%(act) is not a valid classification action")


class InvalidClassificationMark(nexceptions.NeutronException):
    msg = ("%(mark) is not a valid %(classification) classification")


class InvalidClassificationMask(nexceptions.NeutronException):
    msg = ("%(mask) is not a valid %(classification) mask")
