def PrintResultOfMinimumSpanningTree(edges, algorithmName):
    totalLength = 0
    print("The edges of the minimum spanning tree by "+algorithmName+" are:")
    for edge in edges:
        print("from "+str(edge.vertex1)+" to "+str(edge.vertex2)+", length: "+str(edge.length))
        totalLength += edge.length
    print("With a total length of "+str(totalLength))
    print()

def PrintGraph(graph):
    for node in graph.nodes:
        print("Node "+str(node.index))
        for key in node.adjacentVerticesAndDistances: 
            print("To "+str(key)+", length:"+str(node.adjacentVerticesAndDistances[key]))

def NextDecimalNumber(string):
    result = 0
    index = 0
    while(not 48<=ord(string[index])<=57):
        index += 1
    while(index < len(string) and 48<=ord(string[index])<=57):
        result = result*10 + ord(string[index]) - 48
        index += 1
    return result, string[index+1:len(string)]

class QueueNode():
    def __init__(self):
        self.next = None
        self.value = None

class PriorityQueueByDepths():

    def __init__(self):
        self.start = None
        self.end = None

    def NotEmpty(self):
        if(self.start != None):
            return True
        return False
     
    def Enqueue(self, value, depths):
        node = QueueNode()
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
        node = QueueNode()
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

class Node():

    def __init__(self, index):
        self.index = index
        self.edges = []

class Edge():
    
    def __init__(self, vertex1, vertex2, length): #These vertices are their indices
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.length = length

    def TheIndexOfTheOtherVertex(self, vertex):
        if(self.vertex1 == vertex):
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

    def CreateGraph(self, inputFileName):
        lines = open("GenericInput.txt")
        lines = lines.read()
        numberOfVertices, lines = NextDecimalNumber(lines)
        for i in range(numberOfVertices):
            node = Node(i)
            self.vertices.append(node)
        numberOfEdges, lines = NextDecimalNumber(lines)
        for i in range(numberOfEdges):
            vertex1Index, lines = NextDecimalNumber(lines)
            vertex2Index, lines = NextDecimalNumber(lines)
            edgeLength, lines = NextDecimalNumber(lines)
            edge = Edge(vertex1Index, vertex2Index, edgeLength)
            self.vertices[vertex1Index].edges.append(edge)
            self.vertices[vertex2Index].edges.append(edge)
            self.edges.Enqueue(edge)

    def Dijkstra(self, indexOfStart, indexOfDestination): #Returns the length and vertices of the shortest path
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
        
        path = []
        current = self.vertices[indexOfDestination]
        while(current != self.vertices[indexOfStart]):
            for edge in current.edges:
                adjacentIndex = edge.TheIndexOfTheOtherVertex(current.index)
                if(depths[adjacentIndex] == depths[current.index] - edge.length):
                    path.append(current.index)
                    current = self.vertices[adjacentIndex]
                    break
        path.append(current.index)
        path.reverse()
        return depths[indexOfDestination], path

    def TopologicalSort(self):
        pass

    def Kruskal(self): #Returns a set of edges of the minimum spanning tree and the total length of the tree
        edgesResult = []
        subtrees = []
        alreadyInSubtree = []
        subtreesOfVertices = {}
        while(self.edges.NotEmpty()):
            edge = self.edges.Dequeue()            
            if(edge.vertex1 not in alreadyInSubtree and edge.vertex2 not in alreadyInSubtree):
                alreadyInSubtree.append(edge.vertex1)
                alreadyInSubtree.append(edge.vertex2)
                subtreesOfVertices[edge.vertex1] = len(subtrees)
                subtreesOfVertices[edge.vertex2] = len(subtrees)
                subtrees.append([edge.vertex1, edge.vertex2])
                edgesResult.append(edge)
            elif(edge.vertex1 in alreadyInSubtree and edge.vertex2 not in alreadyInSubtree):
                alreadyInSubtree.append(edge.vertex2)
                subtrees[subtreesOfVertices[edge.vertex1]].append(edge.vertex2)
                subtreesOfVertices[edge.vertex2] = subtreesOfVertices[edge.vertex1]
                edgesResult.append(edge)
            elif(edge.vertex1 not in alreadyInSubtree and edge.vertex2 in alreadyInSubtree):
                alreadyInSubtree.append(edge.vertex1)
                subtrees[subtreesOfVertices[edge.vertex2]].append(edge.vertex1)
                subtreesOfVertices[edge.vertex1] = subtreesOfVertices[edge.vertex2]
                edgesResult.append(edge)
            elif(subtreesOfVertices[edge.vertex1] != subtreesOfVertices[edge.vertex2]): #the subtree of vertex1 becomes part of the subtree of vertex2
                previousSubtreeOfVertex1 = subtrees[subtreesOfVertices[edge.vertex1]]
                for vertex in previousSubtreeOfVertex1:
                    subtrees[subtreesOfVertices[edge.vertex2]].append(vertex)
                    subtreesOfVertices[vertex] = subtreesOfVertices[edge.vertex2]
                previousSubtreeOfVertex1.clear()
                edgesResult.append(edge)

        return edgesResult

    def Jarnik(self): #Returns a set of edges of the minimum spanning tree and the total length of the tree
        edgesResult = []
        edgesToTry = PriorityQueueShortestEdges()
        verticesInTheSpanningTreeByIndex = [self.vertices[0]]
        for edge in self.vertices[0].edges:
            edgesToTry.Enqueue(edge)

        while(len(verticesInTheSpanningTreeByIndex) != len(self.vertices)):
            edgeToTry = edgesToTry.Dequeue()
            if(edgeToTry.vertex1 not in verticesInTheSpanningTreeByIndex):
                edgesResult.append(edgeToTry)
                verticesInTheSpanningTreeByIndex.append(edgeToTry.vertex1)               
                for edge in self.vertices[edgeToTry.vertex1].edges:
                    edgesToTry.Enqueue(edge)
            elif(edgeToTry.vertex2 not in verticesInTheSpanningTreeByIndex):
                edgesResult.append(edgeToTry)
                verticesInTheSpanningTreeByIndex.append(edgeToTry.vertex2)
                for edge in self.vertices[edgeToTry.vertex2].edges:
                    edgesToTry.Enqueue(edge)

        return edgesResult

    def Boruvka(self):
        pass

genericGraph = GenericGraph()
genericGraph.CreateGraph("GenericInput.txt")
#PrintGraph(genericGraph)

# length, path = genericGraph.Dijkstra(7,2)
# print("From 7 to 2 the length is: "+str(length))
# print("Path: "+str(path))

kruskalEdges = genericGraph.Kruskal()
PrintResultOfMinimumSpanningTree(kruskalEdges, "Kruskal")

jarnikEdges = genericGraph.Jarnik()
PrintResultOfMinimumSpanningTree(jarnikEdges, "Jarnik")



