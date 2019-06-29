# Copyright 2o18 Premise Data
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class Type:
    identifier = None
    name = None
    description = None
    shape = None

    def __init__(self, identifier, name=None, description=None, shape=None):
        self.identifier = identifier
        self.name = name
        self.description = description
        self.shape = shape

    @classmethod
    def from_values_dict(cls, identifier, values_dict):
        if values_dict is None:
            return None
        name = values_dict.get("name")
        description = values_dict.get("description")
        shape = values_dict.get("shape")
        return Type(identifier, name, description, shape)

    @classmethod
    def from_collection_dict(cls, collection_dict):
        if collection_dict is None:
            return None

        dict = {}
        for identifier, values_dict in collection_dict.iteritems():
            object = Type.from_values_dict(identifier, values_dict)
            dict[identifier] = object
        return dict
