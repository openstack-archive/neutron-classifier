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


class ConsumedClassification(nexceptions.NeutronException):
    message = ("""One or more classification is already being consumed
               and can't be used or deleted.""")


class InvalidClassificationGroupId(nexceptions.NeutronException):
    message = ("One or more id is not a valid classification group id.")


class InvalidClassificationId(nexceptions.NeutronException):
    message = ("One or more id is not a valid classification id")


class ConsumedClassificationGroup(nexceptions.NeutronException):
    message = ("""One or more classification group is being consumed
               and can't be deleted.""")


class InvalidClassificationGroupUpdateRequest(nexceptions.NeutronException):
    message = ("""The update request is invalid. Only the name and description
               can be updated for a classification group""")
