import math
INT_MAX = math.inf
 
class Node:
    def __init__(self, **kwargs):
        if 'node_data' in kwargs:
            self.node_data = kwargs['node_data']
        else:
            self.node_data = None
        
        if 'neighbors' in kwargs:
            self.neighbors = kwargs['neighbors']
        else:
            self.neighbors = []
        
        if 'edges' in kwargs:
            self.edges = kwargs['edges']
        else:
            self.edges = []

        if 'key' in kwargs:
            self.key = kwargs['key']
        else:
            self.key = INT_MAX

        if 'parent' in kwargs:
            self.parent = kwargs['parent']
        else:
            self.parent = None

    def add_neighbor(self, node):
        self.neighbors.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def compare(self, other):
        if self.key < other.key:
            return -1
        elif self.key == other.key:
            return 0
        elif self.key > other.key:
            return 1

class MSTEdge:
    def __init__(self, node1, node2, weight):
        self.node1 = node1
        self.node2 = node2
        self.weight= weight


class Edge:
    def __init__(self, node1, node2, weight):
        self.node1 = node1
        self.node2 = node2
        self.weight= weight

    def hash_key(self):
        return str(self.node1.node_data) + "->" + str(self.node2.node_data)
    
    def compare(self, other):
        if self.weight < other.weight:
            return -1
        elif self.weight == other.weight:
            return 0
        elif self.weight > other.weight:
            return 1

class Graph:
    node_list = {}
    edges = {}
    def __init__(self,node_list = {}, edges = {}):
        self.node_list = node_list
        self.edges = edges

    def add_node(self, node):
        self.node_list[str(node.node_data)] = node

    def find_node_by_element(self, element):
        return self.node_list[element]
    
    def add_undirected_edge(self, node_from, node_to, weight):
        edge1 = Edge(node_from, node_to, weight)
        edge2 = Edge(node_to, node_from, weight)

        if (not(edge1.hash_key() in self.edges) and not(edge2.hash_key() in self.edges)):
            
            self.node_list[node_from.node_data].add_neighbor(node_to)
            self.node_list[node_from.node_data].add_edge(edge1)

            self.node_list[node_to.node_data].add_neighbor(node_from)
            self.node_list[node_to.node_data].add_edge(edge1)

    def add_directed_edge(self, node_from, node_to, weight):
        edge = Edge(node_from, node_to, weight)
        self.edges[edge.hash_key] = weight

        self.node_list[node_from.node_data].add_neighbor(node_to)
        self.node_list[node_from.node_data].add_edge(edge)

    def update_all_nodes_to_distance(self, distance):
        for node in self.node_list:
            node.key = distance
    
    def print_graph(self):
        print("printing graph")
        for node in self.node_list:
            print("Node (" + str(node.node_data) + ")")
            print("Node Neighbors : ")
            index = 0
            for neighbor in node.neighbors:
                print(str(neighbor.node_data) + ' edge ' + str(index) + " " + str(neighbor.edges[index]))
                index += 1

    def minimum_spanning_tree(self):
        mst = Prim_MST()
        return mst.minimum_spanning_tree

    def minimum_spanning_tree_edges(self, edges):
        mst_edges = []
        for edge in edges:
            mst_edge = MSTEdge(str(edge.node1.node_data), str(edge.node1.node_data), edge.weight)
            mst_edges.append(mst_edge)
        return mst_edges


class graph_builder:
    def build_graph(self, object_list):
        graph = Graph()
        for object in object_list:
            node = Node(node_data = object)
            graph.add_node(node)

        return graph

