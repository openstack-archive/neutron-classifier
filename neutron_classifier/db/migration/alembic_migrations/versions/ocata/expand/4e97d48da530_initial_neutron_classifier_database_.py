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

"""initial neutron classifier database expansion

Revision ID: 4e97d48da530
Revises: None
Create Date: 2017-02-08 14:14:31.181166

"""

# revision identifiers, used by Alembic.
from alembic import op
import sqlalchemy as sa

revision = '4e97d48da530'
#down_revision = None
down_revision = 'start_neutron_classifier'
#branch_labels = (cli.EXPAND_BRANCH,)


def upgrade():
    op.create_table(
        'classification_groups',
        sa.Column('group_id', sa.String(length=36), primary_key=True),
        sa.Column('name', sa.String(length=255)),
        sa.Column('description', sa.String(length=255)),
        sa.Column('shared', sa.Boolean(), nullable=False),
        sa.Column('tenant_id', sa.String(length=255),
                  index=True))

    op.create_table(
        'classifications',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('classification_type', sa.String(length=36)),
        sa.Column('name', sa.String(length=32)),
        sa.Column('description', sa.String(length=255)))

    op.create_table(
        'ipv4_classifications',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('classification_type', sa.String(length=36)),
        sa.Column('name', sa.String(length=32)),
        sa.Column('description', sa.String(length=255)),
        sa.Column('dscp', sa.String(length=32)),
        sa.Column('dscp_mask', sa.String(length=32)),
        sa.Column('ecn', sa.String(length=32)),
        sa.Column('ecn_mask', sa.String(length=32)),
        sa.Column('protocol', sa.String(length=32)),
        sa.Column('protocol_mask', sa.String(length=32)),
        sa.Column('source_address', sa.String(length=32)),
        sa.Column('source_address_range', sa.String(length=32)),
        sa.Column('destination_address', sa.String(length=32)),
        sa.Column('destination_address_range', sa.String(length=32)))

    op.create_table(
        'ipv6_classifications',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('classification_type', sa.String(length=36)),
        sa.Column('name', sa.String(length=32)),
        sa.Column('description', sa.String(length=255)),
        sa.Column('traffic_class', sa.String(length=32)),
        sa.Column('traffic_class_mask', sa.String(length=32)),
        sa.Column('next_header', sa.String(length=32)),
        sa.Column('next_header_mask', sa.String(length=32)),
        sa.Column('flow_label', sa.String(length=32)),
        sa.Column('flow_label_mask', sa.String(length=32)),
        sa.Column('source_address', sa.String(length=32)),
        sa.Column('source_address_range', sa.String(length=32)),
        sa.Column('destination_address', sa.String(length=32)),
        sa.Column('destination_address_range', sa.String(length=32)))

    op.create_table(
        'neutron_classifications',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('classification_type', sa.String(length=36)),
        sa.Column('name', sa.String(length=32)),
        sa.Column('description', sa.String(length=255)),
        sa.Column('source_port', sa.String(length=32)),
        sa.Column('destination_port', sa.String(length=32)),
        sa.Column('source_subnet', sa.String(length=32)),
        sa.Column('destination_subnet', sa.String(length=32)),
        sa.Column('source_network', sa.String(length=32)),
        sa.Column('destination_network', sa.String(length=32)))

    op.create_table(
        'ethernet_classifications',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('classification_type', sa.String(length=36)),
        sa.Column('name', sa.String(length=32)),
        sa.Column('description', sa.String(length=255)),
        sa.Column('type', sa.String(length=32)),
        sa.Column('source_mac', sa.String(length=32)),
        sa.Column('destination_mac', sa.String(length=32)),
        sa.Column('source_mac_range', sa.String(length=32)),
        sa.Column('destination_mac_range', sa.String(length=32)))

    op.create_table(
        'port_classifications',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('classification_type', sa.String(length=36)),
        sa.Column('name', sa.String(length=32)),
        sa.Column('description', sa.String(length=255)),
        sa.Column('source_port', sa.String(length=32)),
        sa.Column('destination_port', sa.String(length=32)),
        sa.Column('source_port_min_range', sa.String(length=32)),
        sa.Column('destination_port_min_range', sa.String(length=32)),
        sa.Column('source_port_max_range', sa.String(length=32)),
        sa.Column('destination_port_max_range', sa.String(length=32)))
