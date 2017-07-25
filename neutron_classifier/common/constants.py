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

L2_PREFIX = '/ccf'

DSCP_VALID_MARKS = [0, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32,
                    34, 36, 38, 40, 46, 48, 56]
ECN_VALID_MARKS = [0, 1, 2, 3]

IP_V4 = ['ihl', 'diffserv', 'length', 'flags', 'ttl', 'protocol',
         'src_addr', 'dst_addr', 'options']

IP_V6 = ['traffic_class', 'length', 'next_header', 'hops',
         'src_addr', 'dst_addr']

ETHERNET = ['preamble', 'src_addr', 'dst_addr', 'ethertype']

TCP = ['src_port', 'dst-port', 'flags', 'window', 'data_offset',
       'option_kind']

UDP = ['src_port', 'dst_port', 'length', 'window_size']

ALL_FIELDS = IP_V4 + IP_V6 + ETHERNET

CLASSIFIER_FIELDS = {'ipv4': IP_V4,
                     'ipv6': IP_V6,
                     'tcp': TCP,
                     'udp': UDP,
                     'ethernet': ETHERNET}
