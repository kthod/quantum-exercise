import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, transpile, assemble
import math
import random
import numpy as np
from scipy.optimize import minimize
from matplotlib import pyplot as plt




def ansatz(circ,qubits, parameters):

    for i in range (0, len(qubits)):
        circ.ry(parameters[0][i], qubits[i])

    for i in range (0, len(qubits)-1,2):
        circ.cx(qubits[i], qubits[i+1])
   

    for i in range (0, len(qubits)):
        circ.ry(parameters[1][i], qubits[i])

    for i in range (1, len(qubits)-1,2):
        circ.cx(qubits[i], qubits[i+1])

circ = QuantumCircuit(4)
ansatz(circ,[0, 1, 2], [[1, 1, 1], [1, 1, 1]])
circ.draw(output="mpl")   
plt.show()
