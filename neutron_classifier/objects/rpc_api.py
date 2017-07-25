# Copyright 2017 Intel Corporation.
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

from oslo_log import log as logging
import oslo_messaging

from neutron.common import rpc as n_rpc

LOG = logging.getLogger(__name__)

CLASSIFICATION_TOPIC = 'q-classification-plugin'


class ClassificationPluginApi(object):
    def __init__(self, host, topic=CLASSIFICATION_TOPIC):
        self.host = host
        self.target = oslo_messaging.Target(topic=topic, version='1.0')
        self.client = n_rpc.get_client(self.target)

    def get_classification_by_id(self, context, classification_id):
        cctxt = self.client.prepare()
        return cctxt.call(
            context, 'get_classification_by_id',
            id=classification_id)
