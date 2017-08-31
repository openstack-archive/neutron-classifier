# Copyright 2017 Intel Corporation.
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


import copy

from neutron_classifier.db import models
from neutron_classifier.tests import base

from neutron_lib import context

from oslo_utils import uuidutils


class TestDatabaseModels(base.BaseClassificationTestCase):

    class _MockServicePlugin(object):

        def __init__(self):
            self.cg_list = []

            standard_group = {'name': "Test Group",
                              'description': "Description of test group",
                              'project_id': uuidutils.generate_uuid(),
                              'classifications': '',
                              'classification_groups': '',
                              'shared': True,
                              'operator': 'AND'}
            for n in range(5):
                self.cg_list.append(copy.copy(standard_group))
                self.cg_list[-1]['id'] = uuidutils.generate_uuid()
                self.cg_list[-1]['name'] = "Test Group " + str(n)

            self.cg_to_c_list = [{'container_cg_id': self.cg_list[0]['id'],
                                  'stored_classification_id':
                                      uuidutils.generate_uuid()},
                                 {'container_cg_id': self.cg_list[0]['id'],
                                  'stored_classification_id':
                                      uuidutils.generate_uuid()},
                                 {'container_cg_id': self.cg_list[0]['id'],
                                  'stored_classification_id':
                                      uuidutils.generate_uuid()},
                                 {'container_cg_id': self.cg_list[1]['id'],
                                  'stored_classification_id':
                                      uuidutils.generate_uuid()},
                                 {'container_cg_id': self.cg_list[2]['id'],
                                  'stored_classification_id':
                                      uuidutils.generate_uuid()},
                                 {'container_cg_id': self.cg_list[3]['id'],
                                  'stored_classification_id':
                                      uuidutils.generate_uuid()}]

            self.cg_to_cg_list = [{'container_cg_id': self.cg_list[0]['id'],
                                   'stored_cg_id': self.cg_list[1]['id']},
                                  {'container_cg_id': self.cg_list[0]['id'],
                                   'stored_cg_id': self.cg_list[2]['id']},
                                  {'container_cg_id': self.cg_list[0]['id'],
                                   'stored_cg_id': self.cg_list[3]['id']},
                                  {'container_cg_id': self.cg_list[4]['id'],
                                   'stored_cg_id': self.cg_list[1]['id']},
                                  {'container_cg_id': self.cg_list[4]['id'],
                                   'stored_cg_id': self.cg_list[2]['id']},
                                  {'container_cg_id': self.cg_list[4]['id'],
                                   'stored_cg_id': self.cg_list[3]['id']}]

        def _create_fake_model(self, model):
            model1 = model()
            if model == models.ClassificationGroup:
                model1.id = self.cg_list[0]['id']
                model1.name = self.cg_list[0]['name']
                model1.description = self.cg_list[0]['description']
                model1.project_id = self.cg_list[0]['project_id']
                model1.classifications = ''
                model1.classification_groups = ''
                model1.shared = self.cg_list[0]['shared']
                model1.operator = self.cg_list[0]['operator']
            elif model == models.CGToClassificationMapping:
                model1.container_cg_id = self.cg_to_c_list[0][
                    'container_cg_id']
                model1.stored_classification_id = self.cg_to_c_list[0][
                    'stored_classification_id']
            elif model == models.CGToClassificationGroupMapping:
                model1.container_cg_id = self.cg_to_cg_list[0][
                    'container_cg_id']
                model1.stored_cg_id = self.cg_to_cg_list[0]['stored_cg_id']
            return model1

        def _get_collection(self, context, model, function):
            if model == models.ClassificationGroup:
                return copy.deepcopy(self.cg_list)
            elif model == models.CGToClassificationMapping:
                return copy.deepcopy(self.cg_to_c_list)
            elif model == models.CGToClassificationGroupMapping:
                return copy.deepcopy(self.cg_to_cg_list)

    def setUp(self):
        super(TestDatabaseModels, self).setUp()

        self.ctxt = context.Context('fake_user', 'fake_tenant')
        self.mock_plugin = self._MockServicePlugin()

    def test_read_classification_groups_without_id(self):
        ret = models._read_classification_groups(self.mock_plugin, self.ctxt)

        cg_ids = []
        for cg in ret:
            cg_ids.append(cg['id'])
            if cg['name'] == 'Test Group 0':
                class_group_0 = cg
            if cg['name'] == 'Test Group 4':
                class_group_4 = cg

        self.assertIn(self.mock_plugin.cg_list[0]['id'], cg_ids)
        self.assertIn(self.mock_plugin.cg_list[1]['id'], cg_ids)
        self.assertIn(self.mock_plugin.cg_list[2]['id'], cg_ids)
        self.assertIn(self.mock_plugin.cg_list[3]['id'], cg_ids)
        self.assertIn(self.mock_plugin.cg_list[4]['id'], cg_ids)

        self.assertIn(self.mock_plugin.cg_list[1]['id'],
                      class_group_0['classification_groups'])
        self.assertIn(self.mock_plugin.cg_list[2]['id'],
                      class_group_0['classification_groups'])
        self.assertIn(self.mock_plugin.cg_list[3]['id'],
                      class_group_0['classification_groups'])
        self.assertNotIn(self.mock_plugin.cg_list[4]['id'],
                         class_group_0['classification_groups'])

        self.assertIn(self.mock_plugin.cg_list[1]['id'],
                      class_group_4['classification_groups'])
        self.assertIn(self.mock_plugin.cg_list[2]['id'],
                      class_group_4['classification_groups'])
        self.assertIn(self.mock_plugin.cg_list[3]['id'],
                      class_group_4['classification_groups'])
        self.assertNotIn(self.mock_plugin.cg_list[0]['id'],
                         class_group_4['classification_groups'])

    def test_read_classification_groups_with_id(self):
        funct = models._read_classification_groups
        ret = funct(self.mock_plugin, self.ctxt,
                    self.mock_plugin.cg_list[0]['id'])
        self.assertEqual(ret['name'], self.mock_plugin.cg_list[0]['name'])
        self.assertEqual(ret['id'], self.mock_plugin.cg_list[0]['id'])

        self.assertIn(self.mock_plugin.cg_list[1]['id'],
                      ret['classification_groups'])
        self.assertIn(self.mock_plugin.cg_list[2]['id'],
                      ret['classification_groups'])
        self.assertIn(self.mock_plugin.cg_list[3]['id'],
                      ret['classification_groups'])
        self.assertNotIn(self.mock_plugin.cg_list[4]['id'],
                         ret['classification_groups'])
        self.assertNotEqual(self.mock_plugin.cg_list[0]['classifications'],
                            ret['classifications'])

    def test_generate_dict_from_cg_db(self):
        model = self.mock_plugin._create_fake_model(models.ClassificationGroup)
        ret = models._generate_dict_from_cg_db(model)
        self.assertEqual(ret['name'], model.name)
        self.assertEqual(ret['id'], model.id)
        self.assertEqual(ret['description'], model.description)
        self.assertEqual(ret['project_id'], model.project_id)
        self.assertEqual(ret['classifications'], model.classifications)
        self.assertEqual(ret['classification_groups'],
                         model.classification_groups)
        self.assertEqual(ret['shared'], model.shared)
        self.assertEqual(ret['operator'], model.operator)

    def test_generate_dict_from_cgmapping_db(self):
        model1 = self.mock_plugin._create_fake_model(
            models.CGToClassificationMapping)
        model2 = self.mock_plugin._create_fake_model(
            models.CGToClassificationGroupMapping)
        ret1 = models._generate_dict_from_cgmapping_db(model1)
        ret2 = models._generate_dict_from_cgmapping_db(model2)
        self.assertEqual(ret1['container_cg_id'], model1.container_cg_id)
        self.assertEqual(ret1['stored_classification_id'],
                         model1.stored_classification_id)
        self.assertEqual(ret2['container_cg_id'], model2.container_cg_id)
        self.assertEqual(ret2['stored_cg_id'], model2.stored_cg_id)
