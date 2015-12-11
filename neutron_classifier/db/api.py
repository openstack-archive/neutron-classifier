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

from neutron_classifier.common import constants
from neutron_classifier.db import models
from neutron_classifier.db import validators


def security_group_ethertype_to_ethertype_value(ethertype):
    if ethertype == constants.SECURITYGROUP_ETHERTYPE_IPV6:
        return constants.ETHERTYPE_IPV6
    else:
        return constants.ETHERTYPE_IPV4


def ethertype_value_to_security_group_ethertype(ethertype):
    if ethertype == constants.ETHERTYPE_IPV6:
        return constants.SECURITYGROUP_ETHERTYPE_IPV6
    else:
        return constants.SECURITYGROUP_ETHERTYPE_IPV4


def get_classifier_group(context, classifier_group_id):
    return context.session.query(models.ClassifierGroup).get(
        classifier_group_id)


def create_classifier_chain(classifier_group, classifiers,
                            incremeting_sequence=False):
    if incremeting_sequence:
        seq = 0

    for classifier in classifiers:
        ce = models.ClassifierChainEntry(classifier_group=classifier_group,
                                         classifier=classifier)
        if incremeting_sequence:
            ce.sequence = seq
        classifier_group.classifier_chain.append(ce)


def convert_security_group_to_classifier(context, security_group):
    cgroup = models.ClassifierGroup()
    cgroup.service = 'security-group'
    for rule in security_group['security_group_rules']:
        convert_security_group_rule_to_classifier(context, rule, cgroup)
    context.session.add(cgroup)
    context.session.commit()
    return cgroup


def convert_security_group_rule_to_classifier(context, sgr, group):
    cl1 = cl2 = cl3 = cl4 = None
    # Rule type
    type = validators.SG_RULE_TYPE

    # Ethertype
    if validators.is_ethernetclassifier_valid(sgr, type):
        cl1 = models.EthernetClassifier()
        cl1.ethertype = security_group_ethertype_to_ethertype_value(
            sgr['ethertype'])

    # protocol
    if validators.is_protocolclassifier_valid(sgr, type):
        if cl1 and cl1.ethertype == constants.ETHERTYPE_IPV6:
            cl2 = models.Ipv6Classifier()
            cl2.next_header = sgr['protocol']
        else:
            cl2 = models.Ipv4Classifier()
            cl2.protocol = sgr['protocol']

    # remote ip
    if validators.is_ipclassifier_valid(sgr, type):
        cl3 = models.IpClassifier()
        cl3.source_ip_prefix = sgr['remote_ip_prefix']

    # Ports
    if validators.is_transportclassifier_valid(sgr, type):
        cl4 = models.TransportClassifier(
            destination_port_range_min=sgr['port_range_min'],
            destination_port_range_max=sgr['port_range_max'])

    # Direction
    if validators.is_directionclassifier_valid(sgr, type):
        cl5 = models.DirectionClassifier(direction=sgr['direction'])

    classifiers = [cl1, cl2, cl3, cl4, cl5]
    create_classifier_chain(group, classifiers)


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
            sg_dict['protocol'] = classifier.protocol
            continue
        if classifier_type is models.Ipv6Classifier:
            sg_dict['protocol'] = classifier.next_header
            continue

    return sg_dict


def convert_firewall_policy_to_classifier(context, firewall):
    cgroup = models.ClassifierGroup()
    cgroup.service = 'neutron-fwaas'
    for rule in firewall['firewall_rules']:
        convert_firewall_rule_to_classifier(context, rule, cgroup)
    context.session.add(cgroup)
    context.session.commit()
    return cgroup


def convert_firewall_rule_to_classifier(context, fwr, group):
    cl1 = cl2 = cl3 = cl4 = None
    # Rule type
    type = validators.FW_RULE_TYPE

    # ip_version
    if validators.is_ethernetclassifier_valid(fwr, type):
        cl1 = models.EthernetClassifier()
        cl1.ethertype = fwr['ip_version']

    # protocol
    if validators.is_protocolclassifier_valid(fwr, type):
        if cl1.ethertype == constants.IP_VERSION_6:
            cl2 = models.Ipv6Classifier()
            cl2.next_header = fwr['protocol']
        else:
            cl2 = models.Ipv4Classifier()
            cl2.protocol = fwr['protocol']

    # Source and destination ip
    if validators.is_ipclassifier_valid(fwr, type):
        cl3 = models.IpClassifier()
        cl3.source_ip_prefix = fwr['source_ip_address']
        cl3.destination_ip_prefix = fwr['destination_ip_address']

    # Ports
    if validators.is_transportclassifier_valid(fwr, type):
        cl4 = models.TransportClassifier(
            source_port_range_min=fwr['source_port_range_min'],
            source_port_range_max=fwr['source_port_range_max'],
            destination_port_range_min=fwr['destination_port_range_min'],
            destination_port_range_max=fwr['destination_port_range_max'])

    classifiers = [cl1, cl2, cl3, cl4]
    create_classifier_chain(group, classifiers)


def convert_classifier_to_firewall(context, classifier_group_id):
    fw_dict = {}
    cg = get_classifier_group(context, classifier_group_id)
    for classifier in [link.classifier for link in cg.classifier_chain]:
        classifier_type = type(classifier)
        if classifier_type is models.EthernetClassifier:
            fw_dict['ip_version'] = classifier.ethertype
            continue
        if classifier_type is models.Ipv4Classifier:
            fw_dict['protocol'] = classifier.protocol
            continue
        if classifier_type is models.Ipv6Classifier:
            fw_dict['protocol'] = classifier.next_header
            continue
        if classifier_type is models.TransportClassifier:
            fw_dict['source_port_range_min'] = classifier.source_port_range_min
            fw_dict['source_port_range_max'] = classifier.source_port_range_max
            fw_dict['destination_port_range_min'] = \
                classifier.destination_port_range_min
            fw_dict['destination_port_range_max'] = \
                classifier.destination_port_range_max
            continue
        if classifier_type is models.IpClassifier:
            fw_dict['source_ip_address'] = classifier.source_ip_prefix
            fw_dict['destination_ip_address'] = \
                classifier.destination_ip_prefix
            continue

    return fw_dict
