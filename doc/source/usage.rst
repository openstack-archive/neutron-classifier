=====
Usage
=====

To use neutron-classifier in a project::

    import neutron_classifier


Design
------

Creating a single database table, with columns for each kind of
attribute that can be classified is not ideal, since the number 
of columns in the table will grow as more classifiers are introduced.

Instead of one table with a large number of rows, classifiers are
implemented as SQLAlchemy classes. Since there are a myriad of ways to
classify packets, an attempt was made to try and group attributes into
logical groupings (transport layer, IP layer, etc). In the database,
classifiers are implemented using `joined table inheritance`_ where
rows are inserted into the classifier table, and additional attributes
for each classifier that fit into the logical groupings (transport
layer, IP layer, etc) are inserted into the inheritance tables.

For example - a classifier that matches the following tuple 
(source_ip_prefix, destination_ip_prefix) has a row inserted in the
main 'classifiers' table, and a row inserted into the 'ip_classifiers'
table with the IP layer classification attributes.

The motivation for this is to break classifiers out into separate
tables, so adding new classifiers is as simple as creating a new table
with the specific attributes for that table. 

::

    2015-10-30 23:25:24,249 INFO sqlalchemy.engine.base.Engine BEGIN (implicit)
    2015-10-30 23:25:24,250 INFO sqlalchemy.engine.base.Engine INSERT INTO classifiers (id, classifier_type) VALUES (?, ?)
    2015-10-30 23:25:24,250 INFO sqlalchemy.engine.base.Engine ('7244cbba-03af-4a10-8995-10c75725d7c1', 'ipclassifier')
    2015-10-30 23:25:24,250 INFO sqlalchemy.engine.base.Engine INSERT INTO ip_classifiers (id, source_ip_prefix, destination_ip_prefix) VALUES (?, ?, ?)
    2015-10-30 23:25:24,250 INFO sqlalchemy.engine.base.Engine ('7244cbba-03af-4a10-8995-10c75725d7c1', 'fddf:cb3b:bc4::/48', 'fd70:fbb6:449e::/48')
    2015-10-30 23:25:24,251 INFO sqlalchemy.engine.base.Engine INSERT INTO classifier_groups (tenant_id, id, name, description, service) VALUES (?, ?, ?, ?, ?)
    2015-10-30 23:25:24,251 INFO sqlalchemy.engine.base.Engine ('bc66b697-f145-41b1-8770-5c825d205f88', '0c8c9f51-4d4b-47d9-a030-ddc3cf86418e', 'test classifier', 'ensure all data inserted correctly', 'neutron-fwaas')
    2015-10-30 23:25:24,252 INFO sqlalchemy.engine.base.Engine INSERT INTO classifier_chains (id, classifier_group_id, classifier_id, sequence) VALUES (?, ?, ?, ?)
    2015-10-30 23:25:24,252 INFO sqlalchemy.engine.base.Engine ('099a754f-1e91-42db-853d-9a385ddef39d', '0c8c9f51-4d4b-47d9-a030-ddc3cf86418e', '7244cbba-03af-4a10-8995-10c75725d7c1', 1)
    2015-10-30 23:25:24,253 INFO sqlalchemy.engine.base.Engine COMMIT


Classifier Chain
----------------

In the previous example, we created a `ClassifierGroup` that only has
a single `ClassifierChain` entry, that matches on `source_ip_prefix` and
`destination_ip_prefix`.

A more realistic example is going to be a `ClassifierGroup` that
stores multiple `ClassifierEntry` objects, that can be used to store a
`Security Group Rule`

A Security Group Rule is stored as a `ClassifierGroup` that has a
`IpClassifier` (for `source_ip_prefix` and `destination_ip_prefix`)
and a `TransportClassifier` (for source port and destination port).

::

    2015-12-01 13:09:48,122 INFO sqlalchemy.engine.base.Engine BEGIN (implicit)
    2015-12-01 13:09:48,124 INFO sqlalchemy.engine.base.Engine INSERT INTO classifier_groups (tenant_id, id, name, description, service) VALUES (?, ?, ?, ?, ?)
    2015-12-01 13:09:48,124 INFO sqlalchemy.engine.base.Engine (None, '67dca269-5d41-47de-ba4a-0aa1a6339519', None, None, 'security-group')
    2015-12-01 13:09:48,125 INFO sqlalchemy.engine.base.Engine INSERT INTO classifiers (id, classifier_type) VALUES (?, ?)
    2015-12-01 13:09:48,125 INFO sqlalchemy.engine.base.Engine ('fbf89a6c-919e-4ab2-8110-380602bc071e', 'ipclassifier')
    2015-12-01 13:09:48,126 INFO sqlalchemy.engine.base.Engine INSERT INTO classifiers (id, classifier_type) VALUES (?, ?)
    2015-12-01 13:09:48,126 INFO sqlalchemy.engine.base.Engine ('97674e2b-3765-4eba-945e-d47f5ee4924c', 'transportclassifier')
    2015-12-01 13:09:48,127 INFO sqlalchemy.engine.base.Engine INSERT INTO transport_classifiers (id, source_port_range_max, source_port_range_min, destination_port_range_max, destination_port_range_min) VALUES (?, ?, ?, ?, ?)
    2015-12-01 13:09:48,127 INFO sqlalchemy.engine.base.Engine ('97674e2b-3765-4eba-945e-d47f5ee4924c', None, None, 80, 80)
    2015-12-01 13:09:48,128 INFO sqlalchemy.engine.base.Engine INSERT INTO ip_classifiers (id, source_ip_prefix, destination_ip_prefix) VALUES (?, ?, ?)
    2015-12-01 13:09:48,128 INFO sqlalchemy.engine.base.Engine ('fbf89a6c-919e-4ab2-8110-380602bc071e', 'fddf:cb3b:bc4::/48', None)
    2015-12-01 13:09:48,130 INFO sqlalchemy.engine.base.Engine INSERT INTO classifier_chains (id, classifier_group_id, classifier_id, sequence) VALUES (?, ?, ?, ?)
    2015-12-01 13:09:48,130 INFO sqlalchemy.engine.base.Engine ('f765f038-b8fa-4369-a1ab-73d130f2c7d5', '67dca269-5d41-47de-ba4a-0aa1a6339519', 'fbf89a6c-919e-4ab2-8110-380602bc071e', 1)
    2015-12-01 13:09:48,130 INFO sqlalchemy.engine.base.Engine INSERT INTO classifier_chains (id, classifier_group_id, classifier_id, sequence) VALUES (?, ?, ?, ?)
    2015-12-01 13:09:48,130 INFO sqlalchemy.engine.base.Engine ('41ac7fb9-631a-4885-8240-2597595fefce', '67dca269-5d41-47de-ba4a-0aa1a6339519', '97674e2b-3765-4eba-945e-d47f5ee4924c', 1)
    2015-12-01 13:09:48,131 INFO sqlalchemy.engine.base.Engine COMMIT

.. _joined table inheritance: http://docs.sqlalchemy.org/en/rel_1_0/orm/extensions/declarative/inheritance.html#joined-table-inheritance
