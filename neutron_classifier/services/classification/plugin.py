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

from neutron.common import rpc as n_rpc


from neutron_classifier.db import classification as classification_db
from neutron_classifier.extensions import classification
from neutron_classifier.objects import classifications as class_group
from neutron_classifier.objects import rpc_api
from neutron_classifier.services.classification.drivers import rpc

LOG = logging.getLogger(__name__)


class ClassificationPlugin(classification.NeutronClassificationPluginBase,
                           classification_db.TrafficClassificationDbPlugin):
    supported_extension_aliases = ['neutron_classifier']

    def __init__(self):
        super(ClassificationPlugin, self).__init__()
        self.driver_manager = None
        self._setup_rpc()

    def _setup_rpc(self):
        # Setup a rpc server
        self.topic = rpc_api.CLASSIFICATION_TOPIC
        self.endpoints = [rpc.ClassificationRpcCallback(self)]
        self.conn = n_rpc.create_connection()
        self.conn.create_consumer(self.topic, self.endpoints, fanout=False)
        self.conn.consume_in_threads()

    def get_classification(self, context, classification_id):
        LOG.debug("get_classification")
        classifications = []
        class_id = classification_id

        cl = class_group.ClassificationBase.get_object(context, id=class_id)
        cl_class = class_group.CLASS_MAP[cl.c_type]
        classifications.append(cl_class.get_object(context,
                                                   id=classification_id))
        return classifications

    def __getattr__(self, resource):
        return super(ClassificationPlugin, self).__getattr__(resource)
