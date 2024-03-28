"""
Minizinc 2023


TODO : not finished apparently
"""

from pycsp3 import *
from pycsp3.classes.auxiliary.ptypes import TypeSquareSymmetry
from pycsp3.classes.entities import TypeNode

print(~TypeNode.EQ)

maxCrossovers, nLoci, nGametes, nTreeCells, gametes = data

Node, Leaf, Null = NodeType = range(3)

treeType = VarArray(size=nTreeCells, dom=NodeType)

treeLeft = VarArray(size=nTreeCells, dom=range(nTreeCells + 1))

treeRight = VarArray(size=nTreeCells, dom=range(nTreeCells + 1))

xs = VarArray(size=[nTreeCells, nLoci], dom={0, 1})

index = VarArray(size=nTreeCells, dom=range(nGametes + 1))

source = VarArray(size=[nTreeCells, nLoci], dom={1, 2})

swap = VarArray(size=[nTreeCells, nLoci], dom=lambda i, j: {0, 1} if j > 0 else None)

satisfy(

    # Tree structure
    Increasing(treeType),

    [If(
        treeType[i] == Node,
        Then=[
            treeLeft[i] > i,
            treeRight[i] > i,
            treeType[treeLeft[i]] != Null,
            treeType[treeRight[i]] != Null
        ],
        Else=(treeLeft[i] == 0) & (treeRight[i] == 0)
    ) for i in range(nTreeCells)],

    [(treeType[i] == Leaf) == (index[i] > 0) for i in range(nTreeCells)],
    [(treeType[i] == Null) == (xs[i] == 0) for i in range(nTreeCells)],

    AllDifferent(index, excepting=0),

    [(treeType[i] != Leaf) | (xs[i, j] == gametes[index[i], j]) for i in range(nTreeCells) for j in range(nLoci)],

    # First plant is the desired plant
    [xs[0] == 1, treeType[1] != Null],

    # [IfThenElse(
    #     treeType[i] == Node,
    #     Then=[],
    #     Else=[
    #         [source[i, j] == 1 for j in range(nLoci)],
    #         [swap[i, j] == 0 for j in range(1, nLoci)]
    #     ]
    # ) for i in range(nTreeCells)]
)

minimize(
    Sum(treeType[i] == Node for i in range(nTreeCells))
    # Count(treeType, value=Node)
)
