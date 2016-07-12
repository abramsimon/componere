from graphviz import Digraph


def draw_node_label_table(teams, component):
	node_label = '<<TABLE BORDER="0" CELLSPACING="0" CELLPADDING="4" BGCOLOR="'
	node_label += teams[component.team_identifier].display.background_color
	node_label += '"><TR><TD BORDER="1"><FONT POINT-SIZE="13">'
	node_label += '&lt;&lt;' + component.type + '&gt;&gt;<BR/>'
	node_label += component.name + '</FONT></TD></TR>'
	node_label += '<TR><TD BORDER="1" BALIGN="LEFT">'
	node_label += '+&nbsp;' + component.level_identifier + '&nbsp;:&nbsp;level'

	# For adding more attributes to the node
	if component.release_date is not None:
		node_label += '<BR/>+&nbsp;' + component.release_date.strftime('%m/%d/%Y')
		node_label += '&nbsp;:&nbsp;release date'

	node_label += '</TD></TR></TABLE>>'
	return node_label


def add_components_edges_digraph(digraph, components):
	for component in components.values():
		if component.dependency_identifiers is not None:
			for dependency_identifier in component.dependency_identifiers:
				#only add edges between pre-existed nodes
				if dependency_identifier in components:
					digraph.edge(
						component.identifier,
						dependency_identifier,
						arrowhead='open',
						style="dashed",
					)

def add_teams_color_map(parent_digraph, teams):
	color_map = Digraph("cluster_area.teams_color_map")
	color_map.body.append('label = "Teams Colors Map"')
	color_map.body.append('labeljust="l" fontsize="20"')
	for team_identifier, team in teams.iteritems():
		color_map.node(
			team_identifier,
			label=team.name,
			style='filled',
			color=team.display.background_color,
			fontcolor=team.display.foreground_color,
		)
	parent_digraph.subgraph(color_map)


def find_direct_connected_components(components, component_group):
	connected_components = {}
	#In Edges
	for component_identifier, component in components.iteritems():
		if component.dependency_identifiers is not None:
			for dependency_identifier in component.dependency_identifiers:
				if dependency_identifier in component_group:
					connected_components[component_identifier] = component
					break
	#Out Edges
	for component in component_group.values():
		if component.dependency_identifiers is not None:
			for dependency_identifier in component.dependency_identifiers:
					connected_components[dependency_identifier] = components[dependency_identifier]

	return connected_components


def find_showed_teams(showed_components, teams):
	showed_teams = {}
	for component in showed_components.values():
		showed_teams[component.team_identifier] = teams[component.team_identifier]
	return showed_teams
