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

from neutron_lib.db import api as db_api

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
        c_flag = cg_flag = False

        if 'classification' in details:
            c_flag = True
            validators.check_valid_classifications(context,
                                                   details['classification'])

        if 'classification_group' in details:
            cg_flag = True
            validators.check_valid_classification_groups(
                context, details['classification_group'])
        details['id'] = uuidutils.generate_uuid()
        mappings = {'c_ids': details['classification'] if c_flag else [],
                    'cg_ids': details['classification_group']
                    if cg_flag else []}
        db_dict = details
        if 'tenant_id' in details:
            del details['tenant_id']
        cg = classifications.ClassificationGroup(context, **details)

        with db_api.CONTEXT_WRITER.using(context):
            cg.create()
        db_dict['id'] = cg.id

        with db_api.CONTEXT_WRITER.using(context):
            if c_flag:
                for cl in mappings['c_ids']:
                    cg_c_mapping = classifications.CGToClassificationMapping(
                        context,
                        container_cg_id=cg.id,
                        stored_classification_id=cl)
                    cg_c_mapping.create()
            if cg_flag:
                for cg_id in mappings['cg_ids']:
                    cg_cg_mapping =\
                        classifications.CGToClassificationGroupMapping(
                            context,
                            container_cg_id=cg.id,
                            stored_cg_id=cg_id
                        )
                    cg_cg_mapping.create()
        db_dict['classification'] = details['classification']\
            if c_flag else []
        db_dict['classification_group'] = details['classification_group']\
            if cg_flag else []

        return db_dict

    def delete_classification_group(self, context, classification_group_id):
        if validators.check_can_delete_classification_group(
                context, classification_group_id):
            cg = classifications.ClassificationGroup.get_object(
                context, id=classification_group_id)
            with db_api.CONTEXT_WRITER.using(context):
                cg.delete()

    def update_classification_group(self, context, classification_group_id,
                                    fields_to_update):
        fields_to_update = fields_to_update['classification_group']
        field_keys = list(fields_to_update.keys())
        valid_keys = ['name', 'description']
        for key in field_keys:
            if key not in valid_keys:
                raise exceptions.InvalidUpdateRequest()
        with db_api.CONTEXT_WRITER.using(context):
            cg = classifications.ClassificationGroup.update_object(
                context, fields_to_update, id=classification_group_id)
        db_dict = self._make_db_dict(cg)
        return db_dict

    def _make_db_dict(self, obj):
        db_dict = {'classification_group': {}}
        for key in obj.fields.keys():
            db_dict['classification_group'][key] = obj[key]
        return db_dict

    def _make_db_dicts(self, cgs):
        db_dict = []
        for cg in cgs:
            cg_dict = self._make_db_dict(cg)
            db_dict.append(cg_dict)
        return db_dict

    def _make_c_dict(self, c_obj):
        c_dict = {'id': c_obj['id'],
                  'name': c_obj['name'],
                  'project_id': c_obj['project_id'],
                  'description': c_obj['description'],
                  'c_type': c_obj['c_type'],
                  'negated': c_obj['negated'],
                  'shared': c_obj['shared']}
        return c_dict

    def _make_c_dicts(self, c_objs):
        if not c_objs:
            return []
        ret_list = []

        for clas in c_objs:
            db_dict = self._make_c_dict(clas)
            db_dict['id'] = clas.get('id', None)
            ret_list.append(db_dict)
        return ret_list

    def get_classification_group(self, context, classification_group_id,
                                 fields=None):
        with db_api.CONTEXT_WRITER.using(context):
            cg = classifications.ClassificationGroup.get_object(
                context, id=classification_group_id)
            db_dict = self._make_db_dict(cg)
            mapped_cs = classifications._get_mapped_classifications(context,
                                                                    cg)
            mapped_cgs = classifications._get_mapped_classification_groups(
                context, cg)
            c_dict = self._make_c_dicts(mapped_cs)
            cg_dict = self._make_db_dicts(mapped_cgs)
            db_dict['classification_group']['classifications'] = c_dict
            db_dict['classification_group']['classification_groups'] = cg_dict
        return db_dict

    def get_classification_groups(self, context, sorts=None, limit=None,
                                  marker=None, page_reverse=False,
                                  filters=None, fields=None):
        pager = base_obj.Pager(sorts, limit, page_reverse, marker)
        cgs = classifications.ClassificationGroup.get_objects(context,
                                                              _pager=pager)
        db_dict = self._make_db_dicts(cgs)
        return db_dict
