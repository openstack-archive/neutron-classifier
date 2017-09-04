# Copyright (c) 2018 Intel Corporation.
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

from neutron.db import api as db_api
from neutron.tests.unit import testlib_api

from neutron_classifier.common import exceptions
from neutron_classifier.common import validators
from neutron_classifier.db.classification import\
    TrafficClassificationGroupPlugin as cg_plugin
from neutron_classifier.objects import classifications
from neutron_classifier.services.classification.plugin import\
    ClassificationPlugin as c_plugin
from neutron_classifier.tests import objects_base as obj_base


class ClassificationGroupApiTest(testlib_api.MySQLTestCaseMixin,
                                 testlib_api.SqlTestCase,
                                 obj_base._CCFObjectsTestCommon):
    def setUp(self):
        super(ClassificationGroupApiTest, self).setUp()
        self.test_plugin = cg_plugin()

    def test_get_classification_group(self):
        with db_api.context_manager.writer.using(self.ctx):
            cg = self._create_test_cg('Test Group 0')
            cg_dict = self.test_plugin._make_db_dict(cg)
            fetch_cg = self.test_plugin.get_classification_group(self.ctx,
                                                                 cg.id)
        cg_dict['classification_group']['classifications'] =\
            fetch_cg['classification_group']['classifications']
        cg_dict['classification_group']['classification_groups'] = \
            fetch_cg['classification_group']['classification_groups']
        self.assertEqual(cg_dict, fetch_cg)

    def test_get_classification_groups(self):
        with db_api.context_manager.writer.using(self.ctx):
            cg1 = self._create_test_cg('Test Group 1')
            cg2 = self._create_test_cg('Test Group 2')
            cgs = self.test_plugin.get_classification_groups(self.ctx)
        self.assertIn(cg1, cgs)
        self.assertIn(cg2, cgs)

    def test_create_classification_group(self):
        with db_api.context_manager.writer.using(self.ctx):
            tcp_class = classifications.TCPClassification
            ipv4_class = classifications.IPV4Classification
            cg2 = self._create_test_cg('Test Group 1')
            tcp = self._create_test_classification('tcp', tcp_class)
            ipv4 = self._create_test_classification('ipv4', ipv4_class)
            cg_dict = {'classification_group':
                       {'name': 'Test Group 0',
                        'description': "Description of test group",
                        'project_id': uuidutils.generate_uuid(),
                        'operator': 'AND',
                        'classifications': [tcp.id, ipv4.id],
                        'classification_groups': [cg2.id]
                        }}
            cg1 = self.test_plugin.create_classification_group(self.ctx,
                                                               cg_dict)
            fetch_cg1 = classifications.ClassificationGroup.get_object(
                self.ctx, id=cg1['id'])
            mapped_cgs = classifications._get_mapped_classification_groups(
                self.ctx, fetch_cg1)
            mapped_cs = classifications._get_mapped_classifications(
                self.ctx, fetch_cg1)
            mapped_classification_groups = [cg.id for cg in mapped_cgs]
            mapped_classifications = [c.id for c in mapped_cs]
            self.assertEqual(cg1, cg_dict['classification_group'])
            for cg in mapped_classification_groups:
                self.assertIn(
                    cg,
                    cg_dict['classification_group']['classification_groups'])
            for c in mapped_classifications:
                self.assertIn(
                    c, cg_dict['classification_group']['classifications'])

    def test_update_classification_group(self):
        with db_api.context_manager.writer.using(self.ctx):
            cg1 = self._create_test_cg('Test Group 0')
            cg2 = self._create_test_cg('Test Group 1')
            self.test_plugin.update_classification_group(
                self.ctx, cg1.id,
                {'classification_group': {'name': 'Test Group updated'}})
            fetch_cg1 = classifications.ClassificationGroup.get_object(
                self.ctx, id=cg1['id'])
            self.assertRaises(
                exceptions.InvalidUpdateRequest,
                self.test_plugin.update_classification_group,
                self.ctx, cg2.id,
                {'classification_group': {'name': 'Test Group updated',
                                          'operator': 'OR'}})
            self.assertEqual(fetch_cg1.name, 'Test Group updated')

    def test_delete_classification_group(self):
        with db_api.context_manager.writer.using(self.ctx):
            cg1 = self._create_test_cg('Test Group 0')
            self.test_plugin.delete_classification_group(self.ctx, cg1.id)
            fetch_cg1 = classifications.ClassificationGroup.get_object(
                self.ctx, id=cg1['id'])
        self.assertIsNone(fetch_cg1)


