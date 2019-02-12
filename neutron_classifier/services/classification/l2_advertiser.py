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

from neutron.api.rpc.callbacks import events as rpc_events
from neutron.api.rpc.callbacks.producer import registry as rpc_registry
from neutron.api.rpc.callbacks import resources
from neutron.api.rpc.handlers import resources_rpc
from oslo_log import log as logging

from neutron_classifier.common import constants as nc_consts
from neutron_classifier.objects import classifications as class_group
from neutron.objects import classification as cs_base


LOG = logging.getLogger(__name__)


class NeutronClassifierDriverManager(object):

    def __init__(self):
        self._drivers = []
        self.rpc_notifications_required = True

        self._init_classification_topics()

        rpc_registry.provide(self._create_classification,
                             cs_base.ClassificationBase.obj_name())
        rpc_registry.provide(self._create_classification_group,
                             cs_base.ClassificationGroup.obj_name())

        if self.rpc_notifications_required:
            self.push_api = resources_rpc.ResourcesPushRpcApi()

    def _init_classification_topics(self):
        resources.register_resource_class(cs_base.ClassificationGroup)
        resources.register_resource_class(cs_base.ClassificationBase)
        for cls in class_group.CLASS_MAP.values():
            resources.register_resource_class(cls)

    @staticmethod
    def _create_classification(resource, classification_id, **kwargs):
        print('Sara is utilising this create_classification function')
        context = kwargs.get('context')
        if context is None:
            LOG.warning(
                'Received %(resource)s %(classification_id)s without context',
                {'resource': resource, 'classification_id': classification_id})
            return

        c = cs_base.ClassificationBase(context, id=classification_id)
        class_obj = class_group.CLASS_MAP[c.c_type]
        classification = class_obj.get_object(context, id=classification_id)
        return classification

    @staticmethod
    def _create_classification_group(resource, cg_id, **kwargs):
        print('Sara is utilising CLASSIFICATION GROUP function') 
        context = kwargs.get('context')
        if context is None:
            LOG.warning(
                'Received %(resource)s %(classification_id)s without context',
                {'resource': resource, 'classification_id': cg_id})

        cg = cs_base.ClassificationGroup.get_object(context,
                                                        id=cg_id)
        return cg

    def call(self, method_name, *args, **kwargs):
        """Helper method for calling a method across all extensions."""
        if self.rpc_notifications_required:
            context = kwargs.get('context') or args[0]
            cls_obj = kwargs.get('classification') or args[1]

            # we don't push create_policy events since policies are empty
            # on creation, they only become of any use when rules get
            # attached to them.
            if method_name == nc_consts.CREATE_CLASS:
                self.push_api.push(context, [cls_obj], rpc_events.CREATED)

            elif method_name == nc_consts.DELETE_CLASS:
                self.push_api.push(context, [cls_obj], rpc_events.DELETED)
