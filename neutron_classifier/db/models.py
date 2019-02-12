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

from neutron.db import classification

from neutron_lib.db import model_base
from neutron_lib.db import model_query as mq

import sqlalchemy as sa
from sqlalchemy import orm


class IPV4Classification(classification.ClassificationBase):
    __tablename__ = 'ipv4_classifications'
    __mapper_args__ = {'polymorphic_identity': 'ipv4'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifications.id',
                   ondelete='CASCADE'), primary_key=True)
    dscp = sa.Column(sa.Integer())
    dscp_mask = sa.Column(sa.Integer())
    ecn = sa.Column(sa.Enum("0", "1", "2", "3", name='ecn_types'))
    length_min = sa.Column(sa.Integer())
    length_max = sa.Column(sa.Integer())
    flags = sa.Column(sa.Integer())
    flags_mask = sa.Column(sa.Integer())
    ttl_min = sa.Column(sa.SmallInteger())
    ttl_max = sa.Column(sa.SmallInteger())
    protocol = sa.Column(sa.Integer())
    src_addr = sa.Column(sa.String(19))
    dst_addr = sa.Column(sa.String(19))


class IPV6Classification(classification.ClassificationBase):
    __tablename__ = 'ipv6_classifications'
    __mapper_args__ = {'polymorphic_identity': 'ipv6'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifications.id',
                   ondelete='CASCADE'), primary_key=True)
    dscp = sa.Column(sa.Integer())
    dscp_mask = sa.Column(sa.Integer())
    ecn = sa.Column(sa.Enum("0", "1", "2", "3", name='ecn_types'))
    length_min = sa.Column(sa.Integer())
    length_max = sa.Column(sa.Integer())
    next_header = sa.Column(sa.Integer())
    hops_min = sa.Column(sa.SmallInteger())
    hops_max = sa.Column(sa.SmallInteger())
    src_addr = sa.Column(sa.String(49))
    dst_addr = sa.Column(sa.String(49))


class EthernetClassification(classification.ClassificationBase):
    __tablename__ = 'ethernet_classifications'
    __mapper_args__ = {'polymorphic_identity': 'ethernet'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifications.id',
                   ondelete='CASCADE'), primary_key=True)
    ethertype = sa.Column(sa.Integer())
    src_addr = sa.Column(sa.String(17))
    dst_addr = sa.Column(sa.String(17))


class UDPClassification(classification.ClassificationBase):
    __tablename__ = 'udp_classifications'
    __mapper_args__ = {'polymorphic_identity': 'udp'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifications.id',
                   ondelete='CASCADE'), primary_key=True)
    src_port_min = sa.Column(sa.Integer)
    src_port_max = sa.Column(sa.Integer)
    dst_port_min = sa.Column(sa.Integer)
    dst_port_max = sa.Column(sa.Integer)
    length_min = sa.Column(sa.Integer())
    length_max = sa.Column(sa.Integer())


class TCPClassification(classification.ClassificationBase):
    __tablename__ = 'tcp_classifications'
    __mapper_args__ = {'polymorphic_identity': 'tcp'}
    id = sa.Column(sa.String(36), sa.ForeignKey('classifications.id',
                   ondelete='CASCADE'), primary_key=True)
    src_port_min = sa.Column(sa.Integer)
    src_port_max = sa.Column(sa.Integer)
    dst_port_min = sa.Column(sa.Integer)
    dst_port_max = sa.Column(sa.Integer)
    flags = sa.Column(sa.Integer())
    flags_mask = sa.Column(sa.Integer())
    window_min = sa.Column(sa.Integer())
    window_max = sa.Column(sa.Integer())


def _read_classification_group(context, id):
    """Returns a classification group."""

    cg = mq.get_by_id(context, classification.ClassificationGroup, id)
    return cg


def _read_classifications(context, id):
    """Returns all the classifications mapped/related to a

    classification group.
    """
    class_group = _read_classification_group(context, id)
    return class_group.classifications


def _read_classification_groups(context, id):
    """Returns all the classification groups mapped/related to a

    classification group.
    """
    class_group = _read_classification_group(context, id)
    return class_group.classification_groups


def _generate_dict_from_cg_db(model, fields=None):
    resp = {}

    resp['id'] = model.id
    resp['name'] = model.name
    resp['description'] = model.description
    resp['project_id'] = model.project_id
    resp['classifications'] = model.classifications
    resp['classification_groups'] = model.classification_groups
    resp['shared'] = model.shared
    resp['operator'] = model.operator

    return resp


def _read_all_classification_groups(plugin, context):
    """Returns all classification groups."""

    class_group = plugin._get_collection(context, classification.ClassificationGroup,
                                         _generate_dict_from_cg_db)
    return class_group


RESOURCE_MODELS = {'ethernet_classification': EthernetClassification,
                   'ipv4_classification': IPV4Classification,
                   'ipv6_classification': IPV6Classification,
                   'tcp_classification': TCPClassification,
                   'udp_classification': UDPClassification}
