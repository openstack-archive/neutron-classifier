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

from neutron.db import _model_query as mq
from neutron_classifier.db import models
from neutron_classifier.tests import base

from neutron_lib import context

from oslo_utils import uuidutils


class TestDatabaseModels(base.BaseClassificationTestCase):

    class _MockServicePlugin(object):

        def __init__(self):
            self.cg_list = []

            ctx = context.get_admin_context()

            standard_group = {'description': "Description of test group",
                              'project_id': uuidutils.generate_uuid(),
                              'shared': True,
                              'operator': 'AND'}

            for n in range(4):
                standard_group['name'] = "Test Group" + str(n)
                standard_group['id'] = uuidutils.generate_uuid()
                self._create_db_model(ctx, models.ClassificationGroup,
                                      **standard_group)
                self.cg_list.append(copy.copy(standard_group))

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
                                      uuidutils.generate_uuid()}]

            self.cg_to_cg_list = [{'container_cg_id': self.cg_list[0]['id'],
                                   'stored_cg_id': self.cg_list[1]['id']},
                                  {'container_cg_id': self.cg_list[0]['id'],
                                   'stored_cg_id': self.cg_list[2]['id']},
                                  {'container_cg_id': self.cg_list[0]['id'],
                                   'stored_cg_id': self.cg_list[3]['id']},
                                  {'container_cg_id': self.cg_list[3]['id'],
                                   'stored_cg_id': self.cg_list[1]['id']},
                                  {'container_cg_id': self.cg_list[3]['id'],
                                   'stored_cg_id': self.cg_list[2]['id']}]

            for n in range(4):
                self._create_db_model(ctx, models.CGToClassificationMapping,
                                      **self.cg_to_c_list[n])
                self._create_db_model(ctx,
                                      models.CGToClassificationGroupMapping,
                                      **self.cg_to_cg_list[n])

        def _create_db_model(self, ctx, model, **kwargs):
            model1 = model(**kwargs)
            with ctx.session.begin(subtransactions=True):
                ctx.session.add(model1)

        def _create_fake_model(self, **kwargs):
            model1 = models.ClassificationGroup(**kwargs)
            return model1

        def _get_collection(self, ctx, model, function):
            return mq.get_collection(ctx, model,
                                     models._generate_dict_from_cg_db)

    def setUp(self):
        super(TestDatabaseModels, self).setUp()

        self.ctxt = context.get_admin_context()
        self.mock_plugin = self._MockServicePlugin()

    def test_read_classification_group(self):
        ret = models._read_classification_group(self.ctxt,
                                                self.mock_plugin.cg_list[0]
                                                ['id'])
        cg = self.mock_plugin.cg_list[0]
        self.assertEqual(ret.name, cg['name'])
        self.assertEqual(ret.description, cg['description'])
        self.assertEqual(ret.shared, cg['shared'])
        self.assertEqual(ret.operator, cg['operator'])

    def test_read_classifications(self):
        ret = models._read_classifications(self.ctxt,
                                           self.mock_plugin.cg_list[0]['id'])
        cg = self.mock_plugin.cg_list[0]
        self.assertEqual(len(ret), 3)
        self.assertEqual(ret[0].container_cg_id, cg['id'])
        self.assertEqual(ret[1].container_cg_id, cg['id'])
        self.assertEqual(ret[2].container_cg_id, cg['id'])

    def test_read_classification_groups(self):
        ret = models._read_classification_groups(self.ctxt,
                                                 self.mock_plugin.cg_list[0]
                                                 ['id'])
        cg = self.mock_plugin.cg_list[0]
        self.assertEqual(len(ret), 3)
        self.assertEqual(ret[0].container_cg_id, cg['id'])
        self.assertEqual(ret[1].container_cg_id, cg['id'])
        self.assertEqual(ret[2].container_cg_id, cg['id'])

    def test_read_all_classification_groups(self):
        ret = models._read_classification_groups(self.mock_plugin, self.ctxt)
        cgs = [x.name for x in ret]
        self.assertIn("Test Group 0", cgs)
        self.assertIn("Test Group 1", cgs)
        self.assertIn("Test Group 2", cgs)
        self.assertIn("Test Group 3", cgs)

    def test_generate_dict_from_cg_db(self):
        model = self.mock_plugin._create_fake_model(
            self.mock_plugin.cg_list[0])
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

    def test_cleanup(self):
        ret = models._read_classification_groups(self.mock_plugin, self.ctxt)
        for cg in ret:
            self.ctxt.session.delete(cg)
