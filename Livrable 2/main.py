import random

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['DataProject']
collection_grapgh = db['graph']

# Permet de créer un graphe avec un nombre de noeud définis, un angle moyen et un poid moyen pour les arretes
class RandomGraph:
    # Permet d'initialiser la class RandomGraph
    # On initialise l'instance et on randomise les positions
    def __init__(self, nodes, meanDegree, meanWeight):
        self.nodes = nodes
        self.meanDegree = meanDegree
        self.meanWeight = meanWeight
        self.edges = 0
        self.weight = 0
        self.graph = [[0 for i in range(0, self.nodes)] for j in range(0, self.nodes)]
        self.positions = [(i, j) for i in range(0, self.nodes) for j in range(0, self.nodes) if i < j]
        random.shuffle(self.positions)

    # Calcule le degrés moyen des noeuds
    def avgDegree(self):
        return (self.edges * 2.0) / self.nodes

    # Cacule le poids moyen des arrete
    def avgWeight(self):
        return self.weight / self.edges

    def addEdge(self, i, j, weight=1):
        if self.graph[i][j] == 0 and self.graph[j][i] == 0:
            self.graph[i][j] = weight
            self.graph[j][i] = weight
            self.edges += 1
            self.weight += weight
            self.positions.remove((i, j))

    def addWeight(self, i, j, add=1):
        if self.graph[i][j] > 0:
            self.graph[i][j] += add
            self.graph[j][i] += add
            self.weight += add

    def removeEdge(self, i, j):
        self.graph[i][j] = 0
        self.graph[j][i] = 0

    def getEdges(self):
        return [(i, j, self.graph[i][j]) for i in range(0, self.nodes) for j in range(0, self.nodes) if
                i < j and self.graph[i][j] > 0]

    def getMatrix(self):
        return self.graph

    def getNode(self, node):
        return [(j, self.graph[node][j]) for j in range(0, self.nodes) if self.graph[node][j] > 0]

    def getNodes(self):
        return [(i, self.getNode(i)) for i in range(0, self.nodes)]

    def createGraph(self):
        # First connect even nodes with odd nodes
        for i in range(0, self.nodes, 2):
            if self.avgDegree() >= self.meanDegree:
                break
            if i + 1 < self.nodes:
                self.addEdge(i, i + 1)
        # Now connect odd nodes with even nodes (make chain)
        for i in range(1, self.nodes, 2):
            if self.avgDegree() >= self.meanDegree:
                break
            if i + 1 < self.nodes:
                self.addEdge(i, i + 1)
        if self.avgDegree() < self.meanDegree:
            # Close the chain
            self.addEdge(0, self.nodes - 1)
        # At this point we should start edges randomly until we have reach the average degree
        while len(self.positions) > 0:
            if self.avgDegree() >= self.meanDegree:
                break
            (i, j) = self.positions[0]
            self.addEdge(i, j)
        # Now we have to increase weights until we reach the needed average
        existing_edges = self.getEdges()
        while self.avgWeight() < self.meanWeight:
            (i, j, weight) = random.choice(existing_edges)
            self.addWeight(i, j)


graph = RandomGraph(24, 5, 3.3)
graph.createGraph()
print("All graph edges with weights, list of (node1, node2, weight) tuples\n", graph.getEdges())
print("Nodes connected to node 1, with weights, list of (node, weigh) tuples\n", graph.getNode(2))
print("Complete node info, list of getNode(i) values for all nodes\n", graph.getNodes())
print("Matrix representation, element a[i][j] has the weight of connecting edge, 0 otherwise\n", graph.getMatrix())
print("Average degree of node\n", graph.avgDegree())
print("Average edge weight\n", graph.avgWeight())
