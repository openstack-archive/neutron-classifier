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

from neutron_lib.agent import l2_extension

from neutron.api.rpc.callbacks import resources

from neutron_classifier.objects import classifications as class_group


class NeutronClassifierExtension(l2_extension.L2AgentExtension):

    def __init__(self):
        super(NeutronClassifierExtension, self).__init__()
        resources.register_resource_class(class_group.ClassificationGroup)
        resources.register_resource_class(class_group.ClassificationBase)
        for cls in class_group.CLASS_MAP.values():
            resources.register_resource_class(cls)

    def initialize(self, connection, driver_type):
        pass

    def handle_port(self, context, port):
        pass

    def delete_port(self, context, port):
        pass
