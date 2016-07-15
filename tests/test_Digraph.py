class TestDigraph ():
    direct_edges = set()
    transitive_edges = set()
    
    def edge(self, tail_name, head_name, label="", _attributes=None, **attrs):
        if label == "\<\<transitive\>\>":
            self.transitive_edges.add((tail_name, head_name))
        else:
            self.direct_edges.add((tail_name, head_name))
