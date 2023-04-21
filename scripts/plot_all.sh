#!/bin/sh

usage()
{
    echo "usage: plot_all.sh [-h]"
}

NP=1
while [ "$1" != "" ]; do
    case $1 in
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

repodir=$(dirname $(dirname $(realpath $0) ) )
# set up to work in the zenodo repository
seprandir=$repodir/../sepran

## the steady state case, just the temperature maps
#python3 $repodir/scripts/plot_subduction_benchmark_temperatures.py \
#        -f1 $repodir/case1/subduction_steadystate_linpicard_p2p1p2.tfml.run/Dc_80.0/minres_1.0/V_100.0/A_100.0/run_0/subduction_solid.xdmf \
#            $repodir/case2/subduction_steadystate_linpicard_p2p1p2.tfml.run/Dc_80.0/minres_1.0/V_100.0/A_100.0/run_0/subduction_solid.xdmf \
#        -f2 $seprandir/case1eps/T_500.vtu \
#            $seprandir/case2eps/T_500.vtu

# the steady state case + comparison with the slab temperature
python3 $repodir/scripts/plot_subduction_benchmark_T_w_slabT.py \
       -f1 $repodir/case1/subduction_steadystate_linpicard_p2p1p2.tfml.run/Dc_80.0/minres_1.0/V_100.0/A_100.0/run_0/subduction_solid.xdmf \
           $repodir/case2/subduction_steadystate_linpicard_p2p1p2.tfml.run//Dc_80.0/minres_1.0/V_100.0/A_100.0/run_0/subduction_solid.xdmf \
       -f2 $seprandir/case1/PF/0.5/temp.vtu \
           $seprandir/case2/PF/0.5/temp.vtu
mv subduction_allT_plot.pdf subduction_comparison_plot_tf_sepran.pdf

# time evolution of the slab temperature (also plot the steady state profile)
python3 $repodir/scripts/plot_subduction_benchmark_slabT_td.py  \
        $repodir/case2/subduction_linearized_p2p1p2.tfml.run/Dc_80.0/minres_1.0/cfl_1.0/V_100.0/A_100.0/run_0/subduction_linearized_p2p1p2.tfml \
        -ss $repodir/case2/subduction_steadystate_linpicard_p2p1p2.tfml.run/Dc_80.0/minres_1.0/V_100.0/A_100.0/run_0/subduction_steadystate_linpicard_p2p1p2.tfml \
        -i 2 3 6 11 26

# difference between the steady state and time-dependent after 20 Myr
python3 $repodir/scripts/plot_subduction_benchmark_T_w_slabT.py \
        -f1 $repodir/case2/subduction_linearized_p2p1p2.tfml.run/Dc_80.0/minres_1.0/cfl_1.0/V_100.0/A_100.0/run_0/subduction_solid.xdmf \
        -f2 $repodir/case2/subduction_steadystate_linpicard_p2p1p2.tfml.run/Dc_80.0/minres_1.0/V_100.0/A_100.0/run_0/subduction_solid.xdmf \
        -i1 20 -i2 -1
mv subduction_allT_plot.pdf subduction_comparison_plot_tdep_ss.pdf

python3 $repodir/scripts/plot_subduction_benchmark_T_w_slabT.py \
        -f1  $repodir/case2/subduction_linearized_p2p1p2.tfml.run/Dc_80.0/minres_1.0/cfl_2.0/V_100.0/A_100.0/run_0/subduction_solid.xdmf \
       -f2 $repodir/case2/subduction_p2p1p2.tfml.run/Dc_80.0/minres_1.0/cfl_2.0/V_100.0/A_100.0/run_0/subduction_solid.xdmf \
       -i1 20 -i2 2
mv subduction_allT_plot.pdf subduction_comparison_plot_lin_nlin.pdf

# plot the mesh
python3 $repodir/scripts/plot_subduction_benchmark_mesh.py \
        $repodir/case1/subduction_steadystate_linpicard_p2p1p2.tfml.run/Dc_80.0/minres_1.0/V_100.0/A_100.0/run_0/subduction_solid.xdmf

