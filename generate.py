#!/usr/bin/env python

import sys
import os
import yaml


class Area:
	identifier = None
	name = None
	parent_identifier = None

	def __init__(self, identifier, name=None, parent_identifier=None):
		self.identifier = identifier
		self.name = name
		self.parent_identifier = parent_identifier

	@classmethod
	def from_values_dict(cls, identifer, values_dict):
		identifier = identifer
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
