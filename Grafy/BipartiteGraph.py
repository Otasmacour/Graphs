from GraphParts import Edge, Vertex
from OtherFunctions import NextDecimalNumber
from LinkedLists import PriorityQueueByDepths

class BipartiteGraph:

    def CreateGraph(self, inputFileName):
        lines = open("Inputs/"+inputFileName).read()
        leftNumber, lines = NextDecimalNumber(lines)
        rightNumber, lines = NextDecimalNumber(lines)
        self.leftVertices = []
        self.rightVertices = []
        for i in range(leftNumber):
            vertexL = Vertex(i)
            vertexL.leftYesOrNot = True
            self.leftVertices.append(vertexL)
            self.rightVertices.append(None)
        for i in range(rightNumber):
            vertexR = Vertex(i+leftNumber)
            self.rightVertices.append(vertexR)
        for i in range(leftNumber):
            numberOfEdges, lines = NextDecimalNumber(lines)
            leftVertex = self.leftVertices[i]
            for _ in range(numberOfEdges):
                rightVertexIndex, lines = NextDecimalNumber(lines)
                rightVertex = self.rightVertices[rightVertexIndex]
                edge = Edge(i, rightVertexIndex, None)
                leftVertex.edges.append(edge)
                rightVertex.edges.append(edge)

    def HopcroftKarp(self): #returns a set edges that form a maximal pairing in the given graph
        leftNotThereIndices = []
        rightNotThereIndices = []
        edgesOn = set()
        for leftVertex in self.leftVertices:
            leftNotThereIndices.append(leftVertex.index)
        for rightVertex in self.rightVertices:
            if(rightVertex != None): rightNotThereIndices.append(rightVertex.index)

        while(leftNotThereIndices!=[] and rightNotThereIndices!=[]):
            for leftStart in leftNotThereIndices:
                #Finding the right vertex that is not there and that is reachable by a path from the left starting point
                #If found, the right recognize as it is there, the left too and following the path set all used edges as not used and the not used as used
                #Then break the for cycle, so it can try again some another vertex
                depthsByIndices = {leftStart:0}
                indexOfFoundRight = None
                queue = PriorityQueueByDepths()
                queue.Enqueue(self.leftVertices[leftStart], depthsByIndices)
                notFound = True
                while(queue.NotEmpty() and notFound):
                    vertex = queue.Dequeue()
                    for edge in vertex.edges:
                        otherVertexIndex = edge.TheIndexOfTheOtherVertex(vertex.index)
                        otherVertex = None
                        if(otherVertexIndex > len(self.leftVertices) - 1): #The "vertex" is left
                            otherVertex = self.rightVertices[otherVertexIndex]
                        else: #The "vertex" is right
                            otherVertex = self.leftVertices[otherVertexIndex]

                        if(otherVertexIndex not in depthsByIndices):
                            depthsByIndices[otherVertexIndex] = depthsByIndices[vertex.index] + 1
                            queue.Enqueue(otherVertex, depthsByIndices)
                        elif(depthsByIndices[otherVertexIndex] > depthsByIndices[vertex.index]):
                            depthsByIndices[otherVertexIndex] = depthsByIndices[vertex.index] + 1
                            queue.Enqueue(otherVertex, depthsByIndices)
                        if(otherVertexIndex in rightNotThereIndices):
                            indexOfFoundRight = otherVertexIndex
                            notFound = False
                            break
                if(not notFound):
                    #Now i have to chech, if it is really an augment path by increasing len edgesOn by 1 in total
                    increaseRatio = 0
                    current = self.rightVertices[indexOfFoundRight]
                    while(current != self.leftVertices[leftStart]):
                        for edge in current.edges:
                                adjacentIndex = edge.TheIndexOfTheOtherVertex(current.index)
                                if(adjacentIndex in depthsByIndices):
                                    if(depthsByIndices[adjacentIndex] == depthsByIndices[current.index] - 1):
                                        if(current.index > len(self.leftVertices) - 1): #current is now right
                                            current = self.leftVertices[adjacentIndex]
                                        else: #current is now left
                                             current = self.rightVertices[adjacentIndex]
                                        if(edge in edgesOn):
                                            increaseRatio -= 1
                                        else:
                                            increaseRatio += 1
                                        break
                    if(increaseRatio == 1):
                        rightNotThereIndices.remove(indexOfFoundRight)
                        leftNotThereIndices.remove(leftStart)
                        current = self.rightVertices[indexOfFoundRight]
                        while(current != self.leftVertices[leftStart]):
                            for edge in current.edges:
                                adjacentIndex = edge.TheIndexOfTheOtherVertex(current.index)
                                if(adjacentIndex in depthsByIndices):
                                    if(depthsByIndices[adjacentIndex] == depthsByIndices[current.index] - 1):
                                        if(current.index > len(self.leftVertices) - 1): #current is now right
                                            current = self.leftVertices[adjacentIndex]
                                        else: #current is now left
                                             current = self.rightVertices[adjacentIndex]
                                        if(edge in edgesOn):
                                            edgesOn.remove(edge)
                                        else:
                                            edgesOn.add(edge)
                                        break
                        break #from the for cycle
        return edgesOn
