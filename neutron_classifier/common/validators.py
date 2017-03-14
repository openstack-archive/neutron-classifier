# Copyright (c) 2017 Intel. All Rights Reserved.
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
from neutron_classifier.common import exceptions

#NOTE(davidsha) IPV4 validators
def check_valid_ipv4_classification(classification_dict):
    class_dict = {}
    validators = {'dscp': check_valid_dscp_mark,
                  'dscp_mask':check_valid_dscp_mask,
                  'ecn':check_valid_ecn_mark,
                  'ecn_mask':check_valid_ecn_mask,
                  'protocol':check_valid_protocol_mark,
                  'protocol_mask':check_valid_protocol_mark,
                  'source_address':check_valid_ipv4_address,
                  'source_address_range':check_valid_ipv4_cidr,
                  'destination_address':check_valid_ipv4_address,
                  'destination_address_range':check_valid_ipv4_cidr
                 }

    for key in classification_dict.keys():
        if key.replace('_','-') in constants.IP_V4 and classification_dict[key]:
            class_dict[key] = validators[key](classification_dict[key])
        else:
            class_dict[key] = classification_dict[key]

    return class_dict

def check_valid_dscp_mark(dscp_value):
    dscp = None

    try:
        dscp = int(dscp_value)
    except:
        dscp = int(dscp_value, 0)

    if dscp not in constants.DSCP_VALID_MARKS:
        raise exceptions.InvalidClassificationMark(valid_mark=dscp,
                                                   classification='dscp')
    return str(dscp)

def check_valid_dscp_mask(dscp_mask):
    dscp = None

    try:
        dscp = int(dscp_mask)
    except:
        dscp = int(dscp_mask, 0)

    if dscp > 63 or dscp < 0:
        raise exceptions.InvalidClassificationMask(valid_mark=dscp_mask,
                                                   classification='dscp')
    return str(dscp)

def check_valid_ecn_mark(ecn_value):
    ecn = None

    try:
        ecn = int(ecn_value)
    except:
        ecn = int(ecn_value, 0)

    if ecn not in constants.ECN_VALID_MARKS:
        raise exceptions.InvalidClassificationMark(valid_mark=ecn,
                                                   classification='ecn')
    return str(ecn)

def check_valid_ecn_mask(ecn_mask):
    ecn = None

    try:
        ecn = int(ecn_mask)
    except:
        ecn = int(ecn_mask, 0)

    if ecn > 3 or ecn < 0:
        raise exceptions.InvalidClassificationMask(valid_mark=ecn_mask,
                                                   classification='ecn')
    return str(ecn)

def check_valid_protocol_mark(protocol):
    prot = None

    try:
        proto = int(protocol)
    except:
        proto = int(protocol, 0)

    if proto > 255 or protocol < 0:
        raise exceptions.InvalidClassificationMark(valid_mark=protocol,
                                                   classification='protocol')
    return str(protocol)

def check_valid_ipv4_address(address):
    ip = address.split('.')

    if len(ip) is not 4:
        raise exceptions.InvalidClassificationMark(valid_mark=address,
                                                   classification='address')
    for ip_segment in ip:
        dec = int (ip_segment)

        if dec < 0 or dec > 255:
            raise exceptions.InvalidClassificationMark(valid_mark=address,
                                                   classification='address')

    return address

def check_valid_ipv4_cidr(cidr):
    cidr = int(cidr)

    if cidr < 0  or cidr > 32:
        raise exceptions.InvalidClassificationMask(valid_mark=cidr,
                                                   classification='cidr')
    return str(cidr)
