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
object_path = PREFIX + "/ethernet_classifications"
resource = 'ethernet_classification'


class CreateEthernetClassification(command.ShowOne):
    """Create an Ethernet Classification."""

    def get_parser(self, prog_name):
        parser = super(CreateEthernetClassification,
                       self).get_parser(prog_name)
        parser.add_argument(
            'name', metavar='NAME',
            help=('Name of the Ethernet Classification.'))
        parser.add_argument(
            '--description',
            help=('Description for the Ethernet Classification.'))
        parser.add_argument(
            '--negated',
            help=('Whether the complement of the Ethernet\
                  Classification should be matched.'))
        parser.add_argument(
            '--shared',
            help=('Whether the Ethernet Classification should\
                  be shared with other projects.'))
        parser.add_argument(
            '--preamble',
            help=('Transmission criteria of the Ethernet Classification.'))
        parser.add_argument(
            '--src-addr',
            help=('Source MAC Address of the Ethernet Classification.'))
        parser.add_argument(
            '--dst-addr',
            help=('Destination MAC Address of the Ethernet\
                  Classification.'))
        parser.add_argument(
            '--ethertype',
            help=('Protocol value of the Ethernet Classification.'))

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.neutronclient
        attrs = _get_attrs(self.app.client_manager,
                           parsed_args, is_create=True)
        obj = client.create_ext(object_path, {resource: attrs})
        columns = _get_columns(obj[resource])
        data = utils.get_dict_properties(obj[resource], columns)
        return columns, data


class DeleteEthernetClassification(command.Command):
    """Delete a given Ethernet Classification."""

    def get_parser(self, prog_name):
        parser = super(DeleteEthernetClassification,
                       self).get_parser(prog_name)
        parser.add_argument(
            'ethernet_classification',
            metavar="ETHERNET_CLASSIFICATION",
            help=('ID of the Ethernet Classification to delete.'))

        return parser

    def take_action(self, parsed_args):
        id = parsed_args.ethernet_classification
        client = self.app.client_manager.neutronclient
        client.delete_ext(object_path + '/%s', id)


class ListEthernetClassification(command.Lister):
    """List the Ethernet Classifications that belong to a given tenant."""

    def take_action(self, parsed_args):
        data = self.app.client_manager.neutronclient.list(
            collection='ethernet_classifications',
            path=object_path, retrieve_all=True)
        headers = ('ID', 'Name', 'Description', 'Negated', 'Shared',
                   'Preamble', 'Source Addr', 'Destination Addr',
                   'EtherType')
        columns = ('id', 'name', 'description', 'negated', 'shared',
                   'preamble', 'src-addr', 'dst-addr', 'ethertype')

        return (headers, (utils.get_dict_properties(
            s, columns) for s in data['ethernet_classifications']))


class ShowEthernetClassification(command.ShowOne):
    """Show information of a given Ethernet Classification."""

    def get_parser(self, prog_name):
        parser = super(ShowEthernetClassification, self).get_parser(prog_name)
        parser.add_argument(
            'ethernet_classification',
            metavar="ETHERNET_CLASSIFICATION",
            help=('ID of the Ethernet Classification to display.'))

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.neutronclient
        cl = client.show_ext(object_path + '/%s',
                             parsed_args.ethernet_classification)
        columns = _get_columns(cl[resource])
        data = utils.get_dict_properties(cl[resource], columns)
        return columns, data


class UpdateEthernetClassification(command.Command):
    """Update name and description of a given Ethernet Classification."""

    def get_parser(self, prog_name):
        parser = super(UpdateEthernetClassification,
                       self).get_parser(prog_name)
        parser.add_argument(
            '--name', default='',
            metavar='NAME',
            help=('Name of the Ethernet Classification.'))
        parser.add_argument(
            '--description', default='',
            help=('Description for the Ethernet Classification.'))
        parser.add_argument(
            'ethernet_classification',
            metavar="ETHERNET_CLASSIFICATION",
            help=('ID of the Ethernet Classification to update.'))

        return parser

    def take_action(self, parsed_args):
        id = parsed_args.ethernet_classification
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
        if parsed_args.preamble is not None:
            attrs['preamble'] = parsed_args.preamble
        attribute = 'src-addr'
        if getattr(parsed_args, attribute.replace('-', '_')) is not None:
            attrs['src-addr'] = getattr(
                parsed_args, attribute.replace('-', '_'))
        attribute = 'dst-addr'
        if getattr(parsed_args, attribute.replace('-', '_')) is not None:
            attrs['dst-addr'] = getattr(
                parsed_args, attribute.replace('-', '_'))
        if parsed_args.ethertype is not None:
            attrs['ethertype'] = parsed_args.ethertype

    return attrs


def _get_columns(resource):
    columns = list(resource.keys())
    if 'tenant_id' in columns:
        columns.remove('tenant_id')
    if 'project_id' not in columns:
        columns.append('project_id')
    return tuple(sorted(columns))
