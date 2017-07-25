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
from neutron_classifier.objects import classifications as class_group
from neutron_classifier.services.classification import plugin
from neutron_classifier.tests import base
from neutron_lib import context
from oslo_utils import uuidutils


class TestPlugin(base.BaseClassificationTestCase):

    def setUp(self):
        super(TestPlugin, self).setUp()
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

        self._generate_test_classifications()

    def _generate_test_classifications(self):
        self.test_classification = {
            'classification': {'id': uuidutils.generate_uuid(),
                               'name': 'test_ethernet_classification',
                               'description': 'Test Ethernet Classification',
                               'project_id': uuidutils.generate_uuid(),
                               'shared': True,
                               'negated': True,
                               'c_type': 'ethernet',
                               'definition': {'src_addr': '00:07:E9:63:CE:53',
                                              'dst_addr': '00:07:E9:42:AC:28',
                                              'ethertype': 8100}}}

        self.test_classification_broken_headers = {
            'id': self.test_classification['classification']['id'],
            'name': 'test_ethernet_classification',
            'description': 'Test Ethernet Classification',
            'project_id': self.test_classification[
                'classification']['project_id'],
            'shared': True,
            'negated': True,
            'c_type': 'ethernet',
            'src_addr': '00:07:E9:63:CE:53',
            'dst_addr': '00:07:E9:42:AC:28',
            'ethertype': 8100}

        self.test_classification_2 = {
            'classification': {'id': uuidutils.generate_uuid(),
                               'name': 'test_second_ethernet_cl',
                               'description': 'Test Second '
                                              'Ethernet Classification',
                               'project_id': uuidutils.generate_uuid(),
                               'shared': False,
                               'negated': False,
                               'c_type': 'ethernet',
                               'definition': {'src_addr': '00:54:TY:89:G6:67',
                                              'dst_adrr': '00:54:TY:65:T7:44',
                                              'ethertype': 8100}}}

        self.test_classification_2_broken_headers = {
            'id': self.test_classification_2['classification']['id'],
            'name': 'test_second_ethernet_cl',
            'description': 'Test Second Ethernet Classification',
            'project_id': self.test_classification_2[
                'classification']['project_id'],
            'shared': False,
            'negated': False,
            'c_type': 'ethernet',
            'src_addr': '00:54:TY:89:G6:67',
            'dst_addr': '00:54:TY:65:T7:44',
            'ethertype': 8100}

    def test_classification_break_out_headers(self):
        cl = self.cl_plugin.break_out_headers(
            self.test_classification)
        self.test_classification_broken_headers.pop('id', None)
        self.assertEqual(self.test_classification_broken_headers, cl)

    def test_merge_header(self):
        cl = self.cl_plugin.merge_header(
            self.test_classification_broken_headers)
        self.assertEqual(self.test_classification['classification'],
                         cl)

    @mock.patch.object(class_group.EthernetClassification, 'create')
    @mock.patch.object(class_group.EthernetClassification, 'id',
                       return_value=uuidutils.generate_uuid())
    def test_create_classification(self, mock_ethernet_create,
                                   mock_ethernet_id):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_ethernet_create, 'create')
        mock_manager.attach_mock(mock_ethernet_id, 'id')
        mock_manager.reset_mock()
        mock_manager.start()

        self.test_classification['classification'].pop('id', None)

        val = self.cl_plugin.create_classification(
            self.ctxt, self.test_classification)

        expected_val = self.test_classification['classification']
        expected_val['id'] = class_group.EthernetClassification.id

        mock_call = mock.call.EthernetClassification().create()
        self.assertEqual(mock.call.EthernetClassification().create(),
                         mock_call)
        self.assertEqual(expected_val, val)

    @mock.patch.object(class_group.EthernetClassification, 'update')
    def test_update_classification(self, mock_ethernet_update):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_ethernet_update, 'update')
        mock_manager.reset_mock()
        mock_manager.start()

        class_obj = class_group.EthernetClassification(
            self.ctxt, **self.test_classification_broken_headers)

        ethernet_classification_update = {
            'name': 'test_ethernet_classification Version 2',
            'description': 'Test Ethernet Classification Version 2',
            'negated': True,
            'shared': True,
            'c_type': 'ethernet',
            'ethertype': 2}

        self.cl_plugin.get_classification = mock.Mock()
        self.cl_plugin._get_by_id = mock.Mock(return_value=class_obj)

        self.cl_plugin.update_classification(
            self.ctxt, class_obj.id,
            {'classification': ethernet_classification_update})

        classification_update_mock_call = mock.call.update(
            {'description': 'Test Ethernet Classification Version 2',
             'name': 'test_ethernet_classification Version 2'})
        self.assertIn(classification_update_mock_call, mock_manager.mock_calls)

    @mock.patch.object(class_group.ClassificationBase, 'get_object')
    @mock.patch.object(class_group.EthernetClassification, 'get_object')
    def test_delete_classification(self, mock_base_get, mock_ethernet_get):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_base_get, 'get_object')
        mock_manager.attach_mock(mock_ethernet_get, 'get_object')

        eth_class_obj = class_group.EthernetClassification(
            self.ctxt, **self.test_classification_broken_headers)
        eth_class_obj.delete = mock.Mock()
        base_class_obj = class_group.ClassificationBase(
            self.ctxt, **self.test_classification_broken_headers)

        mock_base_get.return_value = base_class_obj
        mock_ethernet_get.return_value = eth_class_obj

        mock_manager.reset_mock()
        self.cl_plugin.delete_classification(
            self.ctxt, base_class_obj.id)

        get_obj_mock_call = mock.call.get_object(
            self.ctxt,
            id=self.test_classification_broken_headers['id'])
        self.assertIn(get_obj_mock_call, mock_manager.mock_calls)
        self.assertEqual([get_obj_mock_call, get_obj_mock_call],
                         mock_manager.mock_calls)
        self.assertTrue(eth_class_obj.delete.assert_called_once)

    @mock.patch.object(class_group.ClassificationBase, 'get_object')
    @mock.patch.object(class_group.EthernetClassification, 'get_object')
    def test_get_classification(self, mock_base_get,
                                mock_ethernet_get):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_base_get, 'get_object')
        mock_manager.attach_mock(mock_ethernet_get, 'get_object')

        eth_classification = self.test_classification[
            'classification']

        definition = eth_classification.pop('definition')

        base_class_obj = class_group.ClassificationBase(
            self.ctxt, **eth_classification)
        eth_class_obj = class_group.EthernetClassification(
            self.ctxt, **self.test_classification_broken_headers)

        mock_base_get.return_value = eth_class_obj
        mock_ethernet_get.return_value = base_class_obj

        eth_classification['definition'] = definition

        mock_manager.reset_mock()
        value = self.cl_plugin.get_classification(
            self.ctxt, eth_classification['id'])

        get_obj_mock_call = mock.call.get_object(
            self.ctxt, id=eth_classification['id'])
        self.assertIn(get_obj_mock_call, mock_manager.mock_calls)
        self.assertEqual([get_obj_mock_call, get_obj_mock_call],
                         mock_manager.mock_calls)
        self.assertTrue(eth_classification, value)

    @mock.patch.object(class_group.ClassificationBase, 'get_objects')
    @mock.patch.object(class_group.EthernetClassification, 'get_objects')
    @mock.patch.object(base_obj, 'Pager')
    def test_get_classifications(self, mock_pager, mock_ethernet_get,
                                 mock_base_get):
        mock_manager = mock.Mock()
        mock_manager.attach_mock(mock_base_get, 'get_objects')
        mock_manager.attach_mock(mock_ethernet_get, 'get_objects')

        eth_cl_1 = self.test_classification['classification']
        eth_cl_2 = self.test_classification_2['classification']

        definition = eth_cl_1.pop('definition')
        definition_2 = eth_cl_2.pop('definition')

        base_class_obj_1 = class_group.ClassificationBase(
            self.ctxt, **eth_cl_1)
        base_class_obj_2 = class_group.ClassificationBase(
            self.ctxt, **eth_cl_2)
        eth_class_obj_1 = class_group.EthernetClassification(
            self.ctxt, **self.test_classification_broken_headers)
        eth_class_obj_2 = class_group.EthernetClassification(
            self.ctxt, **self.test_classification_2_broken_headers)

        base_list = [base_class_obj_1, base_class_obj_2]
        eth_list = [eth_class_obj_1, eth_class_obj_2]

        mock_base_get.return_value = base_list
        mock_ethernet_get.return_value = eth_list
        mock_pager.return_value = None

        eth_cl_1['definition'] = definition
        eth_cl_2['defintion'] = definition_2

        result_list = [eth_cl_1, eth_cl_2]

        mock_manager.reset_mock()
        value = self.cl_plugin.get_classifications(
            self.ctxt, filters={'c_type': ['ethernet']})

        get_objs_mock_call = mock.call.get_objects(
            self.ctxt, _pager=None, c_type=['ethernet'])
        self.assertIn(get_objs_mock_call, mock_manager.mock_calls)
        self.assertEqual([get_objs_mock_call], mock_manager.mock_calls)
        self.assertTrue(result_list, value)
