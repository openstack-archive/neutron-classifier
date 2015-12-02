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

from neutron_classifier.common import constants
from neutron_classifier.db import models


def security_group_ethertype_to_ethertype_value(ethertype):
    if ethertype == 6:
        return constants.ETHERTYPE_IPV6
    else:
        return constants.ETHERTYPE_IPV4


def ethertype_value_to_security_group_ethertype(ethertype):
    if ethertype == constants.ETHERTYPE_IPV6:
        return 6
    else:
        return 4


def get_classifier_group(context, classifier_group_id):
    return context.session.query(models.ClassifierGroup).get(
        classifier_group_id)


def create_classifier_chain(context, classifier_group, classifier):
    chain = models.ClassifierChainEntry()
    chain.sequence = 1
    chain.classifier = classifier
    chain.classifier_group = classifier_group
    context.session.add(chain)
    context.session.commit()
    return chain


def convert_security_group_to_classifier(context, security_group):
    cgroup = models.ClassifierGroup()
    cgroup.service = 'security-group'
    for rule in security_group['security_group_rules']:
        convert_security_group_rule_to_classifier(context, rule, cgroup)
    context.session.add(cgroup)
    context.session.commit()
    return cgroup


def convert_security_group_rule_to_classifier(context, security_group_rule,
                                              group):
    # Pull the source from the SG rule
    cl1 = models.IpClassifier()
    cl1.source_ip_prefix = security_group_rule['remote_ip_prefix']

    # Ports
    cl2 = models.TransportClassifier()
    cl2.destination_port_range_min = security_group_rule['port_range_min']
    cl2.destination_port_range_max = security_group_rule['port_range_max']

    # Direction
    cl3 = models.DirectionClassifier()
    cl3.direction = security_group_rule['direction']

    # Ethertype
    cl4 = models.EthernetClassifier()
    cl4.ethertype = security_group_ethertype_to_ethertype_value(
        security_group_rule['ethertype'])

    if cl4.ethertype == constants.ETHERTYPE_IPV6:
        cl5 = models.Ipv6Classifier()
        cl5.next_header = security_group_rule['protocol']
    else:
        cl5 = models.Ipv4Classifier()
        cl5.protocol = security_group_rule['protocol']

    chain1 = models.ClassifierChainEntry()
    chain1.classifier_group = group
    chain1.classifier = cl1
    chain1.sequence = 1

    chain2 = models.ClassifierChainEntry()
    chain2.classifier_group = group
    chain2.classifier = cl2
    # Security Group classifiers might not need to be nested or have sequences?
    chain2.sequence = 1

    chain3 = models.ClassifierChainEntry()
    chain3.classifier_group = group
    chain3.classifier = cl3
    chain3.sequence = 1

    chain4 = models.ClassifierChainEntry()
    chain4.classifier_group = group
    chain4.classifier = cl4
    chain4.sequence = 1

    chain5 = models.ClassifierChainEntry()
    chain5.classifier_group = group
    chain5.classifier = cl5
    chain5.sequence = 1

    context.session.add(cl1)
    context.session.add(cl2)
    context.session.add(cl3)
    context.session.add(cl4)
    context.session.add(cl5)
    context.session.add(chain1)
    context.session.add(chain2)
    context.session.add(chain3)
    context.session.add(chain4)
    context.session.add(chain5)


def convert_firewall_rule_to_classifier(context, firewall_rule):
    pass


def convert_classifier_group_to_security_group(context, classifier_group_id):
    sg_dict = {}
    cg = get_classifier_group(context, classifier_group_id)
    for classifier in [link.classifier for link in cg.classifier_chain]:
        classifier_type = type(classifier)
        if classifier_type is models.TransportClassifier:
            sg_dict['port_range_min'] = classifier.destination_port_range_min
            sg_dict['port_range_max'] = classifier.destination_port_range_max
            continue
        if classifier_type is models.IpClassifier:
            sg_dict['remote_ip_prefix'] = classifier.source_ip_prefix
            continue
        if classifier_type is models.DirectionClassifier:
            sg_dict['direction'] = classifier.direction
            continue
        if classifier_type is models.EthernetClassifier:
            sg_dict['ethertype'] = ethertype_value_to_security_group_ethertype(
                classifier.ethertype)
            continue
        if classifier_type is models.Ipv4Classifier:
            sg_dict['protocol'] = classifier.protcol
            continue
        if classifier_type is models.Ipv6Classifier:
            sg_dict['protocol'] = classifier.next_header
            continue

    return sg_dict


def convert_classifier_to_firewall_policy(context, chain_id):
    pass
