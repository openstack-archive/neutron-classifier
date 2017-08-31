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
    rbac_db_cls = ClassificationGroupRBAC
    db_model = models.ClassificationGroup

    fields = {
        'id': common_types.UUIDField(),
        'name': obj_fields.StringField(),
        'description': obj_fields.StringField(),
        'project_id': obj_fields.StringField(),
        'shared': obj_fields.BooleanField(default=False),
        'operator': obj_fields.EnumField(['AND', 'OR'], default='AND'),
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
class CGToClassificationMapping(base.NeutronDbObject):
    VERSION = '1.0'

    rbac_db_model = ClassificationGroupRBAC
    db_model = models.CGToClassificationMapping

    fields = {
        'container_cg_id': obj_fields.ObjectField('ClassificationGroup',
                                                  subclasses=True),
        'store_classification_id': obj_fields.ObjectField('ClassificationBase',
                                                          subclasses=True),
    }


@obj_base.VersionedObjectRegistry.register
class CGToClassificationGroupMapping(base.NeutronDbObject):
    VERSION = '1.0'

    rbac_db_model = ClassificationGroupRBAC
    db_model = models.CGToClassificationGroupMapping

    fields = {
        'container_cg_id': obj_fields.ObjectField('ClassificationGroup',
                                                  subclasses=True),
        'stored_cg_id': obj_fields.ObjectField('ClassificationGroup',
                                               subclasses=True),
    }


@six.add_metaclass(abc.ABCMeta)
class ClassificationBase(base.NeutronDbObject):
    VERSION = '1.0'

    db_model = models.ClassificationBase

    fields = {
        'id': common_types.UUIDField(),
        'name': obj_fields.StringField(),
        'description': obj_fields.StringField(),
        'project_id': obj_fields.StringField(),
        'shared': obj_fields.BooleanField(default=False),
        'c_type': obj_fields.StringField(),
        'negated': obj_fields.BooleanField(default=False),
    }

    fields_no_update = ['id', 'c_type']

    @classmethod
    def get_objects(cls, context, _pager=None, validate_filters=True,
                    **kwargs):
        with db_api.autonested_transaction(context.session):
            objects = super(ClassificationBase,
                            cls).get_objects(context, _pager,
                                             validate_filters,
                                             **kwargs)
            return objects


@obj_base.VersionedObjectRegistry.register
class IPV4Classification(ClassificationBase):
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
            super(ClassificationBase, self).create()

    @classmethod
    def get_object(cls, context, **kwargs):
        with db_api.autonested_transaction(context.session):
            obj = super(IPV4Classification,
                        cls).get_object(context, c_type='ipv4',
                                        **kwargs)
            return obj


@obj_base.VersionedObjectRegistry.register
class IPV6Classification(ClassificationBase):
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
            super(ClassificationBase, self).create()

    @classmethod
    def get_object(cls, context, **kwargs):
        with db_api.autonested_transaction(context.session):
            obj = super(IPV6Classification,
                        cls).get_object(context, c_type='ipv6',
                                        **kwargs)
            return obj


@obj_base.VersionedObjectRegistry.register
class EthernetClassification(ClassificationBase):
    VERSION = '1.0'
    db_model = models.EthernetClassification

    fields = {
        'ethertype': obj_fields.IntegerField(nullable=True),
        'src_addr': obj_fields.StringField(nullable=True),
        'dst_addr': obj_fields.StringField(nullable=True),
    }

    def create(self):
        with db_api.autonested_transaction(self.obj_context.session):
            super(ClassificationBase, self).create()

    @classmethod
    def get_object(cls, context, **kwargs):
        with db_api.autonested_transaction(context.session):
            obj = super(EthernetClassification,
                        cls).get_object(context, c_type='ethernet',
                                        **kwargs)
            return obj


@obj_base.VersionedObjectRegistry.register
class UDPClassification(ClassificationBase):
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
            super(ClassificationBase, self).create()

    @classmethod
    def get_object(cls, context, **kwargs):
        with db_api.autonested_transaction(context.session):
            obj = super(UDPClassification,
                        cls).get_object(context, c_type='udp',
                                        **kwargs)
            return obj


@obj_base.VersionedObjectRegistry.register
class TCPClassification(ClassificationBase):
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
            super(ClassificationBase, self).create()

    @classmethod
    def get_object(cls, context, **kwargs):
        with db_api.autonested_transaction(context.session):
            obj = super(TCPClassification,
                        cls).get_object(context, c_type='tcp',
                                        **kwargs)
            return obj


CLASS_MAP = {'ipv4': IPV4Classification,
             'ethernet': EthernetClassification,
             'ipv6': IPV6Classification,
             'udp': UDPClassification,
             'tcp': TCPClassification}
