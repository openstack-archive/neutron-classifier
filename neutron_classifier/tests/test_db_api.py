# Copyright (c) 2015 Mirantis, Inc.
# Copyright (c) 2015 Huawei Technologies India Pvt Ltd.
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
from neutron_classifier.db import api
from neutron_classifier.db import models
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from oslo_utils import uuidutils
from oslotest import base


FAKE_SG_RULE_V6 = {'direction': 'INGRESS', 'protocol': 'tcp', 'ethertype':
                   'IPv6', 'tenant_id': 'fake_tenant', 'port_range_min': 80,
                   'port_range_max': 80, 'remote_ip_prefix':
                   'fddf:cb3b:bc4::/48', }

FAKE_SG_RULE_V4 = {'direction': 'INGRESS', 'protocol': 'tcp', 'ethertype':
                   'IPv4', 'tenant_id': 'fake_tenant', 'port_range_min': 80,
                   'port_range_max': 80, 'remote_ip_prefix': '10.0.0.0/8', }

FAKE_SG_V6 = {'name': 'fake security group', 'tenant_id':
              uuidutils.generate_uuid(), 'description': 'this is fake',
              'security_group_rules': [FAKE_SG_RULE_V6]}

FAKE_FW_RULE_V4 = {'ip_version': 4, 'protocol': 'udp',
                   'source_port_range_min': 1, 'source_port_range_max': 80,
                   'destination_port_range_min': 1,
                   'destination_port_range_max': 80,
                   'source_ip_address': '20.1.1.1/24',
                   'destination_ip_address': '30.1.1.1/24',
                   'position': 1, 'action': 'ALLOW', 'enabled': True,
                   'tenant_id': 'fake_tenant', }

FAKE_FW_RULE_V6 = {'ip_version': 6, 'protocol': 'udp',
                   'source_port_range_min': 1, 'source_port_range_max': 80,
                   'destination_port_range_min': 1,
                   'destination_port_range_max': 80,
                   'source_ip_address': 'fddf:cb3b:bc4::/48',
                   'destination_ip_address': 'fddf:cb3b:b33f::/48',
                   'position': 1, 'action': 'ALLOW', 'enabled': True,
                   'tenant_id': 'fake_tenant', }

FAKE_FW_V4 = {'name': 'fake firewall policy',
              'tenant_id': uuidutils.generate_uuid(),
              'description': 'this is fake',
              'firewall_rules': [FAKE_FW_RULE_V4]}

FAKE_FW_V6 = {'name': 'fake firewall policy',
              'tenant_id': uuidutils.generate_uuid(),
              'description': 'this is fake',
              'firewall_rules': [FAKE_FW_RULE_V6]}


class ClassifierTestContext(object):
    "Classifier Database Context."
    engine = None
    session = None

    def __init__(self):
        self.engine = sa.create_engine('sqlite:///:memory:', echo=True)
        self.session = sessionmaker(bind=self.engine)()


class DbApiTestCase(base.BaseTestCase):

    def setUp(self):
        super(DbApiTestCase, self).setUp()
        self.context = ClassifierTestContext()
        models.Base.metadata.create_all(self.context.engine)

    def _create_classifier_group(self, service):
        cg = models.ClassifierGroup()
        cg.tenant_id = uuidutils.generate_uuid()
        cg.name = 'test classifier'
        cg.description = 'ensure all data inserted correctly'
        cg.service = service
        return cg

    def test_create_classifier_chain(self):
        cg = self._create_classifier_group('neutron-fwaas')
        ipc = models.IpClassifier()
        ipc.destination_ip_prefix = 'fd70:fbb6:449e::/48'
        ipc.source_ip_prefix = 'fddf:cb3b:bc4::/48'
        api.create_classifier_chain(cg, [ipc])
        self.assertGreater(len(cg.classifier_chain), 0)

    def _test_convert_security_group_rule_to_classifier(self,
                                                        security_group_rule):
        # TODO(sc68cal) make this not call session.commit directly
        cg = self._create_classifier_group('security-group')
        api.convert_security_group_rule_to_classifier(self.context,
                                                      security_group_rule, cg)
        # Save to the database
        self.context.session.add(cg)
        self.context.session.commit()

        # Refresh the classifier group from the DB
        cg = api.get_classifier_group(self.context, cg.id)
        self.assertGreater(len(cg.classifier_chain), 0)

    def test_convert_security_group_rule_v4_to_classifier(self):
        self._test_convert_security_group_rule_to_classifier(FAKE_SG_RULE_V4)

    def test_convert_security_group_rule_v6_to_classifier(self):
        self._test_convert_security_group_rule_to_classifier(FAKE_SG_RULE_V6)

    def test_convert_security_group_to_classifier_chain(self):
        result = api.convert_security_group_to_classifier(self.context,
                                                          FAKE_SG_V6)
        self.assertIsNotNone(result)

    def test_convert_classifier_chain_to_security_group(self):
        classifier_id = api.convert_security_group_to_classifier(
            self.context, FAKE_SG_V6).id
        result = api.convert_classifier_group_to_security_group(self.context,
                                                                classifier_id)
        result['tenant_id'] = FAKE_SG_RULE_V6['tenant_id']
        self.assertEqual(FAKE_SG_RULE_V6, result)

    # Firewall testcases
    def _test_convert_firewall_rule_to_classifier(self, fw_rule):
        cg = self._create_classifier_group('neutron-fwaas')
        api.convert_firewall_rule_to_classifier(self.context, fw_rule, cg)

        # Save to the database
        self.context.session.add(cg)
        self.context.session.commit()

        # Refresh the classifier group from the DB
        cg = api.get_classifier_group(self.context, cg.id)
        self.assertGreater(len(cg.classifier_chain), 0)

    def test_convert_firewall_rule_v4_to_classifier(self):
        self._test_convert_firewall_rule_to_classifier(FAKE_FW_RULE_V4)

    def test_convert_firewall_rule_v6_to_classifier(self):
        self._test_convert_firewall_rule_to_classifier(FAKE_FW_RULE_V6)

    def test_convert_firewall_policy_v4_to_classifier_chain(self):
        result = api.convert_firewall_policy_to_classifier(self.context,
                                                           FAKE_FW_V4)
        self.assertIsNotNone(result)

    def test_convert_firewall_policy_v6_to_classifier_chain(self):
        result = api.convert_firewall_policy_to_classifier(self.context,
                                                           FAKE_FW_V6)
        self.assertIsNotNone(result)

    def test_convert_classifier_chain_to_firewall(self):
        classifier_id = api.convert_firewall_policy_to_classifier(
            self.context, FAKE_FW_V6).id
        result = api.convert_classifier_to_firewall(self.context,
                                                    classifier_id)
        result['tenant_id'] = FAKE_FW_RULE_V6['tenant_id']
        result['position'] = FAKE_FW_RULE_V6['position']
        result['action'] = FAKE_FW_RULE_V6['action']
        result['enabled'] = FAKE_FW_RULE_V6['enabled']
        self.assertEqual(FAKE_FW_RULE_V6, result)
