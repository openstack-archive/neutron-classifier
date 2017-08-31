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

from neutron_classifier.db import models
from neutron_classifier.tests import base


from oslo_utils import uuidutils


class TestDatabaseModels(base.BaseClassificationTestCase):

    class _MockServicePlugin(object):

        def __init__(self):

            self.standard_group = {'id': uuidutils.generate_uuid(),
                                   'name': 'Test Group',
                                   'description': "Description of test group",
                                   'project_id': uuidutils.generate_uuid(),
                                   'classifications': [],
                                   'classification_groups': [],
                                   'shared': True,
                                   'operator': 'AND'}

        def _create_fake_model(self, **kwargs):
            model1 = models.ClassificationGroup(**kwargs)
            return model1

    def setUp(self):
        super(TestDatabaseModels, self).setUp()

        self.mock_plugin = self._MockServicePlugin()

    def test_generate_dict_from_cg_db(self):
        model = self.mock_plugin._create_fake_model(
            **self.mock_plugin.standard_group)
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
