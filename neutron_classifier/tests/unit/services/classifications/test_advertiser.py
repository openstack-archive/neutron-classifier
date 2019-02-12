# Copyright 2019 Intel Corporation.
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

import unittest

import mock
from oslo_utils import uuidutils

from neutron_classifier.services.classification import advertiser


class TestAdvertiser(unittest.TestCase):

    def setUp(self):
        super(TestAdvertiser, self).setUp()
        self.mock_context = mock.Mock()
        self.mock_id = uuidutils.generate_uuid()
        mock.patch.object(advertiser, 'resources_rpc').start()
        self.advertiser = advertiser.ClassificationAdvertiser()

        mock.patch('neutron.objects.db.api.get_object').start()

    @mock.patch.object(advertiser, 'class_group')
    @mock.patch.object(advertiser, 'cs_base')
    def test_get_classification(self, mock_cs_base,
                                mock_cs_group):

        mock_obj = mock.Mock()
        mock_cls = mock.Mock()
        mock_cls.get_object.return_value = mock_obj
        mock_base = mock.Mock()
        mock_cs_base.ClassificationBase = mock.Mock(
            return_value=mock_base)
        mock_cs_group.CLASS_MAP.__getitem__ = mock.\
            Mock(return_value=mock_cls)

        return_obj = self.advertiser.\
            _get_classification('', self.mock_id,
                                context=self.mock_context)

        self.assertEqual(return_obj, mock_obj)

    @mock.patch.object(advertiser, 'cs_base')
    def test_get_classification_group(self, mock_cs_base):

        test_cg = mock.Mock()
        mock_cs_base.ClassificationGroup.get_object.\
            return_value = test_cg
        return_obj = self.advertiser.\
            _get_classification_group('', self.mock_id,
                                      context=self.mock_context)

        self.assertEqual(return_obj, test_cg)

    def tearDown(self):
        super(TestAdvertiser, self).tearDown()
        pass
