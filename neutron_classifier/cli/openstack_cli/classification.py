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
object_path = PREFIX + "/classification_types"
resource = 'classification_type'


class ListClassificationType(command.Lister):
    """List the Classification Types available."""

    def take_action(self, parsed_args):
        data = self.app.client_manager.neutronclient.list(
            collection='classification_types',
            path=object_path, retrieve_all=True)
        headers = ('Name', 'Parameters')
        columns = ('name', 'parameters')

        return (headers, (utils.get_dict_properties(
            s, columns) for s in data['classification_types']))
