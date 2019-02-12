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

import mock
from neutron.objects import base as base_obj
from neutron.objects import classification as cs_base
from neutron_classifier.db import classification as cg_api
from neutron_classifier.tests import base
from neutron_lib import context
from oslo_utils import uuidutils


class TestClassificationGroupPlugin(base.BaseClassificationTestCase):

    def setUp(self):
        super(TestClassificationGroupPlugin, self).setUp()
        self.setup_coreplugin(load_plugins=False)

        mock.patch('neutron.objects.db.api.create_object').start()
        mock.patch('neutron.objects.db.api.update_object').start()
        mock.patch('neutron.objects.db.api.delete_object').start()
        mock.patch('neutron.objects.db.api.get_object').start()

        self.cg_plugin = cg_api.TrafficClassificationGroupPlugin()

        self.ctxt = context.Context('fake_user', 'fake_tenant')
        mock.patch.object(self.ctxt.session, 'refresh').start()
        mock.patch.object(self.ctxt.session, 'expunge').start()

        self.validator_classifications = mock.patch(
            'neutron_classifier.common.validators.check_valid_classifications')
        self.validator_cg = mock.patch(
            'neutron_classifier.common.validators.'
            'check_valid_classification_groups')
        self.validator_cg.start()
        self.validator_classifications.start()

        self.test_classification_attrs = {
            'description': 'Test Classification',
            'project_id': uuidutils.generate_uuid(),
            'shared': True,
            'negated': True,
        }

    def _generate_test_classification_group(self, name):
        self.cg_id = uuidutils.generate_uuid()
        self.c_id1 = uuidutils.generate_uuid()
        self.c_id2 = uuidutils.generate_uuid()

        self.test_cg = {
            'classification_group': {
                'name': name,
                'id': uuidutils.generate_uuid(),
                'description': "Description of test group",
                'project_id': uuidutils.generate_uuid(),
                'operator': 'AND',
                'shared': False,
                'classification': [self.c_id1, self.c_id2],
                'classification_group': [self.cg_id]}
        }
        return self.test_cg

    @mock.patch.object(cs_base.CGToClassificationGroupMapping,
                       'create')
    @mock.patch.object(cs_base.CGToClassificationMapping, 'create')
    @mock.patch.object(cs_base.ClassificationGroup, 'create')
    def test_create_classification_group(self, mock_cg_create,
                                         mock_cg_c_mapping_create,
                                         mock_cg_cg_mapping_create):

        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_cg_create, 'create_cg')
        mock_manager.attach_mock(mock_cg_c_mapping_create, 'create_cg_c')
        mock_manager.attach_mock(mock_cg_cg_mapping_create, 'create_cg_cg')
        mock_manager.reset_mock()

        test_cg = self._generate_test_classification_group('Test Group')
        test_cg['classification_group'].pop('id', None)

        val = self.cg_plugin.create_classification_group(self.ctxt,
                                                         test_cg)

        expected_val = test_cg['classification_group']

        self.assertEqual(val, expected_val)

        c_len = len(val['classification'])
        cg_len = len(val['classification_group'])
        mock_call_len = len(mock_manager.mock_calls)
        self.assertEqual(mock_call_len, c_len + cg_len + 1)

        mock_manager.create_cg.assert_called_once()
        mock_manager.create_cg_cg.assert_called_once()
        self.assertEqual(mock_manager.create_cg_c.call_count, c_len)

    @mock.patch.object(cs_base.ClassificationGroup, 'get_object')
    @mock.patch('neutron_classifier.common.validators.'
                'check_can_delete_classification_group')
    def test_delete_classification_group(self, mock_valid_delete,
                                         mock_cg_get):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_valid_delete, 'valid_del')
        mock_manager.attach_mock(mock_cg_get, 'get_cg')
        mock_manager.reset_mock()

        mock_manager.valid_del.return_value = True

        mock_cg_id = uuidutils.generate_uuid()

        self.cg_plugin.delete_classification_group(self.ctxt, mock_cg_id)

        mock_cg_delete_call = mock.call.get_cg().delete()
        mock_cg_check_validity = mock.call.valid_del(self.ctxt, mock_cg_id)
        mock_cg_get_call = mock.call.get_cg(self.ctxt, id=mock_cg_id)

        mock_cg_delete_call.assert_called_once()
        mock_cg_get_call.assert_called_once_with(mock_cg_id)
        mock_cg_check_validity.assert_called()
        self.assertEqual(3, len(mock_manager.mock_calls))
        self.assertTrue(
            mock_manager.mock_calls.index(mock_cg_check_validity) <
            mock_manager.mock_calls.index(mock_cg_get_call) <
            mock_manager.mock_calls.index(mock_cg_delete_call))

    @mock.patch('neutron_classifier.objects.classifications.'
                '_get_mapped_classification_groups')
    @mock.patch('neutron_classifier.objects.classifications.'
                '_get_mapped_classifications')
    @mock.patch.object(cs_base.ClassificationGroup, 'get_object')
    @mock.patch('neutron_classifier.db.classification.'
                'TrafficClassificationGroupPlugin._make_db_dicts')
    def test_get_classification_group(self, mock_db_dicts, mock_cg_get,
                                      mock_mapped_classifications,
                                      mock_mapped_cgs):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_db_dicts, 'make_db_dicts')
        mock_manager.attach_mock(mock_cg_get, 'get_cg')
        mock_manager.attach_mock(mock_mapped_classifications, 'get_mapped_cs')
        mock_manager.attach_mock(mock_mapped_cgs, 'get_mapped_cgs')
        mock_manager.reset_mock()

        test_cg = self._generate_test_classification_group('Test Group')
        test_cg['classification_group'].pop('classifications', None)
        test_cg['classification_group'].pop('classification_groups', None)
        mock_manager.get_cg.return_value = test_cg

        with mock.patch('neutron_classifier.db.classification.'
                        'TrafficClassificationGroupPlugin._make_db_dict',
                        return_value=test_cg):
            with mock.patch('neutron_classifier.db.classification.'
                            'TrafficClassificationGroupPlugin._make_c_dicts'):
                val1 = self.cg_plugin.get_classification_group(
                    self.ctxt, test_cg['classification_group']['id'])

        self.assertEqual(val1, test_cg)
        mock_manager.get_cg.assert_called_with(
            self.ctxt, id=test_cg['classification_group']['id']
        )

        mock_manager_call_count = len(mock_manager.mock_calls)
        self.assertEqual(4, mock_manager_call_count)
        mock_db_dicts.assert_called_once()
        mock_cg_get.assert_called_once()
        mock_mapped_classifications.assert_called_once()
        mock_mapped_cgs.assert_called_once()

    @mock.patch.object(base_obj, 'Pager')
    @mock.patch.object(cs_base.ClassificationGroup, 'get_objects')
    @mock.patch.object(cg_api.TrafficClassificationGroupPlugin,
                       '_make_db_dicts')
    def test_get_classification_groups(self, mock_db_dicts, mock_cgs_get,
                                       mock_pager):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_cgs_get, 'get_cgs')
        mock_manager.attach_mock(mock_pager, 'pager')
        mock_manager.attach_mock(mock_db_dicts, 'db_dicts')
        mock_manager.reset_mock()

        test_cg1 = self._generate_test_classification_group('Test Group1')
        test_cg2 = self._generate_test_classification_group('Test Group2')
        test_cg1 = test_cg1['classification_group']
        test_cg2 = test_cg2['classification_group']

        cg1 = cs_base.ClassificationGroup(self.ctxt, **test_cg1)
        cg2 = cs_base.ClassificationGroup(self.ctxt, **test_cg2)
        cg_list = [self.cg_plugin._make_db_dict(cg) for cg in [cg1, cg2]]

        mock_manager.get_cgs.return_value = cg_list

        self.cg_plugin.get_classification_groups(self.ctxt)

        mock_manager.get_cgs.assert_called_once()
        mock_manager.pager.assert_called_once()
        mock_manager.db_dicts.assert_called_once()
        self.assertEqual(len(mock_manager.mock_calls), 3)

    @mock.patch.object(cs_base.ClassificationGroup, 'update_object')
    def test_update_classification_group(self, mock_cg_update):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_cg_update, 'cg_update')
        mock_manager.reset_mock()

        test_cg = self._generate_test_classification_group('Test Group')
        test_cg = test_cg['classification_group']

        cg = cs_base.ClassificationGroup(self.ctxt, **test_cg)

        updated_fields = {'classification_group':
                          {'name': 'Test Group Updated',
                           'description': 'Updated Description'}}

        self.cg_plugin.update_classification_group(self.ctxt, cg.id,
                                                   updated_fields)
        updated_fields_called = {'name': 'Test Group Updated',
                                 'description': 'Updated Description'}

        mock_manager.cg_update.assert_called_once()
        mock_manager.cg_update.assert_called_once_with(self.ctxt,
                                                       updated_fields_called,
                                                       id=cg.id)
