# Implementing max-heap class
# Priority decided by second element in tuple (here, storing size of packets i.e capacity)
class Heap:
    def __init__ (self):
        self.data = []

    def parent(self, j):
        return (j-1)//2

    def left(self, j):
        return 2*j + 1
    
    def right(self, j):
        return 2*j + 2

    def hasLeft(self, j):
        return self.left(j) < len(self.data)

    def hasRight(self, j):
        return self.right(j) < len(self.data)

    def swapData(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]
    
    def gt(self, i, j):
        return self.data[i][1] > self.data[j][1]

    def upheap(self, j):
        if j != 0:
            parentIndex = self.parent(j)
            if (j > 0) and self.gt(j, parentIndex):
                self.swapData(j, parentIndex) 
                self.upheap(parentIndex)

    def downheap(self, j):
        if self.hasLeft(j):
            left = self.left(j)
            max_child = left
            if self.hasRight(j):
                right = self.right(j)
                if self.gt(right, left):
                    max_child = right
            if self.gt(max_child, j):
                self.swapData(j, max_child)
                self.downheap(max_child)
    
    def enqueue(self, vertex):
        self.data.append(vertex)
        index = len(self.data) - 1
        self.upheap(index)
    
    def extract_max(self):
        ans = self.data[0]
        end = len(self.data) - 1
        self.swapData(0, end)
        self.data.pop()
        self.downheap(0)
        return ans

# Main function of assignment
def findMaxCapacity(n, L, s, t):
    # Input: n = number of vertices
    #        L = list of edges and their capacities
    #        s = source vertex
    #        t = target vertex

    # Representing graph as adjacency list
    # List at 'i' position is the list of neighbours of 'i' vertex
    adjacency_list = []
    for i in range (0,n):
        adjacency_list.append([])

    for i in range(0, len(L)):
        u, v, c = L[i]
        adjacency_list[u].append((v, c))
        adjacency_list[v].append((u, c))

    # The algorithm is a modified version of Dijkstra's Algorithm.

    visited_vertices = []       # Stores a bit for each vertex. If bit = 1, then that vertex has been extracted from the heap once.
    cap_list = []               # Stores the max size of packets that can be reached to a particular vertex
    parent_list = []            # Stores the vertex which is used to reach that particular vertex
    for i in range (0, n):
        visited_vertices.append(0)
        cap_list.append(-1) 
        parent_list.append(None)
 
    max_heap = Heap()
    max_heap.enqueue((s,0))
    cap_list[s] = 0
    
    while visited_vertices[t] == 0:
        vertex, curr = max_heap.extract_max()
        if visited_vertices[vertex] == 0:
            visited_vertices[vertex] = 1
            neighbours = adjacency_list[vertex]
            for i in range (0, len(neighbours)):
                nb_vertex, cap = neighbours[i]
                if visited_vertices[nb_vertex] == 0:
                    if min(cap, curr) > cap_list[nb_vertex]:
                        parent_list[nb_vertex] = vertex
                        if curr == 0:
                            cap_list[nb_vertex] = cap
                            max_heap.enqueue((nb_vertex, cap))
                        else:
                            if cap >= curr:
                                cap_list[nb_vertex] = curr
                                max_heap.enqueue((nb_vertex, curr))
                            elif cap < curr:
                                cap_list[nb_vertex] = cap
                                max_heap.enqueue((nb_vertex, cap))
    
    reverse_path = [t]
    index = t
    while index != s:
        reverse_path.append(parent_list[index])
        index = parent_list[index]
    
    path = []
    for i in range (0, len(reverse_path)):
        path.append(reverse_path[len(reverse_path)-i-1])

    return (cap_list[t], path)