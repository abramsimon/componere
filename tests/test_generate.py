from unittest import TestCase
import unittest
from componere import *
from test_Digraph import TestDigraph
from graphviz import Digraph
from mock import patch

class GenerateTest(TestCase):
    def setUp(self):
        self.areas = {}
        self.components = {}
        self.levels = {}
        self.teams = {}
        self.path = "../componere/tests/test_file.comp"
        TestDigraph.init()
        load_input.load_objects(self.path, self.areas, self.components, self.levels, self.teams)

    def test_generate_area(self):
        self.assertEqual(6, len(self.areas))
        self.assertEqual(5, len(self.components))

        A_components = generate_area.find_recursive_components_within_area(
            self.components,
            self.areas,
            "A"
        )
        self.assertEqual(4, len(A_components))
        for component_identifier in ["a1", "a2", "a3", "a4"]:
            self.assertNotEqual(None, A_components.get(component_identifier))
        AS1_components = generate_area.find_recursive_components_within_area(
            self.components,
            self.areas,
            "AS1"
        )
        self.assertEqual(2, len(AS1_components))
        for component_identifier in ["a3", "a4"]:
            self.assertNotEqual(None, AS1_components.get(component_identifier))
        B_components = generate_area.find_recursive_components_within_area(
            self.components,
            self.areas,
            "B"
        )
        self.assertEqual(1, len(B_components))
        self.assertNotEqual(None, B_components.get("b1"))
        Empty_components = generate_area.find_recursive_components_within_area(
            self.components,
            self.areas,
            "Empty"
        )
        self.assertEqual(0, len(Empty_components))


    def test_generate_component(self):
        AS1S1_components = generate_area.find_recursive_components_within_area(
            self.components,
            self.areas,
            "AS1S1"
        )
        self.assertEqual(1, len(AS1S1_components))
        self.assertNotEqual(None, AS1S1_components.get("a4"))
        AS1S1_connected_components  = generate_component.find_direct_connected_components(
            self.components,
            AS1S1_components
        )
        self.assertEqual(3, len(AS1S1_connected_components))
        for component_identifier in ["a1", "a2", "b1"]:
            self.assertNotEqual(None, AS1S1_connected_components.get(
                component_identifier
            ))

        AS1S1_showed_teams = generate_component.find_showed_teams(
            AS1S1_components,
            self.teams
        )
        self.assertEqual(1, len(AS1S1_showed_teams))
        self.assertNotEqual(None, AS1S1_showed_teams.get("team-2"))

        AS1S1_showed_teams_connected = generate_component.find_showed_teams(
            AS1S1_connected_components,
            self.teams
        )
        self.assertEqual(2, len(AS1S1_showed_teams_connected))
        self.assertNotEqual(None, AS1S1_showed_teams_connected.get("team-1"))
        self.assertNotEqual(None, AS1S1_showed_teams_connected.get("team-2"))

    def test_generate_overview(self):
        with patch.object(Digraph, 'edge', TestDigraph.edge):
            overview_components = generate_overview.get_components_for_level(
                self.components,
                self.levels,
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
                    self.components,
                    overview_components
                )
        self.assertEqual(2, len(TestDigraph.direct_edges))
        self.assertEqual(True, ('a3', 'a1') in TestDigraph.direct_edges)
        self.assertEqual(True, ('b1', 'b1') in TestDigraph.direct_edges)


    def test_generate_detail(self):
        with patch.object(
            Digraph, 'edge', TestDigraph.edge), patch.object(
            Digraph, 'subgraph', TestDigraph.subgraph), patch.object(
            Digraph, 'render', TestDigraph.render
            ):
            generate_detail.build_detail_digraph(
                "test",
                "test",
                self.areas,
                self.components,
                self.teams,
            )
            prefix = "cluster_area_"
            self.assertEqual(3, len(TestDigraph.subgraphs))
            self.assertEqual(True, "test" in TestDigraph.subgraphs)
            for area in ["A", "AS1"]:
                self.assertEqual(True, prefix + area in TestDigraph.subgraphs)
            self.assertEqual(3, len(TestDigraph.subgraphs["test"]))
            for area in ["A", "B", "Empty"]:
                self.assertEqual(True, prefix + area in TestDigraph.subgraphs["test"])
            self.assertEqual(2, len(TestDigraph.subgraphs[prefix + "A"]))
            for area in ["AS1", "AS2"]:
                self.assertEqual(True, prefix + area in TestDigraph.subgraphs[prefix + "A"])
            self.assertEqual(1, len(TestDigraph.subgraphs[prefix + "AS1"]))
            self.assertEqual(True, prefix + "AS1S1" in TestDigraph.subgraphs[prefix + "AS1"])
            for component in self.components.values():
                if component.dependency_identifiers is not None:
                    for dependency_identifier in component.dependency_identifiers:
                        self.assertEqual(True, (
                            component.identifier, dependency_identifier
                        ) in TestDigraph.direct_edges)


if __name__ == '__main__':
    unittest.main()
