from dataclasses import dataclass


@dataclass
class Graph:
    vertexes: object
    edges: list[object, object]

    def search(self, vertex):  # method
        bfs(self, vertex)


# visitor 1
def bfs(g: Graph, vertex):
    pass


# visitor 2
def dfs(g: Graph, vertex):
    pass
