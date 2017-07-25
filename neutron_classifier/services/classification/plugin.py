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

from neutron.db import api as db_api
from neutron.objects import base as base_obj
from neutron_classifier.common import validators
from neutron_classifier.db import classification as classification_db
from neutron_classifier.extensions import classification
from neutron_classifier.objects import classification_type as type_obj
from neutron_classifier.objects import classifications as class_group

LOG = logging.getLogger(__name__)


class ClassificationPlugin(classification.NeutronClassificationPluginBase,
                           classification_db.TrafficClassificationDbPlugin):
    supported_extension_aliases = ['neutron_classifier']

    def __init__(self):
        super(ClassificationPlugin, self).__init__()
        self.driver_manager = None

    def create_classification(self, context, classification):
        details = self.break_out_headers(classification)
        c_type = details['c_type']
        headers = classification['classification']['definition']

        for key in validators.type_validators[c_type].keys():
            if headers.get(key, None):
                for test in validators.type_validators[c_type][key]:
                    test(headers[key])
            else:
                headers[key] = None

        cl = class_group.CLASS_MAP[c_type](context, **details)
        with db_api.context_manager.writer.using(context):
            cl.create()
        db_dict = self.merge_header(cl)
        db_dict['id'] = cl['id']

        return db_dict

    def delete_classification(self, context, classification_id):
        cl = class_group.ClassificationBase.get_object(context,
                                                       id=classification_id)
        cl_class = class_group.CLASS_MAP[cl.c_type]
        classification = cl_class.get_object(context, id=classification_id)
        validators.check_valid_classifications(self, context,
                                               [classification_id])

        with db_api.context_manager.writer.using(context):
            classification.delete()

    def update_classification(self, context, classification_id,
                              classification):
        details = classification['classification']
        cl = self._get_by_id(context,
                             class_group.ClassificationBase.db_model,
                             classification_id)
        definition = {'name': details.get('name', cl.get('name')),
                      'description': details.get('description',
                                                 cl.get('description'))}
        with db_api.context_manager.writer.using(context):
            cl.update(definition)

        return self.get_classification(context, classification_id)

    def get_classification(self, context, classification_id, fields=None):
        cl = class_group.ClassificationBase.get_object(context,
                                                       id=classification_id)
        cl_class = class_group.CLASS_MAP[cl.c_type]
        classification = cl_class.get_object(context, id=classification_id)

        clas = self.merge_header(classification)
        return clas

    def get_classifications(self, context, filters=None, fields=None,
                            sorts=None, limit=None, marker=None,
                            page_reverse=False):
        c_type = filters['c_type'][0]
        pager = base_obj.Pager(sorts, limit, page_reverse, marker)
        cl = class_group.CLASS_MAP[c_type].get_objects(context,
                                                       _pager=pager, **filters)
        db_dict = self.merge_headers(cl)

        return db_dict

    def get_classification_type(self, context, filters=None, fields=None,
                                sorts=None, limit=None, marker=None,
                                page_reverse=False):
        ret_list = []
        if not filters:
            filters = {}
        for key in class_group.CLASS_MAP.keys():
            types = {}
            obj = type_obj.ClassificationType.get_object(key)
            types['type'] = obj.type
            types['supported_parameters'] = obj.supported_parameters
            ret_list.append(types)

        return ret_list

    def __getattr__(self, resource):
        return super(ClassificationPlugin, self).__getattr__(resource)

    def break_out_headers(self, classification):
        details = classification['classification']

        cl_dict = {'name': details['name'],
                   'description': details['description'],
                   'project_id': details['project_id'],
                   'shared': details['shared'],
                   'c_type': details['c_type'],
                   'negated': details['negated']}

        definition = details['definition']

        for key, value in definition.items():
            cl_dict[key] = value

        return cl_dict

    def merge_headers(self, classifications):
        ret_list = []

        for clas in classifications:
            db_dict = self.merge_header(clas)
            db_dict['id'] = clas.get('id', None)
            ret_list.append(db_dict)

        return ret_list

    def merge_header(self, classification):
        db_dict = {'id': classification['id'],
                   'name': classification['name'],
                   'project_id': classification['project_id'],
                   'description': classification['description'],
                   'c_type': classification['c_type'],
                   'negated': classification['negated'],
                   'shared': classification['shared']}

        c_type = classification['c_type']
        headers = validators.type_validators[c_type].keys()
        definition = {}

        for header in headers:
            definition[header] = classification.get(header, None)

        db_dict['definition'] = definition
        return db_dict
