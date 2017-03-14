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

import netaddr
import six

from oslo_log import helpers as log_helpers
from oslo_log import log as logging
from oslo_utils import uuidutils

import sqlalchemy as sa

from neutron_lib.db import model_base

from neutron.db import common_db_mixin

from neutron_classifier.common import constants
from neutron_classifier.common import resources
from neutron_classifier.common import validators
from neutron_classifier.db import models_v2
from neutron_classifier.extensions import classification

LOG = logging.getLogger(__name__)


class TrafficClassificationDbPlugin(common_db_mixin.CommonDbMixin):

    def __init__(self):
        super(TrafficClassificationDbPlugin, self).__init__()

    def create_classification(self, context, classification):
        cl = classification['classification']
        return {}

    def delete_classification(self, context, classification_id):
        cl = classification['classification']
        return {}

    def generate_dict_from_db(self, model, fields=None):
        name = self._res_name[:-1] if 'classifications' in self._res_name else self._res_name
        response = models_v2.DICT_RESP[name](model, fields)
        return response

    def _create_resource(self, context, **kwargs):
        res_name = self._res_name
        details = kwargs[res_name][res_name]
        db_dict = {'name': details['name'],
                   'project_id': details['project_id'],
                   'description': details['description'],
                   'classification': res_name}

        if 'ipv4' in res_name:
            details = validators.check_valid_ipv4_classification(details)
            src_addr = details['source_address']
            src_addr_range = details['source_address_range']
            dest_addr = details['destination_address']
            dest_addr_range = details['destination_address_range']
            dscp = details['dscp']
            dscp_mask = details['dscp_mask']
            ecn = details['ecn']
            ecn_mask = details['ecn_mask']
            proto = details['protocol']
            proto_mask = details['protocol_mask']

            model = models_v2.IPV4Classification(
                                       source_address=src_addr,
                                       source_address_range=src_addr_range,
                                       destination_address=dest_addr,
                                       destination_address_range=(
                                       dest_addr_range),
                                       dscp=dscp,
                                       dscp_mask=dscp_mask,
                                       ecn=ecn,
                                       ecn_mask=ecn_mask,
                                       protocol=proto,
                                       protocol_mask=proto_mask,
                                       name=details['name'],
                                       description=details['description'])

            for key in details.keys():
                if details[key]:
                    db_dict[key] = details[key]

        elif 'ipv6' in res_name:
            src_addr = details['source_address']
            src_addr_range = details['source_address_range']
            dest_addr = details['destination_address']
            dest_addr_range = details['destination_address_range']
            traffic_cls = details['traffic_class']
            traffic_cls_mask = details['taffic_class_mask']
            next_hdr = details['next_header']
            next_hdr_mask = details['next_header_mask']
            flow_lbl = details['flow_label']
            flow_lbl_mask = details['flow_label_mask']
            model = models_v2.IPV6Classification(
                                       source_address=src_addr,
                                       source_address_range=src_addr_range,
                                       destination_address=dest_addr,
                                       destination_address_range=(
                                       dest_addr_range),
                                       traffic_class=traffic_cls,
                                       traffic_class_mask=traffic_cls_mask,
                                       next_header=next_hdr,
                                       next_header_mask=next_hdr_mask,
                                       flow_label=flow_lbl,
                                       flow_label_mask=flow_lbl_mask,
                                       name=details['name'],
                                       description=details['description'])
            for key in details.keys():
                if details[key]:
                    db_dict[key] = details[key]

        elif 'tcp' in res_name or 'udp' in res_name:
            src_port = details['source_port']
            src_port_min_range = details['source_port_min_range']
            src_port_max_range = details['source_port_max_range']
            dest_port = details['destination_port']
            dest_port_min_range = details['destination_port_min_range']
            dest_port_max_range = details['destination_port_max_range']
            model = models_v2.PortClassification(
                                       source_port_min_range=(
                                       src_port_min_range),
                                       source_port_max_range=(
                                       src_port_max_range),
                                       source_port=src_port,
                                       destination_port_min_range=(
                                       dest_port_min_range),
                                       destination_port_max_range=(
                                       dest_port_max_range),
                                       destination_port=dest_port,
                                       name=details['name'],
                                       description=details['description'])
            if src_port:
                db_dict['source_port'] = port
            elif dest_port:
                db_dict['destination_port'] = port
            elif src_port_max_range:
                db_dict['source_port_min_range'] = src_port_min_range
                db_dict['source_port_max_range'] = src_port_max_range
            elif dest_port_max_range:
                db_dict['source_port_min_range'] = dest_port_min_range
                db_dict['source_port_max_range'] = dest_port_max_range

        elif 'neutron' in res_name:
            src_port = details['source_port']
            src_subnet = details['source_sunbet']
            src_network = details['source_network']
            dest_port = details['destination_port']
            dest_subnet = details['destination_subnet']
            dest_network = details['destination_network']
            model = models_v2.NeutronClassification(
                                       source_port=src_port,
                                       source_subnet=src_subnet,
                                       source_network=src_network,
                                       destination_port=dest_port,
                                       destination_subnet=dest_subnet,
                                       destination_network=dest_network,
                                       name=details['name'],
                                       description=details['description'])

            if None not in src_port:
                db_dict['source_port'] = src_port

            if None not in dest_port:
                db_dict['destination_port'] = dest_port

            if None not in src_subnet:
                db_dict['source_subnet'] = src_subnet

            if None not in dest_subnet:
                db_dict['destination_subnet'] = src_subnet

            if None not in src_network:
                db_dict['source_network'] = src_network

            if None not in dest_network:
                db_dict['destination_network'] = dest_network

        elif 'ethernet' in res_name:
            src_mac = details['source_mac']
            src_mac_range = details['source_mac_range']
            dest_mac = details['destination_mac']
            dest_mac_range = details['destination_mac_range']
            type = details['type']
            type_mask = details['type']
            model = models_v2.EthernetClassification(
                                       source_mac=src_mac,
                                       source_mac_range=src_mac_range,
                                       destination_mac=dest_mac,
                                       destination_mac_range=dest_mac_range,
                                       type=type,
                                       type_mask=type_mask,
                                       name=details['name'],
                                       description=details['description'])
        self._res_name = ""
        with context.session.begin(subtransactions=True):
            context.session.add(model)
            db_dict['id'] = model.id
            return db_dict

    def _delete_resource(self, context, id):
        with context.session.begin(subtransactions=True):
            classification = self._get_by_id(context, models_v2.RESOURCE_MODELS[self._res_name], id)
            context.session.delete(classification)
        self._res_name = ""

    def _get_resource(self, context, id=None, **kwargs):
        if 'classifications' not in self._res_name:
            cl = self._get_by_id(context, models_v2.RESOURCE_MODELS[self._res_name], id)
            classification_dict = self.generate_dict_from_db(cl)
            self._res_name = ""
            return classification_dict
        else:
            fields = kwargs.get('fields')
            filters = kwargs.get('filters')
            sorts = kwargs.get('sorts')
            limit = kwargs.get('limit')
            marker = kwargs.get('marker')
            page_reverse = kwargs.get('page_reverse')
            marker_obj = self._get_marker_obj(context, self._res_name,
                                              limit, marker)
            cl = self._get_collection(context,
                                      models_v2.RESOURCE_MODELS[self._res_name[:-1]],
                                      self.generate_dict_from_db,
                                      filters=filters, fields=fields,
                                      sorts=sorts,
                                      limit=limit, marker_obj=marker_obj,
                                      page_reverse=page_reverse)
            self._res_name = ""
            return cl

    def __getattr__(self, resource):
        res = resource.partition('_')
        action = {'create': self._create_resource,
                  'delete': self._delete_resource,
                  'get': self._get_resource}

        res_action = res[0]
        res_name = res[2]

        if (res_name[:-1] not in constants.CLASSIFIER_FIELDS.keys() and
            res_name not in constants.CLASSIFIER_FIELDS.keys()):
            return super(TrafficClassificationDbPlugin, self).__getattr__(resource)

        if res_action not in actions.keys():
            return super(TrafficClassificationDbPlugin, self).__getattr__(resource)

        self._res_name = res_name
        return action[res_action]
