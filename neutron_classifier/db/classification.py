# Copyright 2017 Intel Corporation.
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

from oslo_log import log as logging

from neutron.db import common_db_mixin

from neutron_classifier.common import validators
from neutron_classifier.db import models

LOG = logging.getLogger(__name__)


class TrafficClassificationDbPlugin(common_db_mixin.CommonDbMixin):

    def __init__(self):
        super(TrafficClassificationDbPlugin, self).__init__()

    def create_classification_group(self, context, classification_group):
        details = classification_group['classification_group']
        if details['classification']:
            validators.check_valid_classifications(self, context,
                                                   details['classification'])
        if details['classification_group']:
            validators.check_valid_classification_groups(
                self, context, details['classification_group'])
        db_dict = {'name': details['name'],
                   'project_id': details['project_id'],
                   'description': details['description'],
                   'classification': details['classification'],
                   'classification_group': details['classification_group'],
                   'shared': details['shared'],
                   'operator': details['operator']}
        model = models.ClassificationGroup(
            name=details['name'],
            description=details['description'],
            shared=details['shared'],
            operator=details['operator'])

        for key in details.keys():
            if details[key]:
                db_dict[key] = details[key]

        with context.session.begin(subtransactions=True):
            context.session.add(model)
        db_dict['id'] = model.id

        with context.session.begin(subtransactions=True):
            for cl in details['classification']:
                mapping_model = models.ClassificationGroupMapping(
                    cg_id=db_dict['id'],
                    classification_id=cl)
                context.session.add(mapping_model)
            cg_model = models.ClassificationGroup
            for c in details['classification_group']:
                context.session.query(cg_model).filter(
                    cg_model.id == c).update({"cg_id": db_dict['id']},
                                             synchronize_session='evaluate')

        return db_dict

    def delete_classification_group(self, context, classification_group_id):
        model = models.ClassificationGroup
        mapping_model = models.ClassificationGroupMapping
        mappings = self._get_collection(
            context, mapping_model, models._generate_dict_from_cgmapping_db)
        validators.check_can_delete_classification_group(
            self, context, classification_group_id)
        with context.session.begin(subtransactions=True):
            for m in mappings:
                if classification_group_id == m['cg_id']:
                    row = self._get_by_id(
                        context,
                        models.ClassificationGroupMapping, m['id'])
                    context.session.delete(row)
            context.session.query(model).filter(
                model.cg_id == classification_group_id).update({
                    "cg_id": None}, synchronize_session='evaluate')
            cg = self._get_by_id(context,
                                 models.ClassificationGroup,
                                 classification_group_id)
            context.session.delete(cg)

        self._res_name = ""

    def update_classification_group(self, context, classification_group_id,
                                    classification_group):
        details = classification_group['classification_group']
        cg = self.get_classification_group(context, classification_group_id)
        if details['name']:
            cg['name'] = details['name']
        if details['description']:
            cg['description'] = details['description']
        model = models.ClassificationGroup
        with context.session.begin(subtransactions=True):
            context.session.query(model).filter(
                model.id == classification_group_id).update(
                    {"name": cg['name'], "description": cg['description']},
                    synchronize_session='evaluate')
        return cg

    def get_classification_group(self, context,
                                 classification_group_id, **kwargs):
        model = models.ClassificationGroup
        mapping_model = models.ClassificationGroupMapping
        cg = models._read_classification_groups(
            self, context, model, mapping_model, classification_group_id)

        return cg

    def get_classification_groups(self, context, filters=None, fields=None,
                                  sorts=None, limit=None, marker=None,
                                  page_reverse=False):
        model = models.ClassificationGroup
        mapping_model = models.ClassificationGroupMapping
        cg = models._read_classification_groups(
            self, context, model, mapping_model)

        self._res_name = ""
        return cg

    def get_classification_types(self, context, **kwargs):
        resp = []
        resp.append({'name': 'ipv4', 'definition': ','.join(
            [key for key in validators.type_validators['ipv4'].keys()])})
        resp.append({'name': 'ipv6', 'definition': ','.join(
            [key for key in validators.type_validators['ipv6'].keys()])})
        resp.append({'name': 'tcp', 'definition': ','.join(
            [key for key in validators.type_validators['tcp'].keys()])})
        resp.append({'name': 'udp', 'definition': ','.join(
            [key for key in validators.type_validators['udp'].keys()])})
        resp.append({'name': 'ethernet', 'definition': ','.join(
            [key for key in validators.type_validators['ethernet'].keys()])})

        return resp

    def generate_dict_from_db(self, model, fields=None):
        name = self._res_name[:-1] if 'classifications' in self._res_name\
            else self._res_name
        response = models.DICT_RESP[name](model, fields)
        return response
