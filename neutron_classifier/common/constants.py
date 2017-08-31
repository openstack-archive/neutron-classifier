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


from neutron_classifier.objects import classifications as cs

FIELDS_IPV4 = cs.IPV4Classification.fields.keys()
FIELDS_IPV6 = cs.IPV6Classification.fields.keys()
FIELDS_TCP = cs.TCPClassification.fields.keys()
FIELDS_UDP = cs.UDPClassification.fields.keys()
FIELDS_ETHERNET = cs.EthernetClassification.fields.keys()


SUPPORTED_FIELDS = {'ipv4': FIELDS_IPV4,
                    'ipv6': FIELDS_IPV6,
                    'tcp': FIELDS_TCP,
                    'udp': FIELDS_UDP,
                    'ethernet': FIELDS_ETHERNET}
