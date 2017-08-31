# Copyright (c) 2017 Intel Corporation.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from neutron_classifier.objects import classification_type
from neutron_classifier.tests import base


class TestClassificationType(base.BaseClassificationTestCase):

    def setUp(self):
        super(TestClassificationType, self).setUp()
        self.ipv4_fields = ['c_type', 'protocol', 'description', 'ttl_min',
                            'shared', 'ecn', 'length_min', 'flags', 'dscp',
                            'id', 'dscp_mask', 'length_max', 'flags_mask',
                            'negated', 'ttl_max', 'src_addr', 'project_id',
                            'dst_addr', 'name']
        self.ipv6_fields = ['c_type', 'src_addr', 'description', 'ecn',
                            'length_min', 'dscp', 'hops_max', 'hops_min',
                            'dscp_mask', 'length_max', 'shared', 'id',
                            'negated', 'next_header', 'project_id',
                            'dst_addr', 'name']
        self.tcp_fields = ['dst_port_min', 'c_type', 'src_port_max',
                           'description', 'window_min', 'dst_port_max', 'name',
                           'flags', 'src_port_min', 'flags_mask', 'shared',
                           'negated', 'project_id', 'id', 'window_max']
        self.udp_fields = ['c_type', 'description', 'src_port_max',
                           'length_max', 'negated', 'id', 'dst_port_min',
                           'name', 'length_min', 'dst_port_max',
                           'src_port_min', 'shared', 'project_id']
        self.ethernet_fields = ['c_type', 'src_addr', 'description',
                                'ethertype', 'id', 'shared', 'negated',
                                'project_id', 'dst_addr', 'name']

    def test_ipv4_cls_type(self):
        ipv4_obj = classification_type.ClassificationType.get_object('ipv4')
        self.assertEqual(sorted(ipv4_obj.supported_parameters),
                         sorted(self.ipv4_fields))

    def test_ipv6_cls_type(self):
        ipv6_obj = classification_type.ClassificationType.get_object('ipv6')
        self.assertEqual(sorted(ipv6_obj.supported_parameters),
                         sorted(self.ipv6_fields))

    def test_tcp_cls_type(self):
        tcp_obj = classification_type.ClassificationType.get_object('tcp')
        self.assertEqual(sorted(tcp_obj.supported_parameters),
                         sorted(self.tcp_fields))

    def test_udp_cls_type(self):
        udp_obj = classification_type.ClassificationType.get_object('udp')
        self.assertEqual(sorted(udp_obj.supported_parameters),
                         sorted(self.udp_fields))

    def test_ethernet_cls_type(self):
        ethernet_obj = classification_type.ClassificationType.get_object(
            'ethernet')
        self.assertEqual(sorted(ethernet_obj.supported_parameters),
                         sorted(self.ethernet_fields))
