# Copyright 2017 Intel. All rights reserved.
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

from neutron.db import rbac_db_models
from neutron_lib.db import model_base


class ClassificationGroupRBAC(rbac_db_models.RBACColumns, model_base.BASEV2):
    """RBAC table for classification groups."""

    object_id = rbac_db_models._object_id_column('classification_groups.id')
    object_type = 'classification_group'

    def get_valid_actions(self):
        return (rbac_db_models.ACCESS_SHARED, rbac_db_models.rbac_db_models, )
