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


class TestPluginIPV4(base.BaseClassificationTestCase):

    def setUp(self):
        super(TestPluginIPV4, self).setUp()
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

        common._generate_fake_ipv4_classifications(self)

    def test_ipv4_classification_break_out_headers(self):
        cl = self.cl_plugin.break_out_headers(self.fake_ipv4_classification)
        self.fake_ipv4_classification_broken_headers.pop('id', None)
        self.assertEqual(self.fake_ipv4_classification_broken_headers, cl)

    def test_ipv4_merge_header(self):
        cl = self.cl_plugin.merge_header(
            self.fake_ipv4_classification_broken_headers)
        self.assertEqual(self.fake_ipv4_classification['classification'], cl)

    @mock.patch.object(class_group.IPV4Classification, 'create')
    @mock.patch.object(class_group.IPV4Classification, 'id',
                       return_value=uuidutils.generate_uuid())
    def test_create_ipv4_classification(self, mock_ipv4_create, mock_ipv4_id):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_ipv4_create, 'create')
        mock_manager.attach_mock(mock_ipv4_id, 'id')
        mock_manager.reset_mock()
        mock_manager.start()

        self.fake_ipv4_classification['classification'].pop('id', None)

        val = self.cl_plugin.create_classification(
            self.ctxt, self.fake_ipv4_classification)

        expected_val = self.fake_ipv4_classification['classification']
        expected_val['id'] = class_group.IPV4Classification.id

        mock_call = mock.call.IPV4Classification().create()
        self.assertEqual(mock.call.IPV4Classification().create(), mock_call)
        self.assertEqual(expected_val, val)

    @mock.patch.object(class_group.IPV4Classification, 'update')
    def test_update_ipv4_classification(self, mock_ipv4_update):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_ipv4_update, 'update')
        mock_manager.reset_mock()
        mock_manager.start()

        class_obj = class_group.IPV4Classification(
            self.ctxt, **self.fake_ipv4_classification_broken_headers)

        ipv4_classification_update = {
            'name': 'test_ipv4_classification Version 2',
            'description': 'Test IPV4 Classification Version 2',
            'negated': True,
            'shared': True,
            'c_type': 'ipv4',
            'ihl': None,
            'diffserv': 32}

        self.cl_plugin.get_classification = mock.Mock()
        self.cl_plugin._get_by_id = mock.Mock(return_value=class_obj)

        self.cl_plugin.update_classification(
            self.ctxt, class_obj.id,
            {'classification': ipv4_classification_update})

        classification_update_mock_call = mock.call.update(
            {'description': 'Test IPV4 Classification Version 2',
             'name': 'test_ipv4_classification Version 2'})
        self.assertIn(classification_update_mock_call, mock_manager.mock_calls)

    @mock.patch.object(class_group.ClassificationBase, 'get_object')
    @mock.patch.object(class_group.IPV4Classification, 'get_object')
    @mock.patch.object(validators, 'check_valid_classifications')
    def test_delete_ipv4_classification(self, mock_validators, mock_base_get,
                                        mock_ipv4_get):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_base_get, 'get_object')
        mock_manager.attach_mock(mock_ipv4_get, 'get_object')

        ipv4_class_obj = class_group.IPV4Classification(
            self.ctxt, **self.fake_ipv4_classification_broken_headers)
        ipv4_class_obj.delete = mock.Mock()
        base_class_obj = class_group.ClassificationBase(
            self.ctxt, **self.fake_ipv4_classification_broken_headers)

        mock_base_get.return_value = base_class_obj
        mock_ipv4_get.return_value = ipv4_class_obj

        mock_manager.reset_mock()
        self.cl_plugin.delete_classification(
            self.ctxt, base_class_obj.id)

        get_obj_mock_call = mock.call.get_object(
            self.ctxt, id=self.fake_ipv4_classification_broken_headers['id'])
        self.assertIn(get_obj_mock_call, mock_manager.mock_calls)
        self.assertEqual([get_obj_mock_call, get_obj_mock_call],
                         mock_manager.mock_calls)
        self.assertTrue(ipv4_class_obj.delete.assert_called_once)

    @mock.patch.object(class_group.ClassificationBase, 'get_object')
    @mock.patch.object(class_group.IPV4Classification, 'get_object')
    def test_get_ipv4_classification(self, mock_base_get, mock_ipv4_get):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_base_get, 'get_object')
        mock_manager.attach_mock(mock_ipv4_get, 'get_object')

        ipv4_classification = self.fake_ipv4_classification['classification']

        definition = ipv4_classification.pop('definition')

        base_class_obj = class_group.ClassificationBase(
            self.ctxt, **ipv4_classification)
        ipv4_class_obj = class_group.IPV4Classification(
            self.ctxt, **self.fake_ipv4_classification_broken_headers)

        mock_base_get.return_value = ipv4_class_obj
        mock_ipv4_get.return_value = base_class_obj

        ipv4_classification['definition'] = definition

        mock_manager.reset_mock()
        value = self.cl_plugin.get_classification(
            self.ctxt, ipv4_classification['id'])

        get_obj_mock_call = mock.call.get_object(
            self.ctxt, id=ipv4_classification['id'])
        self.assertIn(get_obj_mock_call, mock_manager.mock_calls)
        self.assertEqual([get_obj_mock_call, get_obj_mock_call],
                         mock_manager.mock_calls)
        self.assertTrue(ipv4_classification, value)

    @mock.patch.object(class_group.ClassificationBase, 'get_objects')
    @mock.patch.object(class_group.IPV4Classification, 'get_objects')
    @mock.patch.object(base_obj, 'Pager')
    def test_get_ipv4_classifications(self, mock_pager, mock_ipv4_get,
                                      mock_base_get):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_base_get, 'get_objects')
        mock_manager.attach_mock(mock_ipv4_get, 'get_objects')

        ipv4_cl_1 = self.fake_ipv4_classification['classification']
        ipv4_cl_2 = self.fake_ipv4_classification_2['classification']

        definition = ipv4_cl_1.pop('definition')
        definition_2 = ipv4_cl_2.pop('definition')

        base_class_obj_1 = class_group.ClassificationBase(
            self.ctxt, **ipv4_cl_1)
        base_class_obj_2 = class_group.ClassificationBase(
            self.ctxt, **ipv4_cl_2)
        ipv4_class_obj_1 = class_group.IPV4Classification(
            self.ctxt, **self.fake_ipv4_classification_broken_headers)
        ipv4_class_obj_2 = class_group.IPV4Classification(
            self.ctxt, **self.fake_ipv4_classification_2_broken_headers)

        base_list = [base_class_obj_1, base_class_obj_2]
        ipv4_list = [ipv4_class_obj_1, ipv4_class_obj_2]

        mock_base_get.return_value = base_list
        mock_ipv4_get.return_value = ipv4_list
        mock_pager.return_value = None

        ipv4_cl_1['definition'] = definition
        ipv4_cl_2['defintion'] = definition_2

        result_list = [ipv4_cl_1, ipv4_cl_2]

        mock_manager.reset_mock()
        value = self.cl_plugin.get_classifications(
            self.ctxt, filters={'c_type': ['ipv4']})

        get_objs_mock_call = mock.call.get_objects(
            self.ctxt, _pager=None, c_type=['ipv4'])
        self.assertIn(get_objs_mock_call, mock_manager.mock_calls)
        self.assertEqual([get_objs_mock_call], mock_manager.mock_calls)
        self.assertTrue(result_list, value)
