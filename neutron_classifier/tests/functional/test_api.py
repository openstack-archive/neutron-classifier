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

from neutron_classifier.db.classification import\
    TrafficClassificationGroupPlugin as cg_plugin
from neutron_classifier.objects import classifications
from neutron_classifier.tests import objects_base as obj_base


class ClassificationGroupApiTest(testlib_api.MySQLTestCaseMixin,
                                 testlib_api.SqlTestCase,
                                 obj_base._CCFObjectsTestCommon):
    def setUp(self):
        super(ClassificationGroupApiTest, self).setUp()
        self.test_plugin = cg_plugin()

    def test_get_classification_group(self):
        cg = self._create_test_cg('Test Group 0')
        fetch_cg = self.test_plugin.get_classification_group(self.ctx, cg.id)
        self.assertEqual(cg, fetch_cg)

    def test_get_classification_groups(self):
        cg1 = self._create_test_cg('Test Group 1')
        cg2 = self._create_test_cg('Test Group 2')
        cgs = self.test_plugin.get_classification_groups(self.ctx)
        self.assertIn(cg1, cgs)
        self.assertIn(cg2, cgs)

    def test_create_classification_group(self):
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
        with db_api.context_manager.writer.using(self.ctx):
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
        cg1 = self._create_test_cg('Test Group 0')
        self.test_plugin.update_classification_group(
            self.ctx, cg1.id, {'name': 'Test Group updated'})
        fetch_cg1 = classifications.ClassificationGroup.get_object(
            self.ctx, id=cg1['id'])
        self.assertEqual(fetch_cg1.name, 'Test Group updated')

    def test_delete_classification_group(self):
        cg1 = self._create_test_cg('Test Group 0')
        self.test_plugin.delete_classification_group(self.ctx, cg1.id)
        fetch_cg1 = classifications.ClassificationGroup.get_object(
            self.ctx, id=cg1['id'])
        self.assertIsNone(fetch_cg1)
