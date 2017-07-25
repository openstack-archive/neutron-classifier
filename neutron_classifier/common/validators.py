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

from neutron_classifier.common import eth_validators
from neutron_classifier.common import exceptions
from neutron_classifier.common import ipv4_validators
from neutron_classifier.common import ipv6_validators
from neutron_classifier.common import tcp_validators
from neutron_classifier.common import udp_validators
from neutron_classifier.db import models
from neutron_classifier.objects import classifications

from neutron.db import api as db_api

type_validators = {}
type_validators['ethernet'] = eth_validators.validators_dict
type_validators['ipv4'] = ipv4_validators.validators_dict
type_validators['ipv6'] = ipv6_validators.validators_dict
type_validators['tcp'] = tcp_validators.validators_dict
type_validators['udp'] = udp_validators.validators_dict


def check_valid_classifications(context, cs):
    for c_id in cs:
        c_model = classifications.ClassificationBase
        c = c_model.get_object(context, id=c_id)
        c_type_clas = classifications.CLASS_MAP[c.c_type]
        classification = c_type_clas.get_object(context, id=c_id)
        if not classification or (classification.id != c_id):
            raise exceptions.InvalidClassificationId()


def check_valid_classification_groups(context, cgs):
    for cg_id in cgs:
        cg = models._read_classification_group(context, cg_id)
        if not cg or (cg.id != cg_id):
            raise exceptions.InvalidClassificationGroupId()


def check_can_delete_classification_group(context, cg_id):
    """Checks whether a classification group can be deleted.

    Here we are checking whether a classification group is a child of another
    classification group, meaning is already mapped to a parent classification
    group. In that case we cannot delete it and will raise an exception.
    """
    cgs = classifications.ClassificationGroup.get_objects(context)
    for cg in cgs:
        with db_api.context_manager.writer.using(context):
            cg_obj = classifications.ClassificationGroup.get_object(context,
                                                                    id=cg.id)
            mapped_cgs = classifications._get_mapped_classification_groups(
                context, cg_obj)
            if cg_id in [mcg.id for mcg in mapped_cgs]:
                raise exceptions.ConsumedClassificationGroup()

    return True
