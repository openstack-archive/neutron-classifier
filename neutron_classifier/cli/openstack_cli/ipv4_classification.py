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
object_path = PREFIX + "/ipv4_classifications"
resource = 'ipv4_classification'


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
            help=('Whether the complement of the IPV4\
                  Classification should be matched.'))
        parser.add_argument(
            '--shared',
            help=('Whether the IPV4 Classification should be\
                  shared with other projects.'))
        parser.add_argument(
            '--ihl',
            help=('Length of the IP header.'))
        parser.add_argument(
            '--diffserv',
            help=('DSCP Classification value. Type of Service.'))
        parser.add_argument(
            '--length',
            help=('Length of the IP Packet, including IP header\
                  and IP payload.'))
        parser.add_argument(
            '--flags',
            help=('Whether the packet can be fragmented.'))
        parser.add_argument(
            '--ttl',
            help=('Number of hops which the packet may be routed\
                  over.'))
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
            collection='ipv4_classifications',
            path=object_path, retrieve_all=True)
        headers = ('ID', 'Name', 'Description', 'Negated', 'Shared',
                   'IHL', 'DiffServ', 'Length', 'Flags', 'TTL',
                   'Protocol', 'Source Addr', 'Destination Addr', 'Options')
        columns = ('id', 'name', 'description', 'negated', 'shared',
                   'ihl', 'diffserv', 'length', 'flags', 'ttl',
                   'protocol', 'src_addr', 'dst_addr', 'options')

        return (headers, (utils.get_dict_properties(
            s, columns) for s in data['ipv4_classifications']))


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
                             parsed_args.ipv4_classification)
        columns = _get_columns(cl[resource])
        data = utils.get_dict_properties(cl[resource], columns)
        return columns, data


class UpdateIPV4Classification(command.Command):
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
        client.update_ext(object_path + '/%s', id, {resource: attrs})


def _get_attrs(client_manager, parsed_args, is_create=False):
    attrs = {}
    if parsed_args.name is not None:
        attrs['name'] = str(parsed_args.name)
    if parsed_args.description is not None:
        attrs['description'] = str(parsed_args.description)
    if parsed_args.negated is not None:
        attrs['negated'] = str(parsed_args.negated)
    if parsed_args.shared is not None:
        attrs['shared'] = str(parsed_args.shared)
    if is_create:
        if parsed_args.ihl is not None:
            attrs['ihl'] = parsed_args.ihl
        if parsed_args.diffserv is not None:
            attrs['diffserv'] = parsed_args.diffserv
        if parsed_args.length is not None:
            attrs['length'] = parsed_args.length
        if parsed_args.flags is not None:
            attrs['flags'] = parsed_args.flags
        if parsed_args.ttl is not None:
            attrs['ttl'] = parsed_args.min_ttl
        if parsed_args.protocol is not None:
            attrs['protocol'] = parsed_args.protocol
        attribute = 'src-addr'
        if getattr(parsed_args, attribute.replace('-', '_')) is not None:
            attrs['src_addr'] = getattr(
                parsed_args, attribute.replace('-', '_'))
        attribute = 'dst-addr'
        if getattr(parsed_args, attribute.replace('-', '_')) is not None:
            attrs['dst_addr'] = getattr(
                parsed_args, attribute.replace('-', '_'))
        if parsed_args.options is not None:
            attrs['options'] = parsed_args.options

    return attrs


def _get_columns(resource):
    columns = list(resource.keys())
    if 'tenant_id' in columns:
        columns.remove('tenant_id')
    if 'project_id' not in columns:
        columns.append('project_id')
    return tuple(sorted(columns))
