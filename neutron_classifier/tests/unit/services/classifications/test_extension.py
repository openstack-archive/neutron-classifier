# Copyright 2019 Intel Corporation.
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

from neutron.api.rpc.callbacks import events
from neutron.objects import classification as class_group
from neutron_classifier.objects import classifications as classes
from neutron_classifier.services.classification import extension

from oslo_utils import uuidutils

import unittest


class TestClassifierExtension(unittest.TestCase):

    def setUp(self):
        super(TestClassifierExtension, self).setUp()
        self.mock_context = mock.Mock()
        mock.patch.object(extension, 'resources').start()
        self.mock_id = uuidutils.generate_uuid()
        self.extension = extension.NeutronClassifierExtension()
        self.extension.agent_api = mock.Mock()
        mock_rtvt = mock.patch('neutron.api.rpc.handlers.resources_rpc'
                               '.resource_type_versioned_topic')
        mock_r = mock.patch('neutron.api.rpc.callbacks'
                            '.consumer.registry.register')

        mock_rtvt.start()
        mock_r.start()

    def test_register_rpc_consumers(self):
        mock_connection = mock.Mock()
        mock_consumer = mock.MagicMock()
        mock_connection.create_consumer = mock_consumer

        test_supported_resource_types = [
            class_group.ClassificationGroup.obj_name(),
            classes.EthernetClassification.obj_name(),
            classes.IPV4Classification.obj_name(),
            classes.IPV6Classification.obj_name(),
            classes.UDPClassification.obj_name(),
            classes.TCPClassification.obj_name()
            ]

        self.extension._register_rpc_consumers(mock_connection)
        self.assertEqual(mock_consumer.call_count,
                         len(test_supported_resource_types))

    def test_handle_notification_ignores_events(self):

        self.extension.agent_api.register_classification = mock.Mock()
        for event_type in set(events.VALID) - {events.CREATED}:
            self.extension.handle_notification(mock.Mock(), '',
                                               object(), event_type)
            self.assertFalse(self.extension.agent_api.
                             register_classification.called)

    def test_handle_notification_passes_events_classification(self):

        self.extension.agent_api.register_classification = mock.Mock()
        class_obj = mock.Mock()
        self.extension.handle_notification(mock.Mock(), 'IPV4Classification',
                                           [class_obj], events.CREATED)

        self.extension.agent_api.register_classification. \
            assert_called_once()
        self.assertFalse(self.extension.agent_api.
                         register_classification_group.called)

    def test_handle_notification_passes_events_classification_group(self):
        self.extension.agent_api.register_classification_group = mock.Mock()
        class_obj = mock.Mock()
        self.extension.handle_notification(mock.Mock(), 'ClassificationGroup',
                                           [class_obj], events.CREATED)
        self.extension.agent_api.register_classification_group. \
            assert_called_once()
        self.assertFalse(self.extension.agent_api.
                         register_classification.called)

    def tearDown(self):
        super(TestClassifierExtension, self).tearDown()
        pass
