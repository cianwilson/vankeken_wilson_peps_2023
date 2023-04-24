This directory contains input files for TerraFERMA used for the subduction benchmark in:
"An introductory review of thermal structure of subduction zones: II. Numerical approach, validation, and comparison", 
van Keken & Wilson, PEPS, 2023.

## Directories

The primary subdirectories of this directory correspond to the different subduction zones discussed in Syracuse et al., PEPI, 2010,
for example:

The subdirectories of this directory correspond to the two different benchmark cases:

* `case1`: an isoviscous benchmark case
* `case2`: a variable viscosity benchmark case

and a supplementary directory:

* `scripts` : containing various plotting scripts

## Files

Each case directory contains several input files.  The steady state cases use the basename `subduction_steadystate_linpicard_p2p1p2`:

* `subduction_steadystate_linpicard_p2p1p2.tfml`: contains the input to TerraFERMA, a complete description of the steady state numerical problem, including all parameters, equations and boundary conditions (tfml: TerraFERMA markup language)
* `subduction_steadystate_linpicard_p2p1p2.shml`: contains the input to the TerraFERMA simulation harness, a wrapper around TerraFERMA allowing multiple simulations with different parameters to be run and compared (shml: simulation harness markup language)

The time-dependent linearized cases use the basename `subduction_linearized_p2p1p2`:

* `subduction_linearized_p2p1p2.tfml`: contains the input to TerraFERMA, a complete description of the time-dependent numerical problem, including all parameters, equations and boundary conditions (tfml: TerraFERMA markup language)
* `subduction_linearized_p2p1p2.shml`: contains the input to the TerraFERMA simulation harness, a wrapper around TerraFERMA allowing multiple simulations with different parameters to be run and compared (shml: simulation harness markup language)

The time-dependent fully nonlinear cases use the basename `subduction_p2p1p2`:

* `subduction_p2p1p2.tfml`: contains the input to TerraFERMA, a complete description of the time-dependent numerical problem, including all parameters, equations and boundary conditions (tfml: TerraFERMA markup language)
* `subduction_p2p1p2.shml`: contains the input to the TerraFERMA simulation harness, a wrapper around TerraFERMA allowing multiple simulations with different parameters to be run and compared (shml: simulation harness markup language)

## Running a simulation

The following instructions assume an active installation of TerraFERMA (the Transparent Finite ELement Rapid Model Assembler).  If
one is not available the consider using the docker image provided for this directory at:

https://github.com/users/cianwilson/packages/container/package/vankeken_wilson_peps_2023

This docker image contains a complete installation of TerraFERMA and its dependencies, PETSc, FEniCS and SPuD, within an Ubuntu
20.04LTS OS.  For a full description of TerraFERMA please refer to the webpage:

http://terraferma.github.io

To run a simulation use the `tfsimulationharness` command and an input `shml` file.  For example, to run the steady state case for
case 1, from the base directory of the directory, run:

```bash
cd case1
tfsimulationharness --test subduction_steadystate_linpicard_p2p1p2.shml
```

The command is the same regardless of which case is chosen.

## Command-line parameters

The example above runs a single simulation with some set of default parameters.  A set of parameters has been exposed to the command
line through the simulation harness and default to the benchmark values.  These are:

* Dc       - the mechanical coupling depth along the slab (km, default = 80.0)
* minres   - a scaling factor for the resolution setting the minimum element size and scaling all other resolutions appropriately (km, default = 2.0, 1.0, 0.5)
* V        - convergence speed (mm/yr, default = 100.0)
* A        - age of slab at trench (Myr, default = 100.0)
* cfl      - the maximum Courant number to allow when selecting a timestep (only applicable to the time-dependent cases, default = 1.0 & 2.0)

These can be varied with the optional `--parameters` argument to `tfsimulationharness`, e.g.:

```bash
cd case1
tfsimulationharness --parameters Dc 70.0 --test subduction_steadystate_linpicard_p2p1p2.shml
```

to run case 1 with a shallower coupling depth, or:

```bash
cd case1
tfsimulationharness --parameters minres 2.0 minres 1.0 --test subduction_steadystate_linpicard_p2p1p2.shml
```

to run a suite of different resolutions.

## Other parameters

Each `.tfml` file contains a full description of the problem.  Parameters not exposed at the command line can be modified using the GUI, `diamond`, e.g.:

```bash
cd case1
diamond subduction_steadystate_linpicard_p2p1p2.tfml
```

will open a full description of the model, including all parameters, equations, discretizations and boundary conditions.

Similarly, `diamond` can be used to view and edit the `.shml` file, e.g.:

```bash
cd case1
diamond subduction_steadystate_linpicard_p2p1p2.shml
```

which will show the simulation harness file, containing the command line parameters and the post-processing routines.

Tutorials with guidance about using TerraFERMA and its GUI, `diamond`, are available on the TerraFERMA wiki:

https://github.com/TerraFERMA/TerraFERMA/wiki/Documentation#cookbook

## Output

Output is organized by parameters in the `subduction_steadystate_linpicard_p2p1p2.tfml.run` (for steady state cases),
`subduction_linearized_p2p1p2.tfml.run` (for linearized time-dependent cases) and `subduction_p2p1p2.tfml.run` (for fully
non-linear time-dependent cases) subdirectories.  

For example, in the `case1` directory output using the default parameters can be found in the folder:

```
case1/subduction_linearized_p2p1p2.tfml.run/Dc_80.0/minres_1.0/cfl_1.0/V_100.0/A_100.0/run_0
```

The main output files are:

* `subduction_solid.xdmf` (and `subduction_solid.h5`): contains the full temperature field.  This can be opened in standard visualization packages like `paraview` (https://www.paraview.org).
* `terraferma.log-0` and `terraferma.err-0`: the log and error files for TerraFERMA, useful if something goes wrong
* `subduction_solid.det`: contains the output from various point "detectors" that evaluate the temperature at significant points in the simulation domain (mainly along and near the slab, see below for a description of these slab paths), this can be parsed in python using modules provided as part of TerraFERMA (see https://github.com/TerraFERMA/TerraFERMA/wiki/Tools#statfile-parser) or through the files described below for other formats
* `subduction_solid.json`: contains a subset of the data from `subduction_solid.det` but using a `.json` format for easier parsing (see also `.tsv` files below)
* `slab_T.tsv`: a tab separated value list of (x,y,T) temperatures along the slab (a subset of the same data as in the `.det` and `.json` files above, provided for easier parsing)
* `surface_q.tsv`: a tab separated value list of (x,y,qz) surface heat fluxes along the domain surface (a subset of the same data as in the `.det` and `.json` files above, provided for easier parsing)
    
### Plotting

Some rudimentary plotting routines are provided in the `.shml` files to compare suites of simulations.  This can be turned on interactively by setting the environment variable `PLOT=1`, e.g.:

```bash
cd case1
PLOT=1 tfsimulationharness --test subduction_steadystate_linpicard_p2p1p2.shml
```

To re-run the plotting (and post-processing generation of `subduction_solid.json` etc.) on a previously run model use the `--just-test` argument to `tfsimulationharness`, e.g.:

```bash
cd case1
PLOT=1 tfsimulationharness --just-test subduction_steadystate_linpicard_p2p1p2.shml
```

Even without the `PLOT=1` variable, rudimentary plots are saved as `.png` files in the case directories:

* `subduction_T.png`: contains a plot of the slab temperature for all parameters in the most recent run
* `subduction_q.png`: contains a plot of the surface heat flux for all parameters in the most recent run

These can be opened with any standard image viewer, e.g. `eog`.


