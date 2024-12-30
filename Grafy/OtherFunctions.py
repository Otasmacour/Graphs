def ShortestEdge(edges):
    shortest = edges[0]
    for edge in edges:
        if(edge.length < shortest.length):
            shortest = edge
    return shortest    

def NextDecimalNumber(string):
    result = 0
    index = 0
    while(not 48<=ord(string[index])<=57):
        index += 1
    while(index < len(string) and 48<=ord(string[index])<=57):
        result = result*10 + ord(string[index]) - 48
        index += 1
    return result, string[index+1:len(string)]
