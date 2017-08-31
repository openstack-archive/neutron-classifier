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

from neutron_classifier.objects import classifications
from neutron_classifier.tests import tools

from neutron.tests.unit.objects import test_base
from neutron.tests.unit import testlib_api


class _CCFObjectsTestCommon(object):

    def _create_test_cg(self, name):
        attrs = {'name': name,
                 'id': uuidutils.generate_uuid(),
                 'description': "Description of test group",
                 'project_id': uuidutils.generate_uuid(),
                 'operator': 'AND'}
        cg = classifications.ClassificationGroup(self.context, **attrs)
        cg.create()
        return cg


class ClassificationGroupTest(test_base.BaseDbObjectTestCase,
                              testlib_api.SqlTestCase,
                              _CCFObjectsTestCommon):
    # NOTE(ndahiwad): As the FIELD_TYPE_VALUE_GENERATOR_MAP in neutron's
    # test_base for objects doesn't have an entry for Enum fields, we are
    # adding it here for our use rather than adding in neutron.
    test_base.FIELD_TYPE_VALUE_GENERATOR_MAP[
        oslo_versionedobjects.fields.EnumField] = tools.get_random_operator
    _test_class = classifications.ClassificationGroup

    def test_get_object(self):
        cg = self._create_test_cg('Test Group 0')
        fetch_cg = classifications.ClassificationGroup.get_object(
            self.context, id=cg.id)
        self.assertEqual(cg, fetch_cg)

    def test_get_objects(self):
        cg1 = self._create_test_cg('Test Group 1')
        cg2 = self._create_test_cg('Test Group 2')
        cgs = classifications.ClassificationGroup.get_objects(self.context)
        self.assertIn(cg1, cgs)
        self.assertIn(cg2, cgs)
