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
from oslo_utils import uuidutils

from neutron.db import api as db_api
from neutron.db import common_db_mixin
from neutron.objects import base as base_obj

from neutron_classifier.common import exceptions
from neutron_classifier.common import validators
from neutron_classifier.objects import classifications

LOG = logging.getLogger(__name__)


class TrafficClassificationGroupPlugin(common_db_mixin.CommonDbMixin):

    def __init__(self):
        super(TrafficClassificationGroupPlugin, self).__init__()

    def create_classification_group(self, context, classification_group):
        details = classification_group['classification_group']

        if details['classifications']:
            validators.check_valid_classifications(context,
                                                   details['classifications'])

        if details['classification_groups']:
            validators.check_valid_classification_groups(
                context, details['classification_groups'])
        details['id'] = uuidutils.generate_uuid()
        mappings = {'c_ids': details['classifications'],
                    'cg_ids': details['classification_groups']}
        db_dict = details
        cg = classifications.ClassificationGroup(context, **details)

        with db_api.context_manager.writer.using(context):
            cg.create()
        db_dict['id'] = cg.id

        with db_api.context_manager.writer.using(context):
            for cl in mappings['c_ids']:
                cg_c_mapping = classifications.CGToClassificationMapping(
                    context,
                    container_cg_id=cg.id,
                    stored_classification_id=cl)
                cg_c_mapping.create()
            for cg_id in mappings['cg_ids']:
                cg_cg_mapping = classifications.CGToClassificationGroupMapping(
                    context,
                    container_cg_id=cg.id,
                    stored_cg_id=cg_id
                )
                cg_cg_mapping.create()
        db_dict['classifications'] = details['classifications']
        db_dict['classification_group'] = details['classification_groups']

        return db_dict

    def delete_classification_group(self, context, classification_group_id):
        if validators.check_can_delete_classification_group(
                context, classification_group_id):
            cg = classifications.ClassificationGroup.get_object(
                context, id=classification_group_id)
            with db_api.context_manager.writer.using(context):
                cg.delete()

    def update_classification_group(self, context, classification_group_id,
                                    fields_to_update):
        field_keys = fields_to_update.keys()
        if 'name' not in field_keys and 'description' not in field_keys:
            raise exceptions.InvalidUpdateRequest()
        with db_api.context_manager.writer.using(context):
            cg = classifications.ClassificationGroup.update_object(
                context, fields_to_update, id=classification_group_id)
        return cg

    def _make_db_dict(self, obj):
        db_dict = {'classification_group': {}}
        for key in obj.fields.keys():
            db_dict['classification_group'][key] = obj[key]
        return db_dict

    def get_classification_group(self, context, classification_group_id):
        with db_api.context_manager.writer.using(context):
            cg = classifications.ClassificationGroup.get_object(
                context, id=classification_group_id)
            db_dict = self._make_db_dict(cg)
            db_dict['classification_group']['classifications'] =\
                classifications._get_mapped_classifications(context, cg)
            db_dict['classification_group']['classification_groups'] = \
                classifications._get_mapped_classification_groups(context, cg)
            return db_dict

    def get_classification_groups(self, context, sorts=None, limit=None,
                                  marker=None, page_reverse=False):
        pager = base_obj.Pager(sorts, limit, page_reverse, marker)
        cgs = classifications.ClassificationGroup.get_objects(context,
                                                              _pager=pager)
        return cgs
