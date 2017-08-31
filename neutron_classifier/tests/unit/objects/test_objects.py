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

# NOTE(davidsha) This file is largely a copy of the test_object.py file
# from Neutron

import os
import pprint

from oslo_versionedobjects import base as obj_base
from oslo_versionedobjects import fixture

from neutron import objects as n_obj
from neutron.tests.unit.objects import test_objects as n_obj_test

from neutron_classifier import objects
from neutron_classifier.tests.unit import base as test_base


# NOTE: The hashes in this list should only be changed if they come with a
# corresponding version bump in the affected objects. Please keep the list in
# alphabetic order.
# This list also includes VersiondObjects from Neutron that are registered
# through dependencies.
object_data = {
    'ClassificationGroup': '1.0-480c100378a323722fc948d09141962d',
    'ClassificationGroupMapping': '1.0-03c5cdd49015b05436b3ab91056884fe',
    'ClassificationType': '1.0-699af4d3a1ec14a7d24fefb19c44c641',
    'EthernetClassification': '1.0-c6d5d41c306a2783679651f67333a243',
    'IPV4Classification': '1.0-28c50679c819cf3b8780cf21e4f2f179',
    'IPV6Classification': '1.0-f4c53345b567749786222a11d634f022',
    'TCPClassification': '1.0-eb9834e3f59e146a46be7afac7d59903',
    'UDPClassification': '1.0-5f13ed85451d02ec8c8276f65c63254a'}


class TestObjectVersions(test_base.BaseClassificationTestCase):

    def setUp(self):
        super(TestObjectVersions, self).setUp()
        # NOTE(davidsha): Neutron Classifier OvO's need to be seeded,
        # There also appears to be some versioned objects leaking in from
        # Neutron from dependencies.
        # Because of this I've included all Neutron OvO's and added them
        # to the local object_data variable.
        # This dependency will prevent upgrades to a neutron OvO from breaking
        # this test if they were stored statically here.
        objects.register_objects()
        n_obj.register_objects()

    def test_versions(self):
        checker = fixture.ObjectVersionChecker(
            obj_base.VersionedObjectRegistry.obj_classes())
        fingerprints = checker.get_hashes()

        if os.getenv('GENERATE_HASHES'):
            with open('object_hashes.txt', 'w') as hashes_file:
                hashes_file.write(pprint.pformat(fingerprints))

        object_data.update(n_obj_test.object_data)

        expected, actual = checker.test_hashes(object_data)
        self.assertEqual(expected, actual,
                         'Some objects have changed; please make sure the '
                         'versions have been bumped, and then update their '
                         'hashes in the object_data map in this test module.')
