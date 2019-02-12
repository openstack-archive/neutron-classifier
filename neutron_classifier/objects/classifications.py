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

import abc
import six

from oslo_versionedobjects import base as obj_base
from oslo_versionedobjects import fields as obj_fields

from neutron.objects import base
from neutron.objects import classification
from neutron.objects import common_types
from neutron_lib.db import api as db_api

from neutron_classifier.db import models


@base.NeutronObjectRegistry.register
class IPV4Classification(classification.ClassificationBase):
    VERSION = '1.0'
    db_model = models.IPV4Classification

    fields = {
        'dscp': obj_fields.IntegerField(nullable=True),
        'dscp_mask': obj_fields.IntegerField(nullable=True),
        'ecn': obj_fields.EnumField(valid_values=["0", "1", "2", "3"],
                                    nullable=True),
        'length_min': obj_fields.IntegerField(nullable=True),
        'length_max': obj_fields.IntegerField(nullable=True),
        'flags': obj_fields.IntegerField(nullable=True),
        'flags_mask': obj_fields.IntegerField(nullable=True),
        'ttl_min': obj_fields.IntegerField(nullable=True),
        'ttl_max': obj_fields.IntegerField(nullable=True),
        'protocol': obj_fields.IntegerField(nullable=True),
        'src_addr': obj_fields.StringField(nullable=True),
        'dst_addr': obj_fields.StringField(nullable=True),
    }

    def create(self):
        with db_api.autonested_transaction(self.obj_context.session):
            super(classification.ClassificationBase, self).create()

    @classmethod
    def get_object(cls, context, **kwargs):
        with db_api.autonested_transaction(context.session):
            obj = super(IPV4Classification,
                        cls).get_object(context, c_type='ipv4',
                                        **kwargs)
            return obj


@base.NeutronObjectRegistry.register
class IPV6Classification(classification.ClassificationBase):
    VERSION = '1.0'
    db_model = models.IPV6Classification

    fields = {
        'dscp': obj_fields.IntegerField(nullable=True),
        'dscp_mask': obj_fields.IntegerField(nullable=True),
        'ecn': obj_fields.EnumField(valid_values=["0", "1", "2", "3"],
                                    nullable=True),
        'length_min': obj_fields.IntegerField(nullable=True),
        'length_max': obj_fields.IntegerField(nullable=True),
        'next_header': obj_fields.IntegerField(nullable=True),
        'hops_min': obj_fields.IntegerField(nullable=True),
        'hops_max': obj_fields.IntegerField(nullable=True),
        'src_addr': obj_fields.StringField(nullable=True),
        'dst_addr': obj_fields.StringField(nullable=True),
    }

    def create(self):
        with db_api.autonested_transaction(self.obj_context.session):
            super(classification.ClassificationBase, self).create()

    @classmethod
    def get_object(cls, context, **kwargs):
        with db_api.autonested_transaction(context.session):
            obj = super(IPV6Classification,
                        cls).get_object(context, c_type='ipv6',
                                        **kwargs)
            return obj


@base.NeutronObjectRegistry.register
class EthernetClassification(classification.ClassificationBase):
    VERSION = '1.0'
    db_model = models.EthernetClassification

    fields = {
        'ethertype': obj_fields.IntegerField(nullable=True),
        'src_addr': obj_fields.StringField(nullable=True),
        'dst_addr': obj_fields.StringField(nullable=True),
    }

    def create(self):
        with db_api.autonested_transaction(self.obj_context.session):
            super(classification.ClassificationBase, self).create()

    @classmethod
    def get_object(cls, context, **kwargs):
        with db_api.autonested_transaction(context.session):
            obj = super(EthernetClassification,
                        cls).get_object(context, c_type='ethernet',
                                        **kwargs)
            return obj


@base.NeutronObjectRegistry.register
class UDPClassification(classification.ClassificationBase):
    VERSION = '1.0'
    db_model = models.UDPClassification

    fields = {
        'src_port_min': obj_fields.IntegerField(nullable=True),
        'src_port_max': obj_fields.IntegerField(nullable=True),
        'dst_port_min': obj_fields.IntegerField(nullable=True),
        'dst_port_max': obj_fields.IntegerField(nullable=True),
        'length_min': obj_fields.IntegerField(nullable=True),
        'length_max': obj_fields.IntegerField(nullable=True),
    }

    def create(self):
        with db_api.autonested_transaction(self.obj_context.session):
            super(classification.ClassificationBase, self).create()

    @classmethod
    def get_object(cls, context, **kwargs):
        with db_api.autonested_transaction(context.session):
            obj = super(UDPClassification,
                        cls).get_object(context, c_type='udp',
                                        **kwargs)
            return obj


@base.NeutronObjectRegistry.register
class TCPClassification(classification.ClassificationBase):
    VERSION = '1.0'
    db_model = models.TCPClassification

    fields = {
        'src_port_min': obj_fields.IntegerField(nullable=True),
        'src_port_max': obj_fields.IntegerField(nullable=True),
        'dst_port_min': obj_fields.IntegerField(nullable=True),
        'dst_port_max': obj_fields.IntegerField(nullable=True),
        'flags': obj_fields.IntegerField(nullable=True),
        'flags_mask': obj_fields.IntegerField(nullable=True),
        'window_min': obj_fields.IntegerField(nullable=True),
        'window_max': obj_fields.IntegerField(nullable=True),
    }

    def create(self):
        with db_api.autonested_transaction(self.obj_context.session):
            super(classification.ClassificationBase, self).create()

    @classmethod
    def get_object(cls, context, **kwargs):
        with db_api.autonested_transaction(context.session):
            obj = super(TCPClassification,
                        cls).get_object(context, c_type='tcp',
                                        **kwargs)
            return obj


# NOTE(ndahiwade): These methods were added to get the list of mapped
# classifications and classification groups to a ClassificationGroup as
# currently we don't have synthetic fields supporting subclasses and
# self-referential relationships.
def _get_mapped_classifications(context, obj):
    """Returns a list of classifications mapped to a classification group.

    :param context:
    :param obj: ClassificationGroup object
    :return: list of Classification objects
    """
    mapped_db_classifications = models._read_classifications(context, obj.id)
    objs_cls = [CLASS_MAP[c.c_type] for c in mapped_db_classifications]
    mapped_obj_classifications = []
    for x in zip(objs_cls, mapped_db_classifications):
        mapped_obj_classifications.append(x[0]._load_object(context, x[1]))
    return mapped_obj_classifications


def _get_mapped_classification_groups(context, obj):
    """Returns a list of classification groups mapped to another group.

    :param context:
    :param obj: ClassificationGroup object
    :return: list of ClassificationGroup objects
    """
    mapped_cgs = [classification.ClassificationGroup._load_object(context, cg) for cg in
                  models._read_classification_groups(context, obj.id)]
    return mapped_cgs


CLASS_MAP = {'ethernet': EthernetClassification,
             'ipv4': IPV4Classification,
             'ipv6': IPV6Classification,
             'udp': UDPClassification,
             'tcp': TCPClassification}
