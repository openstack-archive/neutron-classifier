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

from oslo_log import log as logging

from neutron.db import common_db_mixin

from neutron_classifier.common import constants
from neutron_classifier.common import resources
from neutron_classifier.common import validators
from neutron_classifier.db import models

LOG = logging.getLogger(__name__)


class TrafficClassificationDbPlugin(common_db_mixin.CommonDbMixin):

    def __init__(self):
        super(TrafficClassificationDbPlugin, self).__init__()

    def create_classification_group(self, context, classification_group):
        details = classification_group['classification_group']
        if details['classification']:
            validators.check_valid_classifications(self, context,
                                                   details['classification'])
        if details['classification_group']:
            validators.check_valid_classification_groups(
                self, context, details['classification_group'])
        db_dict = {'name': details['name'],
                   'project_id': details['project_id'],
                   'description': details['description'],
                   'classification': details['classification'],
                   'classification_group': details['classification_group'],
                   'shared': details['shared'],
                   'operator': details['operator']}
        model = models.ClassificationGroup(
            name=details['name'],
            description=details['description'],
            shared=details['shared'],
            operator=details['operator'])

        for key in details.keys():
            if details[key]:
                db_dict[key] = details[key]

        with context.session.begin(subtransactions=True):
            context.session.add(model)
        db_dict['id'] = model.id

        with context.session.begin(subtransactions=True):
            for cl in details['classification']:
                mapping_model = models.ClassificationGroupMapping(
                    cg_id=db_dict['id'],
                    classification_id=cl)
                context.session.add(mapping_model)
            cg_model = models.ClassificationGroup
            for c in details['classification_group']:
                context.session.query(cg_model).filter(
                    cg_model.id == c).update({"cg_id": db_dict['id']},
                                             synchronize_session='evaluate')

        return db_dict

    def delete_classification_group(self, context, classification_group_id):
        model = models.ClassificationGroup
        mapping_model = models.ClassificationGroupMapping
        mappings = self._get_collection(
            context, mapping_model, models._generate_dict_from_cgmapping_db)
        validators.check_can_delete_classification_group(
            self, context, classification_group_id)
        with context.session.begin(subtransactions=True):
            for m in mappings:
                if classification_group_id == m['cg_id']:
                    row = self._get_by_id(
                        context,
                        models.ClassificationGroupMapping, m['id'])
                    context.session.delete(row)
            context.session.query(model).filter(
                model.cg_id == classification_group_id).update({
                    "cg_id": None}, synchronize_session='evaluate')
            cg = self._get_by_id(context,
                                 models.ClassificationGroup,
                                 classification_group_id)
            context.session.delete(cg)

        self._res_name = ""

    def update_classification_group(self, context, classification_group_id,
                                    classification_group):
        details = classification_group['classification_group']
        cg = self.get_classification_group(context, classification_group_id)
        if details['name']:
            cg['name'] = details['name']
        if details['description']:
            cg['description'] = details['description']
        model = models.ClassificationGroup
        with context.session.begin(subtransactions=True):
            context.session.query(model).filter(
                model.id == classification_group_id).update(
                    {"name": cg['name'], "description": cg['description']},
                    synchronize_session='evaluate')
        return cg

    def get_classification_group(self, context,
                                 classification_group_id, **kwargs):
        model = models.ClassificationGroup
        mapping_model = models.ClassificationGroupMapping
        cg = models._read_classification_groups(
            self, context, model, mapping_model, classification_group_id)

        return cg

    def get_classification_groups(self, context, filters=None, fields=None,
                                  sorts=None, limit=None, marker=None,
                                  page_reverse=False):
        model = models.ClassificationGroup
        mapping_model = models.ClassificationGroupMapping
        cg = models._read_classification_groups(
            self, context, model, mapping_model)

        self._res_name = ""
        return cg

    def get_classification_types(self, context, **kwargs):
        resp = []
        avoid = ['project_id', 'id', 'description']
        resp.append({'name': 'ipv4', 'parameters': ','.join(
            [key for key, value in
                resources.IPV4_CLASSIFICATION_RESOURCE_MAP.iteritems()
                if key not in avoid])})
        resp.append({'name': 'ipv6', 'parameters': ','.join(
            [key for key, value in
                resources.IPV6_CLASSIFICATION_RESOURCE_MAP.iteritems()
                if key not in avoid])})
        resp.append({'name': 'tcp', 'parameters': ','.join(
            [key for key, value in
                resources.TCP_CLASSIFICATION_RESOURCE_MAP.iteritems()
                if key not in avoid])})
        resp.append({'name': 'udp', 'parameters': ','.join(
            [key for key, value in
                resources.UDP_CLASSIFICATION_RESOURCE_MAP.iteritems()
                if key not in avoid])})
        resp.append({'name': 'ethernet', 'parameters': ','.join(
            [key for key, value in
                resources.ETHERNET_CLASSIFICATION_RESOURCE_MAP.iteritems()
                if key not in avoid])})
        return resp

    def generate_dict_from_db(self, model, fields=None):
        name = self._res_name[:-1] if 'classifications' in self._res_name\
            else self._res_name
        response = models.DICT_RESP[name](model, fields)
        return response

    def create_ipv4_classification(self, context, ipv4_classification):
        details = ipv4_classification['ipv4_classification']
        db_dict = {'name': details['name'],
                   'project_id': details['project_id'],
                   'description': details['description'],
                   'c_type': "ipv4_classification"}
        details = validators.check_valid_ipv4_classification(details)
        ihl = details['ihl']
        diffserv = details['diffserv']
        diffserv_mask = details['diffserv_mask']
        flags = details['flags']
        flags_mask = details['flags_mask']
        ttl = details['ttl']
        protocol = details['protocol']
        src_addr = details['src_addr']
        dst_addr = details['dst_addr']
        options = details['options']
        options_mask = details['options_mask']

        model = models.IPV4Classification(
            ihl=ihl,
            diffserv=diffserv,
            diffserv_mask=diffserv_mask,
            flags=flags,
            flags_mask=flags_mask,
            ttl=ttl,
            protocol=protocol,
            src_addr=src_addr,
            dst_addr=dst_addr,
            options=options,
            options_mask=options_mask,
            name=details['name'],
            description=details['description'],
            negated=details['negated'],
            shared=details['shared'])

        for key in details.keys():
            if details[key]:
                db_dict[key] = details[key]

        with context.session.begin(subtransactions=True):
            context.session.add(model)

        db_dict['id'] = model.id
        return db_dict

    def create_ipv6_classification(self, context, ipv6_classification):
        details = ipv6_classification['ipv6_classification']
        db_dict = {'name': details['name'],
                   'project_id': details['project_id'],
                   'description': details['description'],
                   'c_type': "ipv6_classification"}

        traffic_class = details['traffic_class']
        traffic_class_mask = details['traffic_class_mask']
        length = details['length']
        next_header = details['next_header']
        hops = details['hops']
        src_addr = details['src_addr']
        dst_addr = details['dst_addr']
        model = models.IPV6Classification(
            traffic_class=traffic_class,
            traffic_class_mask=traffic_class_mask,
            length=length,
            next_header=next_header,
            hops=hops,
            src_addr=src_addr,
            dst_addr=dst_addr,
            name=details['name'],
            description=details['description'],
            negated=details['negated'],
            shared=details['shared'])

        for key in details.keys():
            if details[key]:
                db_dict[key] = details[key]

        with context.session.begin(subtransactions=True):
            context.session.add(model)

        db_dict['id'] = model.id
        return db_dict

    def create_ethernet_classification(self, context,
                                       ethernet_classification):
        details = ethernet_classification['ethernet_classification']
        db_dict = {'name': details['name'],
                   'project_id': details['project_id'],
                   'description': details['description'],
                   'classification': "ethernet_classification"}
        preamble = details['preamble']
        ethertype = details['ethertype']
        src_addr = details['src_addr']
        dst_addr = details['dst_addr']
        model = models.EthernetClassification(
            ethertype=ethertype,
            preamble=preamble,
            src_addr=src_addr,
            dst_addr=dst_addr,
            name=details['name'],
            description=details['description'],
            negated=details['negated'],
            shared=details['shared'])

        for key in details.keys():
            if details[key]:
                db_dict[key] = details[key]

        with context.session.begin(subtransactions=True):
            context.session.add(model)

        db_dict['id'] = model.id
        return db_dict

    def create_udp_classification(self, context, udp_classification):
        details = udp_classification['udp_classification']
        db_dict = {'name': details['name'],
                   'project_id': details['project_id'],
                   'description': details['description'],
                   'classification': "udp_classification"}
        src_port = details['src_port']
        dst_port = details['dst_port']
        length = details['length']
        window_size = details['window_size']
        model = models.UDPClassification(
            src_port=src_port,
            dst_port=dst_port,
            length=length,
            window_size=window_size,
            name=details['name'],
            description=details['description'],
            negated=details['negated'],
            shared=details['shared'])

        for key in details.keys():
            if details[key]:
                db_dict[key] = details[key]

        with context.session.begin(subtransactions=True):
            context.session.add(model)

        db_dict['id'] = model.id
        return db_dict

    def create_tcp_classification(self, context, tcp_classification):
        details = tcp_classification['tcp_classification']
        db_dict = {'name': details['name'],
                   'project_id': details['project_id'],
                   'description': details['description'],
                   'c_type': "tcp_classification"}
        src_port = details['src_port']
        dst_port = details['dst_port']
        flags = details['flags']
        flags_mask = details['flags_mask']
        windows = details['window']
        data_offset = details['data_offset']
        option_kind = details['option_kind']
        model = models.TCPClassification(
            src_port=src_port,
            dst_port=dst_port,
            flags=flags,
            flags_mask=flags_mask,
            window=windows,
            data_offset=data_offset,
            option_kind=option_kind,
            name=details['name'],
            description=details['description'],
            negated=details['negated'],
            shared=details['shared'])

        for key in details.keys():
            if details[key]:
                db_dict[key] = details[key]

        with context.session.begin(subtransactions=True):
            context.session.add(model)

        db_dict['id'] = model.id
        return db_dict

    def _delete_resource(self, context, id):
        with context.session.begin(subtransactions=True):
            cl = self._get_by_id(context,
                                 models.RESOURCE_MODELS[self._res_name],
                                 id)
            context.session.delete(cl)
        self._res_name = ""

    def _get_resource(self, context, id=None, **kwargs):
        if 'classifications' not in self._res_name:
            cl = self._get_by_id(context,
                                 models.RESOURCE_MODELS[self._res_name],
                                 id)
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
            model = models.RESOURCE_MODELS[self._res_name[:-1]]
            marker_obj = self._get_marker_obj(context, self._res_name,
                                              limit, marker)
            cl = self._get_collection(context, model,
                                      self.generate_dict_from_db,
                                      filters=filters, fields=fields,
                                      sorts=sorts,
                                      limit=limit, marker_obj=marker_obj,
                                      page_reverse=page_reverse)
            self._res_name = ""
            return cl

    def _update_resource(self, context, classification_id, **kwargs):
        cl = self._get_resource(context, classification_id)
        resource_type = kwargs.keys()[0]
        resource = kwargs[resource_type][resource_type]
        model = models.ClassificationBase

        if resource['name']:
            cl['name'] = resource['name']
        if resource['description']:
            cl['description'] = resource['description']
        with context.session.begin(subtransactions=True):
            context.session.query(model).filter(
                model.id == classification_id).update(
                    {"name": cl['name'], "description": cl['description']},
                    synchronize_session='evaluate')
        return cl

    def __getattr__(self, resource):
        res = resource.partition('_')
        action = {'delete': self._delete_resource,
                  'get': self._get_resource,
                  'update': self._update_resource}

        res_action = res[0]
        res_name = res[2]

        if (res_name[:-1] not in constants.CLASSIFIER_FIELDS.keys() and
                res_name not in constants.CLASSIFIER_FIELDS.keys()):
            return (super(TrafficClassificationDbPlugin, self).
                    __getattr__(resource))

        if res_action not in action.keys():
            return (super(TrafficClassificationDbPlugin, self).
                    __getattr__(resource))

        self._res_name = res_name
        return action[res_action]
