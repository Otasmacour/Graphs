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
