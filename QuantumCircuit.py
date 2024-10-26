from math import *
from fractions import Fraction
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
            theta = self.gVal2Theta(self.thetaColorArray[pos])
            qCirc.ry(theta,pos)
        self.qCircuit = qCirc

    def gVal2Theta(self, gValue):
        return (gValue/255)*pi
    
    def generateEncryptionGate(self):
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
    
    def infoChamp(self):
        op = qi.Operator(self.encryptionCircuit)
        print(op)

#~~~~~
c = QuantumCircuitGenerator(["#000000" for x in range(25)], [random.choice(["X","Y","Z","H","S","C"]) for x in range(25)])
c.generateQuantumCircuit()
c.generateEncryptionGate()
c.qCircuit.draw()
