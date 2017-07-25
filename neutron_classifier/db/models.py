# Copyright (c) 2015 Mirantis, Inc.
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

from neutron_classifier.common import constants
from neutron_lib.db import model_base

from oslo_utils import uuidutils
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy import orm

Base = declarative_base()


# Stolen from neutron/db/model_base.py
class HasTenant(object):
    """Tenant mixin, add to subclasses that have a tenant."""

    tenant_id = sa.Column(sa.String(255), index=True)


# Stolen from neutron/db/model_base.py
class HasId(object):
    """id mixin, add to subclasses that have an id."""
    id = sa.Column(sa.String(36),
                   primary_key=True,
                   default=uuidutils.generate_uuid)


class Classifier(Base, HasId):
    __tablename__ = 'classifiers'
    classifier_type = sa.Column(sa.String)
    __mapper_args__ = {'polymorphic_on': classifier_type}


class ClassifierGroup(Base, HasTenant, HasId):
    __tablename__ = 'classifier_groups'
    name = sa.Column(sa.String(255))
    description = sa.Column(sa.String(255))
    classifier_chain = orm.relationship(
        'ClassifierChainEntry',
        backref=orm.backref('classifier_chains', cascade='all, delete'),
        order_by='ClassifierChainEntry.sequence',
        collection_class=ordering_list('sequence', count_from=1))
    service = sa.Column(sa.Enum(*constants.NEUTRON_SERVICES), index=True)


class ClassifierChainEntry(Base, HasId):
    __tablename__ = 'classifier_chains'
    classifier_group_id = sa.Column(sa.String(36),
                                    sa.ForeignKey('classifier_groups.id',
                                                  ondelete="CASCADE"))
    classifier_id = sa.Column(sa.String(36),
                              sa.ForeignKey('classifiers.id',
                                            ondelete="CASCADE"))
    classifier = orm.relationship(Classifier)
    sequence = sa.Column(sa.Integer)
    classifier_group = orm.relationship(ClassifierGroup)

    def __init__(self, classifier_group=None, classifier=None, sequence=None):
        super(ClassifierChainEntry, self).__init__()
        self.classifier = classifier
        self.classifier_group = classifier_group
        self.sequence = sequence


class DirectionClassifier(Classifier):
    __tablename__ = 'direction_classifiers'
    __mapper_args__ = {'polymorphic_identity': 'directionclassifier'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifiers.id'),
                   primary_key=True)
    direction = sa.Column(sa.Enum(*constants.DIRECTIONS))

    def __init__(self, direction=None):
        super(DirectionClassifier, self).__init__()
        self.direction = direction


class EncapsulationClassifier(Classifier):
    __tablename__ = 'encapsulation_classifiers'
    __mapper_args__ = {'polymorphic_identity': 'encapsulationclassifier'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifiers.id'),
                   primary_key=True)
    encapsulation_type = sa.Column(sa.Enum(*constants.ENCAPSULATION_TYPES))
    encapsulation_id = sa.Column(sa.String(255))


class EthernetClassifier(Classifier):
    __tablename__ = 'ethernet_classifiers'
    __mapper_args__ = {'polymorphic_identity': 'ethernetclassifier'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifiers.id'),
                   primary_key=True)
    ethertype = sa.Column(sa.Integer)
    source_mac = sa.Column(sa.String(255))
    destination_mac = sa.Column(sa.String(255))


class IpClassifier(Classifier):
    __tablename__ = 'ip_classifiers'
    __mapper_args__ = {'polymorphic_identity': 'ipclassifier'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifiers.id'),
                   primary_key=True)
    source_ip_prefix = sa.Column(sa.String(255))
    destination_ip_prefix = sa.Column(sa.String(255))


class Ipv4Classifier(Classifier):
    __tablename__ = 'ipv4_classifiers'
    __mapper_args__ = {'polymorphic_identity': 'ipv4classifier'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifiers.id'),
                   primary_key=True)
    dscp_tag = sa.Column(sa.String(255))
    protocol = sa.column(sa.Enum(*constants.PROTOCOLS))
    dscp_mask = sa.Column(sa.String(255))


class Ipv6Classifier(Classifier):
    __tablename__ = 'ipv6_classifiers'
    __mapper_args__ = {'polymorphic_identity': 'ipv6classifier'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifiers.id'),
                   primary_key=True)
    next_header = sa.Column(sa.Enum(*constants.PROTOCOLS))
    traffic_class = sa.Column(sa.String(255))
    flow_label = sa.Column(sa.String(255))


class NeutronPortClassifier(Classifier):
    __tablename__ = 'neutron_port_classifiers'
    __mapper_args__ = {'polymorphic_identity': 'neutronportclassifier'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifiers.id'),
                   primary_key=True)
    logical_source_port = sa.Column(sa.String(255))
    logical_destination_port = sa.Column(sa.String(255))


class TransportClassifier(Classifier):
    __tablename__ = 'transport_classifiers'
    __mapper_args__ = {'polymorphic_identity': 'transportclassifier'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifiers.id'),
                   primary_key=True)
    source_port_range_max = sa.Column(sa.Integer)
    source_port_range_min = sa.Column(sa.Integer)
    destination_port_range_max = sa.Column(sa.Integer)
    destination_port_range_min = sa.Column(sa.Integer)

    def __init__(self, source_port_range_min=None,
                 source_port_range_max=None,
                 destination_port_range_min=None,
                 destination_port_range_max=None):
        super(TransportClassifier, self).__init__()
        self.destination_port_range_min = destination_port_range_min
        self.destination_port_range_max = destination_port_range_max
        self.source_port_range_min = source_port_range_min
        self.source_port_range_max = source_port_range_max


