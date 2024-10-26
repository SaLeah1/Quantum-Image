from math import *
import random

import numpy as np

from qiskit import QuantumCircuit
from qiskit_braket_provider import BraketLocalBackend

class QuantumCircuitGenerator:

    hexColorArray = []
    gValColorArray = []
    thetaColorArray = []

    qubitCount = 0

    qCircuit = None
    encryptionCircuit = []
    encryptionKey = None

    def __init__(self, colorArray, encryptionKey) -> None:
        self.encryptionKey = encryptionKey
        self.hexColorArray = colorArray
        for hexColor in self.hexColorArray:
            hexColor = hexColor.lstrip("#")
            RGB = tuple(int(hexColor[i:i+2], 16) for i in (0, 2, 4))
            gVal = RGB[0]
            self.gValColorArray.append(gVal)
            theta = self.gVal2Theta(gVal)
            self.thetaColorArray.append(theta)
        self.qubitCount = len(self.hexColorArray)

    def generateQuantumCircuit(self):
        qCirc = QuantumCircuit(self.qubitCount)
        for pos in range(self.qubitCount):
            qCirc.ry(self.thetaColorArray[pos],pos)
        self.qCircuit = qCirc

    def gVal2Theta(self, gValue):
        return (gValue/255)*pi
    
    def applyEncryptionGate(self):
        self.encryptionCircuit = QuantumCircuit(len(self.encryptionKey))
        for index in range(len(self.encryptionKey)):
            match self.encryptionKey[index]:
                case "X":
                    self.encryptionCircuit.x(index)
                case "Y":
                    self.encryptionCircuit.y(index)
                case "Z":
                    self.encryptionCircuit.z(index)
                case "H":
                    self.encryptionCircuit.h(index)
                case "S":
                    self.encryptionCircuit.s(index)
                case "C":
                    self.encryptionCircuit.id(index)
        self.encryptionCircuit = self.encryptionCircuit.to_gate()
        self.qCircuit.append(self.encryptionCircuit,range(len(self.encryptionKey)))
    
    def runCircuit(self):
        shotCount = 10000
        newSim = BraketLocalBackend()
        task = newSim.run(self.qCircuit,shots=shotCount)
        results = task.result()
        self.recentCounts = results.get_counts()
        self.recentData = results.data()
        self.recentFrequency = self.recentData["counts"]
        invPx = [0 for x in range(self.qubitCount)]
        for result, count in self.recentFrequency.items():
            for index in range(self.qubitCount):
                invPx[index] += int(result[index])*count
        invPx = [x/shotCount for x in invPx]
        invPx.reverse()
        self.recentgValues = [self.dec2gVal(self.prob2Theta(x)) for x in invPx]


    def prob2Theta(self, pValue):
        root = sqrt(pValue)
        thetaPi = 2*(np.arcsin(root))
        theta = thetaPi/pi
        return theta

    def dec2gVal(self, decVal):
        return int(decVal*255)
    

#~~~~~
c = QuantumCircuitGenerator(["#a0a0a0" for x in range(25)], [random.choice(["X","Y","Z","H","S","C"]) for x in range(25)])
c.generateQuantumCircuit()
c.applyEncryptionGate()
c.applyEncryptionGate()
c.runCircuit()
print(c.recentgValues)