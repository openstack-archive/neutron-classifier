# Copyright 2017 Intel. All rights reserved.
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

from oslo_versionedobjects import fields as obj_fields

from neutron_lib.db import constants as attr

def validate_string(String):
    if String is None:
        String = ''
    return String

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
    'project_id': {
        'allow_post': True, 'allow_put': False,
        'is_visible': True,
        'validate': {'type:string': attr.PROJECT_ID_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'dscp': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE },
        'convert_to': validate_string,
        'required_by_policy': True},
    'dscp_mask': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'ecn': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'ecn_mask': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'protocol': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'protocol_mask': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'source_address': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'source_address_range': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'destination_address': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'destination_address_range': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
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
    'project_id': {
        'allow_post': True, 'allow_put': False,
        'is_visible': True,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'traffic_class': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'traffic_class_mask': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'next_header': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'next_header_mask': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'flow_label': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'flow_label_mask': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'source_address': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'source_address_range': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'destination_address': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'destination_address_range': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.IP_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
}

NEUTRON_CLASSIFICATION_RESOURCE_MAP = {
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
    'project_id': {
        'allow_post': True, 'allow_put': False,
        'is_visible': True,
        'validate': {'type:string': attr.PROJECT_ID_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'source_port_uuid': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.UUID_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'source_subnet_uuid': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.UUID_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'source_network_uuid': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.UUID_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'destination_port_uuid': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.UUID_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'destination_subnet_uuid': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.UUID_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'destination_network_uuid': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.UUID_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
}

TRANSPORT_CLASSIFICATION_RESOURCE_MAP = {
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
    'project_id': {
        'allow_post': True, 'allow_put': False,
        'is_visible': True,
        'validate': {'type:string': attr.PROJECT_ID_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'source_port': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.STATUS_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'source_port_min_range': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.STATUS_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'source_port_range_max': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.STATUS_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'destination_port': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.STATUS_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'destination_port_min_range': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.STATUS_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'destination_port_range_max': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.STATUS_FIELD_SIZE},
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
    'project_id': {
        'allow_post': True, 'allow_put': False,
        'is_visible': True,
        'validate': {'type:string': attr.PROJECT_ID_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'source_mac': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.MAC_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'source_mac_range': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.MAC_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'destination_mac': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.MAC_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'destination_mac_range': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.MAC_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
    'ethernet_type': {
        'allow_post': True, 'allow_put': False,
        'required_by_policy': False,
        'is_visible': True,
        'default': None,
        'validate': {'type:string': attr.MAC_ADDR_FIELD_SIZE},
        'convert_to': validate_string,
        'required_by_policy': True},
}
