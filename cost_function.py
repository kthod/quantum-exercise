import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, transpile, assemble
import math
import numpy as np
from circuits import *

def prob_of_1(o):
    """
    calculating probability of teh ancilla bit being 1, 
    by adding the amplitude^2 of every second state of the 
    state vector (a.k.a each state with the firts qubit being 1)
    """
    m_sum = 0
    for l in range (0, len(o)):
        if (l%2 == 1):
            n = o[l]**2
            m_sum+=n
    return m_sum



def run_circ(circ):
    """"
    Simulating the circuit
    """
    backend = Aer.get_backend('aer_simulator')
    circ.save_statevector()
    t_circ = transpile(circ, backend)
    qobj = assemble(t_circ)
    job = backend.run(qobj)

    result = job.result()
    outputstate = np.real(result.get_statevector(circ, decimals=100))
    return outputstate



def calculate_cost_function(parameters,A,coefficient_set):
    
    global opt

    overall_sum_1 = 0
    num_of_qubits = int(len(parameters)/3)
    parameters = [parameters[0:num_of_qubits], parameters[num_of_qubits:2*num_of_qubits], parameters[2*num_of_qubits:3*num_of_qubits]]

    for i in range(0, len(A)):
        for j in range(0, len(A)):

            
            ancilla = QuantumRegister(1)
            qr = QuantumRegister(num_of_qubits)
            cr = ClassicalRegister(1)
            circ = QuantumCircuit(ancilla,qr, cr)

            
            
            multiply = coefficient_set[i]*coefficient_set[j]

            had_test(circ, qr,A[i],A[j], ancilla, parameters)
            
            o= run_circ(circ)
            
           
            # outputstate = result.get_counts(circ)

            # if ('1' in outputstate.keys()):
            #     m_sum = float(outputstate["1"])/100000
            # else:
            #     m_sum = 0
            overall_sum_1+=multiply*(1-(2*prob_of_1(o)))

    overall_sum_2 = 0

    for i in range(0, len(A)):
        for j in range(0, len(A)):

            multiply = coefficient_set[i]*coefficient_set[j]
            mult = 1

            for extra in range(0, 2):

                ancilla = QuantumRegister(1)
                qr = QuantumRegister(num_of_qubits)
                cr = ClassicalRegister(1)
                circ = QuantumCircuit(ancilla,qr, cr)

                #backend = Aer.get_backend('aer_simulator')

                if (extra == 0):
                    special_had_test(circ,A[i], qr, ancilla, parameters)
                if (extra == 1):
                    special_had_test(circ,A[j], qr, ancilla, parameters)
                
                o= run_circ(circ)
                
                mult = mult*(1-(2*prob_of_1(o)))
                # outputstate = result.get_counts(circ)

                # if ('1' in outputstate.keys()):
                #     m_sum = float(outputstate["1"])/100000
                # else:
                #     m_sum = 0

                #mult = mult*(1-2*m_sum)
            
            overall_sum_2+=multiply*mult
            
    print(1-float(overall_sum_2/overall_sum_1))

    return 1-float(overall_sum_2/overall_sum_1)
