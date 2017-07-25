# Copyright 2018 Intel Corporation.
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

import oslo_versionedobjects

from neutron_classifier.objects import classifications
from neutron_classifier.tests import objects_base as obj_base
from neutron_classifier.tests import tools

from neutron_lib import context

from neutron.db import api as db_api
from neutron.tests.unit.objects import test_base
from neutron.tests.unit import testlib_api


class ClassificationGroupTest(test_base.BaseDbObjectTestCase,
                              testlib_api.SqlTestCase,
                              obj_base._CCFObjectsTestCommon):
    # NOTE(ndahiwade): As the FIELD_TYPE_VALUE_GENERATOR_MAP in neutron's
    # test_base for objects doesn't have an entry for operator Enum fields,
    # we are adding it here for our use rather than adding in neutron.
    test_base.FIELD_TYPE_VALUE_GENERATOR_MAP[
        oslo_versionedobjects.fields.EnumField] = tools.get_random_operator
    _test_class = classifications.ClassificationGroup

    def test_get_object(self):
        cg = self._create_test_cg('Test Group 0')
        fetch_cg = classifications.ClassificationGroup.get_object(
            self.ctx, id=cg.id)
        self.assertEqual(cg, fetch_cg)

    def test_get_objects(self):
        cg1 = self._create_test_cg('Test Group 1')
        cg2 = self._create_test_cg('Test Group 2')
        cgs = classifications.ClassificationGroup.get_objects(self.ctx)
        self.assertIn(cg1, cgs)
        self.assertIn(cg2, cgs)


# NOTE(ndahiwade): Currently BaseDbObjectTestCase doesn't have support for
# mapping class inheritence (polymorphic_identity), and as this is unique to
# CCF we have decided not to use it for tests for individual classifications.
class UDPClassificationTest(testlib_api.SqlTestCase,
                            obj_base._CCFObjectsTestCommon):

    test_class = classifications.UDPClassification

    def test_get_object(self):
        udp = self._create_test_classification('udp', self.test_class)
        fetch_udp = self.test_class.get_object(self.ctx, id=udp.id)
        self.assertEqual(udp, fetch_udp)

    def test_get_objects(self):
        udp1 = self._create_test_classification('udp', self.test_class)
        udp2 = self._create_test_classification('udp', self.test_class)
        fetch_udps = self.test_class.get_objects(self.ctx)
        self.assertIn(udp1, fetch_udps)
        self.assertIn(udp2, fetch_udps)


class IPV4ClassificationTest(testlib_api.SqlTestCase,
                             obj_base._CCFObjectsTestCommon):

    test_class = classifications.IPV4Classification

    def test_get_object(self):
        ipv4 = self._create_test_classification('ipv4', self.test_class)
        fetch_ipv4 = self.test_class.get_object(self.ctx, id=ipv4.id)
        self.assertEqual(ipv4, fetch_ipv4)

    def test_get_objects(self):
        ipv4_1 = self._create_test_classification('ipv4', self.test_class)
        ipv4_2 = self._create_test_classification('ipv4', self.test_class)
        fetch_ipv4s = self.test_class.get_objects(self.ctx)
        self.assertIn(ipv4_1, fetch_ipv4s)
        self.assertIn(ipv4_2, fetch_ipv4s)


class IPV6ClassificationTest(testlib_api.SqlTestCase,
                             obj_base._CCFObjectsTestCommon):

    test_class = classifications.IPV6Classification

    def test_get_object(self):
        ipv6 = self._create_test_classification('ipv6', self.test_class)
        fetch_ipv6 = self.test_class.get_object(self.ctx, id=ipv6.id)
        self.assertEqual(ipv6, fetch_ipv6)

    def test_get_objects(self):
        ipv6_1 = self._create_test_classification('ipv6', self.test_class)
        ipv6_2 = self._create_test_classification('ipv6', self.test_class)
        fetch_ipv6s = self.test_class.get_objects(self.ctx)
        self.assertIn(ipv6_1, fetch_ipv6s)
        self.assertIn(ipv6_2, fetch_ipv6s)


class TCPClassificationTest(testlib_api.SqlTestCase,
                            obj_base._CCFObjectsTestCommon):

    test_class = classifications.TCPClassification

    def test_get_object(self):
        tcp = self._create_test_classification('tcp', self.test_class)
        fetch_tcp = self.test_class.get_object(self.ctx, id=tcp.id)
        self.assertEqual(tcp, fetch_tcp)

    def test_get_objects(self):
        tcp_1 = self._create_test_classification('tcp', self.test_class)
        tcp_2 = self._create_test_classification('tcp', self.test_class)
        fetch_tcps = self.test_class.get_objects(self.ctx)
        self.assertIn(tcp_1, fetch_tcps)
        self.assertIn(tcp_2, fetch_tcps)


