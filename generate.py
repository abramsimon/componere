#!/usr/bin/env python

import sys
import os
import yaml
import datetime

class Area:
	identifier = None
	name = None
	parent_identifier = None

	def __init__(self, identifier, name=None, parent_identifier=None):
		self.identifier = identifier
		self.name = name
		self.parent_identifier = parent_identifier

	@classmethod
	def from_values_dict(cls, identifier, values_dict):
		if values_dict is None:
			return None
		identifier = identifier
		name = values_dict.get("name")
		parent_identifier = values_dict.get("parent")
		return Area(identifier, name, parent_identifier)

	@classmethod
	def from_collection_dict(cls, collection_dict):
		if collection_dict is None:
			return None

		dict = {}
		for identifier, values_dict in collection_dict.iteritems():
			object = Area.from_values_dict(identifier, values_dict)
			dict[identifier] = object
		return dict


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

	def __init__(self, identifier, name=None, team_contact=None, lead_contact=None, display=None):
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

class Component:
	identifier = None
	name = None
	level_identifier = None
	type = None
	team_identifier = None
	area_identifier = None
	description = None
	git = None
	release_date = None
	dependency_identifiers = None

	def __init__(self, identifier, name=None, level_identifier=None, type=None, team_identifier=None,
			area_identifier=None, description=None, git=None, release_date=None, dependency_identifiers=None):
		self.identifier = identifier
		self.name = name
		self.level_identifier = level_identifier
		self.type = type
		self.team_identifier = team_identifier
		self.area_identifier = area_identifier
		self.description = description
		self.git = git
		self.release_date = release_date
		self.dependency_identifiers = dependency_identifiers

	@classmethod
	def from_values_dict(cls, identifier, values_dict):
		if values_dict is None:
			return None
		name = values_dict.get("name")
		level = values_dict.get("level")
		type = values_dict.get("type")
		team_identifier = values_dict.get("team")
		area_identifier = values_dict.get("area")
		description = values_dict.get("description")
		git = values_dict.get("git")
		release_date = values_dict.get("release-date")
		dependency_identifiers = values_dict.get("dependencies")

		return Component(identifier, name, level, type, team_identifier, area_identifier, description, git,
			release_date, dependency_identifiers)

	@classmethod
	def from_collection_dict(cls, collection_dict):
		if collection_dict is None:
			return None

		dict = {}
		for identifier, values_dict in collection_dict.iteritems():
			object = Component.from_values_dict(identifier, values_dict)
			dict[identifier] = object
		return dict


def _load_areas(file):
	if not os.path.isfile(file):
		raise Exception("File {0} is not found".format(file))

	file = open(file)
	areas_dict = yaml.safe_load(file)
	file.close()

	if areas_dict is None:
		return None

	return Area.from_collection_dict(areas_dict)


def _load_levels(file):
	if not os.path.isfile(file):
		raise Exception("File {0} is not found".format(file))

	file = open(file)
	dict = yaml.safe_load(file)
	file.close()

	if dict is None:
		return None

	return Level.from_collection_dict(dict)


def _load_teams(file):
	if not os.path.isfile(file):
		raise Exception("File {0} is not found".format(file))

	file = open(file)
	dict = yaml.safe_load(file)
	file.close()

	if dict is None:
		return None

	return Team.from_collection_dict(dict)


def _load_components(file):
	if not os.path.isfile(file):
		raise Exception("File {0} is not found".format(file))

	file = open(file)
	dict = yaml.safe_load(file)
	file.close()

	if dict is None:
		return None

	return Component.from_collection_dict(dict)


def _print_usage():
	print "Usage:"
	print "  generate.py detail <directory>"
	print "    Generates a Detail Diagram detail.png and detail.html into the <directory>"
	print "  generate.py overview <directory>"
	print "    Generates an Overview diagram overview.png and overview.html into the <directory>"
	print "  generate.py area <area> <directory>"
	print "    Generates an Area diagram <area>.png and <area>.html into the <directory>"
	print "  generate.py areas <directory>"
	print "    Generates all Area diagrams areas.png and area.html into the <directory> and every area"
	print "    into <directory>/areas/<area>.png <area>.html"
	print "  generate.py all <directory>"
	print "    Invokes bad, overview, areas all to the <directory>"


def _main(argv):
	if len(argv) < 1:
		return _main(["all", "wiki"])

	command = argv[0]

	valid_commands = ["detail", "overview", "areas", "all", "area"]
	if command not in valid_commands:
		_print_usage()
		print "ERROR: Command not one of {0}".format(valid_commands)
		return 2

	directory = None

	if command in ["detail", "overview", "areas", "all"]:
		if len(argv) != 2:
			_print_usage()
			print "ERROR: Output directory not given"
			return 3
		directory = argv[1]

	area = None
	if command == "area":
		if len(argv) != 3:
			_print_usage()
			print "ERROR: Area and/or directory not given"
			return 4
		area = argv[1]
		directory = argv[2]

	if not os.path.isdir(directory):
		_print_usage()
		print "ERROR: {0} does not exist or is not a directory".format(directory)
		return 5

	return 0


if __name__ == "__main__":
	sys.exit(_main(sys.argv[1:]))
