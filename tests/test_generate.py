from unittest import TestCase
import unittest
from componere import *
from test_Digraph import TestDigraph
from graphviz import Digraph
from mock import patch

class GenerateTest(TestCase):
	def test_invalid_input(self):
		self.assertEqual(3, __main__._main(['foo', '--all', 'foo', '--detail']))


	def test_generate_area(self):
		areas = load_input.load_areas("test_areas.yaml")
		components = load_input.load_components("test_components.yaml")
		self.assertEqual(6, len(areas))
		self.assertEqual(5, len(components))

		A_components = generate_area.find_recursive_components_within_area(
			components,
			areas,
			"A"
		)
		self.assertEqual(4, len(A_components))
		for component_identifier in ["a1", "a2", "a3", "a4"]:
			self.assertNotEqual(None, A_components.get(component_identifier))
		AS1_components = generate_area.find_recursive_components_within_area(
			components,
			areas,
			"AS1"
		)
		self.assertEqual(2, len(AS1_components))
		for component_identifier in ["a3", "a4"]:
			self.assertNotEqual(None, AS1_components.get(component_identifier))
		B_components = generate_area.find_recursive_components_within_area(
			components,
			areas,
			"B"
		)
		self.assertEqual(1, len(B_components))
		self.assertNotEqual(None, B_components.get("b1"))
		Empty_components = generate_area.find_recursive_components_within_area(
			components,
			areas,
			"Empty"
		)
		self.assertEqual(0, len(Empty_components))


	def test_generate_component(self):
		areas = load_input.load_areas("test_areas.yaml")
		components = load_input.load_components("test_components.yaml")
		teams = load_input.load_components("test_teams.yaml")
		AS1S1_components = generate_area.find_recursive_components_within_area(
			components,
			areas,
			"AS1S1"
		)
		self.assertEqual(1, len(AS1S1_components))
		self.assertNotEqual(None, AS1S1_components.get("a4"))
		AS1S1_connected_components  = generate_component.find_direct_connected_components(
			components,
			AS1S1_components
		)
		self.assertEqual(3, len(AS1S1_connected_components))
		for component_identifier in ["a1", "a2", "b1"]:
			self.assertNotEqual(None, AS1S1_connected_components.get(
				component_identifier
			))

		AS1S1_showed_teams = generate_component.find_showed_teams(
			AS1S1_components,
			teams
		)
		self.assertEqual(1, len(AS1S1_showed_teams))
		self.assertNotEqual(None, AS1S1_showed_teams.get("team-2"))

		AS1S1_showed_teams_connected = generate_component.find_showed_teams(
			AS1S1_connected_components,
			teams
		)
		self.assertEqual(2, len(AS1S1_showed_teams_connected))
		self.assertNotEqual(None, AS1S1_showed_teams_connected.get("team-1"))
		self.assertNotEqual(None, AS1S1_showed_teams_connected.get("team-2"))

	def test_generate_overview(self):
		test_graph = TestDigraph()
		with patch.object(Digraph, 'edge', test_graph.edge):
			components = load_input.load_components("test_components.yaml")
			levels = load_input.load_levels("test_levels.yaml")
			overview_components = generate_overview.get_components_for_level(
				components,
				levels,
				50
			)
			self.assertEqual(3, len(overview_components))
			for component_identifier in ["a1", "a3", "b1"]:
				self.assertNotEqual(None, overview_components.get(component_identifier))

			root = Digraph("test_graph", filename="level_test")
			for component in overview_components.values():
				generate_overview.add_component_edges(
					root,
					component,
					components,
					overview_components
				)
		self.assertEqual(2, len(test_graph.direct_edges))
		self.assertEqual(True, ('a3', 'a1') in test_graph.direct_edges)
		self.assertEqual(True, ('b1', 'b1') in test_graph.direct_edges)

		self.assertEqual(3, len(test_graph.transitive_edges))
		self.assertEqual(True, ('a1', 'b1') in test_graph.transitive_edges)
		self.assertEqual(True, ('a1', 'a3') in test_graph.transitive_edges)
		self.assertEqual(True, ('a1', 'a1') in test_graph.transitive_edges)


if __name__ == '__main__':
    unittest.main()
