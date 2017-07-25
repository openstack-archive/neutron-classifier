# Copyright (c) 2017 Intel Corporation.
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

from neutron_classifier.common import constants
from neutron_classifier.common import eth_validators
from neutron_classifier.common import exceptions
from neutron_classifier.common import ipv4_validators
from neutron_classifier.common import ipv6_validators
from neutron_classifier.common import tcp_validators
from neutron_classifier.common import udp_validators
from neutron_classifier.db import models

type_validators = {}
type_validators['ethernet'] = eth_validators.validators_dict
type_validators['ipv4'] = ipv4_validators.validators_dict
type_validators['ipv6'] = ipv6_validators.validators_dict
type_validators['tcp'] = tcp_validators.validators_dict
type_validators['udp'] = udp_validators.validators_dict


def check_valid_ipv4_classification(classification_dict):
    class_dict = {}
    validators = {'dscp': check_valid_dscp_mark,
                  'dscp_mask': check_valid_dscp_mask,
                  'ecn': check_valid_ecn_mark,
                  'ecn_mask': check_valid_ecn_mask,
                  'protocol': check_valid_protocol_mark,
                  'protocol_mask': check_valid_protocol_mark,
                  'source_address': check_valid_ipv4_address,
                  'source_address_range': check_valid_ipv4_cidr,
                  'destination_address': check_valid_ipv4_address,
                  'destination_address_range': check_valid_ipv4_cidr,
                  }

    for key in classification_dict.keys():
        if key.replace('_', '-') in constants.IP_V4 and \
           classification_dict[key]:
            class_dict[key] = validators[key](classification_dict[key])
        else:
            class_dict[key] = classification_dict[key]

    return class_dict


def check_valid_dscp_mark(dscp_value):
    dscp = None

    try:
        dscp = int(dscp_value)
    except Exception:
        dscp = int(dscp_value, 0)

    if dscp not in constants.DSCP_VALID_MARKS:
        raise exceptions.InvalidClassificationMark(valid_mark=dscp,
                                                   classification='dscp')
    return str(dscp)


def check_valid_dscp_mask(dscp_mask):
    dscp = None

    try:
        dscp = int(dscp_mask)
    except Exception:
        dscp = int(dscp_mask, 0)

    if dscp > 63 or dscp < 0:
        raise exceptions.InvalidClassificationMask(valid_mark=dscp_mask,
                                                   classification='dscp')
    return str(dscp)


def check_valid_ecn_mark(ecn_value):
    ecn = None

    try:
        ecn = int(ecn_value)
    except Exception:
        ecn = int(ecn_value, 0)

    if ecn not in constants.ECN_VALID_MARKS:
        raise exceptions.InvalidClassificationMark(valid_mark=ecn,
                                                   classification='ecn')
    return str(ecn)


def check_valid_ecn_mask(ecn_mask):
    ecn = None

    try:
        ecn = int(ecn_mask)
    except Exception:
        ecn = int(ecn_mask, 0)

    if ecn > 3 or ecn < 0:
        raise exceptions.InvalidClassificationMask(valid_mark=ecn_mask,
                                                   classification='ecn')
    return str(ecn)


def check_valid_protocol_mark(protocol):
    proto = -1

    try:
        proto = int(protocol)
    except Exception:
        proto = int(protocol, 0)

    if proto > 255 or protocol < 0:
        raise exceptions.InvalidClassificationMark(valid_mark=protocol,
                                                   classification='protocol')
    return str(protocol)


def check_valid_ipv4_address(address):
    ip = address.split('.')
    addr = 'address'

    if len(ip) is not 4:
        raise exceptions.InvalidClassificationMark(valid_mark=address,
                                                   classification=addr)
    for ip_segment in ip:
        dec = int(ip_segment)

        if dec < 0 or dec > 255:
            raise exceptions.InvalidClassificationMark(valid_mark=address,
                                                       classification=addr)

    return address


def check_valid_ipv4_cidr(cidr):
    cidr = int(cidr)

    if cidr < 0 or cidr > 32:
        raise exceptions.InvalidClassificationMask(valid_mark=cidr,
                                                   classification='cidr')
    return str(cidr)


def check_valid_classifications(svc_plu, context, cls):
    model = models.ClassificationBase
    cg_model = models.ClassificationGroup
    mapping_model = models.ClassificationGroupMapping
    cl = svc_plu._get_collection(context, model,
                                 models.read_classification_base)
    cl_mapping = models._read_classification_groups(
        svc_plu, context, cg_model, mapping_model)
    ids = []
    for c in cl:
        ids.append(c['id'])
    for m in cl_mapping:
        if set(m['classification'].split(',')) & set(cls):
            raise exceptions.ConsumedClassification(
                valid_mark=ids, classification='id')
    if set(ids).issuperset(set(cls)):
        return True
    else:
        raise exceptions.InvalidClassificationId(
            valid_mark=ids, classification='id')


def check_valid_classification_groups(svc_plu, context, cgs):
    model = models.ClassificationGroup
    cl = svc_plu._get_collection(context, model,
                                 models._generate_dict_from_cg_db)
    ids = []
    for cg in cl:
        ids.append(cg['id'])
        for c in cgs:
            if cg['id'] == c:
                if cg['classification_group'] is not None:
                    raise exceptions.ConsumedClassification(
                        valid_mark=cgs, classification='id')
    if set(ids).issuperset(set(cgs)):
        return True
    else:
        raise exceptions.InvalidClassificationGroupId(valid_mark=ids,
                                                      classification='id')


def check_can_delete_classification_group(svc_plu, context, cg_id):
    model = models.ClassificationGroup
    cgs = svc_plu._get_collection(context, model,
                                  models._generate_dict_from_cg_db)
    for cg in cgs:
        if cg['id'] == cg_id:
            if cg['classification_group'] is not None:
                raise exceptions.ConsumedClassificationGroup(
                    valid_mark=cgs, classification='id')
            else:
                return True
