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
object_path = PREFIX + "/ipv6_classifications"
resource = 'ipv6_classification'


class CreateIPV6Classification(command.ShowOne):
    """Create an IPV6 Classification."""

    def get_parser(self, prog_name):
        parser = super(CreateIPV6Classification, self).get_parser(prog_name)
        parser.add_argument(
            'name', metavar='NAME',
            help=('Name of the IPV6 Classification.'))
        parser.add_argument(
            '--description',
            help=('Description for the IPV6 Classification.'))
        parser.add_argument(
            '--negated',
            help=('Whether the complement of the IPV6\
                  Classification should be matched.'))
        parser.add_argument(
            '--shared',
            help=('Whether the IPV6 Classification should be\
                  shared with other projects.'))
        parser.add_argument(
            '--traffic-class',
            help=('Traffic Class Classification value. Type of Service.'))
        parser.add_argument(
            '--length',
            help=('Length of the Packet, following the IPV6 Header.'))
        parser.add_argument(
            '--next_header',
            help=('Type of the next header. Transport protocol used by\
                  the packet\'s payload.'))
        parser.add_argument(
            '--hops',
            help=('Number of hops which the packet may be routed.'))
        parser.add_argument(
            '--src-addr',
            help=('Source Address of the IPV6 Classification.'))
        parser.add_argument(
            '--dst-addr',
            help=('Destination Address of the IPV6 Classification.'))

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.neutronclient
        attrs = _get_attrs(self.app.client_manager,
                           parsed_args, is_create=True)
        obj = client.create_ext(object_path, {resource: attrs})
        columns = _get_columns(obj[resource])
        data = utils.get_dict_properties(obj[resource], columns)
        return columns, data


class DeleteIPV6Classification(command.Command):
    """Delete a given IPV6 Classification."""

    def get_parser(self, prog_name):
        parser = super(DeleteIPV6Classification, self).get_parser(prog_name)
        parser.add_argument(
            'ipv6_classification',
            metavar="IPV6_CLASSIFICATION",
            help=('ID of the IPV6 Classification to delete.'))

        return parser

    def take_action(self, parsed_args):
        id = parsed_args.ipv6_classification
        client = self.app.client_manager.neutronclient
        client.delete_ext(object_path + '/%s', id)


class ListIPV6Classification(command.Lister):
    """List the IPV6 Classification that belong to a given tenant."""

    def take_action(self, parsed_args):
        data = self.app.client_manager.neutronclient.list(
            collection='ipv6_classifications',
            path=object_path, retrieve_all=True)
        headers = ('ID', 'Name', 'Description', 'Negated', 'Shared',
                   'Traffic Class', 'Length', 'Next Header', 'Hops',
                   'Source Addr', 'Destination Addr')
        columns = ('id', 'name', 'description', 'negated', 'shared',
                   'traffic-class', 'length', 'next-header', 'hops',
                   'src-addr', 'dst-addr')

        return (headers, (utils.get_dict_properties(
            s, columns) for s in data['ipv6_classifications']))


class ShowIPV6Classification(command.ShowOne):
    """Show informcation of a given IPV6 Classification."""

    def get_parser(self, prog_name):
        parser = super(ShowIPV6Classification, self).get_parser(prog_name)
        parser.add_argument(
            'ipv6_classification',
            metavar="IPV6_CLASSIFICATION",
            help=('ID of the IPV6 Classification to display.'))

        return parser

    def take_action(self, parsed_args):
        id = parsed_args.ipv6_classification
        client = self.app.client_manager.neutronclient
        cl = client.show_ext(object_path + '/%s', id)
        columns = _get_columns(cl[resource])
        data = utils.get_dict_properties(cl[resource], columns)
        return columns, data


class UpdateIPV6Classification(command.Command):
    """Update name and description of a given IPV6 Classification."""

    def get_parser(self, prog_name):
        parser = super(UpdateIPV6Classification, self).get_parser(prog_name)
        parser.add_argument(
            '--name', default='',
            metavar='NAME',
            help=('Name of the IPV6 Classification.'))
        parser.add_argument(
            '--description', default='',
            help=('Description for the IPV6 Classification.'))
        parser.add_argument(
            'ipv6_classification',
            metavar="IPV6_CLASSIFICATION",
            help=('ID of the IPV6 Classification to update.'))

        return parser

    def take_action(self, parsed_args):
        id = parsed_args.ipv6_classification
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
        attribute = 'traffic-class'
        if getattr(parsed_args, attribute.replace('-', '_')) is not None:
            attrs['traffic-class'] = getattr(
                parsed_args, attribute.replace('-', '_'))
        if parsed_args.length is not None:
            attrs['length'] = parsed_args.length
        attribute = 'next-header'
        if getattr(parsed_args, attribute.replace('-', '_')) is not None:
            attrs['next-header'] = getattr(
                parsed_args, attribute.replace('-', '-'))
        if parsed_args.hops is not None:
            attrs['hops'] = parsed_args.hops
        attribute = 'src-addr'
        if getattr(parsed_args, attribute.replace('-', '_')) is not None:
            attrs['src-addr'] = getattr(
                parsed_args, attribute.replace('-', '-'))
        attribute = 'dst-addr'
        if getattr(parsed_args, attribute.replace('-', '_')) is not None:
            attrs['dst-addr'] = getattr(
                parsed_args, attribute.replace('-', '_'))

    return attrs


def _get_columns(resource):
    columns = list(resource.keys())
    if 'tenant_id' in columns:
        columns.remove('tenant_id')
    if 'project_id' not in columns:
        columns.append('project_id')
    return tuple(sorted(columns))
