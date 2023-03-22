This repository contains a global suite of input files based on:
"Deep decoupling in subduction zones: observations and temperature limits,", Abers et al., Geosphere, 2020.

## Directories

The primary subdirectories of this repository correspond to the different subduction zones discussed in Syracuse et al., PEPI, 2010,
for example:

* `01_Alaska_Peninsula`: contains input files for the Alaska peninsula subduction zone geometry
* `07_Nicaragua`: contains input files for the Nicaragua subduction zone geometry
* `48_N_Honshu`: contains input files for the N. Honshu subduction zone geometry

with additional directories for:

* `00_Idealized`: contains input files for the idealized planar subduction zone geometry
* `59_CAFE09`: contains input files for the Washington Cascades subduction zone geometry

Where possible (01, 07 & 48), the numbers in the names refer to the indexing system of Syracuse et al., PEPI, 2010.

## Files

Each case directory of the global Syracuse suite contains several input files.  The steady state cases use the basename `subduction_steadystate_linpicard_p2p1p2`:

* `subduction_steadystate_linpicard_p2p1p2.tfml`: contains the input to TerraFERMA, a complete description of the steady state numerical problem, including all parameters, equations and boundary conditions (tfml: TerraFERMA markup language)
* `subduction_steadystate_linpicard_p2p1p2.shml`: contains the input to the TerraFERMA simulation harness, a wrapper around TerraFERMA allowing multiple simulations with different parameters to be run and compared (shml: simulation harness markup language)

The time-dependent cases use the basename `subduction_linearized_p2p1p2`:

* `subduction_linearized_p2p1p2.tfml`: contains the input to TerraFERMA, a complete description of the time-dependent numerical problem, including all parameters, equations and boundary conditions (tfml: TerraFERMA markup language)
* `subduction_linearized_p2p1p2.shml`: contains the input to the TerraFERMA simulation harness, a wrapper around TerraFERMA allowing multiple simulations with different parameters to be run and compared (shml: simulation harness markup language)

Additionally supplementary files are included for the geometry and the sediment thickness:

* `subduction.smml`: contains a description of the geometry and mesh to be generated (smml: subduction mesh markup language)
* `sediment_thickness.py`: contains the sediment thicknesses at the trench and at 15 km depth

## Running a simulation

The following instructions assume an active installation of TerraFERMA (the Transparent Finite ELement Rapid Model Assembler).  If
one is not available the consider using the docker image provided for this repository at:

https://hub.docker.com/r/cianwilson/globalsuite

This docker image contains a complete installation of TerraFERMA and its dependencies, PETSc, FEniCS and SPuD, within an Ubuntu
18.04LTS OS.  For a full description of TerraFERMA please refer to the webpage:

http://terraferma.github.io

To run a simulation use the `tfsimulationharness` command and an input `shml` file.  For example, to run the steady state case for
the Alaska peninsula geometry, from the base directory of the repository, run:

```bash
cd 01_Alaska_Peninsula
tfsimulationharness --test subduction_steadystate_linpicard_p2p1p2.shml
```

The command is the same regardless of which directory/subduction zone is chosen.

## Command-line parameters

The example above runs a single simulation with some set of default parameters.  A set of parameters has been exposed to the command line through the simulation harness to enable reproduction of any case in the paper.  These are:

* mu0      - friction coefficient (non-dim; default = 0.0)
* rheology - a string describing the rheology (available options: WETQZ, WETOLV, WESTERLY, SERP, BIOT1, MUSC; default = WETQZ)
* Dc       - the mechanical coupling depth along the slab (km, default = 80.0)
* minres   - a scaling factor for the resolution setting the minimum element size and scaling all other resolutions appropriately (km, default = 2.0)

For the `00_Idealized` case, the slab thermal parameters and slab dip are also available:

* V   - the convergence rate of the slab (mm/yr, default = 50.0)
* A   - age of the slab (Myr, default depends on case, default = 10.0)
* dip - dip of the slab from horizontal (degrees, default = 20)

These can be varied with the optional `--parameters` argument to `tfsimulationharness`, e.g.:

```bash
cd 01_Alaska_Peninsula
tfsimulationharness --parameters mu0 0.1 --test subduction_steadystate_linpicard_p2p1p2.shml
```

to run the `01_Alaska_Peninsula` case with a higher friction coefficient, or:

```bash
cd 01_Alaska_Peninsula
tfsimulationharness --parameters mu0 0.0 mu0 0.05 mu0 0.1 rheology SERP --test subduction_steadystate_linpicard_p2p1p2.shml
```

to run a suite of different friction coefficients for the `SERP` rheology.

In the idealized case the extra parameters can also be accessed, e.g.:

```bash
cd 00_Idealized
tfsimulationharness --parameters mu0 0.10 dip 30 Dc 85.0 --test subduction_steadystate_linpicard_p2p1p2.shml
```

for a higher friction coefficient, with a slab dipping at 30 degrees and a coupling depth of 85km.

## Other parameters

Each `.tfml` file contains a full description of the problem.  Parameters not exposed at the command line can be modified using the GUI, `diamond`, e.g.:

```bash
cd 01_Alaska_Peninsula
diamond subduction_steadystate_linpicard_p2p1p2.tfml
```

will open a full description of the model, including all parameters, equations, discretizations and boundary conditions.

Similarly, `diamond` can be used to view and edit the `.shml` file, e.g.:

```bash
cd 01_Alaska_Peninsula
diamond subduction_steadystate_linpicard_p2p1p2.shml
```

which will show the simulation harness file, containing the command line parameters and the post-processing routines.

To view or modify the mesh generation input `diamond` can be used on the `.smml` file, e.g.:

```bash
cd 01_Alaska_Peninsula
diamond subduction.smml
```

