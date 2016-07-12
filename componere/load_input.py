import os
import yaml
from area import Area
from component import Component
from team import Team
from level import Level


def load_components(file):
	if not os.path.isfile(file):
		raise Exception("File {0} is not found".format(file))

	file = open(file)
	dict = yaml.safe_load(file)
	file.close()

	if dict is None:
		return None

	return Component.from_collection_dict(dict)


def load_teams(file):
	if not os.path.isfile(file):
		raise Exception("File {0} is not found".format(file))

	file = open(file)
	dict = yaml.safe_load(file)
	file.close()

	if dict is None:
		return None

	return Team.from_collection_dict(dict)


def load_levels(file):
	if not os.path.isfile(file):
		raise Exception("File {0} is not found".format(file))

	file = open(file)
	dict = yaml.safe_load(file)
	file.close()

	if dict is None:
		return None

	return Level.from_collection_dict(dict)


def load_areas(file):
	if not os.path.isfile(file):
		raise Exception("File {0} is not found".format(file))

	file = open(file)
	areas_dict = yaml.safe_load(file)
	file.close()

	if areas_dict is None:
		return None

	return Area.from_collection_dict(areas_dict)
