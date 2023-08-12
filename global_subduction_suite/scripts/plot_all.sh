#!/bin/sh

usage()
{
    echo "usage: plot_all_diffs.sh [-h]"
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

for f1 in `ls $repodir/??_*/subduction_linearized_p2p1p2.tfml.run/Dc_80.0/minres_1.0/cfl_1.0/run_0/subduction_solid.xdmf`;
do
  subdir=`echo $(realpath --relative-to=$repodir $f1) | awk -F "/" '{print $1}'`
  echo "Processing $subdir"
  f2=`ls $seprandir/$subdir/T_*.vtu | sort -n -t _ -k 2 | tail -n1`
  python3 $repodir/scripts/plot_temperatures.py -f1 $f1 -f2 $f2 -t $subdir
done

