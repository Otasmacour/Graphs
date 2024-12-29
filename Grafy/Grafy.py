def PrintResultOfDijkstra(start, destination, pathExists, length, path):
    if(pathExists):
        print("From "+str(start)+" to "+str(destination)+" the length is: "+str(length))
        print("Path: "+str(path))
    else:
        print("Unfortunately, path from "+str(start)+" to "+str(destination)+" doesn't exist")


def PrintTopologicalOrdering(itExists, stack):
    if(itExists):
        print("One of the possible topological ordering looks like this:")
        while(stack.NotEmpty()):
            print(str(stack.Pop()), end=' ')
    else:
        print("There is no topological ordering for this graph, there has to be cycle somewhere there")

def PrintResultOfMinimumSpanningTree(edges, algorithmName):
    totalLength = 0
    print("The edges of one of the possible minimum spanning trees by "+algorithmName+" are:")
    for edge in edges:
        print("from "+str(edge.vertex1)+" to "+str(edge.vertex2)+", length: "+str(edge.length))
        totalLength += edge.length
    print("With a total length of "+str(totalLength))
    print()

def ShortestEdge(edges):
    shortest = edges[0]
    for edge in edges:
        if(edge.length < shortest.length):
            shortest = edge
    return shortest    

def PrintGraph(graph):
    if(not graph.directedYesOrNot):
        print("This graph is not directed")
    else:
        print("This graph is directed")
    for vertex in graph.vertices:
        print("Vertex "+str(vertex.index))
        for edge in vertex.edges:
            print("To "+str(edge.TheIndexOfTheOtherVertex(vertex.index))+", length:"+str(edge.length))
        if(graph.directedYesOrNot):
            print("The edges, that come to vertex "+str(vertex.index)+":")
            for edge in vertex.edgesThatComeToIt:
                print("From "+str(edge.TheIndexOfTheOtherVertex(vertex.index))+", length:"+str(edge.length))
        print()
def NextDecimalNumber(string):
    result = 0
    index = 0
    while(not 48<=ord(string[index])<=57):
        index += 1
    while(index < len(string) and 48<=ord(string[index])<=57):
        result = result*10 + ord(string[index]) - 48
        index += 1
    return result, string[index+1:len(string)]

class LinkedListNode():
    def __init__(self):
        self.next = None
        self.value = None

class Stack():

    def __init__(self):
        self.peek = None

    def NotEmpty(self):
        if(self.peek != None):
            return True
        return False

    def Push(self, value):
        node  = LinkedListNode()
        node.value = value
        if(self.peek == None):
            self.peek = node
        else:
            node.next = self.peek
            self.peek = node

    def Pop(self):
        result = self.peek.value
        self.peek = self.peek.next
        return result

class PriorityQueueByDepths():

    def __init__(self):
        self.start = None
        self.end = None

    def NotEmpty(self):
        if(self.start != None):
            return True
        return False
     
    def Enqueue(self, value, depths):
        node = LinkedListNode()
        node.value = value
        if(self.start == None):
            self.start = node
            self.end = node
        elif(self.start == self.end):
            if(depths[self.start.value.index] > depths[value.index]):
                self.start = node
                node.next = self.end
                
            else:
                self.end = node
                self.start.next = node
        else:
            if(depths[value.index] < depths[self.start.value.index]):
                previousStart = self.start
                self.start = node
                node.next = previousStart
            elif(depths[value.index] > depths[self.end.value.index]):
                previousEnd = self.end
                self.end = node
                previousEnd.next = node
            else:
                current = self.start
                while(depths[current.next.value.index] < depths[value.index]):
                    current = current.next
                node.next = current.next
                current.next = node

    def Dequeue(self):
        if(self.start == self.end):
            node = self.start.value
            self.start = None
            self.end = None
            return node
        else:
            node = self.start.value
            self.start = self.start.next
            return node

class PriorityQueueShortestEdges():

    def __init__(self):
        self.start = None
        self.end = None

    def NotEmpty(self):
        if(self.start != None):
            return True
        return False
    
    def Enqueue(self, value):
        node = LinkedListNode()
        node.value = value
        if(self.start == None):
            self.start = node
            self.end = node
        elif(self.start == self.end):
            if(self.start.value.length > value.length):
                self.start = node
                node.next = self.end
            else:
                self.end = node
                self.start.next = node
        else:
            if(value.length < self.start.value.length):
                previousStart = self.start
                self.start = node
                node.next = previousStart
            elif(value.length > self.end.value.length):
                previousEnd = self.end
                self.end = node
                previousEnd.next = node
            else:
                current = self.start
                while(current.next.value.length < value.length):
                    current = current.next
                node.next = current.next
                current.next = node
    
    def GetAllOfTheEdges(self):
        edges = []
        current = self.start
        while(current != None):
            edges.append(current.value)
            current = current.next
        return(edges)

    def Dequeue(self):
        if(self.start == self.end):
            node = self.start.value
            self.start = None
            self.end = None
            return node
        else:
            node = self.start.value
            self.start = self.start.next
            return node

class Vertex():

    def __init__(self, index):
        self.index = index
        self.edges = []
        self.edgesThatComeToIt = []
    
    def ShortestEdge(self):
        return ShortestEdge(self.edges+self.edgesThatComeToIt)

class Edge():

    def __init__(self, vertex1, vertex2, length, directed=False):  
        self.vertex1 = vertex1  
        self.vertex2 = vertex2  
        self.length = length
        self.directed = directed 

    def TheIndexOfTheOtherVertex(self, vertex):
        if self.vertex1 == vertex:
            return self.vertex2
        else:
            return self.vertex1


class BipartGraph:

    def CreateGraph(self, inputFileName):
        pass
    
    def MaximalMatching(self):
        pass

class GenericGraph:
    
    def __init__(self):
        self.vertices = []
        self.edges = PriorityQueueShortestEdges()
        self.directedYesOrNot = False

    def CreateGraph(self, inputFileName, directed=False):
        lines = open(inputFileName).read()
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

# ------------------------Test samples number 1:------------------------        
# genericGraph = GenericGraph()
# genericGraph.CreateGraph("GenericNotCycleInput.txt", True)
# PrintGraph(genericGraph)

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
# PrintGraph(genericGraph)

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