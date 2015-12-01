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

    def test_create_classifier_chain(self):
        # TODO(sc68cal) Make this not hacky, and make it pass a session
        # in a context
        fake_tenant = uuidutils.generate_uuid()
        a = models.ClassifierGroup()
        a.tenant_id = fake_tenant
        a.name = 'test classifier'
        a.description = 'ensure all data inserted correctly'
        a.service = 'neutron-fwaas'
        b = models.IpClassifier()
        b.destination_ip_prefix = 'fd70:fbb6:449e::/48'
        b.source_ip_prefix = 'fddf:cb3b:bc4::/48'
        result = api.create_classifier_chain(self.context, a, b)
        self.assertIsNotNone(result)

    def test_convert_security_group_rule_to_classifier(self):
        sg_rule = {'direction': 'INGRESS',
                   'protocol': 'tcp',
                   'ethertype': 6,
                   'tenant_id': 'fake_tenant',
                   'port_range_min': 80,
                   'port_range_max': 80,
                   'remote_ip_prefix': 'fddf:cb3b:bc4::/48',
                   }
        result = api.convert_security_group_rule_to_classifier(self.context,
                                                               sg_rule)
        self.assertIsNotNone(result)

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
        pass

    def test_convert_classifier_chain_to_security_group(self):
        pass

    def test_convert_classifier_chain_to_firewall_policy(self):
        pass
