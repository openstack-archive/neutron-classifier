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

from neutron_classifier import objects
from neutron_classifier.tests import base as test_base


# NOTE: The hashes in this list should only be changed if they come with a
# corresponding version bump in the affected objects. Please keep the list in
# alphabetic order.
# This list also includes VersionedObjects from Neutron that are registered
# through dependencies.
object_data = {
    'ClassificationGroup': '1.0-e621ff663f76bb494072872222f5fe72',
    'CGToClassificationGroupMapping': '1.0-8ebed0ef1035bcc4b307da1bbdc6be64',
    'CGToClassificationMapping': '1.0-fe5942adbe82301a38b67bdce484efb1',
    'EthernetClassification': '1.0-267f03162a6e011197b663ee34e6cb0b',
    'IPV4Classification': '1.0-d4f25a09ceaad9ec817dcebb3b5c4e78',
    'IPV6Classification': '1.0-1051e98146a016522d516fe1bec49079',
    'TCPClassification': '1.0-1c8a4bb3b2dcdebe8913adc00788c704',
    'UDPClassification': '1.0-e55c7b58b9e2c7587cf9a0113225586b'}


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

        expected, actual = checker.test_hashes(object_data)
        self.assertEqual(expected, actual,
                         'Some objects have changed; please make sure the '
                         'versions have been bumped, and then update their '
                         'hashes in the object_data map in this test module.')
