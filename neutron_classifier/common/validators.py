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

type_validators = {}
type_validators['ethernet'] = eth_validators.validators_dict
type_validators['ipv4'] = ipv4_validators.validators_dict
type_validators['ipv6'] = ipv6_validators.validators_dict
type_validators['tcp'] = tcp_validators.validators_dict
type_validators['udp'] = udp_validators.validators_dict


def check_valid_classifications(svc_plu, context, cls):
    cg_model = models.ClassificationGroup
    mapping_model = models.ClassificationGroupMapping
    cl_mapping = models._read_classification_groups(
        svc_plu, context, cg_model, mapping_model)

    ids = []
    for id in cls:
        cl = svc_plu.get_classification(context, id)
        ids.append(cl['id'])

    for m in cl_mapping:
        if set(m['classification'].split(',')) & set(ids):
            raise exceptions.ConsumedClassification(
                valid_mark=id, classification='id')
    return True


def check_valid_classification_groups(svc_plu, context, cgs):
    model = models.ClassificationGroup
    cl = svc_plu._get_collection(context, model,
                                 models._generate_dict_from_cg_db)
    ids = []
    for cg in cl:
        ids.append(cg['id'])
        for c in cgs:
            if cg['id'] == c:
                if cg['cg_id'] is not None:
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
            if cg['cg_id'] is not None:
                raise exceptions.ConsumedClassificationGroup(
                    valid_mark=cgs, classification='id')
            else:
                return True
