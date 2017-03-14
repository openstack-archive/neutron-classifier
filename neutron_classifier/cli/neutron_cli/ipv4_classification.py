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
from neutron_classifier.common import exceptions
from neutron_classifier.common import validators


class IPV4Classification(extension.NeutronClientExtension):
    resource = "ipv4_classification"
    resource_plural = '%ss' % resource
    object_path = '/classification/%s' % resource_plural
    resource_path = '/classification/%s/%%s' % resource_plural
    versions = ['2.0']


class IPv4ClassificationCreate(extension.ClientExtensionCreate,
                       IPV4Classification):
    """Create a IPV4 Classification."""
    shell_command = "ipv4-classification-create"

    def add_known_arguments(self, parser):
        parser.add_argument(
            'name',
            metavar='NAME',
            help=_('Name of the IPV4 Classification.'))
        parser.add_argument(
            '--description',
            help=_('Description for the IPV4 Classification.'))
        parser.add_argument(
            '--dscp',
            help=_('DSCP Classification value.'))
        parser.add_argument(
            '--ecn',
            help=_('ECN Classification value.'))
        parser.add_argument(
            '--protocol',
            help=_('Protocol Classification value.'))
        parser.add_argument(
            '--source-address',
            help=_('Source IPV4 Address Classification value.'))
        parser.add_argument(
            '--destination-address',
            help=_('Destination IPV4 Address Classification value.'))

    def args2body(self, parsed_args):
        fields = ['name', 'description', 'type', 'dscp', 'ecn', 'protocol',
                  'source-address', 'destination-address']
        values = {}

        for attribute in fields:
            if hasattr(parsed_args, attribute.replace('-','_')) and getattr(
               parsed_args, attribute.replace('-','_')) is not None:

                values[attribute.replace('-', '_')] = getattr(parsed_args,
                                                   attribute.replace('-','_'))

        if 'dscp' in values.keys() and "/" in values['dscp']:
            proto = values.pop('dscp').split('/')
            values['dscp'] = validators.check_valid_dscp_mark(proto[0])
            values['dscp_mask'] = validators.check_valid_dscp_mask(proto[1])
        elif 'dscp' in values.keys():
            values['dscp'] = validators.check_valid_dscp_mark(values['dscp'])

        if 'ecn' in values.keys() and "/" in values['ecn']:
            proto = values.pop('ecn').split('/')
            values['ecn'] =  validators.check_valid_ecn_mark(proto[0])
            values['ecn_mask']= validators.check_valid_ecn_mask(proto[1])
        elif 'ecn' in values.keys():
            values['ecn'] =  validators.check_valid_ecn_mark(values['ecn'])

        if 'protocol' in values.keys() and "/" in values['protocol']:
            proto = values.pop('protocol').split('/')
            values['protocol'] = validators.check_valid_protocol_mark(
                                                                   proto[0])
            values['protocol_mask']= validators.check_valid_protocol_mark(
                                                                   proto[1])
        elif 'protocol' in values.keys():
            values['protocol'] = validators.check_valid_protocol_mark(
                                                       values['protocol'])

        if 'source_address' in values.keys() and "/" in values['source_address']:
            proto = values.pop('source_address').split('/')
            values['source_address'] = validators.check_valid_ipv4_address(
                                                                   proto[0])
            values['source_address_range']= validators.check_valid_ipv4_cidr(
                                                                   proto[1])
        elif 'source_address' in values.keys():
            values['source_address'] = validators.check_valid_ipv4_address(
                                                   values['source_address'])

        if 'destination_address' in values.keys() and "/" in values['destination_address']:
            proto = values.pop('destination_address').split('/')
            values['destination_address'] = \
                               validators.check_valid_ipv4_address(proto[0])
            values['destination_address_range']= \
                               validators.check_valid_ipv4_cidr(proto[1])
        elif 'destination_address' in values.keys():
            values['destination_address'] = \
                                       validators.check_valid_ipv4_address(
                                               values['destination_address'])

        return {self.resource: values}


class IPv4ClassificationDelete(extension.ClientExtensionDelete,
                       IPV4Classification):
    """Delete a given IPV4 Classification."""

    shell_command = 'ipv4-classification-delete'


class IPV4ClassificationList(extension.ClientExtensionList,
                     IPV4Classification):
    """List the IPV4 Classification that belong to a given tenant."""

    shell_command = 'ipv4-classification-list'
    list_columns = ['id', 'name', 'dscp', 'ecn', 'protocol',
                    'source-address', 'destination-address']
    pagination_support = True
    sorting_support = True


class IPV4ClassificationShow(extension.ClientExtensionShow,
                     IPV4Classification):
    """Show information of a given IPV4Classification."""

    shell_command = 'ipv4-classification-show'
