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
        common_fields = ['c_type', 'description', 'negated', 'shared',
                         'project_id', 'id', 'name']
        common_ipv = ['src_addr', 'ecn', 'length_min', 'dscp', 'dscp_mask',
                      'length_max', 'dst_addr']
        common_tcp_udp = ['src_port_min', 'src_port_max', 'dst_port_min',
                          'dst_port_max']
        self.ipv4_fields = common_fields + common_ipv + ['ttl_max', 'flags',
                                                         'protocol', 'ttl_min',
                                                         'flags_mask']
        self.ipv6_fields = common_fields + common_ipv + ['hops_min',
                                                         'hops_max',
                                                         'next_header']
        self.tcp_fields = common_fields + common_tcp_udp + ['window_min',
                                                            'flags',
                                                            'window_max',
                                                            'flags_mask']
        self.udp_fields = common_fields + common_tcp_udp + ['length_min',
                                                            'length_max']
        self.ethernet_fields = common_fields + ['ethertype', 'src_addr',
                                                'dst_addr']

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
