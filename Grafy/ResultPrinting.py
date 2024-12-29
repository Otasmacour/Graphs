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

