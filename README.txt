QEEOS
=================================

Quantum Espresso - Equation of State and Elastic Constants

Python code.

This code uses pwscf from the Quantum Espresso suite to calculate crystal energies using DFT.

For a full run, this is what the code does:

1.   Reads in the user's input
2.   Creates a template file for PWscf based on the user's input and supplied template file
3.   Creates a vc-relax input file and runs this to find the relaxed a0 and cell parameters
     Also calculates the density of the material based on the DFT results
4.   Creates a series of SFC input files over a range of strains in order to calculate the equation of state
5.   Gathers the energy results and fits the equation of state
6.   Creates a series of SFC input files distorted by 9 distortions in order to find 9 independent elastic constants
7.   Gathers the results and calculates the stiffness (and compliance) matrix
8.   Using the elastic constants, other material properties are calculated or estimated