class VlanClassifier(Classifier):
    __tablename__ = 'vlan_classifiers'
    __mapper_args__ = {'polymorphic_identity': 'vlanclassifier'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifiers.id'),
                   primary_key=True)
vlan_priority = sa.Column(sa.Integer)


# Service plugin models
class ClassificationGroup(model_base.BASEV2, model_base.HasId,
                          model_base.HasProject):
    __tablename__ = 'classification_groups'
    name = sa.Column(sa.String(36))
    description = sa.Column(sa.String(255))
    cg_id = sa.Column(sa.String(36))
    shared = sa.Column(sa.Boolean())
    operator = sa.Column(sa.String(4))


class ClassificationGroupMapping(model_base.BASEV2, model_base.HasId,
                                 model_base.HasProject):
    __tablename__ = 'classification_groups_mapping'
    cg_id = sa.Column(sa.String(36), sa.ForeignKey('classification_groups.id'))
    classification_id = sa.Column(sa.String(36))


class ClassificationBase(Base, HasId, model_base.HasProject,
                         model_base.BASEV2):
    __tablename__ = 'classifications'
    c_type = sa.Column(sa.String(36))
    __mapper_args__ = {'polymorphic_on': c_type}
    name = sa.Column(sa.String(36))
    description = sa.Column(sa.String(255))
    shared = sa.Column(sa.Boolean())
    negated = sa.Column(sa.Boolean())


class IPV4Classification(ClassificationBase):
    __tablename__ = 'ipv4_classifications'
    __mapper_args__ = {'polymorphic_identity': 'ipv4'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifications.id'),
                   primary_key=True)
    ihl = sa.Column(sa.Integer())
    diffserv = sa.Column(sa.Integer())
    diffserv_mask = sa.Column(sa.Integer())
    length = sa.Column(sa.Integer())
    flags = sa.Column(sa.Integer())
    flags_mask = sa.Column(sa.Integer())
    ttl = sa.Column(sa.Integer())
    protocol = sa.Column(sa.Integer())
    src_addr = sa.Column(sa.String(36))
    dst_addr = sa.Column(sa.String(36))
    options = sa.Column(sa.Integer())
    options_mask = sa.Column(sa.Integer())


class IPV6Classification(ClassificationBase):
    __tablename__ = 'ipv6_classifications'
    __mapper_args__ = {'polymorphic_identity': 'ipv6'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifications.id'),
                   primary_key=True)
    traffic_class = sa.Column(sa.Integer())
    traffic_class_mask = sa.Column(sa.Integer())
    length = sa.Column(sa.Integer())
    next_header = sa.Column(sa.Integer())
    hops = sa.Column(sa.Integer())
    src_addr = sa.Column(sa.String(36))
    dst_addr = sa.Column(sa.String(36))


class EthernetClassification(ClassificationBase):
    __tablename__ = 'ethernet_classifications'
    __mapper_args__ = {'polymorphic_identity': 'ethernet'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifications.id'),
                   primary_key=True)
    preamble = sa.Column(sa.Integer())
    ethertype = sa.Column(sa.Integer())
    src_addr = sa.Column(sa.String(36))
    dst_addr = sa.Column(sa.String(36))


class UDPClassification(ClassificationBase):
    __tablename__ = 'udp_classifications'
    __mapper_args__ = {'polymorphic_identity': 'udp'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifications.id'),
                   primary_key=True)
    src_port = sa.Column(sa.String(36))
    dst_port = sa.Column(sa.String(36))
    length = sa.Column(sa.Integer())
    window_size = sa.Column(sa.Integer())


class TCPClassification(ClassificationBase):
    __tablename__ = 'tcp_classifications'
    __mapper_args__ = {'polymorphic_identity': 'tcp'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifications.id'),
                   primary_key=True)
    src_port = sa.Column(sa.String(36))
    dst_port = sa.Column(sa.String(36))
    flags = sa.Column(sa.Integer())
    flags_mask = sa.Column(sa.Integer())
    window = sa.Column(sa.Integer())
    data_offset = sa.Column(sa.Integer())
    option_kind = sa.Column(sa.Integer())


def _read_classification_groups(svc_plu, context, model,
                                mapping_model, id=None):
    cg = svc_plu._get_collection(context, model, _generate_dict_from_cg_db)
    cgm = svc_plu._get_collection(context, mapping_model,
                                  _generate_dict_from_cgmapping_db)
    ids = []
    for c in cg:
        if c['id'] == id:
            cg = c
        for m in cgm:
            if c['id'] == m['cg_id']:
                ids.append(m['classification_id'])
                c['classification'] = ','.join(str(x) for x in ids)
        del ids[:]

    return cg


def _generate_dict_from_cg_db(model, fields=None):
    resp = {}

    resp['id'] = model.id
    resp['name'] = model.name
    resp['description'] = model.description
    resp['project_id'] = model.project_id
    resp['classification'] = ''
    resp['classification_group'] = model.cg_id
    resp['shared'] = model.shared
    resp['operator'] = model.operator

    return resp


def _generate_dict_from_cgmapping_db(model, fields=None):
    resp = {}

    resp['id'] = model.id
    resp['cg_id'] = model.cg_id
    resp['classification_id'] = model.classification_id

    return resp

RESOURCE_MODELS = {'ipv4_classification': IPV4Classification,
                   'ipv6_classification': IPV6Classification,
                   'tcp_classification': TCPClassification,
                   'udp_classification': UDPClassification,
                   'ethernet_classification': EthernetClassification}
