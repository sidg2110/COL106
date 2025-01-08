class Heap:
    def __init__ (self, list):
        self.data = list
        self.index = [] 
        for i in range (0, len(list)):
            self.index.append(i)
        self.heapify()
    
    def __len__ (self):
        return len(self.data)

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
    
    def lt(self, i, j):
        if self.data[i][0] != self.data[j][0]:
            return self.data[i][0] < self.data[j][0]
        else:
            return self.data[i][1] != self.data[j][1]
    
    def upheap(self, j):
        parentData = self.parent(j)
        if (j > 0) and self.lt(j, parentData): 
            self.swapData(j, parentData)
            childBlock = self.data[j][1]
            parentBlock = self.data[parentData][1]
            self.index[childBlock] = j
            self.index[parentBlock] = parentData
            self.upheap(parentData)

    def downheap(self, j):
        if self.hasLeft(j):
            left = self.left(j)
            small_child = left
            if self.hasRight(j):
                right = self.right(j)
                if self.lt(right, left):
                    small_child = right
            if self.lt(small_child, j):
                self.swapData(j, small_child)
                parentBlock = self.data[j][1]
                childBlock = self.data[small_child][1]
                self.index[childBlock] = small_child
                self.index[parentBlock] = j
                self.downheap(small_child)

    def update(self, block, time):
        position = self.index[block]
        self.data[position][0] = time
        if position == 0:
            self.downheap(position)
        elif position != 0:
            parentIndex = self.parent(position)
            if self.lt(parentIndex, position):
                self.downheap(position)
            else:
                self.upheap(position)

    def min(self):
        item = self.data[0]
        return (item[0], item[1])
    
    def heapify(self):
        start = self.parent(len(self) - 1)
        for j in range(start, -1, -1):
            self.downheap(j)

def listCollisions(M, x, v, m, T):
    
    number = len(M)
    unsorted_list = []
    last_collision = []

    for i in range (0, number):
        last_collision.append(0)

    for i in range (0, number - 1):
        if v[i] <= v[i+1]:
            unsorted_list.append([float('inf'), i])
        else:
            time = (x[i+1] - x[i])/(v[i] - v[i+1])
            unsorted_list.append([time, i])
    
    heapData = Heap(unsorted_list)
    heapData.heapify()

    absTime = 0
    numCollisions = 0    
    listOfCollisions = []

    while (numCollisions < m) and (absTime <= T):

        (collisionTime, block) = heapData.min()
        
        heapData.update(block , float('inf'))

        if collisionTime == float('inf') or collisionTime > T:
            break

        numCollisions += 1
        absTime = collisionTime

        m1 = M[block]
        m2 = M[block + 1]
        v1 = v[block]
        v2 = v[block + 1]
        initial_position = x[block]

        v1_final = (((m1-m2)/(m1 + m2)) * v1) + (((2*m2)/(m1 + m2)) * v2)
        v2_final = (((2*m1)/(m1 + m2)) * v1) + (((m2 - m1)/(m1 + m2)) * v2)
        final_position = initial_position + v1 * (absTime - last_collision[block])

        x[block] = final_position
        x[block + 1] = final_position

        v[block] = v1_final
        v[block + 1] = v2_final

        last_collision[block] = absTime
        last_collision[block + 1] = absTime

        if block != 0:
            if v[block-1] <= v[block]:
                heapData.update(block-1 , float('inf'))
            else:
                new_position_before = x[block - 1] + v[block - 1] * (absTime - last_collision[block - 1])
                new_distance_before = x[block] - new_position_before
                new_collision_time_before = new_distance_before / (v[block-1] - v[block])
                newTime_before = absTime + new_collision_time_before
                heapData.update(block-1 , newTime_before)

        if (block != len(M) - 2) :
            if v[block + 1] <= v[block + 2]:
                heapData.update(block + 1 , float('inf'))
            else:
                new_position_after = x[block + 2] + v[block + 2] * (absTime - last_collision[block + 2])
                new_distance_after = new_position_after - x[block + 1]
                new_collision_time_after = new_distance_after / (v[block + 1] - v[block + 2])
                newTime_after = absTime + new_collision_time_after
                heapData.update(block + 1 , newTime_after)

        listOfCollisions.append((round(collisionTime, 4), block, round(final_position, 4)))

    return listOfCollisions