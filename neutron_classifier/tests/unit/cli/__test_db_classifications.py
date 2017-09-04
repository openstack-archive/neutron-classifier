# Can't be run at the moment until migration with openstack-client


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

from neutron.tests.unit.extensions import base as test_extensions_base

from neutronclient.v2_0 import client

OPENSTACK_CLI_ID = "/ccf/classifications"
ASSOCS_PATH = "/ccf/classifications"
NET_ASSOC_ID = "uuid_client_foo"


class OpenstackClientTestCase(test_extensions_base.ExtensionTestCase):

    def setUp(self):
        super(OpenstackClientTestCase, self).setUp()
        self.client = client.Client()
        self.client.list_ext = mock.Mock()
        self.client.create_ext = mock.Mock()
        self.client.show_ext = mock.Mock()
        self.client.update_ext = mock.Mock()
        self.client.delete_ext = mock.Mock()
        print("self.client keys: ", dir(self.client))

    def test_client_url_list(self):
        self.client.ListIPV4Classification(OPENSTACK_CLI_ID)
        self.client.list_ext.assert_called_once_with(mock.ANY, ASSOCS_PATH,
                                                     mock.ANY)

    def test_client_url_create(self):
        self.client.CreateIPV4Classification(OPENSTACK_CLI_ID, {})
        self.client.create_ext.assert_called_once_with(ASSOCS_PATH, mock.ANY)

    def test_client_url_show(self):
        self.client.ShowIPV4Classification(NET_ASSOC_ID, OPENSTACK_CLI_ID)
        self.client.show_ext.assert_called_once_with(ASSOCS_PATH,
                                                     NET_ASSOC_ID)

    def test_client_url_update(self):
        self.client.UpdateIPV4Classification(NET_ASSOC_ID,
                                             OPENSTACK_CLI_ID, {})
        self.client.update_ext.assert_called_once_with(ASSOCS_PATH,
                                                       NET_ASSOC_ID,
                                                       mock.ANY)

    def test_client_url_delete(self):
        self.client.DeleteIPV4Classification(NET_ASSOC_ID, OPENSTACK_CLI_ID)
        self.client.delete_ext.assert_called_once_with(ASSOCS_PATH,
                                                       NET_ASSOC_ID)
