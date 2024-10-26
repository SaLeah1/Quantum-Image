import numpy as np
import random
from math import *

class KeyGenerator:

    X = np.array(
        [[0,1],
         [1,0]]
    )
    Y = np.array(
        [[0, 1j],
         [1j, 0]]
    )
    Z = np.array(
        [[1,0],
         [0,-1]]
    )
    H = np.array(
        [[1/sqrt(2),1/sqrt(2)],
         [1/sqrt(2),-1/sqrt(2)]]
    )
    S = np.array(
        [[1,0],
        [0,1j]]
    )
    C = np.array(
        [[1,0],
        [0,1]]
    )

    matricies = {"X":X,"Y":Y,"Z":Z,"H":H,"S":S,"C":C}

    def key2Matrix(self, key):
        matrix = np.array([1])
        for gate in key:
            gate = self.matricies[gate]
            matrix = np.tensordot(matrix,gate, axes = 0)
        return(matrix)
    
#~~~~~
c = KeyGenerator()
#c.key2Matrix([random.choice(["X","Y","Z","H","S","C"]) for x in range(3)])
matrix = c.key2Matrix("CC")