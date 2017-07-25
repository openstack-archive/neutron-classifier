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
from neutron_classifier.db import classification as cg_api
from neutron_classifier.objects import classifications

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
                'classifications': [self.c_id1, self.c_id2],
                'classification_groups': [self.cg_id]}
        }
        return self.test_cg

    @mock.patch.object(classifications.CGToClassificationGroupMapping,
                       'create')
    @mock.patch.object(classifications.CGToClassificationMapping, 'create')
    @mock.patch.object(classifications.ClassificationGroup, 'create')
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

        c_len = len(val['classifications'])
        cg_len = len(val['classification_groups'])
        mock_call_len = len(mock_manager.mock_calls)
        self.assertEqual(mock_call_len, c_len + cg_len + 1)

        mock_manager.create_cg.assert_called_once()
        mock_manager.create_cg_cg.assert_called_once()
        self.assertEqual(mock_manager.create_cg_c.call_count, c_len)

    @mock.patch.object(classifications.ClassificationGroup, 'get_object')
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

    def _mock_mapped_classifications(self):
        self.mock_c1 = mock.Mock(id=uuidutils.generate_uuid(),
                                 name='Ethernet', c_type='ethernet',
                                 **self.test_classification_attrs)
        self.mock_c2 = mock.Mock(id=uuidutils.generate_uuid(), name='TCP',
                                 c_type='tcp',
                                 **self.test_classification_attrs)
        return [self.mock_c1, self.mock_c2]

    @mock.patch('neutron_classifier.objects.classifications.'
                '_get_mapped_classification_groups')
    @mock.patch('neutron_classifier.objects.classifications.'
                '_get_mapped_classifications')
    @mock.patch.object(classifications.ClassificationGroup, 'get_object')
    def test_get_classification_group(self, mock_cg_get,
                                      mock_mapped_classifications,
                                      mock_mapped_cgs):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_cg_get, 'get_cg')
        mock_manager.attach_mock(mock_mapped_classifications, 'get_mapped_cs')
        mock_manager.attach_mock(mock_mapped_cgs, 'get_mapped_cgs')
        mock_manager.reset_mock()

        mock_manager.get_mapped_cs.side_effect =\
            self._mock_mapped_classifications()
        mock_manager.get_mapped_cgs.side_effect = ['cg2']

        test_cg = self._generate_test_classification_group('Test Group')
        test_cg['classification_group'].pop('classifications', None)
        test_cg['classification_group'].pop('classification_groups', None)
        mock_manager.get_cg.return_value = test_cg

        with mock.patch('neutron_classifier.db.classification.'
                        'TrafficClassificationGroupPlugin._make_db_dict',
                        return_value=test_cg):
            val1 = self.cg_plugin.get_classification_group(
                self.ctxt, test_cg['classification_group']['id'])

        self.assertEqual(val1, test_cg)
        mock_manager.get_cg.assert_called_with(
            self.ctxt, id=test_cg['classification_group']['id']
        )
        self.assertEqual(val1['classification_group']['classifications'],
                         self.mock_c1)

        val1['classification_group']['classifications'] =\
            classifications._get_mapped_classifications(self.ctxt,
                                                        test_cg)
        self.assertEqual(val1['classification_group']['classifications'],
                         self.mock_c2)
        self.assertEqual(val1['classification_group']
                         ['classification_groups'], 'cg2')
        mapped_cs_call_count = mock_manager.get_mapped_cs.call_count
        self.assertEqual(2, mapped_cs_call_count)

    @mock.patch.object(base_obj, 'Pager')
    @mock.patch.object(classifications.ClassificationGroup, 'get_objects')
    def test_get_classification_groups(self, mock_cgs_get, mock_pager):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_cgs_get, 'get_cgs')
        mock_manager.attach_mock(mock_pager, 'pager')
        mock_manager.reset_mock()

        test_cg1 = self._generate_test_classification_group('Test Group1')
        test_cg2 = self._generate_test_classification_group('Test Group2')
        test_cg1 = test_cg1['classification_group']
        test_cg2 = test_cg2['classification_group']

        cg1 = classifications.ClassificationGroup(self.ctxt, **test_cg1)
        cg2 = classifications.ClassificationGroup(self.ctxt, **test_cg2)
        cg_list = [cg1, cg2]

        mock_manager.get_cgs.return_value = cg_list

        val = self.cg_plugin.get_classification_groups(self.ctxt)

        self.assertEqual(val, cg_list)
        mock_manager.get_cgs.assert_called_once()
        mock_manager.pager.assert_called_once()
        self.assertEqual(len(mock_manager.mock_calls), 2)

    @mock.patch.object(classifications.ClassificationGroup, 'update_object')
    def test_update_classification_group(self, mock_cg_update):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_cg_update, 'cg_update')
        mock_manager.reset_mock()

        test_cg = self._generate_test_classification_group('Test Group')
        test_cg = test_cg['classification_group']

        cg = classifications.ClassificationGroup(self.ctxt, **test_cg)

        updated_fields = {'name': 'Test Group Updated',
                          'description': 'Updated Description'}

        self.cg_plugin.update_classification_group(self.ctxt, cg.id,
                                                   updated_fields)

        mock_manager.cg_update.assert_called_once()
        mock_manager.cg_update.assert_called_once_with(self.ctxt,
                                                       updated_fields,
                                                       id=cg.id)
