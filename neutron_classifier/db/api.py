# Copyright (c) 2015 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from neutron_classifier.db import models


def get_classifier_chain():
    pass


def create_classifier_chain(classifier_group, classifier):
    chain = models.ClassifierChainEntry()
    chain.sequence = 1
    chain.classifier = classifier
    chain.classifier_group = classifier_group
    return chain
