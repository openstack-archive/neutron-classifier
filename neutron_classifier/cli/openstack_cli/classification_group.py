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

object_path = "/classification_groups"
resource = 'classification_group'


class CreateClassificationGroup(command.ShowOne):
    """Create a Classification Group."""

    def get_parser(self, prog_name):
        parser = super(CreateClassificationGroup, self).get_parser(prog_name)
        parser.add_argument(
            'name', metavar='NAME',
            help=('Name of the Classification Group.'))
        parser.add_argument(
            '--description',
            help=('Description for the Classification Group.'))
        parser.add_argument(
            '--classification', nargs='*',
            help=('Classification value.'))
        parser.add_argument(
            '--classification_group', nargs='*',
            help=('ID of the Classification group.'))
        parser.add_argument(
            '--operator',
            help=('Operator to be performed.'))
        parser.add_argument(
            '--shared',
            help=('Whether the Classification group should be '
                  'shared with other projects.'))
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.neutronclient
        attrs = _get_attrs(self.app.client_manager,
                           parsed_args, is_create=True)
        obj = client.create_ext(object_path, {resource: attrs})
        columns = _get_columns(obj[resource])
        data = utils.get_dict_properties(obj[resource], columns)
        return columns, data


class DeleteClassificationGroup(command.Command):
    """Delete a given Classification Group."""

    def get_parser(self, prog_name):
        parser = super(DeleteClassificationGroup, self).get_parser(prog_name)
        parser.add_argument(
            'classification_group',
            metavar="CLASSIFICATION_GROUP",
            help=('ID of the Classification Group to delete.'))

        return parser

    def take_action(self, parsed_args):
        id = parsed_args.classification_group
        client = self.app.client_manager.neutronclient
        client.delete_ext(object_path + '/%s', id)


class ListClassificationGroup(command.Lister):
    """List the Classification Groups that belong to a given tenant."""

    def take_action(self, parsed_args):
        data = self.app.client_manager.neutronclient.list(
            collection='classification_groups', path=object_path,
            retrieve_all=True)
        headers = ('ID', 'Name', 'Description', 'Classifications',
                   'Classification_Groups', 'Operator', 'Shared')
        columns = ('id', 'name', 'description', 'classifications',
                   'classification_groups', 'operator', 'shared')
        print(data)
        print('.................client.............')
        for s in data['classification_groups']:
            print(utils.get_dict_properties(s[resource], columns))
        return (headers, (utils.get_dict_properties(
            s[resource], columns) for s in data['classification_groups']))


class ShowClassificationGroup(command.ShowOne):
    """Show information of a given Classification Group."""

    def get_parser(self, prog_name):
        parser = super(ShowClassificationGroup, self).get_parser(prog_name)
        parser.add_argument(
            'classification_group',
            metavar="CLASSIFICATION_GROUP",
            help=('ID of the Classification Group to display.'))

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.neutronclient
        cl = client.show_ext(object_path + '/%s',
                             parsed_args.classification_group)
        columns = _get_columns(cl[resource])
        data = utils.get_dict_properties(cl[resource], columns)
        return columns, data


class UpdateClassificationGroup(command.Command):

    def get_parser(self, prog_name):
        parser = super(UpdateClassificationGroup, self).get_parser(prog_name)
        parser.add_argument(
            '--name', default='',
            metavar='NAME',
            help=('Name of the Classification Group.'))
        parser.add_argument(
            '--description', default='',
            help=('Description for the Classification Group.'))
        parser.add_argument(
            'classification_group',
            metavar="CLASSIFICATION_GROUP",
            help=('ID of the Classification Group to update.'))

        return parser

    def take_action(self, parsed_args):
        id = parsed_args.classification_group
        client = self.app.client_manager.neutronclient
        attrs = _get_attrs(self.app.client_manager,
                           parsed_args, is_create=False)
        cl = client.update_ext(object_path + '/%s', id, {resource: attrs})
        columns = _get_columns(cl[resource])
        data = utils.get_dict_properties(cl[resource], columns)
        return columns, data


def _get_attrs(client_manager, parsed_args, is_create=False):
    attrs = {}
    if parsed_args.name is not None:
        attrs['name'] = str(parsed_args.name)
    if parsed_args.description is not None:
        attrs['description'] = str(parsed_args.description)
    if is_create:
        if parsed_args.classification is not None:
            attrs['classification'] = parsed_args.classification
        if parsed_args.classification_group is not None:
            attrs['classification_group'] = parsed_args.classification_group
        if parsed_args.operator is not None:
            attrs['operator'] = parsed_args.operator
        if parsed_args.shared is not None:
            attrs['shared'] = parsed_args.shared

    return attrs


def _get_columns(resource):
    columns = list(resource.keys())
    if 'tenant_id' in columns:
        columns.remove('tenant_id')
    if 'project_id' not in columns:
        columns.append('project_id')
    return tuple(sorted(columns))
