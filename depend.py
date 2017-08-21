#! /usr/bin/env python2

from collections import defaultdict
from copy import deepcopy


class DiGraph():

    def __init__(self):
        self.d = defaultdict(list)
        self.v = []

    def vertexs(self):
        return self.v

    def addVertexs(self, vs):
        for v in vs:
            self.addVertex(v)

    def addVertex(self, v):
        """
        >>> dg = DiGraph()
        >>> dg.addVertex(1)
        >>> dg.vertexs()
        [1]
        >>> dg.addVertexs([1, 2, 3])
        >>> dg.vertexs()
        [1, 2, 3]
        """
        if v not in self.v:
            self.v.append(v)

    def edges(self):
        r = []
        for b, ends in self.d.iteritems():
            for e in ends:
                r.append([b, e])
        return r

    def addEdges(self, bgns, ends):
        for b in bgns:
            for e in ends:
                self.addEdge(b, e)

    def addEdge(self, bgn, end):
        """
        >>> dg = DiGraph()
        >>> dg.addEdges([1, 2], [4, 5, 6])
        >>> dg.vertexs()
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
        return self.d

    def vertexIn(self, v):
        r = []
        for b, ends in self.d.iteritems():
            if v in ends:
                r.append(b)
        return r

    def degreeOut(self, v):
        return len(self.d[v])

    def degreeIn(self, v):
        return len(self.vertexIn(v))

    def roots(self):
        return [i for i in self.vertexs() if self.degreeIn(i) == 0]

    def showDot(self):
        """
        >>> dg = DiGraph()
        >>> dg.addEdges([1, 2, 3], [4, 5, 6])
        >>> dg.showDot()
        digraph {
            1 -> {4 5 6}
            2 -> {4 5 6}
            3 -> {4 5 6}
        }
        >>> dg.vertexIn(4)
        [1, 2, 3]
        >>> dg.degreeIn(4)
        3
        >>> dg.roots()
        [1, 2, 3]
        """
        print "digraph {"
        for b, ends in self.d.iteritems():
            print "    %s -> {%s}" % (b, " ".join([str(i) for i in ends]))
        print "}"

    def tsort(self):
        """
        # >>> dg.addEdge(2, 0)
        >>> dg = DiGraph()
        >>> dg.addEdge(0, 1)
        >>> dg.addEdge(1, 2)
        >>> dg.addEdge(2, 3)
        >>> dg.addEdge(4, 2)
        >>> dg.topo()
        [4, 0, 1, 2, 3]
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
        if len(dg.edges()) != 0:
            # print dg.d
            # raise Exception('find cycle in DiGraph')
            return []
        return L



class DependTbl():

    def __init__():
        self.dg = DiGraph()

    def dep(xs, ys):
        self.dg.addEdges(xy, ys)

    def chkCycle():
        pass
