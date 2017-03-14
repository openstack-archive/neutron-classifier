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
from neutron_lib.db import model_base

from neutron.db import standard_attr
from neutron_classifier.common import constants
from neutron_classifier.db import models
from neutron_classifier.db import rbac_db_models
from oslo_utils import uuidutils
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy import orm

Base = declarative_base()


class ClassificationGroup(standard_attr.HasStandardAttributes, model_base.BASEV2,
                model_base.HasId, model_base.HasProject):
    __tablename__ = 'classification_groups'
    name = sa.Column(sa.String())
    rbac_entries = sa.orm.relationship(rbac_db_models.ClassificationGroupRBAC,
                                       backref='classification_group',
                                       lazy='subquery')
    api_collections = ['classification_groups']

class ClassificationBase(Base, models.HasId, model_base.BASEV2):
    __tablename__= 'classifications'
    classification_type = sa.Column(sa.String)
    __mapper_args__ = {'polymorphic_on': classification_type}
    name = sa.Column(sa.String(255))
    description = sa.Column(sa.String(255))


class PortClassification(ClassificationBase):
    __tablename__ = 'port_classifications'
    __mapper_args__ = {'polymorphic_identity': 'portclassification'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifications.id'),
                   primary_key=True)
    source_port = sa.Column(sa.String(255))
    source_port_min_range = sa.Column(sa.String(255))
    source_port_max_range = sa.Column(sa.String(255))
    destination_port = sa.Column(sa.String(255))
    destination_port_min_range = sa.Column(sa.String(255))
    destination_port_max_range = sa.Column(sa.String(255))


class NeutronClassification(ClassificationBase):
    __tablename__ = 'neutorn_classifications'
    __mapper_args__ = {'polymorphic_identity': 'neutronclassification'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifications.id'),
                   primary_key=True)
    source_port = sa.Column(sa.String(255))
    destination_port = sa.Column(sa.String(255))
    source_subnet = sa.Column(sa.String(255))
    destination_subnet = sa.Column(sa.String(255))
    source_network = sa.Column(sa.String(255))
    destination_network = sa.Column(sa.String(255))


class IPV4Classification(ClassificationBase):
    __tablename__ = 'ipv4_classifications'
    __mapper_args__ = {'polymorphic_identity': 'ipv4classification'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifications.id'),
                   primary_key=True)
    source_address = sa.Column(sa.String(255))
    source_address_range = sa.Column(sa.String(255))
    destination_address = sa.Column(sa.String(255))
    destination_address_range = sa.Column(sa.String(255))
    dscp = sa.Column(sa.String(255))
    dscp_mask = sa.Column(sa.String(255))
    ecn = sa.Column(sa.String(255))
    ecn_mask = sa.Column(sa.String(255))
    protocol = sa.Column(sa.String(255))
    protocol_mask = sa.Column(sa.String(255))


class IPV6Classification(ClassificationBase):
    __tablename__ = 'ipv6_classifications'
    __mapper_args__ = {'polymorphic_identity': 'ipv6classification'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifications.id'),
                   primary_key=True)
    source_address = sa.Column(sa.String(255))
    source_address_range = sa.Column(sa.String(255))
    destination_address = sa.Column(sa.String(255))
    destination_address_range = sa.Column(sa.String(255))
    traffic_class = sa.Column(sa.String(255))
    taffic_class_mask = sa.Column(sa.String(255))
    next_header = sa.Column(sa.String(255))
    next_header_mask = sa.Column(sa.String(255))
    flow_label = sa.Column(sa.String(255))
    flow_label_mask = sa.Column(sa.String(255))

#NOTE(davidsha) Ethernet metadata
class EthernetClassification(ClassificationBase):
    __tablename__ = 'ethernet_classifications'
    __mapper_args__ = {'polymorphic_identity': 'ethernetclassification'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifications.id'),
                   primary_key=True)
    source_mac = sa.Column(sa.String(255))
    source_mac_range = sa.Column(sa.String(255))
    destination_mac = sa.Column(sa.String(255))
    destination_mac_range = sa.Column(sa.String(255))
    type = sa.Column(sa.String(255))
    type_mask = sa.Column(sa.String(255))


def read_classification_base(model, fields=None):
    resp = {}

    resp['id'] = model.id
    resp['name'] = model.name

    resp['description'] = model.description
    resp['classification_type'] = model.classification_type

    return resp

def _generate_dict_from_ipv4_db(model, fields=None):
    resp = {}

    resp['id'] = model.id
    resp['name'] = model.name

    resp['description'] = model.description
    resp['project_id'] = model.project_id
    resp['dscp'] = model.dscp if None is model.dscp_mask else \
                   model.dscp + '/' + model.dscp_mask
    resp['ecn'] = model.ecn if None is model.ecn_mask else \
                   model.ecn + '/' + model.ecn_mask
    resp['protocol'] = model.protocol if None is model.protocol_mask \
                   else model.dscp + '/' + model.dscp_mask
    resp['source_address'] = model.source_address if None is \
                   model.source_address_range else \
                   model.source_address + '/' + model.source_address_range
    resp['destination_address'] = model.destination_address if None is \
                   model.destination_address_range else \
                   model.destination_address + '/' + \
                   model.destination_address_range
    return resp


RESOURCE_MODELS = {
                   'ipv4_classification': IPV4Classification,
                   'ipv6_classification': IPV6Classification,
                   'tcp_classification': PortClassification,
                   'udp_classification': PortClassification,
                   'ethernet_classification': EthernetClassification,
                   'neutron_classification': NeutronClassification}

DICT_RESP = {
             'ipv4_classification': _generate_dict_from_ipv4_db,
             'ipv6_classification': None,
             'tcp_classification': None,
             'udp_classification': None,
             'ethernet_classification': None,
             'neutron_classification': None}
