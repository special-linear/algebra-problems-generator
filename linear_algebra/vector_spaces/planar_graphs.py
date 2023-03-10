import itertools
import random
import math
import sys
import collections

from linear_algebra.common import *

from problem import Problem


def dist(a, b):
    return math.sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1]))


# check whether p lies on the line segment [s,d] assuming it lies on the line
def point_on_segment(s, d, p):
    return dist(s, p)+dist(p, d)-dist(s, d) < 0.1


def line_intersect_badly(e1, e2):
    Ax, Ay, Bx, By = e1[0][0], e1[0][1], e1[1][0], e1[1][1]
    Cx, Cy, Dx, Dy = e2[0][0], e2[0][1], e2[1][0], e2[1][1]
    crA = (Cx-Dx)*(Ay-Cy)-(Cy-Dy)*(Ax-Cx)
    crB = (Cx-Dx)*(By-Cy)-(Cy-Dy)*(Bx-Cx)
    crC = (Ax-Bx)*(Cy-Ay)-(Ay-By)*(Cx-Ax)
    crD = (Ax-Bx)*(Dy-Ay)-(Ay-By)*(Dx-Ax)
    crs = [crA, crB, crC, crD]
    z = len(list(filter(lambda x: x == 0, crs)))
    ABonCD = len([p for p in e1 if point_on_segment(e2[0], e2[1], p)])
    CDonAB = len([p for p in e2 if point_on_segment(e1[0], e1[1], p)])
    if z == 0:
        return crA*crB < 0 and crC*crD < 0
    elif z == 1:
        return bool(ABonCD) or bool(CDonAB)
    elif z == 2:
        return False
    elif z == 4:
        return (ABonCD, CDonAB) in [(2, 1), (2, 0), (1, 2), (0, 2)] or\
               (ABonCD, CDonAB) == (1, 1) and len({e1[0], e1[1], e2[0], e2[1]}) == 4
    else:
        raise Exception('impossible z')


class LatticePlanarGraph:
    def __init__(self):
        self.vertices, self.adj_m = self.gen_lattice_planar_graph(7)
        self.st = self.find_spanning_tree()
        self.cb = self.find_cycle_basis()

    def render_tikz(self):
        v_str = ' '.join("\\node[vertex] (e{}) at {} {{}};".format(v[0], v[1]) for v in enumerate(self.vertices))
        v_num = len(self.vertices)
        e_list = ((i, j) for i in range(v_num) for j in range(i+1, v_num) if self.adj_m[i][j] == 1)
        e_str = ' '.join("\draw[edge] (e{}) to (e{});".format(e[0], e[1]) for e in e_list)
        return "\\begin{{tikzpicture}}\n{}\n{}\n\end{{tikzpicture}}".format(v_str, e_str)

    def render_tikz_subgraph(self, g):
        v_num = len(self.vertices)
        e_list = ((i, j) for i in range(v_num) for j in range(i + 1, v_num) if self.adj_m[i][j] == 1)
        g_v = {i for i in range(v_num) if any(g[i])}
        v_str = ' '.join(
            "\\node[{}] (e{}) at {} {{}};".format('vertex' if v[0] in g_v else 'shadow-vertex', v[0], v[1]) for v in
            enumerate(self.vertices))
        e_str = ' '.join(
            "\draw[{}] (e{}) to (e{});".format('edge' if g[e[0]][e[1]] else 'shadow-edge', e[0], e[1]) for e in
            e_list)
        return "\\begin{{tikzpicture}}[scale=0.5]\n{}\n{}\n\end{{tikzpicture}}".format(v_str, e_str)

    @staticmethod
    def gen_lattice_planar_graph(cs_dim):
        v_num = 8
        e_num = cs_dim-1+v_num
        width = 4
        lattice_points = {(i, j) for i in range(width) for j in range(3)} #if (i+j) % 2 == 1}
        lattice_points.difference_update([(0, 0), (0, 2), (width-1, 0), (width-1, 2)])
        graph_is_good = False
        c = 0
        what_is_bad = collections.Counter({'planar': 0, 'well_connected': 0})
        while not graph_is_good:
            vertices = random.sample(lattice_points, v_num)
            adj_m = [[0 for _ in range(v_num)] for __ in range(v_num)]
            count = 0
            e_list = [(i, j) for i in range(v_num) for j in range(i + 1, v_num) if adj_m[i][j] == 1]
            graph_is_planar = True
            while count < e_num:
                tries = 0
                while tries < 10:
                    i, j = random.sample(range(v_num), 2)
                    if adj_m[i][j] == 0:
                        tries += 1
                        if not any(
                                line_intersect_badly((vertices[e[0]], vertices[e[1]]), (vertices[i], vertices[j])) for e
                                in e_list) or not e_list:
                            adj_m[i][j], adj_m[j][i] = 1, 1
                            e_list.append((i, j))
                            count += 1
                            break
                else:
                    graph_is_planar = False
                    break
            graph_is_well_connected = all(sum(x > 0 for x in r) > 1 for r in adj_m)
            if not graph_is_well_connected:
                what_is_bad['well_connected'] += 1
            graph_is_good = graph_is_well_connected and graph_is_planar
            c += 1
            sys.stdout.write('\r{} {} {} '.format(c, what_is_bad['well_connected'], what_is_bad['planar']))
            sys.stdout.flush()
        sys.stdout.write('\r')
        sys.stdout.flush()
        return vertices, adj_m

    def find_spanning_tree(self):
        v_num = len(self.vertices)
        st_adj_m = [[0 for _ in range(v_num)] for __ in range(v_num)]
        e_list = [(i, j) for i in range(v_num) for j in range(i + 1, v_num) if self.adj_m[i][j] == 1]
        st_v = {e_list[0][0]}
        while True:
            new_vs = set([])
            for v in st_v:
                for e in e_list:
                    if v == e[0] and e[1] not in st_v and e[1] not in new_vs \
                            or v == e[1] and e[0] not in st_v and e[0] not in new_vs:
                        new_vs.update(e)
                        new_vs.remove(v)
                        st_adj_m[e[0]][e[1]], st_adj_m[e[1]][e[0]] = 1, 1
            if not new_vs:
                break
            st_v.update(new_vs)
        return st_adj_m

    def find_path_in_st(self, v1, v2):
        v_num = len(self.vertices)
        paths = [[v1]]
        while True:
            new_paths = []
            for path in paths:
                for v in range(v_num):
                    if v not in path and self.st[path[0]][v]:
                        new_paths.append([v]+path)
            paths = new_paths
            for path in paths:
                if v2 == path[0]:
                    return path

    def find_cycle_basis(self):
        v_num = len(self.vertices)
        rem_edges = [(i, j) for i in range(v_num) for j in range(i + 1, v_num)
                     if self.adj_m[i][j] == 1 and self.st[i][j] == 0]
        cycle_basis = []
        for e in rem_edges:
            cycle = self.find_path_in_st(*e)
            cycle_adj_m = [[int(i in cycle and j in cycle and self.st[i][j] == 1) for i in range(v_num)] for j in range(v_num)]
            cycle_adj_m[e[0]][e[1]], cycle_adj_m[e[1]][e[0]] = 1, 1
            cycle_basis.append(cycle_adj_m)
        return cycle_basis


