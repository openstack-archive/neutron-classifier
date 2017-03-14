# Copyright 2017 Intel. All rights reserved.
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
from neutron.db import db_base_plugin_common


from neutron_classifier.common import constants
from neutron_classifier.common import exceptions
from neutron_classifier.extensions import classification
from neutron_classifier.db import classifier as classifier_db
from neutron_classifier.db import models_v2
from neutron_classifier.objects import classifications as class_group
from neutron_classifier.objects import rpc_api
from neutron_classifier.services.classification.drivers import rpc

LOG = logging.getLogger(__name__)

class ClassificationPlugin(classification.NeutronClassificationPluginBase, classifier_db.TrafficClassificationDbPlugin):

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

    def create_classification(self, context, classification):
        LOG.debug("create_classification")
        return super(ClassificationPlugin, self).create_classification(context,
                                                                classification)

    def update_classification(self, context, classification_id, classification):
        LOG.debug("update_classification")
        return super(ClassificationPlugin, self).update_classification(context,
                                      classification_id, classification)

    def delete_classification(self, context, classification_id):
        LOG.debug("delete_classification")
        return super(ClassificationPlugin, self).delete_classification(context,
                                      classification_id, classification)

    def get_classification(self, context, classification_id):
        LOG.debug("get_classification")
        classifications = []

        cl = class_group.ClassificationBase.get_object(context, id=classification_id)
        classifications.append(class_group.CLASS_MAP[cl.classification_type].get_object(context, id=classification_id))

        return classifications

    def get_classifications(self, context, **kwargs):
        LOG.debug("get_classifications")
        return super(ClassificationPlugin, self).get_classifications(context,
                                                                     kwargs)

    def __getattr__(self, resource):
        return super(ClassificationPlugin, self).__getattr__(resource)
