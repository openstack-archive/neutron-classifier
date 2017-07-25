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


class TrafficClassificationGroupPlugin(common_db_mixin.CommonDbMixin):

    def __init__(self):
        super(TrafficClassificationGroupPlugin, self).__init__()

    def create_classification_group(self, context, classification_group):
        details = classification_group['classification_group']
        if details['classification']:
            validators.check_valid_classifications(self, context,
                                                   details['classification'])
        if details['cg_id']:
            validators.check_valid_classification_groups(
                self, context, details['cg_id'])
        db_dict = {'name': details['name'],
                   'project_id': details['project_id'],
                   'description': details['description'],
                   'classification': details['classification'],
                   'cg_id': details['cg_id'],
                   'shared': details['shared'],
                   'operator': details['operator']}
        model = models.ClassificationGroup(
            name=details['name'],
            description=details['description'],
            shared=details['shared'],
            project_id=details['project_id'],
            operator=details['operator'])

        with context.session.begin(subtransactions=True):
            context.session.add(model)
        db_dict['id'] = model.id

        with context.session.begin(subtransactions=True):
            for cl in details['classification']:
                mapping_model = models.ClassificationGroupMapping(
                    cg_id=db_dict['id'],
                    classification_id=cl,
                    project_id=details['project_id'])
                context.session.add(mapping_model)
            cg_model = models.ClassificationGroup
            for c in details['cg_id']:
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

        return cg
