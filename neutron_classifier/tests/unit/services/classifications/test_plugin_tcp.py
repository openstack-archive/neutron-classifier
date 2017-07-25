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

import mock
from neutron.objects import base as base_obj
from neutron_classifier.common import validators
from neutron_classifier.objects import classifications as class_group
from neutron_classifier.services.classification import plugin
from neutron_classifier.tests.unit import base
from neutron_classifier.tests.unit.services.classifications import common
from neutron_lib import context
from oslo_utils import uuidutils


class TestPluginTCP(base.BaseClassificationTestCase):

    def setUp(self):
        super(TestPluginTCP, self).setUp()
        self.setup_coreplugin(load_plugins=False)

        mock.patch('neutron.objects.db.api.create_object').start()
        mock.patch('neutron.objects.db.api.update_object').start()
        mock.patch('neutron.objects.db.api.delete_object').start()
        mock.patch('neutron.objects.db.api.get_object').start()

        self.cl_plugin = plugin.ClassificationPlugin()

        self.ctxt = context.Context('fake_user', 'fake_tenant')
        mock.patch.object(self.ctxt.session, 'refresh').start()
        mock.patch.object(self.ctxt.session, 'expunge').start()

        mock.patch('neutron_classifier.objects.classifications').start()

        common._generate_fake_tcp_classifications(self)

    def test_tcp_classification_break_out_headers(self):
        cl = self.cl_plugin.break_out_headers(self.fake_tcp_classification)
        self.fake_tcp_classification_broken_headers.pop('id', None)
        self.assertEqual(self.fake_tcp_classification_broken_headers, cl)

    def test_tcp_merge_header(self):
        cl = self.cl_plugin.merge_header(
            self.fake_tcp_classification_broken_headers)
        self.assertEqual(self.fake_tcp_classification['classification'], cl)

    @mock.patch.object(class_group.TCPClassification, 'create')
    @mock.patch.object(class_group.TCPClassification, 'id',
                       return_value=uuidutils.generate_uuid())
    def test_create_tcp_classification(self, mock_tcp_create, mock_tcp_id):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_tcp_create, 'create')
        mock_manager.attach_mock(mock_tcp_id, 'id')
        mock_manager.reset_mock()
        mock_manager.start()

        self.fake_tcp_classification['classification'].pop('id', None)

        val = self.cl_plugin.create_classification(
            self.ctxt, self.fake_tcp_classification)

        expected_val = self.fake_tcp_classification['classification']
        expected_val['id'] = class_group.TCPClassification.id

        mock_call = mock.call.TCPClassification().create()
        self.assertEqual(mock.call.TCPClassification().create(), mock_call)
        self.assertEqual(expected_val, val)

    @mock.patch.object(class_group.TCPClassification, 'update')
    def test_update_tcp_classification(self, mock_tcp_update):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_tcp_update, 'update')
        mock_manager.reset_mock()
        mock_manager.start()

        class_obj = class_group.TCPClassification(
            self.ctxt, **self.fake_tcp_classification_broken_headers)

        tcp_classification_update = {
            'name': 'test_tcp_classification Version 2',
            'description': 'Test TCP Classification Version 2',
            'negated': True,
            'shared': True,
            'window': None,
            'option_kind': 2}

        self.cl_plugin.get_classification = mock.Mock()
        self.cl_plugin._get_by_id = mock.Mock(return_value=class_obj)

        self.cl_plugin.update_classification(
            self.ctxt, class_obj.id,
            {'classification': tcp_classification_update})

        classification_update_mock_call = mock.call.update(
            {'description': 'Test TCP Classification Version 2',
             'name': 'test_tcp_classification Version 2'})
        self.assertIn(classification_update_mock_call, mock_manager.mock_calls)

    @mock.patch.object(class_group.ClassificationBase, 'get_object')
    @mock.patch.object(class_group.TCPClassification, 'get_object')
    @mock.patch.object(validators, 'check_valid_classifications')
    def test_delete_tcp_classification(self, mock_validators, mock_base_get,
                                       mock_tcp_get):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_base_get, 'get_object')
        mock_manager.attach_mock(mock_tcp_get, 'get_object')

        tcp_class_obj = class_group.TCPClassification(
            self.ctxt, **self.fake_tcp_classification_broken_headers)
        tcp_class_obj.delete = mock.Mock()
        base_class_obj = class_group.ClassificationBase(
            self.ctxt, **self.fake_tcp_classification_broken_headers)

        mock_base_get.return_value = base_class_obj
        mock_tcp_get.return_value = tcp_class_obj

        mock_manager.reset_mock()
        self.cl_plugin.delete_classification(
            self.ctxt, base_class_obj.id)

        get_obj_mock_call = mock.call.get_object(
            self.ctxt, id=self.fake_tcp_classification_broken_headers['id'])
        self.assertIn(get_obj_mock_call, mock_manager.mock_calls)
        self.assertEqual([get_obj_mock_call, get_obj_mock_call],
                         mock_manager.mock_calls)
        self.assertTrue(tcp_class_obj.delete.assert_called_once)

    @mock.patch.object(class_group.ClassificationBase, 'get_object')
    @mock.patch.object(class_group.TCPClassification, 'get_object')
    def test_get_tcp_classification(self, mock_base_get, mock_tcp_get):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_base_get, 'get_object')
        mock_manager.attach_mock(mock_tcp_get, 'get_object')

        tcp_classification = self.fake_tcp_classification['classification']

        definition = tcp_classification.pop('definition')

        base_class_obj = class_group.ClassificationBase(
            self.ctxt, **tcp_classification)
        tcp_class_obj = class_group.TCPClassification(
            self.ctxt, **self.fake_tcp_classification_broken_headers)

        mock_base_get.return_value = tcp_class_obj
        mock_tcp_get.return_value = base_class_obj

        tcp_classification['definition'] = definition

        mock_manager.reset_mock()
        value = self.cl_plugin.get_classification(
            self.ctxt, tcp_classification['id'])

        get_obj_mock_call = mock.call.get_object(
            self.ctxt, id=tcp_classification['id'])
        self.assertIn(get_obj_mock_call, mock_manager.mock_calls)
        self.assertEqual([get_obj_mock_call, get_obj_mock_call],
                         mock_manager.mock_calls)
        self.assertTrue(tcp_classification, value)

    @mock.patch.object(class_group.ClassificationBase, 'get_objects')
    @mock.patch.object(class_group.TCPClassification, 'get_objects')
    @mock.patch.object(base_obj, 'Pager')
    def test_get_tcp_classifications(self, mock_pager, mock_tcp_get,
                                     mock_base_get):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_base_get, 'get_objects')
        mock_manager.attach_mock(mock_tcp_get, 'get_objects')

        tcp_cl_1 = self.fake_tcp_classification['classification']
        tcp_cl_2 = self.fake_tcp_classification_2['classification']

        definition = tcp_cl_1.pop('definition')
        definition_2 = tcp_cl_2.pop('definition')

        base_class_obj_1 = class_group.ClassificationBase(
            self.ctxt, **tcp_cl_1)
        base_class_obj_2 = class_group.ClassificationBase(
            self.ctxt, **tcp_cl_2)
        tcp_class_obj_1 = class_group.TCPClassification(
            self.ctxt, **self.fake_tcp_classification_broken_headers)
        tcp_class_obj_2 = class_group.TCPClassification(
            self.ctxt, **self.fake_tcp_classification_2_broken_headers)

        base_list = [base_class_obj_1, base_class_obj_2]
        tcp_list = [tcp_class_obj_1, tcp_class_obj_2]

        mock_base_get.return_value = base_list
        mock_tcp_get.return_value = tcp_list
        mock_pager.return_value = None

        tcp_cl_1['definition'] = definition
        tcp_cl_2['definition'] = definition_2

        result_list = [tcp_cl_1, tcp_cl_2]

        mock_manager.reset_mock()
        value = self.cl_plugin.get_classifications(
            self.ctxt, filters={'c_type': ['tcp']})

        get_objs_mock_call = mock.call.get_objects(
            self.ctxt, _pager=None, c_type=['tcp'])
        self.assertIn(get_objs_mock_call, mock_manager.mock_calls)
        self.assertEqual([get_objs_mock_call], mock_manager.mock_calls)
        self.assertTrue(result_list, value)
