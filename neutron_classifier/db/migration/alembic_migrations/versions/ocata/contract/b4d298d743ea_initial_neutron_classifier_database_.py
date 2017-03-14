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
#

"""initial neutron classifier database contraction

Revision ID: b4d298d743ea
Revises: None
Create Date: 2017-02-08 14:14:31.181166

"""

# revision identifiers, used by Alembic.
from neutron.db.migration import cli

revision = 'b4d298d743ea'
#down_revision = None
down_revision = 'start_neutron_classifier'
#branch_labels = (cli.CONTRACT_BRANCH,)


def upgrade():
    pass
