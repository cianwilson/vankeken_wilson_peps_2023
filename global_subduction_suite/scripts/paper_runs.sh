#!/bin/sh

usage()
{
    echo "usage: paper_runs.sh [[-n numproc] | [-h]]"
}

NP=1
while [ "$1" != "" ]; do
    case $1 in
        -n )           shift
                       NP=$1
                       ;;
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

repo=$(dirname $(dirname $(realpath $0) ) )
 
# figure 3

tfsimulationharness -n $NP --test --parameters mu0 0.00 mu0 0.03 mu0 0.05 mu0 0.10 mu0 0.15 \
                                               rheology WETQZ \
                                               V 50.0 \
                                               A 50.0 \
                                               dip 20.0 \
                                               Dc 80.0 \
                                               -- $repo/00_Idealized/subduction_steadystate_linpicard_p2p1p2.shml 1> fig3.log 2>&1


# figure 4

tfsimulationharness -n $NP --test --parameters mu0 0.00 mu0 0.03 mu0 0.05 mu0 0.10 mu0 0.15 \
                                               rheology SERP \
                                               V 50.0 \
                                               A 50.0 \
                                               dip 20.0 \
                                               Dc 80.0 \
                                               -- $repo/00_Idealized/subduction_steadystate_linpicard_p2p1p2.shml 1> fig4.log 2>&1

# figure 5

tfsimulationharness -n $NP --test --parameters mu0 0.00 mu0 0.03 \
                                               rheology WETQZ \
                                               V 50.0 \
                                               A 10.0 A 25.0 A 50.0 A 100.0 \
                                               dip 20.0 \
                                               Dc 80.0 \
                                               -- $repo/00_Idealized/subduction_steadystate_linpicard_p2p1p2.shml 1> fig5a.log 2>&1
tfsimulationharness -n $NP --test --parameters mu0 0.10 \
                                               rheology WETQZ \
                                               V 50.0 \
                                               A 10.0 A 25.0 A 50.0 A 100.0 \
                                               dip 20.0 \
                                               Dc 80.0 \
                                               -- $repo/00_Idealized/subduction_steadystate_linpicard_p2p1p2.shml 1> fig5b.log 2>&1
tfsimulationharness -n $NP --test --parameters mu0 0.00 mu0 0.03 \
                                               rheology WETQZ \
                                               V 10.0 \
                                               A 10.0 A 25.0 A 50.0 A 100.0 \
                                               dip 20.0 \
                                               Dc 80.0 \
                                               -- $repo/00_Idealized/subduction_steadystate_linpicard_p2p1p2.shml 1> fig5c.log 2>&1
tfsimulationharness -n $NP --test --parameters mu0 0.00 mu0 0.03 \
                                               rheology WETQZ \
                                               V 10.0 V 20.0 V 50.0 V 100.0 V 200.0 \
                                               A 50.0 \
                                               dip 20.0 \
                                               Dc 80.0 \
                                               -- $repo/00_Idealized/subduction_steadystate_linpicard_p2p1p2.shml 1> fig5d.log 2>&1
tfsimulationharness -n $NP --test --parameters mu0 0.00 mu0 0.03 \
                                               rheology WETQZ \
                                               V 50.0 \
                                               A 50.0 \
                                               dip 15.0 dip 20.0 dip 30.0 dip 45.0 \
                                               Dc 80.0 \
                                               -- $repo/00_Idealized/subduction_steadystate_linpicard_p2p1p2.shml 1> fig5e.log 2>&1
tfsimulationharness -n $NP --test --parameters mu0 0.00 mu0 0.03 \
                                               rheology WETQZ \
                                               V 50.0 \
                                               A 50.0 \
                                               dip 20.0 \
                                               Dc 60.0 Dc 80.0 Dc 100.0 Dc 120.0 Dc 140.0 \
                                               -- $repo/00_Idealized/subduction_steadystate_linpicard_p2p1p2.shml 1> fig5f.log 2>&1

# figure 6

tfsimulationharness -n $NP --test --parameters mu0 0.03 mu0 0.10 \
                                               rheology SERP rheology BIOT1 rheology WETQZ rheology WESTERLY rheology MUSC rheology WETOLV \
                                               V 50.0 \
                                               A 50.0 \
                                               dip 20.0 \
                                               Dc 80.0 \
                                               -- $repo/00_Idealized/subduction_steadystate_linpicard_p2p1p2.shml 1> fig6.log 2>&1

# figure 7, 8 & 9

tfsimulationharness -n $NP --test --parameters mu0 0.00 mu0 0.03 mu0 0.05 mu0 0.10 mu0 0.15 \
                                               rheology WETQZ \
                                               Dc 80.0 \
                                               -- $repo/01_Alaska_Peninsula/subduction_steadystate_linpicard_p2p1p2.shml 1> fig7.log 2>&1

# figure 10 (Alaska run as part of figure 7) & table 2

tfsimulationharness -n $NP --test --parameters mu0 0.00 mu0 0.03 mu0 0.05 \
                                               rheology WETQZ \
                                               Dc 80.0 \
                                               -- $repo/07_Nicaragua/subduction_steadystate_linpicard_p2p1p2.shml \
                                                  $repo/48_N_Honshu/subduction_steadystate_linpicard_p2p1p2.shml \
                                                  $repo/59_CAFE09/subduction_steadystate_linpicard_p2p1p2.shml 1> fig10.log 2>&1

# extra simulations

tfsimulationharness -n $NP --test --parameters mu0 0.10 \
                                               rheology WETQZ \
                                               V 10.0 V 20.0 V 50.0 V 100.0 V 200.0 \
                                               A 50.0 \
                                               dip 20.0 \
                                               Dc 80.0 \
                                               -- $repo/00_Idealized/subduction_steadystate_linpicard_p2p1p2.shml 1> extrasims1.log 2>&1

