#!/bin/sh

usage()
{
    echo "usage: run_tests.sh [-h]"
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

repo=$(dirname $(dirname $(realpath $0) ) )

echo $repo

pytest-3 --disable-warnings $repo/1d_poisson/fenics/poisson.py

tfsimulationharness --test $repo/1d_poisson/tf/poisson.shml



