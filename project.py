import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, transpile, assemble
import math
import random
import numpy as np
import time
from cost_function import *
from scipy.optimize import minimize


""" Definition of A matirx Al an cl"""
A_l0 = [0, 3, 0]
A_l1 = [1, 0, 0]
A_l2 = [0, 0, 2]
A = [A_l0, A_l1, A_l2]

coefficient_set = [0.4, 0.3,0.3]

#start = time.time()
"""minimize cost funtion"""
out = minimize(calculate_cost_function, x0=[float(random.randint(0,3000))/1000 for i in range(0, 9)], args=(A,coefficient_set),method="COBYLA", options={'maxiter':200})
#end = time.time()

#print(end - start)
print(out)

out_f = [out['x'][0:3], out['x'][3:6], out['x'][6:9]]



"""getting the solution |x> using the optimal parameters"""
circ = QuantumCircuit(3, 3)
ansatz(circ,[0, 1, 2], out_f)
circ.save_statevector()

backend = Aer.get_backend('aer_simulator')
t_circ = transpile(circ, backend)
qobj = assemble(t_circ)
job = backend.run(qobj)

result = job.result()
o = result.get_statevector(circ, decimals=10)


""" manually constructing matrix A and |b>"""
a0 = coefficient_set[0]*np.array([[float(1/np.sqrt(2)),0,float(1/np.sqrt(2)),0,0,0,0,0], [0,float(1/np.sqrt(2)),0,float(1/np.sqrt(2)),0,0,0,0], [float(1/np.sqrt(2)),0,-float(1/np.sqrt(2)),0,0,0,0,0], [0,float(1/np.sqrt(2)),0,-float(1/np.sqrt(2)),0,0,0,0], [0,0,0,0,float(1/np.sqrt(2)),0,float(1/np.sqrt(2)),0], [0,0,0,0,0,float(1/np.sqrt(2)),0,float(1/np.sqrt(2))], [0,0,0,0,float(1/np.sqrt(2)),0,-float(1/np.sqrt(2)),0], [0,0,0,0,0,float(1/np.sqrt(2)),0,-float(1/np.sqrt(2))]])

a1 = coefficient_set[1]*np.array([[1,0,0,0,0,0,0,0], [0,-1,0,0,0,0,0,0], [0,0,1,0,0,0,0,0], [0,0,0,-1,0,0,0,0], [0,0,0,0,1,0,0,0], [0,0,0,0,0,-1,0,0], [0,0,0,0,0,0,1,0], [0,0,0,0,0,0,0,-1]])

a2 = coefficient_set[2]*np.array([[0,0,0,0,1,0,0,0], [0,0,0,0,0,1,0,0], [0,0,0,0,0,0,1,0], [0,0,0,0,0,0,0,1], [1,0,0,0,0,0,0,0], [0,1,0,0,0,0,0,0], [0,0,1,0,0,0,0,0], [0,0,0,1,0,0,0,0]])

a3 = np.add(a0,a1)
A = np.add(a3,a2)
b = np.array([float(1/np.sqrt(8)),float(1/np.sqrt(8)),float(1/np.sqrt(8)),float(1/np.sqrt(8)),float(1/np.sqrt(8)),float(1/np.sqrt(8)),float(1/np.sqrt(8)),float(1/np.sqrt(8))])



"""print the inner product <xA|b>"""
print(f"\n <xA|b> = {(b.dot(A.dot(o)/(np.linalg.norm(A.dot(o)))))**2}")