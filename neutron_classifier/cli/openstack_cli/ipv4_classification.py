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

from osc_lib.command import command
from osc_lib import utils

PREFIX = "/ccf"
object_path = PREFIX + "/classifications"
resource = 'classification'


class CreateIPV4Classification(command.ShowOne):
    """Create an IPV4 Classification."""

    def get_parser(self, prog_name):
        parser = super(CreateIPV4Classification, self).get_parser(prog_name)
        parser.add_argument(
            'name', metavar='NAME',
            help=('Name of the IPV4 Classification.'))
        parser.add_argument(
            '--description',
            help=('Description for the IPV4 Classification.'))
        parser.add_argument(
            '--negated',
            help=('Whether the complement of the IPV4 '
                  'Classification should be matched.'))
        parser.add_argument(
            '--shared',
            help=('Whether the IPV4 Classification should be '
                  'shared with other projects.'))
        parser.add_argument(
            '--dscp',
            help=('DSCP Classification value. Type of Service.'))
        parser.add_argument(
            '--dscp-mask',
            help=('DSCP Classification value. Type of Service.'))
        parser.add_argument(
            '--ecn',
            help=('Allows notification of network congestion.'))
        parser.add_argument(
            '--length-min',
            help=('Minimum length of the IP Packet, including '
                  'IP header and IP payload.'))
        parser.add_argument(
            '--length-max',
            help=('Maximum length of the IP Packet, including '
                  'IP header and IP payload.'))
        parser.add_argument(
            '--flags',
            help=('Whether the packet can be fragmented.'))
        parser.add_argument(
            '--flags-mask',
            help=('Whether the packet can be fragmented.'))
        parser.add_argument(
            '--ttl-min',
            help=('Minimum number of hops which the packet may '
                  'be routed over.'))
        parser.add_argument(
            '--ttl-max',
            help=('Maximum number of hops which the packet may '
                  'be routed over.'))
        parser.add_argument(
            '--protocol',
            help=('Type of transport the packet belongs to.'))
        parser.add_argument(
            '--src-addr',
            help=('Source Address of the IPV4 Classification.'))
        parser.add_argument(
            '--dst-addr',
            help=('Destination Address of the IPV4 Classification.'))
        parser.add_argument(
            '--options',
            help=('Options values for the IPV4 Classification.'))
        parser.add_argument(
            '--options-mask',
            help=('Options values for the IPV4 Classification.'))

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.neutronclient
        attrs = _get_attrs(self.app.client_manager,
                           parsed_args, is_create=True)
        obj = client.create_ext(object_path, {resource: attrs})
        columns = _get_columns(obj[resource])
        data = utils.get_dict_properties(obj[resource], columns)
        return columns, data


class DeleteIPV4Classification(command.Command):
    """Delete a given IPV4 Classification."""

    def get_parser(self, prog_name):
        parser = super(DeleteIPV4Classification, self).get_parser(prog_name)
        parser.add_argument(
            'ipv4_classification',
            metavar="IPV4_CLASSIFICATION",
            help=('ID of the IPV4 Classification to delete.'))
        return parser

    def take_action(self, parsed_args):
        id = parsed_args.ipv4_classification
        client = self.app.client_manager.neutronclient
        client.delete_ext(object_path + '/%s', id)


class ListIPV4Classification(command.Lister):
    """List the IPV4 Classification that belong to a given tenant."""

    def take_action(self, parsed_args):
        data = self.app.client_manager.neutronclient.list(
            collection='classifications',
            path=object_path, retrieve_all=True, c_type='ipv4')
        headers = ('ID', 'Name', 'Description', 'Negated', 'Shared',
                   'Definition')
        columns = ('id', 'name', 'description', 'negated', 'shared',
                   'definition')

        return (headers, (utils.get_dict_properties(
            s, columns) for s in data['classifications']))


class ShowIPV4Classification(command.ShowOne):
    """Show information of a given IPV4 Classification"""

    def get_parser(self, prog_name):
        parser = super(ShowIPV4Classification, self).get_parser(prog_name)
        parser.add_argument(
            'ipv4_classification',
            metavar="IPV4_CLASSIFICATION",
            help=('ID of the IPV4 Classification to display.'))

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.neutronclient
        cl = client.show_ext(object_path + '/%s',
                             parsed_args.ipv4_classification, c_type='ipv4')
        columns = _get_columns(cl[resource])
        data = utils.get_dict_properties(cl[resource], columns)
        return columns, data


class UpdateIPV4Classification(command.ShowOne):
    """Update name and description of a given IPV4Classification."""

    def get_parser(self, prog_name):
        parser = super(UpdateIPV4Classification, self).get_parser(prog_name)
        parser.add_argument(
            '--name', default='',
            metavar='NAME',
            help=('Name of the IPV4 Classification.'))
        parser.add_argument(
            '--description', default='',
            help=('Description of the IPV4 Classification.'))
        parser.add_argument(
            'ipv4_classification',
            metavar="IPV4_CLASSIFICATION",
            help=('ID of the IPV4 Classification to update.'))

        return parser

    def take_action(self, parsed_args):
        id = parsed_args.ipv4_classification
        client = self.app.client_manager.neutronclient
        attrs = _get_attrs(self.app.client_manager,
                           parsed_args, is_create=False)
        cl = client.update_ext(object_path + '/%s', id, {resource: attrs})
        columns = _get_columns(cl[resource])
        data = utils.get_dict_properties(cl[resource], columns)
        return columns, data


def _get_attrs(client_manager, parsed_args, is_create=False):
    attrs = {}
    definition = {}

    if parsed_args.name is not None:
        attrs['name'] = str(parsed_args.name)
    if parsed_args.description is not None:
        attrs['description'] = str(parsed_args.description)
    if is_create:
        attrs['c_type'] = 'ipv4'
        if parsed_args.negated is not None:
            attrs['negated'] = str(parsed_args.negated)
        if parsed_args.shared is not None:
            attrs['shared'] = str(parsed_args.shared)
        if parsed_args.dscp is not None:
            definition['dscp'] = parsed_args.dscp
        if parsed_args.dscp_mask is not None:
            definition['dscp_mask'] = parsed_args.dscp_mask
        if parsed_args.ecn is not None:
            definition['ecn'] = parsed_args.ecn
        if parsed_args.length_min is not None:
            definition['length_min'] = parsed_args.length_min
        if parsed_args.length_max is not None:
            definition['length_max'] = parsed_args.length_max
        if parsed_args.ttl_min is not None:
            definition['ttl_min'] = parsed_args.ttl_min
        if parsed_args.flags is not None:
            definition['flags'] = parsed_args.flags
        if parsed_args.flags_mask is not None:
            definition['flags_mask'] = parsed_args.flags_mask
        if parsed_args.protocol is not None:
            definition['protocol'] = parsed_args.protocol
        if parsed_args.src_addr is not None:
            definition['src_addr'] = parsed_args.src_addr
        if parsed_args.dst_addr is not None:
            definition['dst_addr'] = parsed_args.dst_addr
        if parsed_args.options is not None:
            definition['options'] = parsed_args.options
        if parsed_args.options_mask is not None:
            definition['options_mask'] = parsed_args.options_mask
        attrs['definition'] = definition

    return attrs


def _get_columns(resource):
    columns = list(resource.keys())
    if 'tenant_id' in columns:
        columns.remove('tenant_id')
    if 'project_id' not in columns:
        columns.append('project_id')
    return tuple(sorted(columns))
