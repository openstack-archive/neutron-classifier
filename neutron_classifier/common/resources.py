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
from neutron_lib.db import constants as attr


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
        'validate': {'type:string': attr.NAME_FIELD_SIZE}},
    'description': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': '',
        'validate': {'type:string': attr.DESCRIPTION_FIELD_SIZE},
        'convert_to': validate_string},
    'project_id': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': True,
        'validate': {'type:string': attr.PROJECT_ID_FIELD_SIZE},
        'is_visible': True},
    'shared': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': False,
        'convert_to': converters.convert_to_boolean},
    'operator': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': 'and',
        'validate': {'type:string': attr.NAME_FIELD_SIZE},
        'convert_to': validate_string},
    'classification': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': [],
        'convert_to': converters.convert_to_list},
    'classification_group': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': ''},
}

CLASSIFICATION_RESOURCE_MAP = {
    'id': {
        'allow_post': False, 'allow_put': False,
        'validate': {'type:uuid': None},
        'is_visible': True, 'primary_key': True},
    'c_type': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': None,
        'validate': {'type:string': attr.NAME_FIELD_SIZE},
        'convert_to': validate_string},
    'name': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': None,
        'validate': {'type:string': attr.NAME_FIELD_SIZE},
        'convert_to': validate_string},
    'description': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': None,
        'validate': {'type:string': attr.DESCRIPTION_FIELD_SIZE},
        'convert_to': validate_string},
    'negated': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': False,
        'convert_to': converters.convert_to_boolean},
    'shared': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': False,
        'convert_to': converters.convert_to_boolean},
    'project_id': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': True,
        'validate': {'type:string': attr.PROJECT_ID_FIELD_SIZE},
        'is_visible': True},
}

IPV4_CLASSIFICATION_RESOURCE_MAP = {
    'id': {
        'allow_post': False, 'allow_put': False,
        'is_visible': True,
        'validate': {'type:uuid': None},
        'primary_key': True},
    'name': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': None,
        'validate': {'type:string': attr.NAME_FIELD_SIZE},
        'convert_to': validate_string},
    'description': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': None,
        'validate': {'type:string': attr.DESCRIPTION_FIELD_SIZE},
        'convert_to': validate_string},
    'negated': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': False,
        'convert_to': converters.convert_to_boolean},
    'shared': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': False,
        'convert_to': converters.convert_to_boolean},
    'project_id': {
        'allow_post': True, 'allow_put': False,
        'is_visible': True,
        'validate': {'type:string': attr.PROJECT_ID_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'ihl': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'diffserv': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'diffserv_mask': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'length': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'flags': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'flags_mask': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'ttl': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'protocol': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'src_addr': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'dst_addr': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'options': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'options_mask': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
}

IPV6_CLASSIFICATION_RESOURCE_MAP = {
    'id': {
        'allow_post': False, 'allow_put': False,
        'is_visible': True,
        'validate': {'type:uuid': None},
        'primary_key': True},
    'name': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': None,
        'validate': {'type:string': attr.NAME_FIELD_SIZE},
        'convert_to': validate_string},
    'description': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': None,
        'validate': {'type:string': attr.DESCRIPTION_FIELD_SIZE},
        'convert_to': validate_string},
    'negated': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': False,
        'convert_to': converters.convert_to_boolean},
    'shared': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': False,
        'convert_to': converters.convert_to_boolean},
    'project_id': {
        'allow_post': True, 'allow_put': False,
        'is_visible': True,
        'validate': {'type:string': attr.PROJECT_ID_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'traffic_class': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'traffic_class_mask': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'length': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'next_header': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'hops': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'src_addr': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'dst_addr': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
}

ETHERNET_CLASSIFICATION_RESOURCE_MAP = {
    'id': {
        'allow_post': False, 'allow_put': False,
        'is_visible': True,
        'validate': {'type:uuid': None},
        'primary_key': True},
    'name': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': None,
        'validate': {'type:string': attr.NAME_FIELD_SIZE},
        'convert_to': validate_string},
    'description': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': None,
        'validate': {'type:string': attr.DESCRIPTION_FIELD_SIZE},
        'convert_to': validate_string},
    'negated': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': False,
        'convert_to': converters.convert_to_boolean},
    'shared': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': False,
        'convert_to': converters.convert_to_boolean},
    'project_id': {
        'allow_post': True, 'allow_put': False,
        'is_visible': True,
        'validate': {'type:string': attr.PROJECT_ID_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'preamble': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'ethertype': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'src_addr': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.MAC_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'dst_addr': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.MAC_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
}

UDP_CLASSIFICATION_RESOURCE_MAP = {
    'id': {
        'allow_post': False, 'allow_put': False,
        'is_visible': True,
        'validate': {'type:uuid': None},
        'primary_key': True},
    'name': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': None,
        'validate': {'type:string': attr.NAME_FIELD_SIZE},
        'convert_to': validate_string},
    'description': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': None,
        'validate': {'type:string': attr.DESCRIPTION_FIELD_SIZE},
        'convert_to': validate_string},
    'negated': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': False,
        'convert_to': converters.convert_to_boolean},
    'shared': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': False,
        'convert_to': converters.convert_to_boolean},
    'project_id': {
        'allow_post': True, 'allow_put': False,
        'is_visible': True,
        'validate': {'type:string': attr.PROJECT_ID_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'src_port': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'dst_port': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'length': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'window_size': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
}

TCP_CLASSIFICATION_RESOURCE_MAP = {
    'id': {
        'allow_post': False, 'allow_put': False,
        'is_visible': True,
        'validate': {'type:uuid': None},
        'primary_key': True},
    'name': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': None,
        'validate': {'type:string': attr.NAME_FIELD_SIZE},
        'convert_to': validate_string},
    'description': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': None,
        'validate': {'type:string': attr.DESCRIPTION_FIELD_SIZE},
        'convert_to': validate_string},
    'negated': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': False,
        'convert_to': converters.convert_to_boolean},
    'shared': {
        'allow_post': True, 'allow_put': True,
        'is_visible': True, 'default': False,
        'convert_to': converters.convert_to_boolean},
    'project_id': {
        'allow_post': True, 'allow_put': False,
        'is_visible': True,
        'validate': {'type:string': attr.PROJECT_ID_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'src_port': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'dst_port': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'flags': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'flags_mask': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'window': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'data_offset': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
    'option_kind': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'required_by_policy': True},
}
