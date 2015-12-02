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

from neutron_classifier.db import models


def get_classifier_chain():
    pass


def create_classifier_chain(context, classifier_group, classifier):
    chain = models.ClassifierChainEntry()
    chain.sequence = 1
    chain.classifier = classifier
    chain.classifier_group = classifier_group
    context.session.add(chain)
    context.session.commit()
    return chain


def convert_security_group_rule_to_classifier(context, security_group_rule):
    # TODO(sc68cal) Pass in the classifier group
    group = models.ClassifierGroup()
    group.service = 'security-group'

    # Pull the source from the SG rule
    cl1 = models.IpClassifier()
    cl1.source_ip_prefix = security_group_rule['remote_ip_prefix']

    # Ports
    cl2 = models.TransportClassifier()
    cl2.destination_port_range_min = security_group_rule['port_range_min']
    cl2.destination_port_range_max = security_group_rule['port_range_max']

    chain1 = models.ClassifierChainEntry()
    chain1.classifier_group = group
    chain1.classifier = cl1
    chain1.sequence = 1

    chain2 = models.ClassifierChainEntry()
    chain2.classifier_group = group
    chain2.classifier = cl2
    # Security Group classifiers might not need to be nested or have sequences?
    chain2.sequence = 1
    context.session.add(group)
    context.session.add(cl1)
    context.session.add(cl2)
    context.session.add(chain1)
    context.session.add(chain2)
    context.session.commit()
    return group


def convert_firewall_rule_to_classifier(context, firewall_rule):
    group = models.ClassifierGroup()
    group.service = 'firewall_rule'

    # Pull the source from the SG rule
    cl1 = models.IpClassifier()
    cl1.source_ip_prefix = firewall_rule['source_ip_address']
    cl1.destination_ip_prefix = firewall_rule['destination_ip_address']

    # Ports
    cl2 = models.TransportClassifier()
    cl2.protocol = firewall_rule['protocol']
    cl2.source_port_range_min = firewall_rule['source_port_range_min']
    cl2.source_port_range_max = firewall_rule['source_port_range_max']
    chain1 = models.ClassifierChainEntry()
    chain1.classifier_group = group
    chain1.classifier = cl1
    chain1.sequence = 1

    chain2 = models.ClassifierChainEntry()
    chain2.classifier_group = group
    chain2.classifier = cl2
    # Security Group classifiers might not need to be nested or have sequences?
    chain2.sequence = 1
    context.session.add(group)
    context.session.add(cl1)
    context.session.add(cl2)
    context.session.add(chain1)
    context.session.add(chain2)
    context.session.commit()
    return group


def convert_classifier_chain_to_security_group(context, chain_id):
    pass


def convert_classifier_to_firewall_policy(context, chain_id):
    pass