class ClassificationApiTest(testlib_api.MySQLTestCaseMixin,
                            testlib_api.SqlTestCase,
                            obj_base._CCFObjectsTestCommon):
    def setUp(self):
        super(ClassificationApiTest, self).setUp()
        self.test_clas_plugin = c_plugin()

    def test_create_classification(self):
        attrs = self.get_random_attrs(classifications.EthernetClassification)
        c_type = 'ethernet'
        attrs['c_type'] = c_type
        attrs['definition'] = {}
        for key in validators.type_validators[c_type].keys():
            attrs['definition'][key] = attrs.pop(key, None)
        c_attrs = {'classification': attrs}
        with db_api.context_manager.writer.using(self.ctx):
            c1 = self.test_clas_plugin.create_classification(self.ctx,
                                                             c_attrs)
            fetch_c1 = classifications.EthernetClassification.get_object(
                self.ctx, id=c1['id']
            )
            c_attrs['classification']['definition']['src_port'] = 'xyz'
        self.assertRaises(exceptions.InvalidClassificationDefintion,
                          self.test_clas_plugin.create_classification,
                          self.ctx, c_attrs)
        eth = c1.pop('definition', None)
        for k, v in c1.items():
            self.assertEqual(v, fetch_c1[k])
        for x, y in eth.items():
            self.assertEqual(y, fetch_c1[x])

    def test_delete_classification(self):
        tcp_class = classifications.TCPClassification
        with db_api.context_manager.writer.using(self.ctx):
            tcp = self._create_test_classification('tcp', tcp_class)
            self.test_clas_plugin.delete_classification(self.ctx, tcp.id)
            fetch_tcp = classifications.TCPClassification.get_object(
                self.ctx, id=tcp.id)
        self.assertIsNone(fetch_tcp)

    def test_get_classification(self):
        ipv4_class = classifications.IPV4Classification
        with db_api.context_manager.writer.using(self.ctx):
            ipv4 = self._create_test_classification('ipv4', ipv4_class)
            fetch_ipv4 = self.test_clas_plugin.get_classification(self.ctx,
                                                                  ipv4.id)
        self.assertEqual(fetch_ipv4, self.test_clas_plugin.merge_header(ipv4))

    def test_get_classifications(self):
        with db_api.context_manager.writer.using(self.ctx):
            c1 = self._create_test_classification(
                'ipv6', classifications.IPV6Classification)
            c2 = self._create_test_classification(
                'udp', classifications.UDPClassification)
            fetch_cs = self.test_clas_plugin.get_classifications(
                self.ctx, filters={'c_type': ['udp', 'ipv6']})
        c1_dict = self.test_clas_plugin.merge_header(c1)
        c2_dict = self.test_clas_plugin.merge_header(c2)
        self.assertIn({'UDPClassifications': [c2_dict]},
                      fetch_cs['classifications'])
        self.assertIn({'IPV6Classifications': [c1_dict]},
                      fetch_cs['classifications'])

    def test_update_classification(self):
        c1 = self._create_test_classification(
            'ethernet', classifications.EthernetClassification)
        updated_name = 'Test Updated Classification'
        with db_api.context_manager.writer.using(self.ctx):
            self.test_clas_plugin.update_classification(
                self.ctx, c1.id, {'classification': {'name': updated_name}})
            fetch_c1 = classifications.EthernetClassification.get_object(
                self.ctx, id=c1.id)
        self.assertEqual(fetch_c1.name, updated_name)
