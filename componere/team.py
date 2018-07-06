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
class Contact:
	name = None
	email = None

	def __init__(self, name=None, email=None):
		self.name = name
		self.email = email

	@classmethod
	def from_values_dict(cls, values_dict):
		if values_dict is None:
			return None
		name = values_dict.get("name")
		email = values_dict.get("email")
		return Contact(name, email)


class Display:
	background_color = None
	foreground_color = None

	def __init__(self, background_color=None, foreground_color=None):
		self.background_color = background_color
		self.foreground_color = foreground_color

	@classmethod
	def from_values_dict(cls, values_dict):
		if values_dict is None:
			return None
		background_color = values_dict.get("background-color")
		foreground_color = values_dict.get("foreground-color")
		return Display(background_color, foreground_color)


class Team:
	identifier = None
	name = None
	team_contact = None
	lead_contact = None
	display = None

	def __init__(
		self,
		identifier,
		name=None,
		team_contact=None,
		lead_contact=None,
		display=None
	):
		self.identifier = identifier
		self.name = name
		self.team_contact = team_contact
		self.lead_contact = lead_contact
		self.display = display

	@classmethod
	def from_values_dict(cls, identifier, values_dict):
		if values_dict is None:
			return None
		name = values_dict.get("name")
		team_contact = Contact.from_values_dict(values_dict.get("team-contact"))
		lead_contact = Contact.from_values_dict(values_dict.get("lead-contact"))
		display = Display.from_values_dict(values_dict.get("display"))
		return Team(identifier, name, team_contact, lead_contact, display)

	@classmethod
	def from_collection_dict(cls, collection_dict):
		if collection_dict is None:
			return None

		dict = {}
		for identifier, values_dict in collection_dict.iteritems():
			object = Team.from_values_dict(identifier, values_dict)
			dict[identifier] = object
		return dict
