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

from oslo_utils import uuidutils


def _generate_all_fake_classifications(self):
    self._generate_fake_ipv4_classifications()
    self._generate_fake_ipv6_classifications()
    self._generate_fake_ethernet_classifications()
    self._generate_fake_udp_classifications()
    self._generate_fake_tcp_classifications()


def _generate_fake_ipv4_classifications(self):
    self.fake_ipv4_classification = {
        'classification': {'id': uuidutils.generate_uuid(),
                           'name': 'test_ipv4_classification',
                           'description': 'Test IPV4 Classification',
                           'project_id': uuidutils.generate_uuid(),
                           'shared': True,
                           'negated': True,
                           'c_type': 'ipv4',
                           'definition': {'ihl': 20,
                                          'diffserv': None,
                                          'diffserv_mask': None,
                                          'length': 390,
                                          'flags': None,
                                          'flags_mask': None,
                                          'ttl': 128,
                                          'protocol': 17,
                                          'src_addr': '192.168.2.2',
                                          'dst_addr': '192.168.2.4',
                                          'options': None,
                                          'options_mask': None}}}

    self.fake_ipv4_classification_broken_headers = {
        'id': self.fake_ipv4_classification['classification']['id'],
        'name': 'test_ipv4_classification',
        'description': 'Test IPV4 Classification',
        'project_id': self.fake_ipv4_classification[
            'classification']['project_id'],
        'shared': True,
        'negated': True,
        'c_type': 'ipv4',
        'ihl': 20,
        'diffserv': None,
        'diffserv_mask': None,
        'length': 390,
        'flags': None,
        'flags_mask': None,
        'ttl': 128,
        'protocol': 17,
        'src_addr': '192.168.2.2',
        'dst_addr': '192.168.2.4',
        'options': None,
        'options_mask': None}

    self.fake_ipv4_classification_2 = {
        'classification': {'id': uuidutils.generate_uuid(),
                           'name': 'test_ipv4_classification_2',
                           'description': 'Test IPV4 Classification 2',
                           'project_id': uuidutils.generate_uuid(),
                           'shared': False,
                           'negated': False,
                           'c_type': 'ipv4',
                           'definition': {'ihl': 32,
                                          'diffserv': None,
                                          'diffserv_mask': None,
                                          'lenght': 260,
                                          'flags': None,
                                          'flags_mask': None,
                                          'ttl': 45,
                                          'protocol': 6,
                                          'src_addr': '192.168.4.5',
                                          'dst_addr': '192.168.4.8',
                                          'options': None,
                                          'options_mask': None}}}

    self.fake_ipv4_classification_2_broken_headers = {
        'id': self.fake_ipv4_classification_2['classification']['id'],
        'name': 'test_ipv4_classification_2',
        'description': 'Test IPV4 Classification 2',
        'project_id': self.fake_ipv4_classification_2[
            'classification']['project_id'],
        'shared': False,
        'negated': False,
        'c_type': 'ipv4',
        'ihl': 32,
        'diffserv': None,
        'diffserv_mask': None,
        'ttl': 45,
        'protocol': 6,
        'scr_addr': '192.168.4.5',
        'dst_addr': '192.168.4.8',
        'options': None,
        'options_mask': None}


