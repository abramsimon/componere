#!/usr/bin/env python

import sys
import os


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
		_print_usage()
		print "ERROR: No arguments given"
		return 1

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
