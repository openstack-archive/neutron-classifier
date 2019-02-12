# Copyright 2018 Intel Corporation.
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

from oslo_utils import uuidutils
import oslo_versionedobjects

from neutron_lib import context

from neutron.objects import classification as cs_base
from neutron.tests.unit.objects import test_base

from neutron_classifier.objects import classifications
from neutron_classifier.tests import tools


class _CCFObjectsTestCommon(object):

    # TODO(ndahiwade): this represents classifications containing Enum fields,
    # will need to be reworked if more classifications are added here later.
    _Enum_classifications = [classifications.IPV4Classification,
                             classifications.IPV6Classification]
    _Enumfield = oslo_versionedobjects.fields.EnumField
    ctx = context.get_admin_context()

    def get_random_attrs(self, obj=None):
        obj = obj
        attrs = {}
        for field, field_obj in obj.fields.items():
            if field != 'c_type' and type(field_obj) != self._Enumfield:
                random_generator = test_base.FIELD_TYPE_VALUE_GENERATOR_MAP[
                    type(field_obj)]
                attrs[field] = random_generator()
        return attrs

    def _create_test_cg(self, name):
        attrs = {'name': name,
                 'id': uuidutils.generate_uuid(),
                 'description': "Description of test group",
                 'project_id': uuidutils.generate_uuid(),
                 'shared': False,
                 'operator': 'AND'}
        cg = cs_base.ClassificationGroup(self.ctx, **attrs)
        cg.create()
        return cg

    def _create_test_classification(self, c_type, classification):
        attrs = self.get_random_attrs(classification)
        if classification in self._Enum_classifications:
            attrs['ecn'] = tools.get_random_ecn()
        attrs['c_type'] = c_type
        c = classification(self.ctx, **attrs)
        c.create()
        return c

    def _create_test_cg_cg_mapping(self, cg1, cg2):
        attrs = {'container_cg_id': cg1,
                 'stored_cg_id': cg2}
        cg_m_cg = cs_base.CGToClassificationGroupMapping(self.ctx,
                                                         **attrs)
        cg_m_cg.create()
        return cg_m_cg

    def _create_test_cg_c_mapping(self, cg, c):
        attrs = {'container_cg_id': cg,
                 'stored_classification_id': c}
        cg_m_c = cs_base.CGToClassificationMapping(self.ctx,
                                                   **attrs)
        cg_m_c.create()
        return cg_m_c
