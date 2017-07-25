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
#

"""initial CCF database expansion

Revision ID: 4e97d48da530
Revises: None
Create Date: 2017-02-08 14:14:31.181166

"""

# revision identifiers, used by Alembic.
from alembic import op
import sqlalchemy as sa

revision = '4e97d48da530'
down_revision = 'start_neutron_classifier'


def upgrade():
    op.create_table(
        'classification_groups',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('name', sa.String(length=36)),
        sa.Column('description', sa.String(length=255)),
        sa.Column('project_id', sa.String(length=255),
                  index=True),
        sa.Column('shared', sa.Boolean(), nullable=False),
        sa.Column('operator', sa.String(length=4), nullable=False),
        sa.Column('cg_id', sa.String(length=36)))

    op.create_table(
        'classification_groups_mapping',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('cg_id', sa.String(length=36)),
        sa.Column('classification_id', sa.String(length=36)))

    op.create_table(
        'classifications',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('c_type', sa.String(length=36)),
        sa.Column('name', sa.String(length=36)),
        sa.Column('description', sa.String(length=255)),
        sa.Column('negated', sa.Boolean(), nullable=True),
        sa.Column('shared', sa.Boolean(), nullable=True),
        sa.Column('project_id', sa.String(length=255),
                  index=True))

    op.create_table(
        'ipv4_classifications',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('c_type', sa.String(length=36)),
        sa.Column('name', sa.String(length=36)),
        sa.Column('description', sa.String(length=255)),
        sa.Column('ihl', sa.Integer()),
        sa.Column('diffserv', sa.Integer()),
        sa.Column('diffserv_mask', sa.Integer()),
        sa.Column('length', sa.Integer()),
        sa.Column('flags', sa.Integer()),
        sa.Column('flags_mask', sa.Integer()),
        sa.Column('ttl', sa.Integer()),
        sa.Column('protocol', sa.Integer()),
        sa.Column('src_addr', sa.String(length=36)),
        sa.Column('dst_addr', sa.String(length=36)),
        sa.Column('options', sa.Integer()),
        sa.Column('options_mask', sa.Integer()))

    op.create_table(
        'ipv6_classifications',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('c_type', sa.String(length=36)),
        sa.Column('name', sa.String(length=36)),
        sa.Column('description', sa.String(length=255)),
        sa.Column('traffic_class', sa.Integer()),
        sa.Column('traffic_class_mask', sa.Integer()),
        sa.Column('length', sa.Integer()),
        sa.Column('next_header', sa.Integer()),
        sa.Column('hops', sa.Integer()),
        sa.Column('src_addr', sa.String(length=36)),
        sa.Column('dst_addr', sa.String(length=36)))

    op.create_table(
        'ethernet_classifications',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('c_type', sa.String(length=36)),
        sa.Column('name', sa.String(length=36)),
        sa.Column('description', sa.String(length=255)),
        sa.Column('preamble', sa.Integer()),
        sa.Column('ethertype', sa.Integer()),
        sa.Column('src_addr', sa.String(length=36)),
        sa.Column('dst_addr', sa.String(length=36)))

    op.create_table(
        'udp_classifications',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('c_type', sa.String(length=36)),
        sa.Column('name', sa.String(length=36)),
        sa.Column('description', sa.String(length=255)),
        sa.Column('src_port', sa.String(length=36)),
        sa.Column('dst_port', sa.String(length=36)),
        sa.Column('length', sa.Integer()),
        sa.Column('window_size', sa.Integer()))

    op.create_table(
        'tcp_classifications',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('c_type', sa.String(length=36)),
        sa.Column('name', sa.String(length=36)),
        sa.Column('description', sa.String(length=255)),
        sa.Column('src_port', sa.String(length=36)),
        sa.Column('dst_port', sa.String(length=36)),
        sa.Column('flags', sa.Integer()),
        sa.Column('flags_mask', sa.Integer()),
        sa.Column('window', sa.Integer()),
        sa.Column('data_offset', sa.Integer()),
        sa.Column('option_kind', sa.Integer()))
