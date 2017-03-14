# Copyright (c) 2017 Intel. All Rights Reserved.
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

from neutronclient.common import extension
from neutronclient.neutron import v2_0 as neutronv20

from neutron_classifier._i18n import _
from neutron_classifier.common import constants


class Classification(extension.NeutronClientExtension):
    resource = "classification"
    resource_plural = '%ss' % resource
    object_path = '/classification/%s' % resource_plural
    resource_path = '/classification/%s/%%s' % resource_plural
    versions = ['2.0']


class ClassificationCreate(extension.ClientExtensionCreate,
                       Classification):
    """Create a Classification."""
    shell_command = "classification-create"

    def add_known_arguments(self, parser):
        parser.add_argument(
            'name',
            metavar='NAME',
            help=_('Name of the Classification.'))
        parser.add_argument(
            '--description',
            help=_('Description for the Classification.'))
        parser.add_argument(
            '--type',
            help=_('Classification traffic type.'))
        for field in constants.ALL_FIELDS:
            parser.add_argument(
                '--' + field,
                help=_('Packet Header Field.'))

    def args2body(self, parsed_args):
        fields = [field.replace('-', '_') for field in constants.ALL_FIELDS] + ['name', 'description', 'type']
        values = {}
        for attribute in fields:
            if hasattr(parsed_args, attribute) and getattr(parsed_args, attribute) is not None:
                values[attribute.replace('_', '-')] = getattr(parsed_args, attribute)

        for field in values.keys():
            if field is 'type' or field is 'name' or field is 'description':
                continue
            elif field in constants.CLASSIFIER_FIELDS[body['type']]:
                continue
            else:
                print("raise exception, %s not in %s header" %
                     (field.replace('-', '_'), values['type']))

        return {self.resource: values}


class ClassificationUpdate(extension.ClientExtensionUpdate,
                       Classification):
    """Update a Classification."""
    shell_command = "classification-update"

    def add_known_arguments(self, parser):
        parser.add_argument(
            'name',
            metavar='NAME',
            help=_('Name of the Classification.'))
        parser.add_argument(
            '--description',
            help=_('Description for the Classification.'))
        parser.add_argument(
            '--type',
            help=_('Classification traffic type.'))
        for field in constants.ALL_FIELDS:
            parser.add_argument(
                '--' + field,
                help=_('Packet Header Field.'))

    def args2body(self, parsed_args):
        body = {}
        neutronv20.update_dict(parsed_args, body, ['name', 'description',
                                                   'type'] +
                                                  constants.ALL_FIELDS)
        for field in body.keys():
            if field is 'type' or field is 'name' or field is 'description':
                continue
            elif field in constants.CLASSIFIER_FIELDS[body['type']]:
                continue
            else:
                print("raise exception, %s not in %s header" %
                     (field, body['type']))
        return {self.resource: body}


class ClassificationDelete(extension.ClientExtensionDelete,
                       Classification):
    """Delete a given Classification."""

    shell_command = 'classification-delete'


class ClassificationList(extension.ClientExtensionList,
                     Classification):
    """List the Classification that belong to a given tenant."""

    shell_command = 'classification-list'
    list_columns = ['id', 'name', 'type']
    pagination_support = True
    sorting_support = True


class ClassificationShow(extension.ClientExtensionShow,
                     Classification):
    """Show information of a given Classification."""

    shell_command = 'classification-show'
