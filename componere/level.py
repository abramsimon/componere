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
class Level:
    identifier = None
    order = None
    name = None

    def __init__(self, identifier, order=None, name=None):
        self.identifier = identifier
        self.order = order
        self.name = name

    @classmethod
    def from_values_dict(cls, identifier, values_dict):
    	if values_dict is None:
    		return None
    	order = values_dict.get("order")
    	name = values_dict.get("name")
    	return Level(identifier, order, name)

    @classmethod
    def from_collection_dict(cls, collection_dict):
    	if collection_dict is None:
    		return None

    	dict = {}
    	for identifier, values_dict in collection_dict.iteritems():
    		object = Level.from_values_dict(identifier, values_dict)
    		dict[identifier] = object
    	return dict
