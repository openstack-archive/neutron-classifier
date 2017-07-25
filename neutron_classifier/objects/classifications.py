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

from neutron.db import api as db_api
from neutron.objects import base
from neutron.objects import common_types
from neutron.objects import rbac_db

from neutron_classifier.db import models
from neutron_classifier.db.rbac_db_models import ClassificationGroupRBAC


@obj_base.VersionedObjectRegistry.register
class ClassificationGroup(rbac_db.NeutronRbacObject):
    # Version 1.0: Initial version
    VERSION = '1.0'

    # required by RbacNeutronMetaclass
    rbac_db_model = ClassificationGroupRBAC
    db_model = models.ClassificationGroup

    fields = {
        'id': common_types.UUIDField(),
        'name': obj_fields.StringField(),
        'description': obj_fields.StringField(),
        'project_id': obj_fields.StringField(),
        'shared': obj_fields.BooleanField(default=False),
        'operator': obj_fields.StringField(default='and'),
        'cg_id': obj_fields.ObjectField('ClassificationGroup',
                                        subclasses=True),
    }

    fields_no_update = ['id', 'project_id']

    @classmethod
    def get_object(cls, context, **kwargs):
        # We want to get the policy regardless of its tenant id. We'll make
        # sure the tenant has permission to access the policy later on.
        admin_context = context.elevated()
        with db_api.autonested_transaction(admin_context.session):
            obj = super(ClassificationGroup, cls).get_object(admin_context,
                                                             **kwargs)
            if not obj or not cls.is_accessible(context, obj):
                return

            return obj


@obj_base.VersionedObjectRegistry.register
class ClassificationGroupMapping(base.NeutronDbObject):
    VERSION = '1.0'

    rbac_db_model = ClassificationGroupRBAC
    db_model = models.ClassificationGroupMapping

    fields = {
        'id': common_types.UUIDField(),
        'cg_id': obj_fields.StringField(),
        'classification_id': obj_fields.StringField(),
    }


@six.add_metaclass(abc.ABCMeta)
class ClassificationBase(base.NeutronDbObject):
    VERSION = '1.0'

    db_model = models.ClassificationBase

    fields = {
        'id': common_types.UUIDField(),
        'c_type': obj_fields.StringField(),
        'name': obj_fields.StringField(),
        'description': obj_fields.StringField(),
        'negated': obj_fields.BooleanField(default=False),
        'shared': obj_fields.BooleanField(default=False),
        'project_id': obj_fields.StringField(),
    }

    fields_no_update = ['id', 'c_type']


@obj_base.VersionedObjectRegistry.register
class IPV4Classification(ClassificationBase):
    VERSION = '1.0'
    db_model = models.IPV4Classification

    fields = {
        'ihl': obj_fields.IntegerField(nullable=True),
        'diffserv': obj_fields.IntegerField(nullable=True),
        'diffserv_mask': obj_fields.IntegerField(nullable=True),
        'length': obj_fields.IntegerField(nullable=True),
        'flags': obj_fields.IntegerField(nullable=True),
        'flags_mask': obj_fields.IntegerField(nullable=True),
        'ttl': obj_fields.IntegerField(nullable=True),
        'protocol': obj_fields.IntegerField(nullable=True),
        'src_addr': obj_fields.StringField(nullable=True),
        'dst_addr': obj_fields.StringField(nullable=True),
        'options': obj_fields.IntegerField(nullable=True),
        'options_mask': obj_fields.IntegerField(nullable=True),
    }


@obj_base.VersionedObjectRegistry.register
class IPV6Classification(ClassificationBase):
    VERSION = '1.0'
    db_model = models.IPV6Classification

    fields = {
        'traffic_class': obj_fields.IntegerField(),
        'traffic_class_mask': obj_fields.IntegerField(),
        'length': obj_fields.IntegerField(),
        'next_header': obj_fields.IntegerField(),
        'hops': obj_fields.IntegerField(),
        'src_addr': obj_fields.StringField(),
        'dst_addr': obj_fields.StringField(),
    }


@obj_base.VersionedObjectRegistry.register
class EthernetClassification(ClassificationBase):
    VERSION = '1.0'
    db_model = models.EthernetClassification

    fields = {
        'preamble': obj_fields.IntegerField(),
        'ethertype': obj_fields.StringField(),
        'src_addr': obj_fields.StringField(),
        'dst_addr': obj_fields.StringField(),
    }


@obj_base.VersionedObjectRegistry.register
class UDPClassification(ClassificationBase):
    VERSION = '1.0'
    db_model = models.UDPClassification

    fields = {
        'src_port': obj_fields.StringField(),
        'dst_port': obj_fields.StringField(),
        'length': obj_fields.IntegerField(),
        'window_size': obj_fields.IntegerField(),
    }


@obj_base.VersionedObjectRegistry.register
class TCPClassification(ClassificationBase):
    VERSION = '1.0'
    db_model = models.TCPClassification

    fields = {
        'src_port': obj_fields.StringField(),
        'dst_port': obj_fields.StringField(),
        'flags': obj_fields.IntegerField(),
        'flags_mask': obj_fields.IntegerField(),
        'window': obj_fields.IntegerField(),
        'data_offset': obj_fields.IntegerField(),
        'option_kind': obj_fields.IntegerField(),
    }


CLASS_MAP = {'ipv4classification': IPV4Classification,
             'ethernetclassification': EthernetClassification,
             'ipv6classification': IPV6Classification,
             'udpclassification': UDPClassification,
             'tcpclassification': TCPClassification}
