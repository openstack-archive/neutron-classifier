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

from neutron_classifier.common import constants
from neutron_classifier.objects import classification_type
from neutron_classifier.tests import base


class TestClassificationType(base.BaseClassificationTestCase):

    def setUp(self):
        super(TestClassificationType, self).setUp()
        self.ipv4_fields = constants.FIELDS_IP_V4
        self.ipv6_fields = constants.FIELDS_IP_V6
        self.tcp_fields = constants.FIELDS_TCP
        self.udp_fields = constants.FIELDS_UDP
        self.ethernet_fields = constants.FIELDS_ETHERNET

    def test_ipv4_cls_type(self):
        ipv4_obj = classification_type.ClassificationType.get_object('ipv4')
        self.assertEqual(ipv4_obj.supported_parameters, self.ipv4_fields)

    def test_ipv6_cls_type(self):
        ipv6_obj = classification_type.ClassificationType.get_object('ipv6')
        self.assertEqual(ipv6_obj.supported_parameters, self.ipv6_fields)

    def test_tcp_cls_type(self):
        tcp_obj = classification_type.ClassificationType.get_object('tcp')
        self.assertEqual(tcp_obj.supported_parameters, self.tcp_fields)

    def test_udp_cls_type(self):
        udp_obj = classification_type.ClassificationType.get_object('udp')
        self.assertEqual(udp_obj.supported_parameters, self.udp_fields)

    def test_ethernet_cls_type(self):
        ethernet_obj = classification_type.ClassificationType.get_object(
            'ethernet')
        self.assertEqual(ethernet_obj.supported_parameters,
                         self.ethernet_fields)
