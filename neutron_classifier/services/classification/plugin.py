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

from neutron.common import rpc as n_rpc
from neutron.db import api as db_api
from neutron.objects import base as base_obj
from neutron_classifier.common import validators
from neutron_classifier.db import classification as classification_db
from neutron_classifier.extensions import classification
from neutron_classifier.objects import classifications as class_group
from neutron_classifier.objects import rpc_api
from neutron_classifier.services.classification.drivers import rpc

LOG = logging.getLogger(__name__)


class ClassificationPlugin(classification.NeutronClassificationPluginBase,
                           classification_db.TrafficClassificationDbPlugin):
    supported_extension_aliases = ['neutron_classifier']

    def __init__(self):
        super(ClassificationPlugin, self).__init__()
        self.driver_manager = None
        self._setup_rpc()

    def _setup_rpc(self):
        # Setup a rpc server
        self.topic = rpc_api.CLASSIFICATION_TOPIC
        self.endpoints = [rpc.ClassificationRpcCallback(self)]
        self.conn = n_rpc.create_connection()
        self.conn.create_consumer(self.topic, self.endpoints, fanout=False)
        self.conn.consume_in_threads()

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
        db_dict = self.merge_header(cl, c_type)
        db_dict['id'] = cl['id']

        return db_dict

    def delete_classification(self, context, classification_id):
        cl = class_group.ClassificationBase.get_object(context,
                                                       id=classification_id)
        cl_class = class_group.CLASS_MAP[cl.c_type]
        classification = cl_class.get_object(context, id=classification_id)

        with db_api.context_manager.writer.using(context):
            classification.delete()

    def update_classification(self, context, classification_id,
                              classification):
        details = classification['classification']
        cl = self._get_by_id(context,
                             class_group.ClassificationBase.db_model,
                             classification_id)
        for key, value in details.items():
            if(key != 'name' and key != 'description'):
                details.pop(key)
            elif(value == ''):
                details[key] = cl.get(key)
        with db_api.context_manager.writer.using(context):
            cl.update(details)

        return self.get_classification(context, classification_id)

    def get_classification(self, context, classification_id, fields=None):
        cl = class_group.ClassificationBase.get_object(context,
                                                       id=classification_id)
        cl_class = class_group.CLASS_MAP[cl.c_type]
        classification = cl_class.get_object(context, id=classification_id)

        clas = self.merge_header(classification, cl.c_type)
        return clas

    def get_classifications(self, context, filters=None, fields=None,
                            sorts=None, limit=None, marker=None,
                            page_reverse=False):
        c_type = filters['c_type'][0]
        pager = base_obj.Pager(sorts, limit, page_reverse, marker)
        cl = class_group.CLASS_MAP[c_type].get_objects(context,
                                                       _pager=pager, **filters)
        db_dict = self.merge_headers(cl, c_type)
        return db_dict

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

    def merge_headers(self, classifications, c_type):
        ret_list = []

        for clas in classifications:
            db_dict = self.merge_header(clas, c_type)
            db_dict['id'] = clas.get('id', None)
            ret_list.append(db_dict)

        return ret_list

    def merge_header(self, classification, c_type):
        db_dict = {'name': classification['name'],
                   'project_id': classification['project_id'],
                   'description': classification['description'],
                   'c_type': classification['c_type'],
                   'negated': classification['negated'],
                   'shared': classification['shared']}

        headers = validators.type_validators[c_type].keys()
        definition = {}
        for key, value in classification.items():
            for header in headers:
                if key == header:
                    definition[key] = value
                    headers.remove(header)
                else:
                    definition[header] = None

        db_dict['definition'] = definition
        return db_dict
