

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

class PriorityQueue():

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
        self.adjacentVerticesAndDistances = {}

class Edge():
    
    def __init__(self, vertex1, vertex2, length):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.length = length

class BipartGraph:

    def CreateGraph(self, inputFileName):
        pass
    
    def MaximalMatching(self):
        pass

class GenericGraph:
    
    def __init__(self):
        self.nodes = []
        self.edges = PriorityQueue()

    def CreateGraph(self, inputFileName):
        lines = open("GenericInput.txt")
        lines = lines.read()
        numberOfVertices, lines = NextDecimalNumber(lines)
        for i in range(numberOfVertices):
            node = Node(i)
            self.nodes.append(node)
        numberOfEdges, lines = NextDecimalNumber(lines)
        for i in range(numberOfEdges):
            vertex1Index, lines = NextDecimalNumber(lines)
            vertex2Index, lines = NextDecimalNumber(lines)
            edgeLength, lines = NextDecimalNumber(lines)
            self.nodes[vertex1Index].adjacentVerticesAndDistances[vertex2Index] = edgeLength
            self.nodes[vertex2Index].adjacentVerticesAndDistances[vertex1Index] = edgeLength
            edge = Edge(vertex1Index, vertex2Index, edgeLength)
            self.edges.Enqueue(edge)

    def Dijkstra(self, indexOfStart, indexOfDestination): #Returns the length and vertices of the shortest path
        queue = PriorityQueue()
        depths = {indexOfStart:0}
        queue.Enqueue(self.nodes[indexOfStart], depths)
        while(queue.NotEmpty()):
            node = queue.Dequeue()
            for adjacentIndex in node.adjacentVerticesAndDistances:
                if(adjacentIndex not in depths):
                    depths[adjacentIndex] = depths[node.index] + node.adjacentVerticesAndDistances[adjacentIndex]
                    queue.Enqueue(self.nodes[adjacentIndex], depths)
                elif(depths[adjacentIndex] > depths[node.index] + node.adjacentVerticesAndDistances[adjacentIndex]):
                    depths[adjacentIndex] = depths[node.index] + node.adjacentVerticesAndDistances[adjacentIndex]
                    queue.Enqueue(self.nodes[adjacentIndex], depths)
        
        path = []
        current = self.nodes[indexOfDestination]
        while(current != self.nodes[indexOfStart]):
            for adjacentIndex in current.adjacentVerticesAndDistances:
                if(depths[adjacentIndex] == depths[current.index] - current.adjacentVerticesAndDistances[adjacentIndex]):
                    path.append(current.index)
                    current = self.nodes[adjacentIndex]
                    break
        path.append(current.index)
        path.reverse()
        return depths[indexOfDestination], path

    def TopologicalSort(self):
        pass

    def Kruskal(self): #Returns a set of edges of the minimum spanning tree
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

    def Jarnik(self): #Returns a set of edges of the minimum spanning tree in format: vertex1Index vertex2Index length
        pass

    def Boruvka(self):
        pass

genericGraph = GenericGraph()
genericGraph.CreateGraph("GenericInput.txt")
#PrintGraph(genericGraph)

# length, path = genericGraph.Dijkstra(0, 7)
# print(length)
# print(path)

# edges = genericGraph.Kruskal()
# for edge in edges:
#     print("from "+str(edge.vertex1)+" to "+str(edge.vertex2)+", length: "+str(edge.length))

genericGraph.Jarnik()

