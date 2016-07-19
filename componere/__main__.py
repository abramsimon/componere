#!/usr/bin/env python
"""
componere:
Usage:
    componere <input> (--detail | --overview=<level> | --area=<area-name>| --areas | --all)... <output>
    componere --i=<input> --o=<output> (--detail | --overview=<level> | --area=<area-name> |  --areas | --all)...
    componere -h | --help

Arguments:
    <input>         Input directory containing the yaml files.
    <output>        Output directory will contain output png files.

Options:
    -h--help            Show help page.
    --i=<input>         Input directory containing the comp files
                        or path of an only one input comp file.
    --o=<output>        Output directory will contain output .png files.
    --detail            Generates a Detail diagram detail.png into the <output>
    --overview=<level>  Generates a Overview diagram level_<level>.png into the <output>/overview
                        has all componets, that their level is higher than or equal to <level>.
    --area=<area-name>  Generates an Area diagram <area-name>.png into the <output>/area.
    --areas             Generates all Areas diagrams "each-area-name".png into the <output>/area.
    --all               Generates all diagrams (detail, overview <level = 50>, and all areas)
                        into the <output>.

Examples:
    componere ./system/input.comp --detail --overview ./wiki
    componere --i=./system --detail  --o=./wiki --overview
    componere --i=./system --area=platforn --area=application --o=./wiki
    componere --i=./system --area=platforn --o=./wiki --all    #--all will dominate
"""

import sys
import os
import load_input
import generate_detail
import generate_overview
import generate_area
from docopt import docopt


def _main(argv=sys.argv[1:]):
	arguments = docopt(__doc__, argv)
	input_path = arguments['--i'] if arguments['--i'] is not None else arguments['<input>']
	output_directory = arguments['--o'] if arguments['--i'] is not None else arguments['<output>']

	areas = {}
	components = {}
	levels = {}
	teams = {}

	load_input.load_objects(input_path, areas, components, levels, teams)

	if not os.path.isdir(output_directory):
		os.mkdir(output_directory)

	all_commands = arguments['--all']
	detail_commands = arguments['--detail']
	areas_commands = arguments['--areas']
	area_commands = set(arguments['--area'])
	overview_commands = set(arguments['--overview'])

	if all_commands != 0:
		detail_commands = 1
		overview_commands.add(50)

	if areas_commands != 0 or all_commands != 0:
		area_commands.clear()
		area_commands.add(None)

	if detail_commands > 0:
		generate_detail.build_detail_digraph(
			"Detail",
			output_directory + "/detail",
			areas,
			components,
			teams
		)

	if len(overview_commands) != 0:
		for level_order in overview_commands:
			generate_overview.build_overview_digraph(
				"Overview",
				output_directory + "/overview/",
				areas,
				components,
				levels,
				teams,
				int(level_order)
			)

	if len(overview_commands) != 0:
		for area in area_commands:
			generate_area.build_area_digraph(
				output_directory + "/areas/",
				areas,
				components,
				teams,
				area
			)

	return 0

if __name__ == "__main__":
	sys.exit(_main(sys.argv[1:]))