class EthernetClassificationTest(testlib_api.SqlTestCase,
                                 obj_base._CCFObjectsTestCommon):

    test_class = classifications.EthernetClassification

    def test_get_object(self):
        ethernet = self._create_test_classification('ethernet',
                                                    self.test_class)
        fetch_ethernet = self.test_class.get_object(self.ctx, id=ethernet.id)
        self.assertEqual(ethernet, fetch_ethernet)

    def test_get_objects(self):
        ethernet_1 = self._create_test_classification('ethernet',
                                                      self.test_class)
        ethernet_2 = self._create_test_classification('ethernet',
                                                      self.test_class)
        fetch_ethernets = self.test_class.get_objects(self.ctx)
        self.assertIn(ethernet_1, fetch_ethernets)
        self.assertIn(ethernet_2, fetch_ethernets)


class CGToClassificationGroupMappingTest(testlib_api.SqlTestCase,
                                         obj_base._CCFObjectsTestCommon):

    def test_get_object(self):
        with db_api.context_manager.writer.using(self.ctx):
            cg1 = self._create_test_cg('Test Group 0')
            cg2 = self._create_test_cg('Test Group 1')
            cg_m_cg = self._create_test_cg_cg_mapping(cg1.id, cg2.id)
            fetch_cg = classifications.ClassificationGroup.get_object(
                self.ctx, id=cg1.id)
            mapped_cg = classifications._get_mapped_classification_groups(
                self.ctx, fetch_cg)
            fetch_cg_m_cg = classifications.CGToClassificationGroupMapping.\
                get_object(self.ctx, id=cg_m_cg.container_cg_id)
            self.assertEqual(mapped_cg[0], cg2)
            self.assertEqual(cg_m_cg, fetch_cg_m_cg)

    def test_multiple_cg_mappings(self):
        with db_api.context_manager.writer.using(self.ctx):
            cg1 = self._create_test_cg('Test Group 0')
            cg2 = self._create_test_cg('Test Group 1')
            cg3 = self._create_test_cg('Test Group 2')
            cg4 = self._create_test_cg('Test Group 3')
            cgs = [cg2, cg3, cg4]
            for cg in cgs:
                self._create_test_cg_cg_mapping(cg1.id, cg.id)
            fetch_cg1 = classifications.ClassificationGroup.get_object(
                self.ctx, id=cg1.id)
            mapped_cgs = classifications._get_mapped_classification_groups(
                self.ctx, fetch_cg1)
            for cg in cgs:
                self.assertIn(cg, mapped_cgs)


class CGToClassificationMappingTest(testlib_api.SqlTestCase,
                                    obj_base._CCFObjectsTestCommon):

    ctx = context.get_admin_context()

    def test_get_object(self):
        with db_api.context_manager.writer.using(self.ctx):
            cg = self._create_test_cg('Test Group')
            cl_ = self._create_test_classification(
                'udp', classifications.UDPClassification)
            cg_m_c = self._create_test_cg_c_mapping(cg.id, cl_.id)
            fetch_c = classifications.UDPClassification.get_object(
                self.ctx, id=cl_.id)
            fetch_cg = classifications.ClassificationGroup.get_object(
                self.ctx, id=cg.id)
            mapped_cs = classifications._get_mapped_classifications(
                self.ctx, fetch_cg)
            fetch_cg_m_c = classifications.CGToClassificationMapping. \
                get_object(self.ctx, id=cg_m_c.container_cg_id)
            self.assertIn(fetch_c, mapped_cs)
            self.assertEqual(cg_m_c, fetch_cg_m_c)

    def test_multiple_c_mappings(self):
        with db_api.context_manager.writer.using(self.ctx):
            cg = self._create_test_cg('Test Group')
            c1 = self._create_test_classification(
                'tcp', classifications.TCPClassification)
            c2 = self._create_test_classification(
                'udp', classifications.UDPClassification)
            c3 = self._create_test_classification(
                'ethernet', classifications.EthernetClassification)
            cs = [c1, c2, c3]
            for c in cs:
                self._create_test_cg_c_mapping(cg.id, c.id)
            fetch_cg = classifications.ClassificationGroup.get_object(
                self.ctx, id=cg.id)
            mapped_cs = classifications._get_mapped_classifications(
                self.ctx, fetch_cg)
            for c in cs:
                self.assertIn(c, mapped_cs)
