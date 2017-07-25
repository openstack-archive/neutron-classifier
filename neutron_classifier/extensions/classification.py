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

from abc import ABCMeta
import six

from oslo_config import cfg

from neutron_lib.api import extensions as api_ext
from neutron_lib.services import base as service_base

from neutron.api import extensions as ext
from neutron.api.v2 import resource_helper

from neutron_classifier.common import resources as classifier_resources
from neutron_classifier import extensions


cfg.CONF.import_opt('api_extensions_path', 'neutron.common.config')
ext.append_api_extensions_path(extensions.__path__)

EXT_NAME = "neutron_classifier"


def validate_string(String):
    if String is None:
        String = ''
    return String

RESOURCE_ATTRIBUTE_MAP = {
    'classification_type':
        classifier_resources.CLASSIFICATION_TYPE_RESOURCE_MAP,
    'classification_groups':
        classifier_resources.CLASSIFICATION_GROUP_RESOURCE_MAP,
    'classifications':
        classifier_resources.CLASSIFICATION_RESOURCE_MAP,
}


class Classification(api_ext.ExtensionDescriptor):
    """Classification API extension."""

    @classmethod
    def get_name(cls):
        return "Neutron Classifier"

    @classmethod
    def get_alias(cls):
        return "neutron_classifier"

    @classmethod
    def get_description(cls):
        return "Extension that provides a common classification framework."

    @classmethod
    def get_updated(cls):
        return "2015-07-12T10:00:00-00:00"

    @classmethod
    def get_plugin_interface(cls):
        return extensions.classification.NeutronClassificationPluginBase

    @classmethod
    def get_resources(cls):
        """Returns Ext Resources."""
        special_mappings = {}
        plural_mappings = resource_helper.build_plural_mappings(
            special_mappings, RESOURCE_ATTRIBUTE_MAP)

        resources = resource_helper.build_resource_info(plural_mappings,
                                                        RESOURCE_ATTRIBUTE_MAP,
                                                        EXT_NAME,
                                                        translate_name=False,
                                                        allow_bulk=True)

        for resource in resources:
            resource.path_prefix = '/classifications'

        return resources

    def update_attributes_map(self, attributes, extension_attrs_map=None):
        super(Classification, self).update_attributes_map(
            attributes, extension_attrs_map=RESOURCE_ATTRIBUTE_MAP)

    def get_extended_resources(self, version):
        return RESOURCE_ATTRIBUTE_MAP


@six.add_metaclass(ABCMeta)
class NeutronClassificationPluginBase(service_base.ServicePluginBase):

    path_prefix = '/classifications'

    def get_plugin_name(self):
        return EXT_NAME

    def get_plugin_type(self):
        return EXT_NAME

    def get_plugin_description(self):
        return 'Neutron Classifier service plugin.'

    def create_classification(self, context, classification):
        pass

    def update_classification(self, context, classification_id,
                              classification):
        pass

    def delete_classification(self, context, classification_id):
        pass

    def get_classification(self, context, classification_id):
        pass

    def get_classifications(self, context, **kwargs):
        pass

    def get_classification_type(self, context, **kwargs):
        pass