def _generate_fake_ipv6_classifications(self):
    self.fake_ipv6_classification = {
        'classification': {'id': uuidutils.generate_uuid(),
                           'name': 'test_ipv6_classification',
                           'description': 'Test IPV6 Classification',
                           'project_id': uuidutils.generate_uuid(),
                           'shared': True,
                           'negated': True,
                           'c_type': 'ipv6',
                           'definition': {'traffic_class': None,
                                          'traffic_class_mask': None,
                                          'length': 20,
                                          'next_header': 6,
                                          'hops': 64,
                                          'src_addr': '2::2',
                                          'dst_addr': '2::1'}}}

    self.fake_ipv6_classification_broken_headers = {
        'id': self.fake_ipv6_classification['classification']['id'],
        'name': 'test_ipv6_classification',
        'description': 'Test IPV6 Classification',
        'project_id': self.fake_ipv6_classification[
            'classification']['project_id'],
        'shared': True,
        'negated': True,
        'c_type': 'ipv6',
        'traffic_class': None,
        'traffic_class_mask': None,
        'length': 20,
        'next_header': 6,
        'hops': 64,
        'src_addr': '2::2',
        'dst_addr': '2::1'}

    self.fake_ipv6_classification_2 = {
        'classification': {'id': uuidutils.generate_uuid(),
                           'name': 'test_ipv6_classification_2',
                           'description': 'Test IPV6 Classification 2',
                           'project_id': uuidutils.generate_uuid(),
                           'shared': False,
                           'negated': False,
                           'c_type': 'ipv6',
                           'definition': {'traffic_class': None,
                                          'traffic_class_mask': None,
                                          'length': 64,
                                          'next_header': 17,
                                          'hops': 120,
                                          'src_addr': '2::1',
                                          'dst_addr': '2::2'}}}

    self.fake_ipv6_classification_2_broken_headers = {
        'id': self.fake_ipv6_classification_2['classification']['id'],
        'name': 'test_ipv6_classification_2',
        'description': 'Test IPV6 Classification 2',
        'project_id': self.fake_ipv6_classification_2[
            'classification']['project_id'],
        'shared': False,
        'negated': False,
        'c_type': 'ipv6',
        'traffic_class': None,
        'traffic_class_mask': None,
        'length': 64,
        'next_header': 17,
        'hops': 120,
        'src_addr': '2::1',
        'dst_addr': '2::2'}


def _generate_fake_ethernet_classifications(self):
    self.fake_ethernet_classification = {
        'classification': {'id': uuidutils.generate_uuid(),
                           'name': 'test_ethernet_classification',
                           'description': 'Test Ethernet Classification',
                           'project_id': uuidutils.generate_uuid(),
                           'shared': True,
                           'negated': True,
                           'c_type': 'ethernet',
                           'definition': {'preamble': 20,
                                          'src_addr': '00:07:E9:63:CE:53',
                                          'dst_addr': '00:07:E9:42:AC:28',
                                          'ethertype': 8100}}}

    self.fake_ethernet_classification_broken_headers = {
        'id': self.fake_ethernet_classification['classification']['id'],
        'name': 'test_ethernet_classification',
        'description': 'Test Ethernet Classification',
        'project_id': self.fake_ethernet_classification[
            'classification']['project_id'],
        'shared': True,
        'negated': True,
        'c_type': 'ethernet',
        'preamble': 20,
        'src_addr': '00:07:E9:63:CE:53',
        'dst_addr': '00:07:E9:42:AC:28',
        'ethertype': 8100}

    self.fake_ethernet_classification_2 = {
        'classification': {'id': uuidutils.generate_uuid(),
                           'name': 'test_second_ethernet_cl',
                           'description': 'Test Second \
                                          Ethernet Classification',
                           'project_id': uuidutils.generate_uuid(),
                           'shared': False,
                           'negated': False,
                           'c_type': 'ethernet',
                           'definition': {'preamble': 16,
                                          'src_addr': '00:54:TY:89:G6:67',
                                          'dst_adrr': '00:54:TY:65:T7:44',
                                          'ethertype': 8100}}}

    self.fake_ethernet_classification_2_broken_headers = {
        'id': self.fake_ethernet_classification_2['classification']['id'],
        'name': 'test_second_ethernet_cl',
        'description': 'Test Second Ethernet Classification',
        'project_id': self.fake_ethernet_classification_2[
            'classification']['project_id'],
        'shared': False,
        'negated': False,
        'c_type': 'ethernet',
        'preamble': 16,
        'src_addr': '00:54:TY:89:G6:67',
        'dst_addr': '00:54:TY:65:T7:44',
        'ethertype': 8100}


