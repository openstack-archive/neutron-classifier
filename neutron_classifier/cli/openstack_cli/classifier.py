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

from osc_lib.command import command
from osc_lib import utils

from neutron_classifier.common import constants

CLASSIFIER_PATH = '/classifier'
resource = 'classifier'


class CreateClassifier(command.ShowOne):
    '''Create a traffic classifier for an extension to consume'''

    def get_parser(self, prog_name):
        parser = super(CreateClassifier, self).get_parser(prog_name)

        parser.add_argument(
            'name',
            help=_('Name of the traffic Classifier'))
        parser.add_argument(
            '--description',
            help=_('Description for the Classifier.'))
        parser.add_argument(
            '--type',
            help=_('Classifier traffic type.'))
        for field in constants.ALL_FIELDS:
            parser.add_argument(
                '--' + field,
                help=_('Packet Header Field.'))

        return parser

    def take_action(self, parsed_args):
        pass


class UpdateClassifier(command.Command):
    '''Update a classifier instance'''

    def get_parser(self, prog_name):
        parser = super(CreateClassifier, self).get_parser(prog_name)

        parser.add_argument(
            'name',
            help=_('Name of the traffic Classifier'))
        parser.add_argument(
            '--description',
            help=_('Description for the Classifier.'))
        parser.add_argument(
            'classifier',
            help=_('ID of the Classifier being updated.'))

        return parser

    def take_action(self, parsed_args):
        pass


class DeleteClassifier(command.Command):
    '''Update a classifier instance'''

    def get_parser(self, prog_name):
        parser = super(CreateClassifier, self).get_parser(prog_name)

        parser.add_argument(
            'classifier',
            help=_('ID of the Classifier being updated.'))

        return parser

    def take_action(self, parsed_args):
        pass


class ShowClassifier(command.Command):
    '''Update a classifier instance'''

    def get_parser(self, prog_name):
        parser = super(CreateClassifier, self).get_parser(prog_name)

        parser.add_argument(
            'classifier',
            help=_('ID of the Classifier being updated.'))

        return parser

    def take_action(self, parsed_args):
        pass


class ListClassifier(command.Command):
    '''List all classifier instances'''

    def take_action(self, parsed_args):
        pass
