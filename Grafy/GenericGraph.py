from LinkedLists import PriorityQueueShortestEdges
from LinkedLists import PriorityQueueByDepths
from LinkedLists import Stack
from OtherFunctions import NextDecimalNumber
from GraphParts import Vertex
from GraphParts import Edge

class GenericGraph:
    
    def __init__(self):
        self.vertices = []
        self.edges = PriorityQueueShortestEdges()
        self.directedYesOrNot = False

    def CreateGraph(self, inputFileName, directed=False):
        lines = open("Inputs/"+inputFileName).read()
        numberOfVertices, lines = NextDecimalNumber(lines)
        for i in range(numberOfVertices):
            node = Vertex(i)
            self.vertices.append(node)
        numberOfEdges, lines = NextDecimalNumber(lines)
        for i in range(numberOfEdges):
            vertex1Index, lines = NextDecimalNumber(lines)
            vertex2Index, lines = NextDecimalNumber(lines)
            edgeLength, lines = NextDecimalNumber(lines)
            edge = Edge(vertex1Index, vertex2Index, edgeLength, directed)
            self.vertices[vertex1Index].edges.append(edge)
            if not directed:
                self.vertices[vertex2Index].edges.append(edge)
            else:
                self.vertices[vertex2Index].edgesThatComeToIt.append(edge)
            self.edges.Enqueue(edge)
            self.directedYesOrNot = directed

    def Dijkstra(self, indexOfStart, indexOfDestination): #Returns if the path even exists, the length and the vertices of the shortest path
        queue = PriorityQueueByDepths()
        depths = {indexOfStart:0}
        queue.Enqueue(self.vertices[indexOfStart], depths)
        while(queue.NotEmpty()):
            vertex = queue.Dequeue()
            for edge in vertex.edges:
                adjacentIndex = edge.TheIndexOfTheOtherVertex(vertex.index)
                if(adjacentIndex not in depths):
                    depths[adjacentIndex] = depths[vertex.index] + edge.length
                    queue.Enqueue(self.vertices[adjacentIndex], depths)
                elif(depths[adjacentIndex] > depths[vertex.index] + edge.length):
                    depths[adjacentIndex] = depths[vertex.index] + edge.length
                    queue.Enqueue(self.vertices[adjacentIndex], depths)

        if(indexOfDestination not in depths):
            return False, None, None

        path = []
        current = self.vertices[indexOfDestination]
        if(self.directedYesOrNot):
            while(current != self.vertices[indexOfStart]):
                for edge in current.edgesThatComeToIt:
                    adjacentIndex = edge.TheIndexOfTheOtherVertex(current.index)
                    if(adjacentIndex in depths):
                        if(depths[adjacentIndex] == depths[current.index] - edge.length):
                            path.append(current.index)
                            current = self.vertices[adjacentIndex]
                            break

        else:
            while(current != self.vertices[indexOfStart]):
                for edge in current.edges:
                    adjacentIndex = edge.TheIndexOfTheOtherVertex(current.index)
                    if(adjacentIndex in depths):
                        if(depths[adjacentIndex] == depths[current.index] - edge.length):
                            path.append(current.index)
                            current = self.vertices[adjacentIndex]
                            break
        path.append(current.index)
        path.reverse()
        return True, depths[indexOfDestination], path

    def TopologicalSort(self): #Returns if the graph even has a topological ordering and a stack of the topological ordering
        def IsThereACycle():
            alreadyThere = []
            start = self.vertices[0]
            vertices =[start]
            alreadyThere = [start.index]
            while(vertices != []):
                vertex = vertices.pop()
                for edge in vertex.edges:
                    adjacentVertexIndex = edge.TheIndexOfTheOtherVertex(vertex.index)
                    if(adjacentVertexIndex not in alreadyThere):
                        alreadyThere.append(adjacentVertexIndex)
                        vertices.append(self.vertices[adjacentVertexIndex])
                    else:
                        return True
            return False

        def AddItToTopologicalOrdering(vertex):
            for edge in self.vertices[vertex].edges:
                adjacentVertexIndex = edge.TheIndexOfTheOtherVertex(vertex)
                if(adjacentVertexIndex in verticesNotThere):
                    AddItToTopologicalOrdering(adjacentVertexIndex)
            if(vertex in verticesNotThere):
                verticesNotThere.remove(vertex)
            result.Push(vertex)
        
        if(IsThereACycle()):
            return False, None

        result = Stack()
        verticesNotThere = set()
        for i in range(len(self.vertices)):
            verticesNotThere.add(self.vertices[i].index)
        while(len(verticesNotThere) != 0):
            vertex = verticesNotThere.pop()
            AddItToTopologicalOrdering(vertex)

        return True, result

    def Kruskal(self): #Returns a list of edges of the minimum spanning tree
        edgesResult = []
        verticesOfsubtrees = []
        subtreesOfVertices = {}
        while(self.edges.NotEmpty()):
            edge = self.edges.Dequeue()            
            if(edge.vertex1 not in subtreesOfVertices and edge.vertex2 not in subtreesOfVertices):
                subtreesOfVertices[edge.vertex1] = len(verticesOfsubtrees)
                subtreesOfVertices[edge.vertex2] = len(verticesOfsubtrees)
                verticesOfsubtrees.append([edge.vertex1, edge.vertex2])
                edgesResult.append(edge)
            elif(edge.vertex1 in subtreesOfVertices and edge.vertex2 not in subtreesOfVertices):
                verticesOfsubtrees[subtreesOfVertices[edge.vertex1]].append(edge.vertex2)
                subtreesOfVertices[edge.vertex2] = subtreesOfVertices[edge.vertex1]
                edgesResult.append(edge)
            elif(edge.vertex1 not in subtreesOfVertices and edge.vertex2 in subtreesOfVertices):
                verticesOfsubtrees[subtreesOfVertices[edge.vertex2]].append(edge.vertex1)
                subtreesOfVertices[edge.vertex1] = subtreesOfVertices[edge.vertex2]
                edgesResult.append(edge)
            elif(subtreesOfVertices[edge.vertex1] != subtreesOfVertices[edge.vertex2]): #the subtree of vertex1 becomes part of the subtree of vertex2
                previousSubtreeOfVertex1 = verticesOfsubtrees[subtreesOfVertices[edge.vertex1]]
                for vertex in previousSubtreeOfVertex1:
                    verticesOfsubtrees[subtreesOfVertices[edge.vertex2]].append(vertex)
                    subtreesOfVertices[vertex] = subtreesOfVertices[edge.vertex2]
                previousSubtreeOfVertex1.clear()
                edgesResult.append(edge)

        return edgesResult

    def Jarnik(self): #Returns a list of edges of the minimum spanning tree
        edgesResult = []
        edgesToTry = PriorityQueueShortestEdges()
        verticesInTheSpanningTreeByIndex = {self.vertices[0]}
        for edge in self.vertices[0].edges:
            edgesToTry.Enqueue(edge)
        for edge in self.vertices[0].edgesThatComeToIt:
            edgesToTry.Enqueue(edge)

        while(len(verticesInTheSpanningTreeByIndex) != len(self.vertices)):
            edgeToTry = edgesToTry.Dequeue()
            if(edgeToTry.vertex1 not in verticesInTheSpanningTreeByIndex):
                edgesResult.append(edgeToTry)
                verticesInTheSpanningTreeByIndex.add(edgeToTry.vertex1)               
                for edge in self.vertices[edgeToTry.vertex1].edges:
                    edgesToTry.Enqueue(edge)
                for edge in self.vertices[edgeToTry.vertex1].edgesThatComeToIt:
                    edgesToTry.Enqueue(edge)
            elif(edgeToTry.vertex2 not in verticesInTheSpanningTreeByIndex):
                edgesResult.append(edgeToTry)
                verticesInTheSpanningTreeByIndex.add(edgeToTry.vertex2)
                for edge in self.vertices[edgeToTry.vertex2].edges:
                    edgesToTry.Enqueue(edge)
                for edge in self.vertices[edgeToTry.vertex2].edgesThatComeToIt:
                    edgesToTry.Enqueue(edge)

        return edgesResult

    def Boruvka(self): #Returns a set of edges of the minimum spanning tree
        edgesResult = set()
        edgesToTryOfSubtrees = [] #List of PriorityQueueShortestEdges
        verticesOfsubtrees = []
        subtreesOfVertices = {}
        #First part, for each vertex, find the shortest edge and create subtrees from it
        for vertex in self.vertices:
            shortestEdge = vertex.ShortestEdge()
            edgesResult.add(shortestEdge)
            otherVertex = shortestEdge.TheIndexOfTheOtherVertex(vertex.index) 
            if(vertex.index not in subtreesOfVertices and otherVertex not in subtreesOfVertices):
                newSubtree = len(verticesOfsubtrees)
                subtreesOfVertices[vertex.index] = newSubtree
                subtreesOfVertices[otherVertex] = newSubtree
                verticesOfsubtrees.append([vertex.index, otherVertex])
                edgesToTryOfSubtrees.append(PriorityQueueShortestEdges())
                for edge in vertex.edges+vertex.edgesThatComeToIt+self.vertices[otherVertex].edges+self.vertices[otherVertex].edgesThatComeToIt:
                    if(edge != shortestEdge):
                        edgesToTryOfSubtrees[newSubtree].Enqueue(edge)
            elif((vertex.index not in subtreesOfVertices and otherVertex in subtreesOfVertices) or (vertex.index in subtreesOfVertices and otherVertex not in subtreesOfVertices)):    
                isThere = vertex
                notThere = self.vertices[otherVertex]
                if(vertex.index not in subtreesOfVertices):
                    isThere = notThere
                    notThere = vertex
                subtreesOfVertices[notThere.index] = subtreesOfVertices[isThere.index]
                verticesOfsubtrees[subtreesOfVertices[isThere.index]].append(notThere.index)
                for edge in notThere.edges+notThere.edgesThatComeToIt:
                    if(edge != shortestEdge):
                        edgesToTryOfSubtrees[subtreesOfVertices[isThere.index]].Enqueue(edge)
            elif(vertex.index in subtreesOfVertices and otherVertex in subtreesOfVertices and subtreesOfVertices[vertex.index]!=subtreesOfVertices[otherVertex]):
                #the subtree of vertex becomes part of the subtree of otherVertex
                oldSubtree = subtreesOfVertices[vertex.index]
                newSubtree = subtreesOfVertices[otherVertex]
                for vertex in verticesOfsubtrees[oldSubtree]:
                    subtreesOfVertices[vertex] = newSubtree
                    verticesOfsubtrees[newSubtree].append(vertex)
                verticesOfsubtrees[oldSubtree].clear()
                while(edgesToTryOfSubtrees[oldSubtree].NotEmpty()):
                    edge = edgesToTryOfSubtrees[oldSubtree].Dequeue()
                    edgesToTryOfSubtrees[newSubtree].Enqueue(edge)
        #Second part, until there is only one subtree (minimum spanning tree in this case), pick one not empty subtree, find the shortest edge, that is coming from it and connect that subtree with another one, that is connect to it by the edge
        while(len(edgesResult)!=len(self.vertices)-1):
            indexOfSubtree = 0
            verticesOfsubtreesList = verticesOfsubtrees[indexOfSubtree]
            while(verticesOfsubtreesList == []):
                indexOfSubtree += 1
                verticesOfsubtreesList = verticesOfsubtrees[indexOfSubtree]
            shortestEdge = edgesToTryOfSubtrees[indexOfSubtree].Dequeue()
            vertex = shortestEdge.vertex1
            otherVertex = shortestEdge.vertex2
            if(subtreesOfVertices[vertex] != subtreesOfVertices[otherVertex]): #It may be one of the edges, that is not relevant for me
                NewSubtree = subtreesOfVertices[otherVertex]
                OldSubtree = subtreesOfVertices[vertex]
                edgesResult.add(shortestEdge)
                #the subtree of vertex becomes part of the subtree of otherVertex
                for vertex in verticesOfsubtrees[OldSubtree]:
                    subtreesOfVertices[vertex] = NewSubtree
                    verticesOfsubtrees[NewSubtree].append(vertex)
                verticesOfsubtrees[OldSubtree].clear()
                while(edgesToTryOfSubtrees[OldSubtree].NotEmpty()):
                    edge = edgesToTryOfSubtrees[OldSubtree].Dequeue()
                    if(edge.vertex1 != vertex or edge.vertex1 != otherVertex or edge.vertex2 != vertex or edge.vertex2 != otherVertex):
                        #Cutting of edges, that connect two vertices of the NewSubtree (those won't be used anymore)
                        edgesToTryOfSubtrees[NewSubtree].Enqueue(edgesToTryOfSubtrees[OldSubtree].Dequeue())
        return edgesResult
