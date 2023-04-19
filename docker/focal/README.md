# Software

All numerical simulations described here use TerraFERMA (the Transparent Finite Element Rapid Model Assembler).  
This docker image contains a complete installation of TerraFERMA and its dependencies, PETSc, FEniCS and SPuD, within an Ubuntu
20.04LTS OS.  For a full description of TerraFERMA please refer to the webpage:

http://terraferma.github.io

The environment variables have been set automatically using environment modules and it should now be possible to build and run
TerraFERMA models within this container.  

## Docker configuration

**Necessary to allow file transfers and to open the TerraFERMA GUI.**

In order to open the TerrFERMA GUI or transfer files out of the docker container it is necessary to run docker with some extra
command line flags.  A brief summary of these is provided below for linux and mac OS.  A full discussion of this topic is available at:

https://github.com/terraferma/terraferma/wiki/Installation#docker

where it is necessary to replace any occurrence of `ghcr.io/terraferma/dev` with `ghcr.io/cianwilson/vankeken_wilson_peps_2023` for this docker image.

### Linux

Change to a directory where output is to be transferred, then run the command:

```bash
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v $PWD:/home/tfuser/shared ghcr.io/cianwilson/vankeken_wilson_peps_2023
```

The `-v` flags share folders between the local computer and the docker container while the `-e` flag shares environment variables.
Inside the docker container any files that should be transferred to the host computer can be placed in the `/home/tfuser/shared`
directory from where they will be accessible in the current directory on the host machine.

### Mac

These instructions require Docker for Mac (not Docker toolbox) and an up to date installation of XQuartz.  To allow the GUI to open
please ensure that "Allow Connections from Network Clients" is checked in the XQuartz security preferences.  Before starting docker
it is also necessary to find the local IP address of the machine.  This is normally accessible using the `ifconfig` command:

```bash
ip=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
```

but details may change on different machines (e.g. `en0` may not be the appropriate interface).

After setting the `ip` environment variable, it may also be necessary to open XQuartz and add the IP address to `xhost`:

```bash
open -a XQuartz
xhost + ${ip}
```

Finally, change to a directory where output is to be transferred and run the command:

```bash
docker run -it --rm -e DISPLAY=${ip}:0 -v /tmp/.X11_unix:/tmp -v $PWD:/home/tfuser/shared ghcr.io/cianwilson/vankeken_wilson_peps_2023
```

As for linux `-v` shares folders between the local computer and the docker container while `-e` shares environment
variables.  Inside the docker container any files that should be transferred to the host computer can be placed in the `/home/tfuser/shared` 
directory from where they will be accessible in the current directory on the host machine.  

After exiting the docker container if
the IP address was added to `xhost` it is possible to unset it again:

```bash
xhost - ${ip}
```

# Input files

The folder `vankeken_wilson_peps_2023` contains all input files used in:
"An introductory review of thermal structure of subduction zones: II. Numerical approach, validation, and comparison", 
van Keken & Wilson, PEPS, 2023.

## Directories

The primary subdirectories of `vankeken_wilson_peps_2023` correspond to the different examples presented in van Keken & Wilson, PEPS, 2023:

* `poisson`: contains 1d and 2d example Poisson problems using both FEniCS and TerraFERMA
* `cornerflow`: contains the Batchelor cornerflow example using TerraFERMA
* `blankenbach`: contains the Blankenbach benchmarks using TerraFERMA
* `subduction_benchmark`: contains the new subduction zone benchmark using TerraFERMA
* `global_subduction_suite`: contains TerraFERMA input files for the revised subduction suite modified from Syracuse et al., PEPI, 2010 (see README.md in this directory)

## Running a TerraFERMA simulation

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



