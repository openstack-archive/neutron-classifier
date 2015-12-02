# Copyright (c) 2015 Mirantis, Inc.
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

CLASSIFIER_TYPES = ['ip_classifier', 'ipv4_classifier', 'ipv6_classifier',
                    'transport_classifier', 'ethernet_classifier',
                    'encapsulation_classifier', 'neutron_port_classifier']

# TODO(sc68cal) add more protocols`
PROTOCOLS = ['tcp', 'udp', 'icmp', 'icmpv6']

ENCAPSULATION_TYPES = ['vxlan', 'gre']

NEUTRON_SERVICES = ['neutron-fwaas', 'networking-sfc', 'security-group']

DIRECTIONS = ['INGRESS', 'EGRESS']

ETHERTYPE_IPV4 = 0x0800
ETHERTYPE_IPV6 = 0x86DD
