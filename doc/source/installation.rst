============
Installation
============

At the command line::

    $ pip install neutron-classifier

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv neutron-classifier
    $ pip install neutron-classifier




Database Installation
---------------------

This library will use the `branches`_ feature of Alembic, so that
consumers of this library will have the schema for the classifiers
automatically installed as part of the migration. Hopefully.

.. _branches: http://alembic.readthedocs.org/en/latest/branches.html?highlight=branches
