#!/usr/bin/env python

import sys
import os
import load_input
import generate_detail
import generate_overview
import generate_area

def _print_usage():
	print "Usage:"
	print "  generate.py detail <directory>"
	print "    Generates a Detail Diagram detail.png and detail.html into the <directory>"
	print "  generate.py overview <level_order> <directory>"
	print "    Generates an Overview diagram overview.png and overview.html into the <directory>"
	print "  generate.py area <area> <directory>"
	print "    Generates an Area diagram <area>.png and <area>.html into the <directory>"
	print "  generate.py areas <directory>"
	print "    Generates all Area diagrams areas.png and area.html into the <directory> and every area"
	print "    into <directory>/areas/<area>.png <area>.html"
	print "  generate.py all <directory>"
	print "    Invokes detail, overview, areas all to the <directory>"


def _main(argv=sys.argv[1:]):
	if len(argv) < 1:
		return _main(["all", "wiki"])

	command = argv[0]

	valid_commands = ["detail", "overview", "areas", "all", "area"]
	if command not in valid_commands:
		_print_usage()
		print "ERROR: Command not one of {0}".format(valid_commands)
		return 2

	directory = None
	def_directory = "system/"
	areas_file = def_directory + "areas.yaml"
	components_file = def_directory + "components.yaml"
	levels_file = def_directory + "levels.yaml"
	teams_file = def_directory + "teams.yaml"

	if command in ["detail", "areas", "all"]:
		if len(argv) != 2:
			_print_usage()
			print "ERROR: Output directory not given"
			return 3
		directory = argv[1]

	level_order = 50
	if command == "overview":
		if len(argv) < 2:
			_print_usage()
			print "ERROR: Output directory not given"
			return 3
		if len(argv) == 3 and argv[1].isdigit():
			level_order = int(argv[1])
		directory = argv[len(argv) - 1]

	area = None
	if command == "area":
		if len(argv) != 3:
			_print_usage()
			print "ERROR: Area and/or directory not given"
			return 4
		area = argv[1]
		directory = argv[2]

	if not os.path.isdir(directory):
		os.mkdir(directory)

	areas = load_input.load_areas(areas_file)
	components = load_input.load_components(components_file)
	teams = load_input.load_teams(teams_file)

	if command in ["detail", "all"]:
		generate_detail.build_detail_digraph(
			"Detail",
			directory + "/detail",
			areas,
			components,
			teams
		)

	if command in ["overview", "all"]:
		generate_overview.build_overview_digraph(
			"Overview",
			directory + "/overview",
			areas,
			components,
			load_input.load_levels(levels_file),
			teams,
			level_order
		)

	if command in ["area", "areas", "all"]:
		generate_area.build_area_digraph(
			directory + "/areas/",
			areas,
			components,
			teams,
			area
		)

	return 0


if __name__ == "__main__":
	sys.exit(_main(sys.argv[1:]))
