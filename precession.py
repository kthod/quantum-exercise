
from qiskit import QuantumCircuit, assemble, Aer
from math import pi, sqrt
import matplotlib 
from matplotlib import pyplot as plt
from qiskit.visualization import plot_bloch_multivector, plot_histogram, circuit_drawer
sim = Aer.get_backend('aer_simulator')

# Let's do an X-gate on a |0> qubit
qc = QuantumCircuit(1)
qc.x(0)
qc.x(0)
qc.draw(output = "mpl" )
print(qc)

plt.show()
    
def had_test(gate_type,num_of_qubits, parameters):

    ancilla = QuantumRegister(1,'ancilla')
    qr = QuantumRegister(num_of_qubits,'q')
    cr = ClassicalRegister(1)
    circ =QuantumCircuit(ancilla,qr,cr)
    circ.h(ancilla[0])



    apply_fixed_ansatz(circ,qr[0:3], parameters)

    for i in range (0, len(gate_type[0])):
        if (gate_type[0][i] == 1):
            circ.cz(ancilla[0], qr[i])

    for i in range (0, len(gate_type[0])):
        if (gate_type[1][i] == 1):
            circ.cz(ancilla[0], qr[i])
    
    circ.h(ancilla[0])
    circ.measure(ancilla,cr)
    circ.draw(output="mpl")

had_test([[0, 0, 0], [0, 0, 1]], 3, [[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        


    
