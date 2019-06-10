def insert_edge(g,src, dest, weight):
    
    if src not in g:
        print("Vertex " + str(src) + " not in graph")
    elif dest not in g:
        print("Vertex " + str(dest) + " not in graph")
    elif weight <= 0:
        print("Weight cannot be Zero or Negative.")
    else :
        if not g.contains_edge(src, dest):
            g.add_edge(src, dest, weight)
            g.add_edge(dest, src, weight)

            print("Edge Created.")
        else:
            print("Edge Already Exists.")
    return g


class Vertex:

    def __init__(self, key):
        self.key = key
        self.neighbors = {}

    def get_key(self):
        return self.key

    def add_neighbor(self, dest, weight):
        self.neighbors[dest] = weight

    def get_neighbors(self):
        return self.neighbors.keys()

    def get_weight(self, dest):
        return self.neighbors[dest]

    def is_neighbor(self, dest):
        return dest in self.neighbors

class Graph:
    
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, key):
        vertex = Vertex(key)
        self.vertices[key] = vertex

    def get_vertex(self, key):
        return self.vertices[key]

    def __contains__(self, key):
        return key in self.vertices 
    
    def add_edge(self, src_key, dest_key, weight = 1):
        self.vertices[src_key].add_neighbor(self.vertices[dest_key], weight)

    def contains_edge(self, src_key, dest_key):
        return self.vertices[src_key].is_neighbor(self.vertices[dest_key])



    def print_graph(self):
        print("printing graph")
        print('Vertices: ', end='')
        for v in self:
            print(v.get_key(), end=' ')
        print()
 
        print('Edges: ')
        for v in self:
            for dest in v.get_neighbors():
                w = v.get_weight(dest)
                print('(src={}, dest={}, weight={}) '.format(v.get_key(),
                                                             dest.get_key(), w))

    def __len__(self):
        return len(self.vertices)
    
    def __iter__(self):
        return iter(self.vertices.values())

def mst_prim(g):
    """Return a minimum cost spanning tree of the connected graph g."""
    mst = Graph() # create new Graph object to hold the MST
 
    # if graph is empty
    if not g:
        return mst
 
    # nearest_neighbour[v] is the nearest neighbour of v that is in the MST
    # (v is a vertex outside the MST and has at least one neighbour in the MST)
    nearest_neighbour = {}
    # smallest_distance[v] is the distance of v to its nearest neighbour in the MST
    # (v is a vertex outside the MST and has at least one neighbour in the MST)
    smallest_distance = {}
    # v is in unvisited iff v has not been added to the MST
    unvisited = set(g)
 
    u = next(iter(g)) # select any one vertex from g
    mst.add_vertex(u.get_key()) # add a copy of it to the MST
    unvisited.remove(u)
 
    # for each neighbour of vertex u
    for n in u.get_neighbors():
        if n is u:
            # avoid self-loops
            continue
        # update dictionaries
        nearest_neighbour[n] = mst.get_vertex(u.get_key())
        smallest_distance[n] = u.get_weight(n)
 
    # loop until smallest_distance becomes empty
    while (smallest_distance):
        # get nearest vertex outside the MST
        outside_mst = min(smallest_distance, key=smallest_distance.get)
        # get the nearest neighbour inside the MST
        inside_mst = nearest_neighbour[outside_mst]
 
        # add a copy of the outside vertex to the MST
        mst.add_vertex(outside_mst.get_key())
        # add the edge to the MST
        mst.add_edge(outside_mst.get_key(), inside_mst.get_key(),
                     smallest_distance[outside_mst])
        mst.add_edge(inside_mst.get_key(), outside_mst.get_key(),
                     smallest_distance[outside_mst])
 
        # now that outside_mst has been added to the MST, remove it from our
        # dictionaries and the set unvisited
        unvisited.remove(outside_mst)
        del smallest_distance[outside_mst]
        del nearest_neighbour[outside_mst]
 
        # update dictionaries
        for n in outside_mst.get_neighbors():
            if n in unvisited:
                if n not in smallest_distance:
                    smallest_distance[n] = outside_mst.get_weight(n)
                    nearest_neighbour[n] = mst.get_vertex(outside_mst.get_key())
                else:
                    if smallest_distance[n] > outside_mst.get_weight(n):
                        smallest_distance[n] = outside_mst.get_weight(n)
                        nearest_neighbour[n] = mst.get_vertex(outside_mst.get_key())
 
    return mst


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

        for element in self.elements:
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