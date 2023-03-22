# Copyright (C) 2013 Columbia University in the City of New York and others.
#
# Please see the AUTHORS file in the main source directory for a full list
# of contributors.
#
# This file is part of TerraFERMA.
#
# TerraFERMA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TerraFERMA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with TerraFERMA. If not, see <http://www.gnu.org/licenses/>.
#
#
# Builds a Docker image with a full installation of TerraFERMA and the
# tutorial materials for CIDER 2017, Berkeley, CA.  
# The built image can be found at:
#
#   https://hub.docker.com/r/terraferma/cider_tutorials
#

# build using the TerraFERMA v1.0.1
FROM terraferma/dev:fenics-2019.1.0
MAINTAINER cwilson <cwilson@carnegiescience.edu>

USER root
WORKDIR /tmp

# download and install gmsh from source
ENV GMSH_PREFIX /usr/local/gmsh
RUN git clone -b gmsh_4_0_7 -q https://gitlab.onelab.info/gmsh/gmsh.git && \
cd gmsh && \
mkdir build && \
cd build && \
cmake -DCMAKE_INSTALL_PREFIX=${GMSH_PREFIX} ../. && \
make && \
make install && \
pip3 install pygmsh==6.0.2 && \
rm -rf /tmp/*
# install an environment module for gmsh
COPY gmsh.configmodule /usr/local/share/environment-modules/gmsh

# install a few extra packages
RUN apt-get update && \
    apt-get -y --with-new-pkgs \
        -o Dpkg::Options::="--force-confold" -o Dpkg::Options::="--force-confdef" upgrade && \
    apt-get -y install \
                       eog \
                       libxt-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# download and install tferma_utils from source
ENV TFERMA_UTILS_PREFIX /usr/local/tferma_utils
ARG CACHEBUST=1
RUN git clone -b fenics-2019.1.0 -q https://bitbucket.org/tferma/tferma_utils.git && \
    cd tferma_utils && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_INSTALL_PREFIX=${TFERMA_UTILS_PREFIX} ../. && \
    make && \
    make install && \
    rm -rf /tmp/*
# install an environment module for tferma_utils
COPY tferma_utils.configmodule /usr/local/share/environment-modules/tferma_utils

USER tfuser
WORKDIR $TF_HOME

# install and build the subduction repos
RUN export PYTHONPATH=$TF_PREFIX/lib/python3.6/site-packages:$SPUD_PREFIX/lib/python3.6/site-packages:$FENICS_PREFIX/lib/python3.6/site-packages && \
    export PATH=$TF_PREFIX/bin:$SPUD_PREFIX/bin:$FENICS_PREFIX/bin:$PATH && \
    export LD_LIBRARY_PATH=$SPUD_PREFIX/lib:$FENICS_PREFIX/lib:$LD_LIBRARY_PATH && \
    export PETSC_DIR=$PETSC_PREFIX && \
    export PKG_CONFIG_PATH=$FENICS_PREFIX/lib/pkgconfig:$PKG_CONFIG_PATH && \
    export DIAMOND_CONFIG_PATH=$TF_PREFIX/share/buckettools/diamond:$DIAMOND_CONFIG_PATH && \
    export CMAKE_MODULE_PATH=$TF_PREFIX/share/buckettools/cmake/modules:$CMAKE_MODULE_PATH && \
    export TF_CMAKE_PATH=$TF_PREFIX/share/terraferma/cpp && \
    git clone -b global_suite -q https://bitbucket.org/cwilson/global_suite_w_shearheating.git global_suite

USER root
WORKDIR /tmp
# install an environment module for extra scripts
COPY extra_scripts.configmodule /usr/local/share/environment-modules/extra_scripts
USER tfuser
WORKDIR $TF_HOME

COPY bash.load-modules $TF_HOME/.bash.load-modules
RUN cat $TF_HOME/.bash.load-modules >> $TF_HOME/.profile
# set some useful aliases
COPY bash_aliases $TF_HOME/.bash_aliases
# update welcome message
COPY WELCOME $TF_HOME/WELCOME
COPY README.md $TF_HOME/README.md

USER root