Tutorials with guidance about using TerraFERMA and its GUI, `diamond`, are available on the TerraFERMA wiki:

https://github.com/TerraFERMA/TerraFERMA/wiki/Documentation#cookbook

## Output

Output is organized by parameters in the `subduction_steadystate_linpicard_p2p1p2.tfml.run` (for steady state cases) and
`subduction_linearized_p2p1p2.tfml.run` (for time-dependent cases) subdirectories.  

For example, in the `00_Idealized` case output using the default parameters can be found in the folder:

```
00_Idealized/subduction_steadystate_linpicard_p2p1p2.tfml.run/mu0_0.0/rheology_WETQZ/V_50.0/A_10.0/dip_20/Dc_80.0/run_0
```

Similarly, for the non-default parameters demonstrated above output will be in:

```
00_Idealized/subduction_steadystate_linpicard_p2p1p2.tfml.run/mu0_0.10/rheology_WETQZ/V_50.0/A_10.0/dip_30/Dc_85.0/run_0
```

The main output files are:

* `subduction_solid.xdmf` (and `subduction_solid.h5`): contains the full temperature field.  This can be transfered out of the docker image and opened in standard visualization packages like `paraview` (https://www.paraview.org) or plotted using the script `scripts/plot_temperature.py`.
* `terraferma.log-0` and `terraferma.err-0`: the log and error files for TerraFERMA, useful if something goes wrong
* `subduction_solid.det`: contains the output from various point "detectors" that evaluate the temperature at significant points in the simulation domain (mainly along and near the slab, see below for a description of these slab paths), this can be parsed in python using modules provided as part of TerraFERMA (see https://github.com/TerraFERMA/TerraFERMA/wiki/Tools#statfile-parser) or through the files described below for other formats
* `subduction_solid.json`: contains a subset of the data from `subduction_solid.det` but using a `.json` format for easier parsing (see also `.tsv` files below)
* `slab_T.tsv`: a tab separated value list of (x,y,T) temperatures along the slab (a subset of the same data as in the `.det` and `.json` files above, provided for easier parsing)
* `surface_q.tsv`: a tab separated value list of (x,y,qz) surface heat fluxes along the domain surface (a subset of the same data as in the `.det` and `.json` files above, provided for easier parsing)
* `slab_T_*.tsv`: tab separated value lists of (x,y,T) temperatures along various paths near the slab (described below, this file contains a subset of the same data as in the `.det` and `.json` files above, provided for easier parsing)
    

### Slab paths

The temperature is output in the `subduction_solid.det`, `subduction_solid.json` and `slab_T*.tsv` files is provided along a variety of "paths" (sub)parallel to the slab surface.  These are numbered according to the following convention:

* "98": the slab surface (therefore `slab_T.tsv` and `slab_T_98.tsv` contain the same data, as do the `slab_T` and `slab_T_98` keys of `subduction_solid.json`)
* "97": 0.5 km above (in the mantle wedge and over-riding plate) and parallel to the slab surface ("98")
* "88"-"96": 1 km increments above and parallel to "97" (so "96" and "88" are 1.5 km and 9.5 km from the slab surface, "98", respectively)
* "99": below and subparallel to the slab surface ("98"), halfway through the sediments
* "100": below and subparallel to the slab surface ("98"), the base of the sediments
* "101": 0.15 km below and parallel to the base of the sediments ("100")
* "102": 0.45 km below and parallel to the base of the sediments ("100")
* "103": 1.4 km below and parallel to the base of the sediments ("100")
* "104"-"112": 1 km increments below and parallel to "100" (so "104" and "112" are 2.5 km and 10.5 km below the base of the sediments, "100", respectively)

The sediment thicknesses are defined at the trench and at 15 km depth in the `sediment_thickness.py` file. Between these depths the sediment thickness varies linearly.
Below 15 km depth, the sediment thickness is assumed constant.  Sediment thicknesses are only used in post-processing to extract the slab paths
described above, not in the model setup or simulation.

### Plotting

Some rudimentary plotting routines are provided in the `.shml` files to compare suites of simulations.  This can be turned on interactively by setting the environment variable `PLOT=1`, e.g.:

```bash
cd 01_Alaska_Peninsula
PLOT=1 tfsimulationharness --test subduction_steadystate_linpicard_p2p1p2.shml
```

To re-run the plotting (and post-processing generation of `subduction_solid.json` etc.) on a previously run model use the `--just-test` argument to `tfsimulationharness`, e.g.:

```bash
cd 01_Alaska_Peninsula
PLOT=1 tfsimulationharness --just-test subduction_steadystate_linpicard_p2p1p2.shml
```

Even without the `PLOT=1` variable, rudimentary plots are saved as `.png` files in the case directories:

* `subduction_T.png`: contains a plot of the slab temperature for all parameters in the most recent run
* `subduction_q.png`: contains a plot of the surface heat flux for all parameters in the most recent run

These can be opened with any standard image viewer, e.g. `eog`.

In addition to these simple plots of slab temperature and surface heat flux an additional basic python script is provided to plot the temperature over the whole domain, `scripts/plot_temperature.py`.  For the default `00_Idealized` example run above:

```bash
cd 00_Idealized
python3 ../scripts/plot_temperature.py subduction_steadystate_linpicard_p2p1p2.tfml.run/mu0_0.0/rheology_WETQZ/V_50.0/A_10.0/dip_20/Dc_80.0/run_0/subduction_solid.xdmf
```

This will display the plot and save it in the run directory as `subduction_T_plot.png`.  In this example:

```
00_Idealized/subduction_steadystate_linpicard_p2p1p2.tfml.run/mu0_0.0/rheology_WETQZ/V_50.0/A_10.0/dip_20/Dc_80.0/run_0/subduction_T_plot.png
```