def _generate_fake_udp_classifications(self):
    self.fake_udp_classification = {
        'classification': {'id': uuidutils.generate_uuid(),
                           'name': 'test_udp_classification',
                           'description': 'Test UDP Classification',
                           'project_id': uuidutils.generate_uuid(),
                           'shared': True,
                           'negated': True,
                           'c_type': 'udp',
                           'definition': {'src_port': '22689',
                                          'dst_port': '58547',
                                          'length': 12,
                                          'window_size': None}}}

    self.fake_udp_classification_broken_headers = {
        'id': self.fake_udp_classification['classification']['id'],
        'name': 'test_udp_classification',
        'description': 'Test UDP Classification',
        'project_id': self.fake_udp_classification[
            'classification']['project_id'],
        'shared': True,
        'negated': True,
        'c_type': 'udp',
        'src_port': '22689',
        'dst_port': '58547',
        'length': 12,
        'window_size': None}

    self.fake_udp_classification_2 = {
        'classification': {'id': uuidutils.generate_uuid(),
                           'name': 'test_udp_classification_2',
                           'description': 'Test UDP Classification 2',
                           'project_id': uuidutils.generate_uuid(),
                           'shared': False,
                           'negated': False,
                           'c_type': 'udp',
                           'definition': {'src_port': '56378',
                                          'dst_port': '87654',
                                          'length': 20,
                                          'window_size': 32}}}

    self.fake_udp_classification_2_broken_headers = {
        'id': self.fake_udp_classification_2['classification']['id'],
        'name': 'test_udp_classification_2',
        'description': 'Test UDP Classification 2',
        'project_id': self.fake_udp_classification_2[
            'classification']['project_id'],
        'shared': False,
        'negated': False,
        'c_type': 'udp',
        'src_port': '56378',
        'dst_port': '87654',
        'length': 20,
        'window_size': 32}


def _generate_fake_tcp_classifications(self):
    self.fake_tcp_classification = {
        'classification': {'id': uuidutils.generate_uuid(),
                           'name': 'test_tcp_classification',
                           'description': 'Test TCP Classification',
                           'project_id': uuidutils.generate_uuid(),
                           'shared': True,
                           'negated': True,
                           'c_type': 'tcp',
                           'definition': {'src_port': '55075',
                                          'dst_port': '50100',
                                          'flags': None,
                                          'flags_mask': None,
                                          'window': 43820,
                                          'data_offset': None,
                                          'option_kind': 20}}}

    self.fake_tcp_classification_broken_headers = {
        'id': self.fake_tcp_classification['classification']['id'],
        'name': 'test_tcp_classification',
        'description': 'Test TCP Classification',
        'project_id': self.fake_tcp_classification[
            'classification']['project_id'],
        'shared': True,
        'negated': True,
        'c_type': 'tcp',
        'src_port': '55075',
        'dst_port': '50100',
        'flags': None,
        'flags_mask': None,
        'window': 43820,
        'data_offset': None,
        'option_kind': 20}

    self.fake_tcp_classification_2 = {
        'classification': {'id': uuidutils.generate_uuid(),
                           'name': 'test_tcp_classification_2',
                           'description': 'Test TCP Classification 2',
                           'project_id': uuidutils.generate_uuid(),
                           'shared': False,
                           'negated': False,
                           'c_type': 'tcp',
                           'definition': {'src_port': '42870',
                                          'dst_port': '76346',
                                          'flags': None,
                                          'flags_mask': None,
                                          'window': 76550,
                                          'data_offset': None,
                                          'option_kind': 17}}}

    self.fake_tcp_classification_2_broken_headers = {
        'id': self.fake_tcp_classification_2['classification']['id'],
        'name': 'test_tcp_classification_2',
        'description': 'Test TCP Classification 2',
        'project_id': self.fake_tcp_classification_2[
            'classification']['project_id'],
        'shared': False,
        'negated': False,
        'c_type': 'tcp',
        'src_port': '42870',
        'dst_port': '76346',
        'flags': None,
        'flags_mask': None,
        'window': 76550,
        'data_offset': None,
        'option_kind': 17}
