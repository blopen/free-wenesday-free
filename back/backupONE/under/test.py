import numpy as np
from pyscf import gto, scf
# define the molecule
mol = gto.M(atom='H 0 0 0; H 0 0 0.7414;', basis='sto3g')
# define the Hartree-Fock driver
mf = scf.RHF(mol)
# run the Hartree-Fock calculation
mf.kernel()
PySCFDriver = mf.run()
# Define the molecule and basis set to use
molecule = 'H .0 .0 .0; H .0 .0 0.7414'
driver = PySCFDriver(molecule, unit=ANGSTROM,
                     charge=0, spin=0, basis='sto3g')
def run_vqe(molecule, basis, charge, spin, unit, backend, max_trials):
    # Set up the quantum computer backend
    backend = qiskit.BasicAer.get_backend(backend)
# Set up the quantum computer backend
backend = qiskit.BasicAer.get_backend('statevector_simulator')
# Define the quantum circuit
var_form = UCCSD(num_orbitals=driver.num_orbitals,
                 num_particles=driver.num_particles,
                 initial_state=None,
                 qubit_mapping='parity',
                 two_qubit_reduction=True,
                 num_time_slices=1)
# Define the optimizer to use
optimizer = SPSA(max_trials=300)
# Set up the VQE algorithm
vqe = VQE(var_form, optimizer, 'matrix', backend=backend)
# Run the VQE algorithm and get the results
results = vqe.run(driver)
# Print the results
print(results)



from qiskit.chemistry import FermionicOperator
from qiskit.chemistry.drivers import PySCFDriver, UnitsType
from qiskit.aqua.algorithms import VQE, SPSA
from qiskit.aqua.components.optimizers import SPSA
from qiskit.chemistry.components.variational_forms import UCCSD

# Define the molecule and basis set to use
molecule = 'H .0 .0 .0; H .0 .0 0.7414'
driver = PySCFDriver(molecule, unit=UnitsType.ANGSTROM,
                     charge=0, spin=0, basis='sto3g')
# Get the fermionic operator
ferOp = FermionicOperator(h1=driver.one_body_integrals, h2=driver.two_body_integrals)
# Define the quantum circuit
var_form = UCCSD(num_orbitals=driver.num_orbitals,
                 num_particles=driver.num_particles,
                 initial_state=None,
                 qubit_mapping='parity',
                 two_qubit_reduction=True,
                 num_time_slices=1)
# Define the optimizer to use
optimizer = SPSA(max_trials=300)
# Set up the VQE algorithm
vqe = VQE(var_form, optimizer, 'matrix', backend=backend)
# Run the VQE algorithm and get the results
results = vqe.run(ferOp)
# Print the results

print(results)

// wei schlafen delfine


Delfine schlafen nicht wie Menschen. Sie schlafen nur mit einer Hälfte ihres Gehirns, während die andere Hälfte wach bleibt, um sie vor Gefahren zu schützen. Dieser Zustand wird als unihemisphärisches Schlafen bezeichnet. Delfine schlafen auch nicht lange. Sie schlafen nur für kurze Zeiträume, normalerweise weniger als eine Stunde.

import numpy as np # //Refactoring, dependend https://ibmquantumawards.bemyapp.com/#/event
OPENQASM 2.0;
include "qelib1.inc";

qreg q[4];
cx q[0], q[1];
x q[3];
ccx q[0], q[1], q[2];
x q[0];
ccx q[1], q[2], q[3];
ccx q[0], q[1], q[2];
h q[3];
h q[0];
p(pi / 2) q[0];
p(pi / 2) q[1];
z q[2];
h q[3];
measure q[0] -> c[0];
measure q[1] -> c[1];
tdg q[0];
tdg q[1];
rccx q[1], q[2], q[3];
h q[2];
h q[3];
h q[0];
measure q[1] -> c[1];
h q[2];
z q[0];
h q[3];
h q[1];
p(pi / 2) q[1];
p(pi / 2) q[3];
p(pi / 2) q[2];
measure q[0] -> c[0];
p(pi / 2) q[0];