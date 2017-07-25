# Copyright 2017 Intel Corporation.
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

from neutron_lib.api import converters
from neutron_lib.db import constants as const


def validate_string(String):
    if String is None:
        String = ''
    return String

CLASSIFICATION_GROUP_RESOURCE_MAP = {
    'id': {
        'allow_post': False, 'allow_put': False,
        'validate': {'type:uuid': None},
        'is_visible': True, 'primary_key': True},
    'name': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': '',
        'validate': {'type:string': const.NAME_FIELD_SIZE}},
    'description': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': '',
        'validate': {'type:string': const.DESCRIPTION_FIELD_SIZE},
        'convert_to': validate_string},
    'project_id': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': True,
        'validate': {'type:string': const.PROJECT_ID_FIELD_SIZE},
        'is_visible': True},
    'shared': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': False,
        'convert_to': converters.convert_to_boolean},
    'operator': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': 'and',
        'validate': {'type:string': const.NAME_FIELD_SIZE},
        'convert_to': validate_string},
    'classifications': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': [],
        'convert_to': converters.convert_to_list},
    'cg_ids': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': []},
}

CLASSIFICATION_RESOURCE_MAP = {
    'id': {
        'allow_post': False, 'allow_put': False,
        'validate': {'type:uuid': None},
        'is_visible': True, 'primary_key': True},
    'name': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': None,
        'validate': {'type:string': const.NAME_FIELD_SIZE},
        'convert_to': validate_string},
    'description': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': None,
        'validate': {'type:string': const.DESCRIPTION_FIELD_SIZE},
        'convert_to': validate_string},
    'project_id': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': True,
        'validate': {'type:string': const.PROJECT_ID_FIELD_SIZE},
        'is_visible': True},
    'shared': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': False,
        'convert_to': converters.convert_to_boolean},
    'c_type': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': None,
        'validate': {'type:string': const.NAME_FIELD_SIZE},
        'convert_to': validate_string},
    'negated': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': False,
        'convert_to': converters.convert_to_boolean},
    'definition': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True,
        'convert_to': converters.convert_none_to_empty_dict},
}

CLASSIFICATION_TYPE_RESOURCE_MAP = {
    'type': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': None,
        'validate': {'type:string': const.NAME_FIELD_SIZE},
        'convert_to': validate_string},
    'supported_parameters': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': [],
        'convert_to': converters.convert_to_list},
}
