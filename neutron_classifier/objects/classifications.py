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

import itertools
import six
import abc

from oslo_utils import versionutils
from oslo_versionedobjects import base as obj_base
from oslo_versionedobjects import exception
from oslo_versionedobjects import fields as obj_fields

from neutron._i18n import _
from neutron.common import exceptions
from neutron.db import api as db_api
from neutron.db import models_v2
from neutron.objects import base
from neutron.objects import common_types
from neutron.objects.db import api as obj_db_api
from neutron.objects import rbac_db

from neutron_classifier.db.rbac_db_models import ClassificationGroupRBAC
from neutron_classifier.db import models_v2


@obj_base.VersionedObjectRegistry.register
class ClassificationGroup(rbac_db.NeutronRbacObject):
    # Version 1.0: Initial version
    VERSION = '1.0'

    # required by RbacNeutronMetaclass
    rbac_db_model = ClassificationGroupRBAC
    db_model = models_v2.ClassificationGroup

    fields = {
        'id': common_types.UUIDField(),
        'project_id': obj_fields.StringField(),
        'name': obj_fields.StringField(),
        'shared': obj_fields.BooleanField(default=False),
        'classification': obj_fields.ListOfObjectsField('ClassificationBase', subclasses=True),
    }

    fields_no_update = ['id', 'project_id']

    synthetic_fields = ['classifications']

    @classmethod
    def get_object(cls, context, **kwargs):
        # We want to get the policy regardless of its tenant id. We'll make
        # sure the tenant has permission to access the policy later on.
        admin_context = context.elevated()
        with db_api.autonested_transaction(admin_context.session):
            obj = super(ClassificationGroup, cls).get_object(admin_context,
                                                          **kwargs)
            if (not obj or
                not cls.is_accessible(context, obj)):
                return

            return obj


@six.add_metaclass(abc.ABCMeta)
class ClassificationBase(base.NeutronDbObject):
    VERSION = '1.0'

    db_model = models_v2.ClassificationBase

    fields = {
        'id': common_types.UUIDField(),
        'classification_type': obj_fields.StringField()
    }

    fields_no_update = ['id', 'classification_type']


@obj_base.VersionedObjectRegistry.register
class IPV4Classification(ClassificationBase):
    VERSION = '1.0'
    db_model = models_v2.IPV4Classification

    fields = {
        'dscp': obj_fields.StringField(),
        'dscp_mask': obj_fields.StringField(),
        'ecn': obj_fields.StringField(),
        'ecn_mask': obj_fields.StringField(),
        'protocol': obj_fields.StringField(),
        'protocol_mask': obj_fields.StringField(),
        'source_address': obj_fields.StringField(),
        'source_address_range': obj_fields.StringField(),
        'destination_address': obj_fields.StringField(),
        'destination_address_range': obj_fields.StringField(),
    }


CLASS_MAP = {'ipv4classification': IPV4Classification}
