
import math

DATA_FILE = 'karate-network.csv'

def main():
    graph = load_matrix(DATA_FILE)
    kl = KernighanLin(graph)
    kl.start()

def load_matrix(filename):
    with open(filename) as f:
        edges = []
        vertex_ids = []
        vertex = []
        for row in f:
            left, right = row.rstrip("\n").split(',')
            left = int(left)
            right = int(right)
            edges.append(Edge(left, right))
            if left not in vertex_ids:
                vertex_ids.append(left)
                vertex.append(Vertex(left))
            if right not in vertex_ids:
                vertex_ids.append(right);
                vertex.append(Vertex(right))
    return Graph(vertex, edges)

class Edge(object):
    def __init__(self, left, right):
        self.left_id = left
        self.right_id = right

    def set_left_vertex(self, left_vrtx):
        self.left_vertex = left_vrtx
        left_vrtx.add_edge(self)

    def set_right_vertex(self, right_vrtx):
        self.right_vertex = right_vrtx
        right_vrtx.add_edge(self)

class Vertex(object):
    def __init__(self, id):
        self.id = id
        self.edges = []

    def get_id(self):
        return self.id
    def get_edges(self):
        return self.edges
    def get_group(self):
        return self.group
    def set_group(self, group):
        self.group = group
    def add_edge(self, edge):
        for existing_edge in self.edges:
            if existing_edge.left_id == edge.right_id and existing_edge.right_id == edge.left_id:
                return
        self.edges.append(edge)

    def get_cost(self):
        cost = 0

        for edge in self.edges:
            if edge.left_id != self.id:
                other_vertex = edge.left_vertex
            elif edge.right_id != self.id:
                other_vertex = edge.right_vertex

            if other_vertex.group != self.group:
                cost += 1
            else:
                cost -= 1

        return cost


class Graph(object):
    def __init__(self, vertex, edges):
        self.vertex = vertex
        self.__vertex_map = {vx.get_id() : vx for vx in self.vertex}
        self.edges = edges
        self.cut_size = len(self.vertex)/2
        self.create_random_groups()
        self.__create_links()

    def __create_links(self):
        links_map = {}
        for edge in self.edges:
            edge.set_left_vertex(self.__vertex_map[edge.left_id])
            edge.set_right_vertex(self.__vertex_map[edge.right_id])

    def create_random_groups(self):
        self.group_a = []
        self.group_b = []
        for i in range(self.cut_size):
            self.vertex[i].set_group('A')
            self.group_a.append(self.vertex[i])
        for i in range(self.cut_size, len(self.vertex)):
            self.vertex[i].set_group('B')
            self.group_b.append(self.vertex[i])

    def get_random_groups(self):
        return self.group_a, self.group_b

    def get_groups(self):
        a_group = []
        b_group = []
        for vertex in self.vertex:

            if vertex.get_group() == 'A':
                a_group.append(vertex)
            elif vertex.get_group() == 'B':
                b_group.append(vertex)
        return a_group, b_group

    def get_cut_size(self):
        return self.cut_size

    def get_edges(self):
        return self.edges
    def get_vertexs(self):
        return self.vertex


class KernighanLin(object):
    def __init__(self, graph):
        self.graph = graph

    def start(self):
        self.group_a_unchosen, self.group_b_unchosen = \
            self.graph.get_random_groups()
        cut_size = self.graph.get_cut_size()
        nominal_cut_size = float("Inf")
        
        min_id = -1
        self.swaps = []
        while self.get_nominal_cut_size() < nominal_cut_size:
            nominal_cut_size = self.get_nominal_cut_size()
            min_cost = float("Inf")
            for i in range(cut_size):
                self.single_swaps()
                cost = self.get_nominal_cut_size()
                if cost < min_cost:
                    min_cost = cost
                    min_id = i
            
            # Undo swaps done after the minimum was reached
            for i in range(min_id+1, cut_size):
                vertice_b, vertice_a = self.swaps[i]
                self.do_swap((vertice_a, vertice_b))

            self.group_a_unchosen, self.group_b_unchosen = \
            self.graph.get_groups()

            print('============')


        self.print_result()

    def single_swaps(self):
        best_pair = False
        best_heuristic = -1 * float("Inf")

        for vertice_a in self.group_a_unchosen:
            for vertice_b in self.group_b_unchosen:
                cost_edge = len(set(vertice_a.get_edges()).intersection(vertice_b.get_edges()))
                heuristic = vertice_a.get_cost() + vertice_b.get_cost() - 2*cost_edge
                if heuristic > best_heuristic:
                    best_heuristic = heuristic
                    best_pair = vertice_a, vertice_b
        if best_pair:
            vertice_a, vertice_b = best_pair
            self.group_a_unchosen.remove(vertice_a)
            self.group_b_unchosen.remove(vertice_b)
            self.do_swap((vertice_a, vertice_b))
            self.swaps.append(best_pair)

            return best_heuristic
        else:
            raise Exception('empty maximum')
    
    def get_nominal_cut_size(self):
        cost = 0
        for edge in self.graph.get_edges():
            if edge.left_vertex.get_group() != edge.right_vertex.get_group():
                cost += 1

        return cost


    def do_swap(self, vertices):
        vertice_a, vertice_b = vertices

        vertice_a.set_group('B')
        vertice_b.set_group('A')

    def print_result(self):
        values = {v.id: v.get_group() for v in self.graph.get_vertexs()}
        str_out = "["
        for key in values.iterkeys():
            if values[key] == 'A':
                val = '1'
            else:
                val = '0'
            str_out += "%s ;" % val
        str_out += "]"
        print("Paste this \"state\" vector in the matlab graphviz script..  ")
        print(str_out)

if __name__ == "__main__":
    main()