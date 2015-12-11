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

from neutron_classifier.common import constants as const
from neutron_classifier.common import exceptions as exc

import netaddr

SG_RULE_TYPE = 1
FW_RULE_TYPE = 2


def _get_attr_value(dict, key):
    return dict.get(key, None)


def _validate_fwr_protocol_parameters(fwr, protocol):
    """Check if given port values and  protocol are valid or not"""
    if protocol not in (const.PROTO_NAME_TCP, const.PROTO_NAME_UDP):
        source_port_range_min = _get_attr_value(fwr, 'source_port_range_min')
        source_port_range_max = _get_attr_value(fwr, 'source_port_range_max')
        destination_port_range_min = _get_attr_value(
            fwr, 'destination_port_range_min')
        destination_port_range_max = _get_attr_value(
            fwr, 'destination_port_range_max')
        if (source_port_range_min or source_port_range_max or
                destination_port_range_min or destination_port_range_max):
            raise exc.InvalidICMPParameter(param="Source, destination port")


def _validate_sg_ethertype_and_protocol(rule, protocol):
    """Check if given ethertype and  protocol are valid or not"""
    eth_value = _get_attr_value(rule, 'ethertype')
    if protocol == const.PROTO_NAME_ICMP_V6:
        if eth_value == const.SECURITYGROUP_ETHERTYPE_IPV4:
            raise exc.EthertypeConflictWithProtocol(ethertype=eth_value,
                                                    protocol=protocol)


def _validate_port_range(min_port, max_port):
    """Check that port_range is valid."""
    if int(min_port) > int(max_port):
        port_range = '%s:%s' % (min_port, max_port)
        raise exc.InvalidPortRange(port_range=port_range)


def is_ethernetclassifier_valid(rule, type):
    """Check ethertype or ip_version in rule dict"""
    if type == SG_RULE_TYPE:
        attr_type = 'ethertype'
        attr_list = [const.SECURITYGROUP_ETHERTYPE_IPV4,
                     const.SECURITYGROUP_ETHERTYPE_IPV6]
    else:
        attr_type = 'ip_version'
        attr_list = [const.IP_VERSION_4, const.IP_VERSION_6]

    eth_value = _get_attr_value(rule, attr_type)
    if not eth_value:
        return False
    elif eth_value not in attr_list:
        raise exc.InvalidEthernetClassifier(eth_type=attr_type)
    return True


def is_protocolclassifier_valid(rule, type):
    """Check protocol in rule dict and validate dependent params"""
    protocol = _get_attr_value(rule, 'protocol')

    if not protocol:
        return False

    if type == SG_RULE_TYPE:
        _validate_sg_ethertype_and_protocol(rule, protocol)
    else:
        _validate_fwr_protocol_parameters(rule, protocol)

    return True


def is_ipclassifier_valid(rule, type):
    """validate the ip address received in rule dict"""
    src_ip_version = dst_ip_version = None
    src_ip_address = dst_ip_address = None
    if type == SG_RULE_TYPE:
        dst_ip_address = _get_attr_value(rule, 'remote_ip_prefix')
        attr_type = 'ethertype'
    else:
        src_ip_address = _get_attr_value(rule, 'source_ip_address')
        dst_ip_address = _get_attr_value(rule, 'destination_ip_address')
        attr_type = 'ip_version'

    if src_ip_address:
        src_ip_version = netaddr.IPNetwork(src_ip_address).version
    if dst_ip_address:
        dst_ip_version = netaddr.IPNetwork(dst_ip_address).version

    rule_ip_version = _get_attr_value(rule, attr_type)
    if type == SG_RULE_TYPE:
        if rule_ip_version != "IPv%d" % dst_ip_version:
            raise exc.IpAddressConflict()
    elif ((src_ip_version and src_ip_version != rule_ip_version) or
            (dst_ip_version and dst_ip_version != rule_ip_version)):
        raise exc.IpAddressConflict()
    return True


def is_directionclassifier_valid(rule, type):
    """Check direction param in rule dict"""
    direction = _get_attr_value(rule, 'direction')
    if not direction:
        return False
    return True


def is_transportclassifier_valid(rule, type):
    """Verify port range values"""
    if type == SG_RULE_TYPE:
        port_range_min = _get_attr_value(rule, 'port_range_min')
        port_range_max = _get_attr_value(rule, 'port_range_max')
        _validate_port_range(port_range_min, port_range_max)
    else:
        source_port_range_min = _get_attr_value(rule, 'source_port_range_min')
        source_port_range_max = _get_attr_value(rule, 'source_port_range_max')
        destination_port_range_min = _get_attr_value(
            rule, 'destination_port_range_min')
        source_port_range_max = _get_attr_value(
            rule, 'destination_port_range_max')
        _validate_port_range(source_port_range_min, source_port_range_max)
        _validate_port_range(destination_port_range_min, source_port_range_max)
    return True
