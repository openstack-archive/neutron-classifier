# Copyright (c) 2015 Mirantis, Inc.
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

from neutron_classifier.common import constants
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
    protocol = sa.Enum(*constants.PROTOCOLS)
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


class VlanClassifier(Classifier):
    __tablename__ = 'vlan_classifiers'
    __mapper_args__ = {'polymorphic_identity': 'vlanclassifier'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifiers.id'),
                   primary_key=True)
    vlan_priority = sa.Column(sa.Integer)
