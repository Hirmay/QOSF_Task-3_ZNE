import numpy as np
import pennylane as qml
from pennylane import numpy as qnp
from scipy.optimize import minimize, curve_fit

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Session
# from qiskit_ibm_runtime import IBMQ
# from qiskit import  IBMQ
from qiskit_aer import noise
from qiskit_aer.noise import NoiseModel
from qiskit_aer import AerSimulator
from qiskit.circuit.library import EfficientSU2
#import copy for copying the qiskit circuit
import copy

def exp_func(x, a, b, c):
    return c + a * np.exp(-b * x)

def power_func(x,a,b,p):
    # similar to equation 9 of reference [1]
    return a + b* p ** (-x)

# this is a simple implementation of some arbitrary circuit
def QuantumCircuit_Generator(Layers, num_qubits, params, N_1_flag=False, m_value=0):
    qc = QuantumCircuit(num_qubits)
    for iter in range(Layers):            
        for j in range(num_qubits):
            qc.rz(params[iter, j], j)
        for k in range(num_qubits-1):
            qc.cx(k, k+1)
    if N_1_flag:
    # converting into the |N-1> state
        for l in range(num_qubits):
            qc.x(l)
    qc.barrier()
    qc = apply_folding_method(qc, m_value)
    return qc


def count_gates(qc_gate_dict):
    gates_count = 0
    for i in qc_gate_dict:
        # counting barrier since we'll be applying it
        # if i == 'barrier':
        #     continue
        gates_count += qc_gate_dict[i]
    return gates_count

def apply_folding_method(qc, m_value):
    # m_value determines the repetition
    gates_count = count_gates(dict(qc.count_ops()))
    total_gate_fold = int(m_value*gates_count)
    for i in range(total_gate_fold):
        circuit_data = qc.data[i]
        operation = circuit_data.operation
        operation_inverse = operation.inverse()
        if operation.name != 'barrier':
            qc.append(operation_inverse, circuit_data.qubits, circuit_data.clbits)
        qc.append(operation, circuit_data.qubits, circuit_data.clbits)
    return qc

class DepolarizingNoiseModel:
    """
    A Depolarizing Noise Model class for simulation circuits for different noise levels 
    and then using the extrapolation method to obtain the expectation value for noise level
        Args:
        noise_levels (list): 
            A list containing different levels of depolarizing noise to get the expectation data, if using with unitary
            fold, this indicates the m_value
        circuit:
            The Quantum circuit on which to run the model on
        value_to_extrapolate (binary):
            A binary value to extrapolate
        unitary_fold (bool):
            A flag which determines whether to use unitary fold method or artificially increase gate error probabilities
    Returns:
        The expectation when noise level is zero and functions of the extrapolation values.
    """
    def __init__(self, noise_levels, circuit, value_to_extrapolate,unitary_fold=False):
        self.noise_levels = noise_levels
        self.original_circuit = circuit
        # a copy of circuit needed for unitary folding
        self.circuit = circuit
        self.value_to_extrapolate = value_to_extrapolate
        self.all_data = []
        # results data will only contain data for the value to be extrapolated
        self.results_data = []
        self.unitary_fold = unitary_fold
    
    def noisy_backend_model(self,noise_level, err_single, err_2_qubit):
        # taken from qiskit-aer's documentation example for a custom noise model
        # gate error prob for single and 2 qubit gates
        prob_single = err_single * noise_level  
        prob_2_qubit =  err_2_qubit * noise_level  

        # Depolarizing quantum errors
        error_1 = noise.depolarizing_error(prob_single, 1)
        error_2 = noise.depolarizing_error(prob_2_qubit, 2)

        # Add errors to noise model
        noise_model = noise.NoiseModel()
        # applying the error rates to the following single and 2 qubit gates 
        noise_model.add_all_qubit_quantum_error(error_1, ['rz', 'x','h', 'rx','ry'])
        noise_model.add_all_qubit_quantum_error(error_2, ['cx', 'cz'])
        
        backend = AerSimulator(noise_model=noise_model)
        
        return backend

    
    # Initializing the depolarizing noise channel using qiskit
    def depolarizing_initiation(self, noise_level, shots, err_single=1e-3, err_2_qubit=1e-2, qiskit_backend=None):

        # If the backend given as an IBM quantum computer then don't do use the noise model 
        if qiskit_backend is not None:
            backend = qiskit_backend
        elif self.unitary_fold:
    # no need to increase gate errors since we're increasing errors with folding method.
            backend = self.noisy_backend_model(1, err_single, err_2_qubit)
        else:
            backend = self.noisy_backend_model(noise_level, err_single=err_single, err_2_qubit=err_2_qubit)
        # copying circuit and measuring it
        copied_circuit = copy.deepcopy(self.circuit)
        # now transpiling the circuit with the NoiseModel
        circuit_transpiled = transpile(copied_circuit, backend)
        circuit_transpiled.measure_all()
        # obtaining the counts
        prob_counts = backend.run(circuit_transpiled,shots=shots).result().get_counts() 
        self.all_data.append(prob_counts)
        # extracting probabilities out of the results
        keys=list(prob_counts.keys())
        num_qubits = copied_circuit.num_qubits
        for i in range(2**num_qubits):
            bin = "{0:b}".format(int(i)).zfill(num_qubits)
            if bin not in keys:
              prob_counts[bin] = 0 
            prob_counts[bin] = prob_counts[bin]/shots
        self.results_data.append(prob_counts[self.value_to_extrapolate])
    
    # creating a function to obtain the expectation data for all noise levels
    def get_noise_level_data(self, shots, qiskit_backend=None):
        for noise_level in self.noise_levels:
            if self.unitary_fold:
                original_circuit = copy.deepcopy(self.original_circuit)
                self.circuit = apply_folding_method(original_circuit, noise_level)
            self.depolarizing_initiation(noise_level, shots, qiskit_backend=qiskit_backend)
    
    def ZNE(self,p0_power=None):
        # use the extrapolation method to find the appropriate function
        linear_function = np.poly1d(np.polyfit(x=self.noise_levels, y=self.results_data, deg=1))
        quadratic_function = np.poly1d(np.polyfit(x=self.noise_levels, y=self.results_data, deg=2))
        polynomial_function = np.poly1d(np.polyfit(x=self.noise_levels, y=self.results_data, deg=5))
        # based on the equation 9 of reference [1]
        x=np.array(self.noise_levels)
        y=np.array(self.results_data)
        exponential_function = curve_fit(exp_func, x, y, maxfev=10**4)
        power_function = curve_fit(power_func, x, y, maxfev=10**4,p0=p0_power)
        self.ZNE_functions = [linear_function, quadratic_function, polynomial_function,exponential_function, power_function]