#!/usr/bin/env python
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

def write_contact_to_file(file, list_name, contact):
	if contact is None:
		return
	file.write("* {0}:\n".format(list_name))
	if contact.name is not None:
		file.write("  * Name: {0}\n".format(contact.name))
	if contact.email is not None:
		file.write("  * Email: {0}\n".format(contact.email))

def write_components_sublist_to_file(file, list_name, sublist, components):
	if sublist is None:
		return
	file.write("* {0}:\n".format(list_name))
	for item in sorted(sublist):
		file.write("  * [{0}]({1}.md)\n".format(components[item].name, item))

def create_wiki(areas, components, levels, teams):
	if not os.path.isdir("wiki"):
		os.mkdir("wiki")

	file = open("wiki/README.md", "w")

	if not os.path.isdir("wiki/teams"):
		os.mkdir("wiki/teams")

	file.write("## Teams\n")
	for team in sorted(teams):
		obj = teams[team]
		team_file = open("wiki/teams/{0}.md".format(obj.identifier), "w")
		team_file.write("# {0}\n".format(obj.name))
		write_contact_to_file(team_file, "Team Contact", obj.team_contact)
		write_contact_to_file(team_file, "Lead Contact", obj.lead_contact)
		team_file.close()
		file.write("* [{0}](teams/{1}.md)\n".format(obj.name, obj.identifier))

	if not os.path.isdir("wiki/components"):
		os.mkdir("wiki/components")

	depends_on = {}
	for component in components:
		dependents = components[component].dependency_identifiers
		if dependents is not None:
			for dependent in dependents:
				if not dependent in depends_on:
					depends_on[dependent] = []
				depends_on[dependent].append(component)

	file.write("\n## Components\n")
	for component in sorted(components):
		obj = components[component]
		comp_file = open("wiki/components/{0}.md".format(obj.identifier), "w")
		comp_file.write("# {0}\n".format(obj.name))
		if obj.description is not None:
			comp_file.write("### {0}\n".format(obj.description))
		if obj.git is not None:
			comp_file.write("* Git: {0}\n".format(obj.git))
		if obj.release_date is not None:
			comp_file.write("* Release Date: {0}\n".format(obj.release_date))
		if obj.team_identifier is not None:
			team_name = teams[obj.team_identifier].name
			comp_file.write(
				"* Team: [{0}](../teams/{1}.md)\n".format(team_name, obj.team_identifier)
			)
		if obj.type is not None:
			comp_file.write("* Type: {0}\n".format(obj.type))
		if obj.level_identifier is not None:
			comp_file.write("* Level: {0}\n".format(levels[obj.level_identifier].name))
		if obj.area_identifier is not None:
			comp_file.write("* Area: [{0}](../areas/{1}.png)\n".format(
				areas[obj.area_identifier].name, obj.area_identifier
			))
		write_components_sublist_to_file(
			comp_file, "Dependents", obj.dependency_identifiers, components
		)
		write_components_sublist_to_file(
			comp_file, "Depends On", depends_on.get(component), components
		)
		comp_file.close()
		file.write("* [{0}](components/{1}.md)\n".format(obj.name, obj.identifier))

	file.write("\n## Areas\n")
	for area in sorted(areas):
		obj = areas[area]
		generate_area.build_area_digraph(
			"wiki/areas/", areas, components, teams, area
		)
		file.write("* [{0}](areas/{1}.png)\n".format(
			area if obj.name is None else obj.name, area
		))

	file.write("\n## Levels (Order)\n")
	for level in sorted(levels):
		obj = levels[level]
		file.write("* {0} ({1})\n".format(level if obj.name is None else obj.name, obj.order))

	file.close()

def _main(argv=sys.argv[1:]):
	arguments = docopt(__doc__, argv)
	input_path = arguments['--i'] if arguments['--i'] is not None else arguments['<input>']
	output_directory = arguments['--o'] if arguments['--o'] is not None else arguments['<output>']

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

	if len(area_commands) != 0:
		for area in area_commands:
			generate_area.build_area_digraph(
				output_directory + "/areas/",
				areas,
				components,
				teams,
				area
			)

	create_wiki(areas, components, levels, teams)
	return 0

if __name__ == "__main__":
	sys.exit(_main(sys.argv[1:]))
