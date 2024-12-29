from OtherFunctions import ShortestEdge

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
