import igraph as ig

class Graph():
  def __init__(self):
    self.graph = ig.Graph()
    self.count = dict()

  def add_vertex(self, token):
    if token not in self.count:
      self.count[token] = 0
    else:
      self.count[token] += 1
    name = f'{token} ({self.count[token]})'
    self.graph.add_vertex(name)
    self.graph.vs['token'] = token

    return name

  def add_edges(self, source, targets):
    for target in targets:
      self.graph.add_edge(source, target)

  def delete_vertices(self, vs):
    for v in vs:
      token = self.graph.vs.find(v)['token']
      self.count[token] -= 1
    self.graph.delete_vertices(vs)

  def delete_edges(self, es):
    self.graph.delete_edges(es)