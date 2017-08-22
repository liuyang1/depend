dep = {}
dep["A"] = ["B", "C", "D"]
dep["B"] = ["E", "F", "D"]
dep["D"] = ["G"]

cfg = {}

# default to False
cfg["A"] = True
cfg["B"] = False
cfg["C"] = False
cfg["D"] = True

###############################################################################
from depend import DependTbl, printDep

print cfg

dep = dep

depTbl = DependTbl()
depTbl.load(dep)

print depTbl.showDot()

print depTbl.chkCircle()

ret = depTbl.chkDep(cfg)
print ret
printDep(ret)

with open("test.dot", "w") as fp:
    print >> fp, depTbl.showDotWithSt(cfg)

cfg["G"] = True
ret = depTbl.chkDep(cfg)
print ret
printDep(ret)

cfg["B"] = True
cfg["C"] = True
cfg["E"] = True
cfg["F"] = True
ret = depTbl.chkDep(cfg)
print ret
printDep(ret)

# test on circle

dep["E"] = ["A"]
depTbl.load(dep)
print depTbl.chkCircle()
