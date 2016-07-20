import os
import yaml
from area import Area
from component import Component
from team import Team
from level import Level

def load_file(file, areas, components, levels, teams):
	file = open(file)
	dict = yaml.safe_load(file)
	file.close()

	if dict is None:
		return
	for identifier, values_dict in dict.iteritems():
		if identifier == "areas":
			areas.update(Area.from_collection_dict(values_dict))
		elif identifier == "components":
			components.update(Component.from_collection_dict(values_dict))
		elif identifier == "levels":
			levels.update(Level.from_collection_dict(values_dict))
		elif identifier == "teams":
			teams.update(Team.from_collection_dict(values_dict))
		else:
			print "Undefined identifier %s" % identifier

def load_objects(path, areas, components, levels, teams):
	if os.path.isfile(path) and path.endswith(".comp"):
		load_file(path, areas, components, levels, teams)
	elif os.path.isdir(path):
		for tup in os.walk(path, topdown=True):
			for name in tup[2]:
				file = os.path.join(tup[0], name)
				if file.endswith(".comp"):
					load_file(file, areas, components, levels, teams)
	else:
		raise Exception("Invalid File/Directory {0}".format(path))