class CycleSpaceSubspaces(Problem):
    def __init__(self):
        self.graph, self.U_adj_ms, self.V_adj_ms = self.gen_cycle_space_subspaces()

    def render(self):
        return "Рассмотрим граф\n\\begin{{center}}\n{}\n\end{{center}}\nи два семейства его эйлеровых подграфов\n" \
               "\\begin{{align*}}\n" \
               "& \\begin{{tikzpicture}}[baseline=(base.base)]" \
               "\\node(base) at (0,0) {{}};" \
               "\\node at (0,0.5) {{$A\colon$}};" \
               "\end{{tikzpicture}}\quad\n{}\n\\\\\n" \
               "& \\begin{{tikzpicture}}[baseline=(base.base)]" \
               "\\node(base) at (0,0) {{}};" \
               "\\node at (0,0.5) {{$B\colon$}};" \
               "\end{{tikzpicture}}\quad\n{}\n\end{{align*}}\n" \
               "Найти все подграфы, которые можно получить операцией симметрической разности" \
               " как из набора $A$, так и из набора $B$.\nДля каждого такого подграфа предъявить" \
               " его разложения на элементы $A$ и $B$.\nСколько различных подграфов можно получить" \
               " операцией симметрической разницы из объединения наборов $A$ и $B$?".format(
            self.graph.render_tikz(),
            '\n\quad\n'.join(self.graph.render_tikz_subgraph(sg) for sg in self.U_adj_ms),
            '\n\quad\n'.join(self.graph.render_tikz_subgraph(sg) for sg in self.V_adj_ms)
        )

    @staticmethod
    def gen_cycle_space_subspaces():
        graph = LatticePlanarGraph()
        U = sp.Matrix([[1, 0, 0, 1],
                       [0, 1, 0, 0],
                       [0, 0, 1, 1],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0]])
        V = sp.Matrix([[1, 0, 0, 1],
                       [1, 0, 0, 1],
                       [1, 0, 1, 0],
                       [0, 1, 1, 1],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0]])
        c = gen_glzmz_matrix2(7, modulo=2)
        cU = c*U
        cV = c*V
        mod2 = lambda x: x % 2
        basis = [sp.Matrix(e) for e in graph.cb]
        U_adj_ms = []
        for c in (cU.col(i) for i in range(4)):
            subgraph = sp.zeros(len(graph.vertices))
            for x, e in zip(sp.utilities.iterables.flatten(c), basis):
                subgraph += x*e
                subgraph = subgraph.applyfunc(mod2)
            U_adj_ms.append(subgraph.tolist())
        V_adj_ms = []
        for c in (cV.col(i) for i in range(4)):
            subgraph = sp.zeros(len(graph.vertices))
            for x, e in zip(sp.utilities.iterables.flatten(c), basis):
                subgraph += x * e
                subgraph = subgraph.applyfunc(mod2)
            V_adj_ms.append(subgraph.tolist())
        return graph, U_adj_ms, V_adj_ms
