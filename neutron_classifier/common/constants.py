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


CLASSIFIER_TYPES = ['ip_classifier', 'ipv4_classifier', 'ipv6_classifier',
                    'transport_classifier', 'ethernet_classifier',
                    'encapsulation_classifier', 'neutron_port_classifier']

# Protocol names and numbers
PROTO_NAME_ICMP = 'icmp'
PROTO_NAME_ICMP_V6 = 'icmpv6'
PROTO_NAME_TCP = 'tcp'
PROTO_NAME_UDP = 'udp'

# TODO(sc68cal) add more protocols`
PROTOCOLS = [PROTO_NAME_ICMP, PROTO_NAME_ICMP_V6,
             PROTO_NAME_TCP, PROTO_NAME_UDP]

ENCAPSULATION_TYPES = ['vxlan', 'gre']

NEUTRON_SERVICES = ['neutron-fwaas', 'networking-sfc', 'security-group']

DIRECTIONS = ['INGRESS', 'EGRESS', 'BIDIRECTIONAL']

ETHERTYPE_IPV4 = 0x0800
ETHERTYPE_IPV6 = 0x86DD

IP_VERSION_4 = 4
IP_VERSION_6 = 6

SECURITYGROUP_ETHERTYPE_IPV4 = 'IPv4'
SECURITYGROUP_ETHERTYPE_IPV6 = 'IPv6'
