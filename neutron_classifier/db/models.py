# Copyright (c) 2015 Mirantis, Inc.
# Copyright 2017 Intel Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from neutron_lib.db import model_base

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import pdb

Base = declarative_base()


# Service plugin models
class ClassificationGroup(model_base.BASEV2, model_base.HasId,
                               model_base.HasProject):
    __tablename__ = 'classification_groups'
    name = sa.Column(sa.String(255))
    description = sa.Column(sa.String(255))
    shared = sa.Column(sa.Boolean(), default=False, nullable=False)
    operator = sa.Column(sa.Enum('AND', 'OR', name='operator_types'), default='AND', nullable=False)

class CGToClassificationMapping(model_base.BASEV2):
    __tablename__ = 'classification_group_to_classification_mappings'
    container_cg_id = sa.Column(sa.String(36),
                                sa.ForeignKey('classification_groups.id'),
                                primary_key=True)
    stored_classification_id = sa.Column(sa.String(36),
                               sa.ForeignKey('classifications.id'),
                               primary_key=True)


class CGToClassificationGroupMapping(model_base.BASEV2):
    __tablename__ = 'classification_group_to_cg_mappings'
    container_cg_id = sa.Column(sa.String(36),
                                sa.ForeignKey('classification_groups.id'),
                                primary_key=True)
    stored_cg_id = sa.Column(sa.String(36),
                             sa.ForeignKey('classification_groups.id'),
                             primary_key=True)


class ClassificationBase(model_base.BASEV2, model_base.HasId,
                         model_base.HasProject):
    __tablename__ = 'classifications'
    c_type = sa.Column(sa.String(36))
    __mapper_args__ = {'polymorphic_on': c_type}
    name = sa.Column(sa.String(255))
    description = sa.Column(sa.String(255))
    shared = sa.Column(sa.Boolean(), nullable=True)
    negated = sa.Column(sa.Boolean(), nullable=True)

class IPV4Classification(model_base.BASEV2):
    __tablename__ = 'ipv4_classifications'
    __mapper_args__ = {'polymorphic_identity': 'ipv4'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifications.id'),
                   primary_key=True)
    dscp = sa.Column(sa.Integer())
    dscp_mask = sa.Column(sa.Integer())
    ecn = sa.Column(sa.Enum("0", "1", "2", "3", name="ecn_types"))
    length_min = sa.Column(sa.Integer())
    length_max = sa.Column(sa.Integer())
    flags = sa.Column(sa.Integer())
    flags_mask = sa.Column(sa.Integer())
    ttl_min = sa.Column(sa.SmallInteger())
    ttl_max = sa.Column(sa.SmallInteger())
    protocol = sa.Column(sa.Integer())
    src_addr = sa.Column(sa.String(19))
    dst_addr = sa.Column(sa.String(19))

#class IPV6Classification(ClassificationBase):
class IPV6Classification(model_base.BASEV2):
    __tablename__ = 'ipv6_classifications'
    __mapper_args__ = {'polymorphic_identity': 'ipv6'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifications.id'),
                   primary_key=True)
    dscp = sa.Column(sa.Integer())
    dscp_mask = sa.Column(sa.Integer())
    ecn = sa.Column(sa.Enum("0", "1", "2", "3", name="ecn_types"))
    length_min = sa.Column(sa.Integer())
    length_max = sa.Column(sa.Integer())
    next_header = sa.Column(sa.Integer())
    hops_min = sa.Column(sa.SmallInteger())
    hops_max = sa.Column(sa.SmallInteger())
    src_addr = sa.Column(sa.String(49))
    dst_addr = sa.Column(sa.String(49))


#class EthernetClassification(ClassificationBase):
class EthernetClassification(model_base.BASEV2):
    __tablename__ = 'ethernet_classifications'
    __mapper_args__ = {'polymorphic_identity': 'ethernet'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifications.id'),
                   primary_key=True)
    ethertype = sa.Column(sa.Integer())
    src_addr = sa.Column(sa.String(17))
    dst_addr = sa.Column(sa.String(17))


#class UDPClassification(ClassificationBase):
class UDPClassification(model_base.BASEV2):
    __tablename__ = 'udp_classifications'
    __mapper_args__ = {'polymorphic_identity': 'udp'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifications.id'),
                   primary_key=True)
    src_port_min = sa.Column(sa.Integer)
    src_port_max = sa.Column(sa.Integer)
    dst_port_min = sa.Column(sa.Integer)
    dst_port_max = sa.Column(sa.Integer)
    length_min = sa.Column(sa.Integer())
    length_max = sa.Column(sa.Integer())


#class TCPClassification(ClassificationBase):
class TCPClassification(model_base.BASEV2):
    __tablename__ = 'tcp_classifications'
    __mapper_args__ = {'polymorphic_identity': 'tcp'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifications.id'),
                   primary_key=True)
    src_port_min = sa.Column(sa.Integer)
    src_port_max = sa.Column(sa.Integer)
    dst_port_min = sa.Column(sa.Integer)
    dst_port_max = sa.Column(sa.Integer)
    flags = sa.Column(sa.Integer())
    flags_mask = sa.Column(sa.Integer())
    window_min = sa.Column(sa.Integer())
    window_max = sa.Column(sa.Integer())


def _read_classification_groups(svc_plu, context, id=None):
    class_group = svc_plu._get_collection(context, ClassificationGroup,
                                          _generate_dict_from_cg_db)
    cg_m_c = svc_plu._get_collection(context, CGToClassificationMapping,
                                     _generate_dict_from_cgmapping_db)
    cg_m_cg = svc_plu._get_collection(context, CGToClassificationGroupMapping,
                                      _generate_dict_from_cgmapping_db)

    id_class = None
    pdb.set_trace()
    for cg in class_group:
        class_ids = []
        group_ids = []
        if id and cg['id'] != id:
            continue
        for mapping in cg_m_c:
            if cg['id'] == mapping['container_cg_id']:
                class_ids.append(mapping['stored_classification_id'])
        for mapping in cg_m_cg:
            if cg['id'] == mapping['container_cg_id']:
                group_ids.append(mapping['stored_cg_id'])
        cg['classifications'] = ','.join(str(x) for x in class_ids)
        cg['classification_groups'] = ','.join(str(x) for x in group_ids)
        id_class = cg

    if id:
        return id_class
    else:
        return class_group


def _generate_dict_from_cg_db(model, fields=None):
    resp = {}

    resp['id'] = model.id
    resp['name'] = model.name
    resp['description'] = model.description
    resp['project_id'] = model.project_id
    resp['classifications'] = ''
    resp['classification_groups'] = ''
    resp['shared'] = model.shared
    resp['operator'] = model.operator

    return resp


def _generate_dict_from_cgmapping_db(model, fields=None):
    resp = {}

    resp['container_cg_id'] = model.container_cg_id
    if 'stored_cg_id' in model:
        resp['stored_cg_id'] = model.stored_cg_id
    else:
        resp['strored_classification_id'] = model.stored_classification_id

    return resp

RESOURCE_MODELS = {'ipv4_classification': IPV4Classification,
                   'ipv6_classification': IPV6Classification,
                   'tcp_classification': TCPClassification,
                   'udp_classification': UDPClassification,
                   'ethernet_classification': EthernetClassification}