class Prim_MST:
    def __init__(self, graph):
        self.graph = graph
        self.included_nodes = {}
        self.included_edges = []
        self.excluded_nodes = {}
        self.min_heap = MinHeap()

    def minimum_Spanning_trees(self):
        self.graph.update_all_nodes_to_distance(INT_MAX)

        index = 0
        for  node in self.graph.node_list:
            if index == 0:
                node.key = 0
            self.excluded_nodes[node.node_data] = node
            self.min_heap.append(node)
            index += 1

        while len(self.excluded_nodes) > 0:
            min_node = self.min_heap.extract_min()

            min_edge = self.find_min_edge(min_node, self.min_heap, self.included_nodes)

            if min_edge is not None:
                self.included_edges.append(min_edge)

            self.incldued_nodes[min_node.node_data] = min_node
            self.excluded_nodes.pop(min_node.node_data)


        if len(self.inlcuded_edges) == len(self.graph.node_list) - 1:
            return self.included_edges 
        else:
            return None

    def find_min_edge(self, min_node, min_heap, included_nodes):
        min_edge_weight = INT_MAX
        min_edge_index = None
        index = 0
        for neighbor in min_node.neighbors:
            if min_node.edges[index].weight < neighbor.key:
                neighbor.parent = min_node.node_data
                neighbor.key = min_node.edges[index].weight

                if min_heap.contains_element(neighbor):
                    min_heap.delete_element(neighbor)
                    min_heap.append(neighbor)

            if min_node.edges[index].weight < min_edge_weight and neighbor.node_data in included_nodes:
                min_edge_weight = min_node.edges[index].weight
                min_edge_index = index
            index += 1

        if min_edge_index is not None:
            min_edge = min_node.edges[min_edge_index] 
        return min_edge

class minHeap:
    def __init__(self):
        self.elements = [None]
        self.element_position_map = {}
    
    def append(self, element):
        self.elements.append(element)
        self.element_position_map[element.node_data] = self.elements.size - 1

        self.__sift_up(len(self.elements) - 1)

    def __sift_up(self, index):
        # we get the parent of the index so we can see if it is larger than the new node
        parent_index = (index / 2)

        # we get the parent of the index so we can see if it is larger than the new node
        if index <= 1:
            return index
        
        if self.elements[index] >= self.elements[parent_index]:
            return 

        # otherwise we exchange the two - the smaller element goes into the parent location
        self.__exchange(index, parent_index)

        # and we recursively call this method to keep sifting up the smaller element
        self.__sift_up(parent_index)

    def __exchange(self, source_index, target_index):
        tmp_source = self.elements[source_index]
        tmp_target = self.elements[target_index]

        source_element_position = self.element_position_map[tmp_source.node_data]
        target_element_position = self.element_position_map[tmp_target.node_data]

        self.elements[source_index] = tmp_target
        self.elements[target_index] = tmp_source

        self.element_position_map[tmp_source.node_data] = target_element_position
        self.element_position_map[tmp_target.node_data] = source_element_position
        
    def count(self):
        return (len(self.elements) - 1)

    def elements_remove_nil(self):
        return self.elements.pop(0) # make sure nil element is removed

    # get the minimum value from the heap
    def peek_min(self):
        return self.elements[1]

    # return the actual elements and re-heapify the minheap
    def extract_min(self):
         # exchange the minimum element with the last one in the list
        self.__exchange(1, len(self.elements) - 1)

        # remove the last element
        min_element = self.elements.pop()
        self.element_position_map.remove(min_element.node_data)

        # make sure the tree is ordered - call the helper method to sift down the new root node into appropriate position
        self.__sift_down(1)

        # return the min element
        return min_element

    def contains_element(self, element):
        if self.element_position_map.has_key(element.node_data):
            return True
        else:
            return False


    def delete_element(self, element):
        element_position = self.element_position_map[element.node_data]

        if element_position is not None:
            # exchange the element with the last one in the list
            self.__exchange(element_position, len(self.elements) - 1)

            # remove the last element
            element_to_remove = self.elements.pop()
            self.element_position_map.pop(element_to_remove.node_data) # Check if this works

            # make sure the tree is ordered - call the helper method to sift down the new root node into appropriate position
            self.__sift_down(element_position)

            return element_to_remove

    def print_heap(self):
        print('printing min heap')

        for element in elements:
            if element is None:
                print("None")
            else:
                print(str(element.node_data))
    
     
    def __sift_down(self, index):

        # get the first child (the left child)
        child_index = (index * 2)

        # if the child index is greater than the size of the array it does not exist and we can return
        if child_index > len(elements) - 1:
            return True
        else:
            return False

        # determine the greater of the two children (if they both exist - and set the child index)
        if child_index < len(elements) - 1:
            not_the_last_element = True
        else :
            not_the_last_element = False    
        
        left_child = self.elements[child_index]
        right_child = self.elements[child_index + 1]

        # find the smallest of the two children
        if not_the_last_element and right_child < left_child:
            child_index += 1
    

        # if the element at the current index is smaller than the children, return
        if self.elements[index] <= self.elements[child_index]:
            return True 
        else:
            return False

        # exchange the larger index with the smaller child
        self.__exchange(index, child_index)

        # keep sifting down, this time from the farther along child index
        self.__sift_down(child_index)