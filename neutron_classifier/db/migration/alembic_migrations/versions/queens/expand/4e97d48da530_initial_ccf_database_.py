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
Create Date: 2017-08-28 14:14:31.181166

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
        sa.Column('name', sa.String(length=255)),
        sa.Column('description', sa.String(length=255)),
        sa.Column('project_id', sa.String(length=255),
                  index=True),
        sa.Column('shared', sa.Boolean(), nullable=False),
        sa.Column('operator', sa.Enum("AND", "OR", name="operator_types"),
                  nullable=False))

    op.create_table(
        'classifications',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('c_type', sa.String(length=36)),
        sa.Column('name', sa.String(length=255)),
        sa.Column('description', sa.String(length=255)),
        sa.Column('negated', sa.Boolean(), nullable=True),
        sa.Column('shared', sa.Boolean(), nullable=True),
        sa.Column('project_id', sa.String(length=255),
                  index=True))

    op.create_table(
        'classification_group_to_classification_mappings',
        sa.Column('container_cg_id', sa.String(length=36), sa.ForeignKey(
                  "classification_groups.id"), primary_key=True),
        sa.Column('stored_classification_id', sa.String(length=36),
                  sa.ForeignKey("classifications.id"), primary_key=True))

    op.create_table(
        'classification_group_to_cg_mappings',
        sa.Column('container_cg_id', sa.String(length=36), sa.ForeignKey(
                  "classification_groups.id"), primary_key=True),
        sa.Column('stored_cg_id', sa.String(length=36), sa.ForeignKey(
                  "classification_groups.id"), primary_key=True))

    op.create_table(
        'ipv4_classifications',
        sa.Column('id', sa.String(length=36), sa.ForeignKey(
                  "classifications.id"), primary_key=True),
        sa.Column('dscp', sa.Integer()),
        sa.Column('dscp_mask', sa.Integer()),
        sa.Column('ecn', sa.Enum("0", "1", "2", "3", name="ecn_types")),
        sa.Column('length_min', sa.Integer()),
        sa.Column('length_max', sa.Integer()),
        sa.Column('flags', sa.Integer()),
        sa.Column('flags_mask', sa.Integer()),
        sa.Column('ttl_min', sa.SmallInteger()),
        sa.Column('ttl_max', sa.SmallInteger()),
        sa.Column('protocol', sa.Integer()),
        sa.Column('src_addr', sa.String(length=19)),
        sa.Column('dst_addr', sa.String(length=19)))

    op.create_table(
        'ipv6_classifications',
        sa.Column('id', sa.String(length=36), sa.ForeignKey(
                  "classifications.id"), primary_key=True),
        sa.Column('dscp', sa.Integer()),
        sa.Column('dscp_mask', sa.Integer()),
        sa.Column('ecn', sa.Enum("0", "1", "2", "3", name="ecn_types")),
        sa.Column('length_min', sa.Integer()),
        sa.Column('length_max', sa.Integer()),
        sa.Column('next_header', sa.Integer()),
        sa.Column('hops_min', sa.SmallInteger()),
        sa.Column('hops_max', sa.SmallInteger()),
        sa.Column('src_addr', sa.String(length=49)),
        sa.Column('dst_addr', sa.String(length=49)))

    op.create_table(
        'ethernet_classifications',
        sa.Column('id', sa.String(length=36), sa.ForeignKey(
                  "classifications.id"), primary_key=True),
        sa.Column('ethertype', sa.Integer()),
        sa.Column('src_addr', sa.String(length=17)),
        sa.Column('dst_addr', sa.String(length=17)))

    op.create_table(
        'udp_classifications',
        sa.Column('id', sa.String(length=36), sa.ForeignKey(
                  "classifications.id"), primary_key=True),
        sa.Column('src_port_min', sa.Integer()),
        sa.Column('src_port_max', sa.Integer()),
        sa.Column('dst_port_min', sa.Integer()),
        sa.Column('dst_port_max', sa.Integer()),
        sa.Column('length_min', sa.Integer()),
        sa.Column('length_max', sa.Integer()))

    op.create_table(
        'tcp_classifications',
        sa.Column('id', sa.String(length=36), sa.ForeignKey(
                  "classifications.id"), primary_key=True),
        sa.Column('src_port_min', sa.Integer()),
        sa.Column('src_port_max', sa.Integer()),
        sa.Column('dst_port_min', sa.Integer()),
        sa.Column('dst_port_max', sa.Integer()),
        sa.Column('window_min', sa.Integer()),
        sa.Column('window_max', sa.Integer()),
        sa.Column('flags', sa.Integer()),
        sa.Column('flags_mask', sa.Integer()))
