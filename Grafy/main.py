from BipartiteGraph import BipartiteGraph
from GenericGraph import GenericGraph
from ResultPrinting import (PrintGenericGraph, PrintBipartiteGraph, PrintResultOfDijkstra, PrintResultOfMinimumSpanningTree, PrintTopologicalOrdering, PrintingResultOfTheHopcroftKarp)

# ------------------------Test samples number 1:------------------------        
# genericGraph = GenericGraph()
# genericGraph.CreateGraph("GenericNotCycleInput.txt", True)

# start, destination = 0, 7
# pathExists, length, path = genericGraph.Dijkstra(start, destination)
# PrintResultOfDijkstra(start, destination, pathExists, length, path)

# kruskalEdges = genericGraph.Kruskal()
# PrintResultOfMinimumSpanningTree(kruskalEdges, "Kruskal")

# jarnikEdges = genericGraph.Jarnik()
# PrintResultOfMinimumSpanningTree(jarnikEdges, "Jarnik")

# boruvkaEdges = genericGraph.Boruvka()
# PrintResultOfMinimumSpanningTree(boruvkaEdges, "Boruvka")

# itExists, stackTopologicalOrdering = genericGraph.TopologicalSort()
# PrintTopologicalOrdering(itExists, stackTopologicalOrdering)

# ------------------------Test samples number 2:------------------------
# genericGraphWithCycle = GenericGraph()
# genericGraphWithCycle.CreateGraph("GenericCycleThereInput.txt", True)

# start, destination = 0, 5
# pathExists, length, path = genericGraphWithCycle.Dijkstra(start, destination)
# PrintResultOfDijkstra(start, destination, pathExists, length, path)

# kruskalEdges = genericGraphWithCycle.Kruskal()
# PrintResultOfMinimumSpanningTree(kruskalEdges, "Kruskal")

# jarnikEdges = genericGraphWithCycle.Jarnik()
# PrintResultOfMinimumSpanningTree(jarnikEdges, "Jarnik")

# boruvkaEdges = genericGraphWithCycle.Boruvka()
# PrintResultOfMinimumSpanningTree(boruvkaEdges, "Boruvka")

# itExists, stackTopologicalOrdering = genericGraphWithCycle.TopologicalSort()
# PrintTopologicalOrdering(itExists, stackTopologicalOrdering)

# ------------------------Test samples number 3:------------------------
bipartiteGraph = BipartiteGraph()
bipartiteGraph.CreateGraph("BipartiteInput.txt")
#PrintBipartiteGraph(bipartiteGraph)

edges = bipartiteGraph.HopcroftKarp()
PrintingResultOfTheHopcroftKarp(edges)