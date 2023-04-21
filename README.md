This repository contains the input files for TerraFERMA and FEniCS as used in:
"An introductory review of thermal structure of subduction zones: II. Numerical approach, validation, and comparison", 
van Keken & Wilson, PEPS, 2023.

## Directories

The primary subdirectories of this directory correspond to the different examples presented in van Keken & Wilson, PEPS, 2023:

* `poisson`: contains 1d and 2d example Poisson problems using both FEniCS and TerraFERMA
* `cornerflow`: contains the Batchelor cornerflow example using TerraFERMA
* `blankenbach`: contains the Blankenbach benchmarks using TerraFERMA
* `subduction_benchmark`: contains the new subduction zone benchmark using TerraFERMA
* `global_subduction_suite`: contains TerraFERMA input files for the revised subduction suite modified from Syracuse et al., PEPI, 2010 (see README.md in this directory)

## Running a TerraFERMA simulation

The following instructions assume an active installation of TerraFERMA (the Transparent Finite ELement Rapid Model Assembler).  If
one is not available the consider using the docker image provided for this directory at:

https://github.com/users/cianwilson/packages/container/package/vankeken_wilson_peps_2023

This docker image contains a complete installation of TerraFERMA and its dependencies, PETSc, FEniCS and SPuD, within an Ubuntu
20.04LTS OS.  For a full description of TerraFERMA please refer to the README.md file in the `docker` directory and/or the webpage:

http://terraferma.github.io

To run a simulation use the `tfsimulationharness` command and an input `shml` file.  For example, to run the 1D Poisson problem,
run:

```bash
cd poisson/1d/TF
tfsimulationharness --test poisson.shml
```

This example also has a FEniCS implementation, which can be run using:

```bash
cd poisson/1d/fenics
python3 poisson.py
```

## Parameters

The TerraFERMA example above runs a single simulation with some suite of default parameters.  A set of parameters has been exposed to the
command line through the simulation harness to enable reproduction of any case in the paper.  These can be viewed in the `.shml`
files, e.g.:

```bash
cd poisson/1d/TF
diamond poisson.shml
```

Each `.tfml` file contains a full description of the problem.  Parameters not exposed at the command line can be modified using the GUI, `diamond`, e.g.:

```bash
cd poisson/1d/TF
diamond poisson.tfml
```

will open a full description of the model, including all parameters, equations, discretizations and boundary conditions.

Tutorials with guidance about using TerraFERMA and its GUI, `diamond`, are available on the TerraFERMA wiki:

https://github.com/TerraFERMA/TerraFERMA/wiki/Documentation#cookbook

