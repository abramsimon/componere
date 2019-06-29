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


def build_detail_digraph(
        name,
        output_file,
        areas,
        components,
        teams,
        types
):
    root = Digraph(name, filename=output_file, format="png")
    generate_area.add_detail_area_components_digraph(
        root,
        areas,
        components,
        teams,
        types,
    )
    generate_component.add_components_edges_digraph(root, components)
    generate_component.add_teams_color_map(
        root,
        generate_component.find_showed_teams(components, teams)
    )
    root.render(view=False, cleanup=True)
