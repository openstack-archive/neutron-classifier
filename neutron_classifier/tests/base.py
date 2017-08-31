# Copyright 2010-2011 OpenStack Foundation
# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
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

from neutron.api.rpc.callbacks import resource_manager
from neutron.tests import base


class BaseClassificationTestCase(base.BaseTestCase):
    def setUp(self):
        super(BaseClassificationTestCase, self).setUp()

        with mock.patch.object(
            resource_manager.ResourceCallbacksManager, '_singleton',
                new_callable=mock.PropertyMock(return_value=False)):

            self.consumer_manager = resource_manager.\
                ConsumerResourceCallbacksManager()
            self.producer_manager = resource_manager.\
                ProducerResourceCallbacksManager()
            for manager in (self.consumer_manager, self.producer_manager):
                manager.clear()
