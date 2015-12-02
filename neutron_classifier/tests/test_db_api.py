# Copyright (c) 2015 Mirantis, Inc.
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

CREATED = False

FAKE_SG_RULE = {'direction': 'INGRESS', 'protocol': 'tcp', 'ethertype': 6,
                'tenant_id': 'fake_tenant', 'port_range_min': 80,
                'port_range_max': 80, 'remote_ip_prefix': 'fddf:cb3b:bc4::/48',
                }

FAKE_SG = {'name': 'fake security group',
           'tenant_id': uuidutils.generate_uuid(),
           'description': 'this is fake',
           'security_group_rules': [FAKE_SG_RULE]}


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

        if not CREATED:
            models.Base.metadata.create_all(self.context.engine)
            global CREATED
            CREATED = True

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
        result = api.create_classifier_chain(self.context, cg, ipc)
        self.assertIsNotNone(result)

    def test_convert_security_group_rule_to_classifier(self):
        # TODO(sc68cal) make this not call session.commit directly
        cg = self._create_classifier_group('security-group')
        api.convert_security_group_rule_to_classifier(self.context,
                                                      FAKE_SG_RULE, cg)
        # Save to the database
        self.context.session.add(cg)
        self.context.session.commit()

        # Refresh the classifier group from the DB
        cg = api.get_classifier_group(self.context, cg.id)
        self.assertGreater(len(cg.classifier_chain), 0)

    def test_convert_firewall_rule_to_classifier(self):
        firewall_rule = {'protocol': 'foo',
                         'ip_version': 6,
                         'source_ip_address': 'fddf:cb3b:bc4::/48',
                         'destination_ip_address': 'fddf:cb3b:b33f::/48',
                         'source_port': 80,
                         'destination_port': 80,
                         'position': 1,
                         'action': 'ALLOW',
                         'enabled': True
                         }
        api.convert_firewall_rule_to_classifier(self.context, firewall_rule)

    def test_convert_firewall_policy_to_classifier_chain(self):
        pass

    def test_convert_security_group_to_classifier_chain(self):
        result = api.convert_security_group_to_classifier(self.context,
                                                          FAKE_SG)
        self.assertIsNotNone(result)

    def test_convert_classifier_chain_to_security_group(self):
        classifier_id = api.convert_security_group_to_classifier(
            self.context, FAKE_SG).id
        result = api.convert_classifier_group_to_security_group(self.context,
                                                                classifier_id)
        result['tenant_id'] = FAKE_SG_RULE['tenant_id']
        self.assertEqual(FAKE_SG_RULE, result)

    def test_convert_classifier_chain_to_firewall_policy(self):
        pass
