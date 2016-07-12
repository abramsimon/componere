from graphviz import Digraph
import generate_area
import generate_component


def build_detail_digraph(
	name,
	output_file,
	areas,
	components,
	teams
):
	root = Digraph(name, filename=output_file, format="png")
	generate_area.add_detail_area_components_digraph(
		root,
		areas,
		components,
		teams,
	)
	generate_component.add_components_edges_digraph(root, components)
	generate_component.add_teams_color_map(
		root,
		generate_component.find_showed_teams(components, teams)
	)
	root.render(view=False, cleanup=True)
