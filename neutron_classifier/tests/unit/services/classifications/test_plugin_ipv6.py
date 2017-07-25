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


class TestPluginIPV6(base.BaseClassificationTestCase):

    def setUp(self):
        super(TestPluginIPV6, self).setUp()
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

        common._generate_fake_ipv6_classifications(self)

    def test_ipv6_classification_break_out_headers(self):
        cl = self.cl_plugin.break_out_headers(self.fake_ipv6_classification)
        self.fake_ipv6_classification_broken_headers.pop('id', None)
        self.assertEqual(self.fake_ipv6_classification_broken_headers, cl)

    def test_ipv6_merge_header(self):
        cl = self.cl_plugin.merge_header(
            self.fake_ipv6_classification_broken_headers)
        self.assertEqual(self.fake_ipv6_classification['classification'], cl)

    @mock.patch.object(class_group.IPV6Classification, 'create')
    @mock.patch.object(class_group.IPV6Classification, 'id',
                       return_value=uuidutils.generate_uuid())
    def test_create_ipv6_classification(self, mock_ipv6_create, mock_ipv6_id):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_ipv6_create, 'create')
        mock_manager.attach_mock(mock_ipv6_id, 'id')
        mock_manager.reset_mock()
        mock_manager.start()

        self.fake_ipv6_classification['classification'].pop('id', None)

        val = self.cl_plugin.create_classification(
            self.ctxt, self.fake_ipv6_classification)

        expected_val = self.fake_ipv6_classification['classification']
        expected_val['id'] = class_group.IPV6Classification.id

        mock_call = mock.call.IPV6Classification().create()
        self.assertEqual(mock.call.IPV6Classification().create(), mock_call)
        self.assertEqual(expected_val, val)

    @mock.patch.object(class_group.IPV6Classification, 'update')
    def test_update_ipv6_classification(self, mock_ipv6_update):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_ipv6_update, 'update')
        mock_manager.reset_mock()
        mock_manager.start()

        class_obj = class_group.IPV6Classification(
            self.ctxt, **self.fake_ipv6_classification_broken_headers)

        ipv6_classification_update = {
            'name': 'test_ipv6_classification Version 2',
            'description': 'Test IPV6 Classification Version 2',
            'negated': True,
            'shared': True,
            'c_type': 'ipv6',
            'length': 16,
            'hops': None}

        self.cl_plugin.get_classification = mock.Mock()
        self.cl_plugin._get_by_id = mock.Mock(return_value=class_obj)

        self.cl_plugin.update_classification(
            self.ctxt, class_obj.id,
            {'classification': ipv6_classification_update})

        classification_update_mock_call = mock.call.update(
            {'description': 'Test IPV6 Classification Version 2',
             'name': 'test_ipv6_classification Version 2'})
        self.assertIn(classification_update_mock_call, mock_manager.mock_calls)

    @mock.patch.object(class_group.ClassificationBase, 'get_object')
    @mock.patch.object(class_group.IPV6Classification, 'get_object')
    @mock.patch.object(validators, 'check_valid_classifications')
    def test_delete_ipv6_classification(self, mock_validators, mock_base_get,
                                        mock_ipv6_get):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_base_get, 'get_object')
        mock_manager.attach_mock(mock_ipv6_get, 'get_object')

        ipv6_class_obj = class_group.IPV6Classification(
            self.ctxt, **self.fake_ipv6_classification_broken_headers)
        ipv6_class_obj.delete = mock.Mock()
        base_class_obj = class_group.ClassificationBase(
            self.ctxt, **self.fake_ipv6_classification_broken_headers)

        mock_base_get.return_value = base_class_obj
        mock_ipv6_get.return_value = ipv6_class_obj

        mock_manager.reset_mock()
        self.cl_plugin.delete_classification(
            self.ctxt, base_class_obj.id)

        get_obj_mock_call = mock.call.get_object(
            self.ctxt, id=self.fake_ipv6_classification_broken_headers['id'])
        self.assertIn(get_obj_mock_call, mock_manager.mock_calls)
        self.assertEqual([get_obj_mock_call, get_obj_mock_call],
                         mock_manager.mock_calls)
        self.assertTrue(ipv6_class_obj.delete.assert_called_once)

    @mock.patch.object(class_group.ClassificationBase, 'get_object')
    @mock.patch.object(class_group.IPV6Classification, 'get_object')
    def test_get_ipv6_classification(self, mock_base_get, mock_ipv6_get):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_base_get, 'get_object')
        mock_manager.attach_mock(mock_ipv6_get, 'get_object')

        ipv6_classification = self.fake_ipv6_classification['classification']

        definition = ipv6_classification.pop('definition')

        base_class_obj = class_group.ClassificationBase(
            self.ctxt, **ipv6_classification)
        ipv6_class_obj = class_group.IPV6Classification(
            self.ctxt, **self.fake_ipv6_classification_broken_headers)

        mock_base_get.return_value = ipv6_class_obj
        mock_ipv6_get.return_value = base_class_obj

        ipv6_classification['definition'] = definition

        mock_manager.reset_mock()
        value = self.cl_plugin.get_classification(
            self.ctxt, ipv6_classification['id'])

        get_obj_mock_call = mock.call.get_object(
            self.ctxt, id=ipv6_classification['id'])
        self.assertIn(get_obj_mock_call, mock_manager.mock_calls)
        self.assertEqual([get_obj_mock_call, get_obj_mock_call],
                         mock_manager.mock_calls)
        self.assertTrue(ipv6_classification, value)

    @mock.patch.object(class_group.ClassificationBase, 'get_objects')
    @mock.patch.object(class_group.IPV6Classification, 'get_objects')
    @mock.patch.object(base_obj, 'Pager')
    def test_get_ipv6_classifications(self, mock_pager, mock_ipv6_get,
                                      mock_base_get):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_base_get, 'get_objects')
        mock_manager.attach_mock(mock_ipv6_get, 'get_objects')

        ipv6_cl_1 = self.fake_ipv6_classification['classification']
        ipv6_cl_2 = self.fake_ipv6_classification_2['classification']

        definition = ipv6_cl_1.pop('definition')
        definition_2 = ipv6_cl_2.pop('definition')

        base_class_obj_1 = class_group.ClassificationBase(
            self.ctxt, **ipv6_cl_1)
        base_class_obj_2 = class_group.ClassificationBase(
            self.ctxt, **ipv6_cl_2)
        ipv6_class_obj_1 = class_group.IPV6Classification(
            self.ctxt, **self.fake_ipv6_classification_broken_headers)
        ipv6_class_obj_2 = class_group.IPV6Classification(
            self.ctxt, **self.fake_ipv6_classification_2_broken_headers)

        base_list = [base_class_obj_1, base_class_obj_2]
        ipv6_list = [ipv6_class_obj_1, ipv6_class_obj_2]

        mock_base_get.return_value = base_list
        mock_ipv6_get.return_value = ipv6_list
        mock_pager.return_value = None

        ipv6_cl_1['definition'] = definition
        ipv6_cl_2['definition'] = definition_2

        result_list = [ipv6_cl_1, ipv6_cl_2]

        mock_manager.reset_mock()
        value = self.cl_plugin.get_classifications(
            self.ctxt, filters={'c_type': ['ipv6']})

        get_objs_mock_call = mock.call.get_objects(
            self.ctxt, _pager=None, c_type=['ipv6'])
        self.assertIn(get_objs_mock_call, mock_manager.mock_calls)
        self.assertEqual([get_objs_mock_call], mock_manager.mock_calls)
        self.assertTrue(result_list, value)
