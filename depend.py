#! /usr/bin/env python2

from collections import defaultdict
from copy import deepcopy


class DiGraph(object):
    """
    Directed Grapah
    """

    def __init__(self):
        """
        self.d :: {source vertex: [destination vertexes]}
        self.v :: {[vertexes]}
        """
        self.d = defaultdict(list)
        self.v = []

    def vertexes(self):
        """
        return all vertexes
        self -> [vertex]
        """
        return self.v

    def addVertexes(self, vs):
        """
        add vertexes to Directed Graph
        self -> [vertex] -> None
        """
        for v in vs:
            self.addVertex(v)

    def addVertex(self, v):
        """
        add vertex to Directed Graph
        self -> vertex -> None
        >>> dg = DiGraph()
        >>> dg.addVertex(1)
        >>> dg.vertexes()
        [1]
        >>> dg.addVertexes([1, 2, 3])
        >>> dg.vertexes()
        [1, 2, 3]
        """
        if v not in self.v:
            self.v.append(v)

    def edges(self):
        """
        return all edges
        self -> [(source vertex, destination vertex)]
        """
        r = []
        for b, ends in self.d.iteritems():
            for e in ends:
                r.append([b, e])
        return r

    def addEdges(self, bgns, ends):
        """
        add edges to Directed Graph
        self -> [source vertex] -> [destination vertex] -> None
        """
        for b in bgns:
            for e in ends:
                self.addEdge(b, e)

    def addEdge(self, bgn, end):
        """
        add edge to Directed Graph
        self -> source vertex -> destionation vertex -> None
        >>> dg = DiGraph()
        >>> dg.addEdges([1, 2], [4, 5, 6])
        >>> dg.vertexes()
        [1, 4, 5, 6, 2]
        >>> dg.edges()
        [[1, 4], [1, 5], [1, 6], [2, 4], [2, 5], [2, 6]]
        """
        self.addVertex(bgn)
        self.addVertex(end)
        self.d[bgn].append(end)

    def dfs(self, v0):
        """
        >>> dg = DiGraph()
        >>> dg.addEdges([1], [3, 4])
        >>> dg.addEdges([2], [4])
        >>> dg.addEdges([3], [5])
        >>> dg.addEdges([4], [5, 6])
        >>> dg.edges()
        [[1, 3], [1, 4], [2, 4], [3, 5], [4, 5], [4, 6]]
        >>> dg.dfs(1)
        [1, 4, 6, 5, 3]
        """
        return self.dfsFilter(v0, lambda(v): True)

    def dfsFilter(self, v0, pred):
        r = []
        Q = [v0]
        while len(Q) != 0:
            v = Q.pop()
            nxt = self.d[v]
            nxt = [i for i in nxt if i not in r]
            if pred(v):
                r.append(v)
            Q.extend(nxt)
        return r

    def vertexOut(self, v):
        """
        return all vertexes from v
        self -> source vertex -> [destionation vertex]
        """
        return self.d[v]

    def vertexIn(self, v):
        """
        return all vertexes to v
        self -> destination vertex -> [source vertex]
        """
        r = []
        for b, ends in self.d.iteritems():
            if v in ends:
                r.append(b)
        return r

    def degreeOut(self, v):
        """
        return number of vertexes from v
        self -> source vertex -> Int
        """
        return len(self.d[v])

    def degreeIn(self, v):
        """
        return number of vertexes to v
        self -> destination vertex -> Int
        """
        return len(self.vertexIn(v))

    def roots(self):
        """
        return vertexes in Graph which in-degree is zero
        self -> [vertex]
        """
        return [i for i in self.vertexes() if self.degreeIn(i) == 0]

    def showDot(self):
        """
        self -> string
        >>> dg = DiGraph()
        >>> dg.addEdges([1, 2, 3], [4, 5, 6])
        >>> print dg.showDot(),
        digraph {
            1 -> {4 5 6}
            2 -> {4 5 6}
            3 -> {4 5 6}
        }
        >>> dg.vertexIn(4)
        [1, 2, 3]
        >>> dg.vertexOut(2)
        [4, 5, 6]
        >>> dg.degreeIn(4)
        3
        >>> dg.roots()
        [1, 2, 3]
        """
        s = ""
        s += "digraph {\n"
        for b, ends in self.d.iteritems():
            s += "    %s -> {%s}\n" % (b, " ".join([str(i) for i in ends]))
        s += "}\n"
        return s

    def showDotWithSt(self, st):
        fullst = {k: False for k in self.vertexes() if k not in st.keys()}
        fullst.update(st)
        s = ""
        s += "digraph {\n"
        for k, v in fullst.iteritems():
            if not v:
                s += '    %s [style = "filled" fillcolor = "gray"]\n' % (k)
        for b, ends in self.d.iteritems():
            s += "    %s -> {%s}\n" % (b, " ".join([str(i) for i in ends]))
        s += "}\n"
        return s

    def tsort(self):
        """
        topological sorting on DiGraph
        return vertexes, and residual edges if have circle in graph
        self -> ([vertex], DiGraph)
        >>> dg = DiGraph()
        >>> dg.addEdge(0, 1)
        >>> dg.addEdge(1, 2)
        >>> dg.addEdge(2, 3)
        >>> dg.addEdge(4, 2)
        >>> L, cg = dg.tsort()
        >>> L
        [4, 0, 1, 2, 3]
        >>> dg.addEdge(2, 0)
        >>> L, cg = dg.tsort()
        >>> L
        [4]
        >>> dg.chkCircle()
        True
        >>> print cg.showDot(),
        digraph {
            0 -> {1}
            1 -> {2}
            2 -> {3 0}
            4 -> {}
        }
        """
        dg = deepcopy(self)
        L = []
        S = dg.roots()
        while len(S) != 0:
            b = S.pop()
            L.append(b)
            M = dg.d[b]
            dg.d[b] = []
            for m in M:
                if dg.degreeIn(m) == 0:
                    S.append(m)
        return L, dg
        # if len(dg.edges()) != 0:
        # print dg.d
        # raise Exception('find cycle in DiGraph')
        #     return []
        # return L

    def chkCircle(self):
        """
        self -> Boolean
        """
        _, cg = self.tsort()
        return len(cg.edges()) != 0


class DependTbl(object):

    def __init__(self):
        self.dg = DiGraph()

    def dep(self, xs, ys):
        """
        self -> [vertex] -> [vertex] -> None
        """
        self.dg.addEdges(xs, ys)

    def load(self, d):
        """
        self -> {source vertex: [destination vertex]} -> None
        """
        for k, v in d.iteritems():
            self.dep([k], v)

    def showDot(self):
        return self.dg.showDot()

    def showDotWithSt(self, st):
        return self.dg.showDotWithSt(st)

    def chkCircle(self):
        return self.dg.chkCircle()

    def chkDep(self, st):
        """
        return unmeet sub-graph with DICT type
        self -> {vertex : Boolean} -> {source vertex: [destination vertex]}
        """
        ret = {}
        for k, v in st.iteritems():
            if not v:
                continue
            vs = self.dg.dfs(k)
            unmeet = [i for i in vs if i not in st or not st[i]]
            if len(unmeet) != 0:
                ret[k] = unmeet
        return ret


def printDep(unmeetDct):
    for k, v in unmeetDct.iteritems():
        print "find dependency confict, when try to enable '%s' feature" % (k)
        print "    cfg['%s'] = %s" % (k, False)
        print "---- or ----"
        for i in v:
            print "    cfg['%s'] = %s" % (i, True)
    if len(unmeetDct) == 0:
        print "all dependency is meeted"
