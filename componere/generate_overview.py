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
import generate_area
import generate_component


def get_components_for_level(components, levels, level_order):
    level_components = {}
    for component in components.values():
        if levels[component.level_identifier].order >= level_order:
            level_components[component.identifier] = component
    return level_components


def add_component_edges(
        digraph,
        component,
        all_components,
        components,
        visited={},
        parent=None,
):
    if component.identifier in visited:
        return
    visited[component.identifier] = True
    if component.dependency_identifiers is not None:
        for dependency_identifier in component.dependency_identifiers:
            if dependency_identifier in components:
                if parent is None:
                    digraph.edge(
                        component.identifier,
                        dependency_identifier,
                        arrowhead='open',
                        style="dashed",
                    )
                else:
                    digraph.edge(
                        parent.identifier,
                        dependency_identifier,
                        arrowhead='open',
                        style="dashed",
                        label="\<\<transitive\>\>",
                    )
            else:
                add_component_edges(
                    digraph,
                    all_components[dependency_identifier],
                    all_components,
                    components,
                    visited,
                    component if parent is None else parent
                )


def build_overview_digraph(
        name,
        output_file,
        areas,
        components,
        levels,
        teams,
        types,
        level_order
):
    root = Digraph(name, filename=output_file + "level_" +
                   str(level_order), format="png")
    overview_components = get_components_for_level(
        components,
        levels,
        level_order,
    )
    generate_area.add_detail_area_components_digraph(
        root,
        areas,
        overview_components,
        teams,
        types,
    )
    for component in overview_components.values():
        add_component_edges(root, component, components, overview_components)

    generate_component.add_teams_color_map(
        root,
        generate_component.find_showed_teams(overview_components, teams),
    )
    root.render(view=False, cleanup=True)
