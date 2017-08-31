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


IP_V4 = ['dscp', 'dscp_mask', 'ecn', 'length_min', 'length_max', 'flags',
         'flags_mask', 'ttl_min', 'ttl_max', 'protocol',
         'src_addr', 'dst_addr']

IP_V6 = ['dscp', 'dscp_mask', 'ecn', 'length_min', 'length_max',
         'next_header', 'hops_min', 'hops_max', 'src_addr', 'dst_addr']

ETHERNET = ['ethertype', 'src_addr', 'dst_addr']

TCP = ['src_port_min', 'src_port_max', 'dst_port_min', 'dst_port_max',
       'flags', 'flags_mask', 'window_min', 'window_max']

UDP = ['src_port_min', 'src_port_max', 'dst_port_min', 'dst_port_max',
       'length_min', 'length_max']

CLASSIFIER_FIELDS = {'ipv4': IP_V4,
                     'ipv6': IP_V6,
                     'tcp': TCP,
                     'udp': UDP,
                     'ethernet': ETHERNET}
