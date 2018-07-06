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
from graphviz import Digraph
import generate_component

def add_area_with_components_inside(
    area,
    area_components,
    teams,
    highlited_area_identifier=None,
):
	digraph = Digraph("cluster_area_" + area.identifier)
	digraph.body.append("label = " + '"' + area.name + '"')
	digraph.body.append('style=bold labeljust="l" fontsize="20"')
	if highlited_area_identifier == area.identifier:
		digraph.body.append('style="filled, bold" fillcolor=lightgrey')
	for component in area_components.values():
		digraph.node(
			component.identifier,
			label=generate_component.draw_node_label_table(teams, component),
			fontname="Bitstream Vera Sans",
			fontsize="12",
			shape="plaintext",
			fontcolor=teams[component.team_identifier].display.foreground_color,
		)
	return digraph


def find_child_areas(areas, parent_area_identifier):
	found_areas = []
	for area in areas.values():
		#Source
		if parent_area_identifier is None and area.parent_identifier is None:
			found_areas.append(area)
		#Child
		elif area.parent_identifier == parent_area_identifier:
			found_areas.append(area)
	return found_areas


def find_area_components(components, area_identifier):
	found_components = {}
	for component_identifier, component in components.iteritems():
		if area_identifier is None and component.area_identifier is None:
			found_components[component_identifier] = component
		elif component.area_identifier == area_identifier:
			found_components[component_identifier] = component
	return found_components


def add_detail_area_components_digraph(
	digraph,
	areas,
	components,
	teams,
	area=None,
	highlited_area_identifier=None,
	depth=1,
):
	if depth > 100:
		raise Exception("Too many recursions")

	parent_digraph = None
	if digraph is not None:
		parent_digraph = digraph
	else:
		parent_digraph = add_area_with_components_inside(
			area,
			find_area_components(components, area.identifier),
			teams,
			highlited_area_identifier,
		)

	for child_area in find_child_areas(
		areas, area.identifier if area is not None else None
	):
		parent_digraph.subgraph(add_detail_area_components_digraph(
			None,
			areas,
			components,
			teams,
			child_area,
			highlited_area_identifier,
			depth + 1,
		))

	return parent_digraph


def find_recursive_components_within_area(
	components,
	areas,
	area_identifier,
	depth=1,
):
	if depth > 100:
		raise Exception("Too many recursions")

	found_components = find_area_components(components, area_identifier)
	for child_area in find_child_areas(areas, area_identifier):
		found_components.update(find_recursive_components_within_area(
			components,
			areas,
			child_area.identifier,
			depth + 1,
		))

	return found_components


def add_specific_area_digraph(
	digraph,
	areas,
	area,
	components,
	teams,
	highlited_area_identifier=None,
):
	area_recursive_components = find_recursive_components_within_area(
		components,
		areas,
		area.identifier
	)
	showed_components = area_recursive_components
	showed_components.update(generate_component.find_direct_connected_components(
		components,
		area_recursive_components,
	))
	add_detail_area_components_digraph(
		digraph,
		areas,
		showed_components,
		teams,
		None,
		highlited_area_identifier,
	)
	generate_component.add_components_edges_digraph(digraph, showed_components)
	generate_component.add_teams_color_map(
        digraph,
        generate_component.find_showed_teams(showed_components, teams),
    )


def build_area_digraph(
	output_file,
	areas,
	components,
	teams,
	specific_area_identifier=None,
):
	for area_identifier, area in areas.iteritems():
		if (specific_area_identifier is None or
            specific_area_identifier == area_identifier):
			root = Digraph(
                area_identifier,
                filename=output_file + area_identifier,
                format="png",
            )
			add_specific_area_digraph(
                root,
                areas,
                area,
                components,
                teams,
                area_identifier,
            )
			root.render(view=False, cleanup=True)
