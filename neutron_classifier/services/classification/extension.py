# Copyright ..19 Intel Corporation.
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

from neutron.api.rpc.callbacks.consumer import registry
from neutron.api.rpc.callbacks import events
from neutron.api.rpc.callbacks import resources
from neutron.api.rpc.handlers import resources_rpc
from neutron.objects import classification as class_group
from neutron_classifier.objects import classifications as classes
from neutron_lib.agent import l2_extension
from neutron_lib.agent import l3_extension

from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class NeutronClassifierExtension(l2_extension.L2AgentExtension,
                                 l3_extension.L3AgentExtension):

    SUPPORTED_RESOURCE_TYPES = [
        class_group.ClassificationGroup.obj_name(),
        classes.EthernetClassification.obj_name(),
        classes.IPV4Classification.obj_name(),
        classes.IPV6Classification.obj_name(),
        classes.UDPClassification.obj_name(),
        classes.TCPClassification.obj_name()]

    def __init__(self):
        super(NeutronClassifierExtension, self).__init__()
        resources.register_resource_class(class_group.ClassificationGroup)
        self.class_type_list = []
        for cls in classes.CLASS_MAP.values():
            resources.register_resource_class(cls)
            self.class_type_list.append(cls.obj_name())

    def initialize(self, connection, driver_type):
        super(NeutronClassifierExtension, self).initialize(connection,
                                                           driver_type)
        self._register_rpc_consumers(connection)

    def handle_port(self, context, port):
        pass

    def delete_port(self, context, port):
        pass

    def add_router(self, context, port):
        pass

    def update_router(self, context, port):
        pass

    def delete_router(self, context, port):
        pass

    def ha_state_change(self, context, port):
        pass

    def consume_api(self, agent_api):
        self.agent_api = agent_api

    def _register_rpc_consumers(self, connection):

        '''Allows an extension to receive notifications.

        The notification shows the updates made to
        items of interest.
        '''

        endpoints = [resources_rpc.ResourcesPushRpcCallback()]
        for resource_type in self.SUPPORTED_RESOURCE_TYPES:
            registry.register(self.handle_notification, resource_type)
            topic = resources_rpc.resource_type_versioned_topic(resource_type)
            connection.create_consumer(topic, endpoints, fanout=True)

    def handle_notification(self, context, resource_type,
                            class_objs, event_type):
        '''Alerts the l2 extensin agent.

        Notifies if a classification or a classification
        group has been made.
        '''

        if (event_type == events.CREATED
                and resource_type ==
                class_group.ClassificationGroup.obj_name()):
            for class_obj in class_objs:
                self.agent_api.register_classification_group(
                    class_obj.id, class_obj)

        if (event_type == events.CREATED and resource_type
                in self.class_type_list):
            for class_obj in class_objs:
                self.agent_api.register_classification(class_obj.id,
                                                       class_obj)

        LOG.debug("handle_notification was utilized.resource types"
                  "% (resource_type)s and event type % (event_type)s logged.",
                  {'resource_type': resource_type,
                   'event_type': event_type})
