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

object_path = "/classifications"
resource = 'classification'


class CreateTCPClassification(command.ShowOne):
    """Create a TCP Classification."""

    def get_parser(self, prog_name):
        parser = super(CreateTCPClassification, self).get_parser(prog_name)
        parser.add_argument(
            'name', metavar='NAME',
            help=('Name of the TCP Classification.'))
        parser.add_argument(
            '--description',
            help=('Description for the TCP Classification.'))
        parser.add_argument(
            '--negated',
            help=('Whether the complement of the TCP '
                  'Classification should be matched.'))
        parser.add_argument(
            '--shared',
            help=('Whether the TCP Classification should be '
                  'shared with other projects.'))
        parser.add_argument(
            '--src-port-min',
            help=('Source port TCP Classification minimum value.'))
        parser.add_argument(
            '--src-port-max',
            help=('Source port TCP Classification maximum value.'))
        parser.add_argument(
            '--dst-port-min',
            help=('Destination port TCP Classification minimum value.'))
        parser.add_argument(
            '--dst-port-max',
            help=('Destination port TCP Classification maximum value.'))
        parser.add_argument(
            '--flags',
            help=('Control flag value for the TCP Classification.'))
        parser.add_argument(
            '--flags-mask',
            help=('Control flag valye for the TCP Classification.'))
        parser.add_argument(
            '--window-min',
            help=('The minimum size of the receive window. Number of data '
                  'octets the receiver is willing to accept.'))
        parser.add_argument(
            '--window-max',
            help=('The maximum size of the receive window. Number of data '
                  'octets the receiver is willing to accept.'))
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.neutronclient
        attrs = _get_attrs(self.app.client_manager,
                           parsed_args, is_create=True)
        obj = client.create_ext(object_path, {resource: attrs})
        columns = _get_columns(obj[resource])
        data = utils.get_dict_properties(obj[resource], columns)
        return columns, data


class DeleteTCPClassification(command.Command):
    """Delete a given TCP Classification."""

    def get_parser(self, prog_name):
        parser = super(DeleteTCPClassification, self).get_parser(prog_name)
        parser.add_argument(
            'tcp_classification',
            metavar="TCP_CLASSIFICATION",
            help=('ID of the TCP Classification to delete.'))

        return parser

    def take_action(self, parsed_args):
        id = parsed_args.tcp_classification
        client = self.app.client_manager.neutronclient
        client.delete_ext(object_path + '/%s', id)


class ListTCPClassification(command.Lister):
    """List the TCP Classification that belong to a given tenant."""

    def take_action(self, parsed_args):
        data = self.app.client_manager.neutronclient.list(
            collection='classifications',
            path=object_path, retrieve_all=True, c_type='tcp')
        headers = ('C_Type', 'ID', 'Name', 'Description', 'Negated', 'Shared')
        columns = ('c_type', 'id', 'name', 'description', 'negated', 'shared')

        return (headers, (utils.get_dict_properties(
            s, columns) for s in data['classifications']))


class ShowTCPClassification(command.ShowOne):
    """Show information of a given TCP Classification."""

    def get_parser(self, prog_name):
        parser = super(ShowTCPClassification, self).get_parser(prog_name)
        parser.add_argument(
            'tcp_classification',
            metavar="TCP_CLASSIFICATION",
            help=('ID of the TCP Classification to display.'))

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.neutronclient
        cl = client.show_ext(object_path + '/%s',
                             parsed_args.tcp_classification, c_type='tcp')
        columns = _get_columns(cl[resource])
        data = utils.get_dict_properties(cl[resource], columns)
        return columns, data


class UpdateTCPClassification(command.ShowOne):
    """Update name and description of a given TCP Classification."""

    def get_parser(self, prog_name):
        parser = super(UpdateTCPClassification, self).get_parser(prog_name)
        parser.add_argument(
            '--name', default='',
            metavar='NAME',
            help=('Name of the TCP Classification.'))
        parser.add_argument(
            '--description', default='',
            help=('Description of the TCP Classification.'))
        parser.add_argument(
            'tcp_classification',
            metavar="TCP_CLASSIFICATION",
            help=('ID of the TCP Classification to update.'))

        return parser

    def take_action(self, parsed_args):
        id = parsed_args.tcp_classification
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
        attrs['c_type'] = 'tcp'
        if parsed_args.negated is not None:
            attrs['negated'] = str(parsed_args.negated)
        if parsed_args.shared is not None:
            attrs['shared'] = str(parsed_args.shared)
        if parsed_args.src_port_min is not None:
            definition['src_port_min'] = parsed_args.src_port_min
        if parsed_args.src_port_max is not None:
            definition['src_port_max'] = parsed_args.src_port_max
        if parsed_args.dst_port_min is not None:
            definition['dst_port_min'] = parsed_args.dst_port_min
        if parsed_args.dst_port_max is not None:
            definition['dst_port_max'] = parsed_args.dst_port_max
        if parsed_args.flags is not None:
            definition['flags'] = parsed_args.flags
        if parsed_args.flags_mask is not None:
            definition['flags_mask'] = parsed_args.flags_mask
        if parsed_args.window_min is not None:
            definition['window_min'] = parsed_args.window_min
        if parsed_args.window_max is not None:
            definition['window_max'] = parsed_args.window_max
        attrs['definition'] = definition

    return attrs


def _get_columns(resource):
    columns = list(resource.keys())
    if 'tenant_id' in columns:
        columns.remove('tenant_id')
    if 'project_id' not in columns:
        columns.append('project_id')
    return tuple(sorted(columns))
