# Copyright 2018 Intel Corporation.
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

import json
import uuid

from openstackclient.tests.functional import base


class IPV4Test(base.TestCase):
    """Functional tests for ipv4 classification cli"""

    @classmethod
    def setUpClass(cls):
        super(IPV4Test, cls).setUpClass()
        cls.haz_network = base.is_service_enabled('network')

    def test_create_ipv4(self):
        name1 = uuid.uuid4().hex
        cmd_output = json.loads(self.openstack(
            'network classification ipv4 create -f json ' + name1
        ))
        self.assertIsNotNone(cmd_output['id'])

        self.assertEqual(
            name1,
            cmd_output["name"])

        # create with more options
        name2 = 'test_ipv4'
        description2 = 'test_description'
        cmd_output_2 = json.loads(self.openstack(
            'network classification ipv4 create -f json ' + name2 +
            ' --description ' + description2))

        self.assertIsNotNone(cmd_output_2['id'])

        self.assertEqual(
            name2,
            cmd_output_2['name'])

        self.assertEqual(
            description2,
            cmd_output_2['description'])

        # Clean up
        raw_output_1 = self.openstack(
            'network classification ipv4 delete ' + cmd_output['id'])
        raw_output_2 = self.openstack(
            'network classification ipv4 delete ' + cmd_output_2['id'])
        self.assertOutput('', raw_output_1)
        self.assertOutput('', raw_output_2)

    def test_show_ipv4(self):
        name1 = uuid.uuid4().hex
        cmd_create = json.loads(self.openstack(
            'network classification ipv4 create -f json ' + name1
        ))

        cmd_output = json.loads(self.openstack(
            'network classification ipv4 show -f json ' + cmd_create['id']
        ))
        self.assertIsNotNone(cmd_output['id'])
        self.assertEqual(name1, cmd_output['name'])
        self.assertEqual(False, cmd_output['shared'])
        self.assertEqual(False, cmd_output['negated'])

        # Clean up
        raw_output = self.openstack(
            'network classification ipv4 delete ' + cmd_create['id'])
        self.assertOutput('', raw_output)

    def test_list_ipv4(self):
        name1 = uuid.uuid4().hex
        name2 = uuid.uuid4().hex
        description1 = 'test_desc_1'
        description2 = 'test_desc_2'
        cmd_create_1 = json.loads(self.openstack(
            'network classification ipv4 create -f json ' + name1 +
            ' --description ' + description1))
        cmd_create_2 = json.loads(self.openstack(
            'network classification ipv4 create -f json ' + name2 +
            ' --description ' + description2))

        self.addCleanup(self.openstack,
                        'network classification ipv4 delete ' +
                        cmd_create_1['id'])
        self.addCleanup(self.openstack,
                        'network classification ipv4 delete ' +
                        cmd_create_2['id'])

        cmd_output = json.loads(self.openstack(
            'network classification ipv4 list -f json'))
        name_list = [x['Name'] for x in cmd_output]
        desc_list = [x['Description'] for x in cmd_output]
        self.assertIn(name1, name_list)
        self.assertIn(name2, name_list)
        self.assertIn(description1, desc_list)
        self.assertIn(description2, desc_list)

    def test_delete_ipv4(self):
        name1 = uuid.uuid4().hex
        cmd_create_1 = json.loads(self.openstack(
            'network classification ipv4 create -f json ' + name1
        ))

        del_output = self.openstack(
            'network classification ipv4 delete ' + cmd_create_1['id']
        )
        self.assertOutput('', del_output)

    def test_update_ipv4(self):
        name1 = uuid.uuid4().hex
        description1 = 'test_description'
        cmd_create_1 = json.loads(self.openstack(
            'network classification ipv4 create -f json ' + name1 +
            ' --description ' + description1))

        self.addCleanup(self.openstack,
                        'network classification ipv4 delete ' +
                        cmd_create_1['id'])

        cmd_output = json.loads(self.openstack(
            'network classification ipv4 update -f json ' + cmd_create_1['id']
            + ' --description test_description_updated'
        ))
        self.assertIsNotNone(cmd_output['id'])
        self.assertEqual('test_description_updated', cmd_output['description'])
