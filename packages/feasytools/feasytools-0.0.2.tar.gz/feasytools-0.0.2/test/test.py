import sys
from pathlib import Path
print(__file__)
sys.path.append(str(Path(__file__).parent.parent))
print(sys.path)
from feasytools import *

print("ArgChecker test:")
print(ArgChecker())

print("PQ test:")
hp = Heap()
hp.push("h")
hp.push("e")
assert hp.empty() == False
assert len(hp) == 2
assert hp.remove("h") == True
hp.push("f")
assert hp.pop() == "e"
assert hp.pop() == "f"
assert hp.empty() == True

q = PQueue()
q.push(3,"henks")
q.push(1,"shjd")
assert q.pop() == (1,"shjd")
assert q.remove("henks") == True

print("Rangelist test:")
rl = RangeList([(0,1),(2,3),(4,5)])
assert 0 in rl
assert not 1 in rl

# More general tests will be added in the future

print("TimeFunc test:")
f1 = ConstFunc(1)
f2 = TimeImplictFunc(lambda: 1+2+3)
f3 = ComFunc(lambda t: t)
f4 = ManualFunc(1)
f4.setManual(2)
print(f1(0))
print(f2(0))
print(f3(0))
print(f4(0))
print(f1)
print(f2)
print(f3)
print(f4)
f5 = quicksum([f1,f2,f3,f4])
print(f5)
f6 = quickmul([f1,f2,f3,f4])
print(f6)
f7 = f5 + 1
print(f7)
f8 = f6 * 2
print(f8)
f9 = f5 + f6
print(f9)
f10 = f5 * f6
print(f10)