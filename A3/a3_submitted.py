class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.isLeaf = False
        self.leftLeaves = []
        self.rightLeaves = []
        self.yTree = None

def build_1D_tree(data_list):

    n = len(data_list)

    if n % 2 == 1:
        median_index = n // 2
    elif n % 2 == 0:
        median_index = (n // 2) - 1
    
    node = Node(data_list[median_index])
    node.leftLeaves = data_list[0 : median_index + 1]
    node.rightLeaves = data_list[median_index + 1 :]

    if len(data_list) == 1:
        node.isLeaf = True
        node.leftLeaves = [(data_list[0])]
        node.rightLeaves = [(data_list[0])]

    else:
        node.left = build_1D_tree(data_list[0 : median_index+1])
        node.right = build_1D_tree(data_list[median_index+1 :])
    
    return node

def build_2D_tree(data_list):
    
    n = len(data_list)
    ySortedList = sorted(data_list, key=lambda x : x[1])
    
    if n % 2 == 1:
        median_index = n // 2
    elif n % 2 == 0:
        median_index = (n // 2) - 1

    node = Node(data_list[median_index])
    node.yTree = build_1D_tree(ySortedList)
    node.leftLeaves = data_list[0 : median_index + 1]
    node.rightLeaves = data_list[median_index + 1 :]

    if len(data_list) == 1:
        node.isLeaf = True

    else:
        yList = sorted(data_list, key = lambda xy: xy[1])
        node.yTree = build_1D_tree(yList)
        node.left = build_2D_tree(data_list[0 : median_index+1])
        node.right = build_2D_tree(data_list[median_index+1 :])
    return node

def find_break_node(root, min, max, dim):

    break_node = root
    while break_node != None:
        coordinate = break_node.value[dim]
        if min > coordinate:
            break_node = break_node.right
        elif max < coordinate:
            break_node = break_node.left
        elif min <= coordinate <= max:
            break
    return break_node

def search_query_1D(root, min, max, dim):

    results = []
    node = find_break_node(root, min, max, dim)
    
    if node == None:
        return []

    if node.isLeaf:
        results.append(node.value)
    
    query_node_min = node.left
    while query_node_min != None:
        if min <= query_node_min.value[dim]:
            results += query_node_min.rightLeaves
            query_node_min = query_node_min.left
        elif min > query_node_min.value[dim]:
            query_node_min = query_node_min.right
    

    query_node_max = node.right
    while query_node_max != None:
        if max >= query_node_max.value[dim]:
            results += query_node_max.leftLeaves
            query_node_max = query_node_max.right
        elif max < query_node_max.value[dim]:
            query_node_max = query_node_max.left

    return results

class PointDatabase:

    def __init__(self, list):
        
        listSorted = sorted(list, key=lambda x:x[0])
        if len(list) != 0:
            self.root = build_2D_tree(listSorted)
        else:
            self.root = None

    def searchNearby(self, queryPoint, distance):
        (x,y) = queryPoint
        x_min = x - distance
        x_max = x + distance
        y_min = y - distance
        y_max = y + distance

        results = []
        x_node = find_break_node(self.root, x_min, x_max, 0)
        if x_node == None:
            return []

        if x_node.isLeaf and y_min <= x_node.value[1] <= y_max:
            results.append(x_node.value)

        query_node_min = x_node.left
        while query_node_min != None:
            if not query_node_min.isLeaf:
                if x_min <= query_node_min.value[0]:
                    yRightChild = query_node_min.right.yTree
                    ans = search_query_1D(yRightChild, y_min, y_max, 1)
                    results += ans
                    query_node_min = query_node_min.left
                
                elif x_min > query_node_min.value[0]:
                    query_node_min = query_node_min.right
            else:
                x = query_node_min.value[0]
                y = query_node_min.value[1]
                if (x_min < x < x_max) and (y_min < y < y_max):
                    results.append((x,y))
                query_node_min = None

        query_node_max = x_node.right

        while query_node_max != None:
            if not query_node_max.isLeaf:
                if x_max >= query_node_max.value[0]:
                    yLeftChild = query_node_max.left.yTree
                    ans = search_query_1D(yLeftChild, y_min, y_max, 1)
                    results += ans
                    query_node_max = query_node_max.right
                
                elif x_max < query_node_max.value[0]:
                    query_node_max = query_node_max.left
            else:
                x = query_node_max.value[0]
                y = query_node_max.value[1]
                if (x_min < x < x_max) and (y_min < y < y_max):
                    results.append((x,y))
                query_node_max = None
        return results