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


class Component:
    identifier = None
    name = None
    level_identifier = None
    type_identifier = None
    team_identifier = None
    area_identifier = None
    description = None
    shape = None
    git = None
    release_date = None
    dependency_identifiers = None

    def __init__(
        self,
        identifier,
        name=None,
        level_identifier=None,
        type_identifier=None,
        team_identifier=None,
        area_identifier=None,
        description=None,
        shape=None,
        git=None,
        release_date=None,
        dependency_identifiers=None
    ):
        self.identifier = identifier
        self.name = name
        self.level_identifier = level_identifier
        self.type_identifier = type_identifier
        self.team_identifier = team_identifier
        self.area_identifier = area_identifier
        self.description = description
        self.shape = shape
        self.git = git
        self.release_date = release_date
        self.dependency_identifiers = dependency_identifiers

    @classmethod
    def from_values_dict(cls, identifier, values_dict):
        if values_dict is None:
            return None
        name = values_dict.get("name")
        level = values_dict.get("level")
        type_identifier = values_dict.get("type")
        team_identifier = values_dict.get("team")
        area_identifier = values_dict.get("area")
        description = values_dict.get("description")
        shape = values_dict.get("shape")
        git = values_dict.get("git")
        release_date = values_dict.get("release-date")
        dependency_identifiers = values_dict.get("dependencies")

        return Component(
            identifier,
            name,
            level,
            type_identifier,
            team_identifier,
            area_identifier,
            description,
            shape,
            git,
            release_date,
            dependency_identifiers
        )

    @classmethod
    def from_collection_dict(cls, collection_dict):
        if collection_dict is None:
            return None

        dict = {}
        for identifier, values_dict in collection_dict.iteritems():
            object = Component.from_values_dict(identifier, values_dict)
            dict[identifier] = object
        return dict
