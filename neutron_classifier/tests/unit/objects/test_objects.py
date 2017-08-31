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

from oslo_utils import uuidutils
import oslo_versionedobjects

from neutron_classifier.objects import classifications
from neutron_classifier.tests import tools

from neutron_lib import context

from neutron.tests.unit.objects import test_base
from neutron.tests.unit import testlib_api


class _CCFObjectsTestCommon(object):

    # TODO(ndahiwade): this represents classifications containing Enum fields,
    # will need to be reworked if more classifications are added here later.
    _Enum_classifications = [classifications.IPV4Classification,
                             classifications.IPV6Classification]
    _Enumfield = oslo_versionedobjects.fields.EnumField
    ctx = context.get_admin_context()

    def get_random_attrs(self, obj=None):
        obj = obj
        attrs = {}
        for field, field_obj in obj.fields.items():
            if field != 'c_type' and type(field_obj) != self._Enumfield:
                random_generator = test_base.FIELD_TYPE_VALUE_GENERATOR_MAP[
                    type(field_obj)]
                attrs[field] = random_generator()
        return attrs

    def _create_test_cg(self, name):
        attrs = {'name': name,
                 'id': uuidutils.generate_uuid(),
                 'description': "Description of test group",
                 'project_id': uuidutils.generate_uuid(),
                 'operator': 'AND'}
        cg = classifications.ClassificationGroup(self.context, **attrs)
        cg.create()
        return cg

    def _create_test_classification(self, c_type, classification):
        attrs = self.get_random_attrs(classification)
        if classification in self._Enum_classifications:
            attrs['ecn'] = tools.get_random_ecn()
        attrs['c_type'] = c_type
        c = classification(self.ctx, **attrs)
        c.create()
        return c


class ClassificationGroupTest(test_base.BaseDbObjectTestCase,
                              testlib_api.SqlTestCase,
                              _CCFObjectsTestCommon):
    # NOTE(ndahiwade): As the FIELD_TYPE_VALUE_GENERATOR_MAP in neutron's
    # test_base for objects doesn't have an entry for Enum fields, we are
    # adding it here for our use rather than adding in neutron.
    test_base.FIELD_TYPE_VALUE_GENERATOR_MAP[
        oslo_versionedobjects.fields.EnumField] = tools.get_random_operator
    _test_class = classifications.ClassificationGroup

    def test_get_object(self):
        cg = self._create_test_cg('Test Group 0')
        fetch_cg = classifications.ClassificationGroup.get_object(
            self.context, id=cg.id)
        self.assertEqual(cg, fetch_cg)

    def test_get_objects(self):
        cg1 = self._create_test_cg('Test Group 1')
        cg2 = self._create_test_cg('Test Group 2')
        cgs = classifications.ClassificationGroup.get_objects(self.context)
        self.assertIn(cg1, cgs)
        self.assertIn(cg2, cgs)


# NOTE(ndahiwade): Currently BaseDbObjectTestCase doesn't have support for
# mapping class inheritence (polymorphic_identity), and as this is unique to
# CCF we have decided to not use it for tests for individual classifications.
class UDPClassificationTest(testlib_api.SqlTestCase,
                            _CCFObjectsTestCommon):

    ctx = context.get_admin_context()
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
                             _CCFObjectsTestCommon):

    ctx = context.get_admin_context()
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
                             _CCFObjectsTestCommon):

    ctx = context.get_admin_context()
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
                            _CCFObjectsTestCommon):

    ctx = context.get_admin_context()
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
                                 _CCFObjectsTestCommon):

    ctx = context.get_admin_context()
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
