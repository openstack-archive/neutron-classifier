# Copyright (c) 2017 Intel Corporation.
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

from neutron.objects import base
from neutron_classifier.common import constants
from oslo_versionedobjects import base as obj_base
from oslo_versionedobjects import fields as obj_fields


@obj_base.VersionedObjectRegistry.register
class ClassificationType(base.NeutronObject):

    VERSION = '1.0'

    fields = {
        'type': obj_fields.StringField(),
        'supported_parameters': obj_fields.ListOfStringsField(),
    }

    @classmethod
    def get_object(cls, classification_type, **kwargs):

        parameters = constants.CLASSIFIER_FIELDS[classification_type]

        return cls(type=classification_type, supported_parameters=parameters)
