# Copyright (c) 2015 Mirantis, Inc.
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

from neutron.objects import classification as cs_base
from neutron_classifier.objects import classifications as cs

COMMON_FIELDS = cs_base.ClassificationBase.fields.keys()
FIELDS_IPV4 = list(set(cs.IPV4Classification.fields.keys()) -
                   set(COMMON_FIELDS))
FIELDS_IPV6 = list(set(cs.IPV6Classification.fields.keys()) -
                   set(COMMON_FIELDS))
FIELDS_TCP = list(set(cs.TCPClassification.fields.keys()) -
                  set(COMMON_FIELDS))
FIELDS_UDP = list(set(cs.UDPClassification.fields.keys()) -
                  set(COMMON_FIELDS))
FIELDS_ETHERNET = list(set(cs.EthernetClassification.fields.keys()) -
                       set(COMMON_FIELDS))


SUPPORTED_FIELDS = {'ipv4': FIELDS_IPV4,
                    'ipv6': FIELDS_IPV6,
                    'tcp': FIELDS_TCP,
                    'udp': FIELDS_UDP,
                    'ethernet': FIELDS_ETHERNET}

# Method names for receiving classifications
PRECOMMIT_POSTFIX = '_precommit'
CREATE_CLASS = 'create_classification'
CREATE_CLASS_PRECOMMIT = CREATE_CLASS + PRECOMMIT_POSTFIX
UPDATE_CLASS = 'update_classification'
UPDATE_CLASS_PRECOMMIT = UPDATE_CLASS + PRECOMMIT_POSTFIX
DELETE_CLASS = 'delete_classification'
DELETE_CLASS_PRECOMMIT = DELETE_CLASS + PRECOMMIT_POSTFIX

CLASS_CALL_METHODS = (
    CREATE_CLASS,
    CREATE_CLASS_PRECOMMIT,
    UPDATE_CLASS,
    UPDATE_CLASS_PRECOMMIT,
    DELETE_CLASS,
    DELETE_CLASS_PRECOMMIT, )
