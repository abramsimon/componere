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
class TestDigraph ():
    direct_edges = set()
    transitive_edges = set()
    subgraphs = {}
    @staticmethod
    def init():
        TestDigraph.direct_edges.clear()
        TestDigraph.transitive_edges.clear()
        TestDigraph.subgraphs.clear()

    @staticmethod
    def edge(cls, tail_name, head_name, label="", _attributes=None, **attrs):
        if label == "\<\<transitive\>\>":
            TestDigraph.transitive_edges.add((tail_name, head_name))
        else:
            TestDigraph.direct_edges.add((tail_name, head_name))

    @staticmethod
    def subgraph(self, graph):
        if graph.name == "cluster_area.teams_color_map":
            return

        if TestDigraph.subgraphs.get(self.name) is None:
            TestDigraph.subgraphs[self.name] = set()
        TestDigraph.subgraphs[self.name].add(graph.name)

    @staticmethod
    def render(self, filename=None, directory=None, view=False, cleanup=False):
        return
