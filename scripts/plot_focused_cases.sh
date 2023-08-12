#!/bin/sh

usage()
{
    echo "usage: plot_focused_cases.sh [-h]"
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
seprandir=$repodir/../sepran

python3 $repodir/scripts/plot_multiple_temperatures.py \
        -f1 $repodir/01_Alaska_Peninsula/subduction_linearized_p2p1p2.tfml.run/Dc_80.0/minres_1.0/cfl_1.0/run_0/subduction_solid.xdmf \
            $repodir/04_Cascadia/subduction_linearized_p2p1p2.tfml.run/Dc_80.0/minres_1.0/cfl_1.0/run_0/subduction_solid.xdmf \
            $repodir/47_C_Honshu/subduction_linearized_p2p1p2.tfml.run/Dc_80.0/minres_1.0/cfl_1.0/run_0/subduction_solid.xdmf \
        -f2 $seprandir/01_Alaska_Peninsula/T_040.vtu \
            $seprandir/04_Cascadia/T_040.vtu \
            $seprandir/47_C_Honshu/T_040.vtu

