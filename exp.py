from qiskit import QuantumCircuit,QuantumRegister,assemble,Aer, transpiler,IBMQ, execute
import numpy as np
from qiskit.providers.aer import QasmSimulator
from math import sqrt, pi
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit.visualization import circuit_drawer, array_to_latex
from matplotlib import pyplot as plt

qc = QuantumCircuit(2,1)
qc.initialize([0,1],1)
#qc.x(y)
qc.h(0)
qc.h(1)
qc.i(0)
qc.i(1)
qc.h(0)
qc.measure(1,0)
#qc.draw()
qc.draw(output='mpl')

# Let's see the result

# Let's see the result
svsim = Aer.get_backend('qasm_simulator')
qc.save_statevector()
qobj = assemble(qc)
result= svsim.run(qobj).result()
statevector = result.get_statevector()
print(statevector)
print(result.get_counts()['1'])
plot_histogram(result.get_counts())

plt.show()