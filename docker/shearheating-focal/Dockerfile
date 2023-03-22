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
FROM terraferma/dev:fenics-2019.1.0-focal
MAINTAINER cwilson <cwilson@carnegiescience.edu>

USER root
WORKDIR /tmp

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
ARG CACHEBUST=1
RUN git clone -b fenics-2019.1.0 -q https://bitbucket.org/tferma/tferma_utils.git && \
    cd tferma_utils && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_INSTALL_PREFIX=${INSTALL_PREFIX} ../. && \
    make && \
    make install && \
    rm -rf /tmp/*

USER tfuser
WORKDIR $TF_HOME

# install and build the subduction repos
RUN git clone -b global_suite -q https://bitbucket.org/cwilson/global_suite_w_shearheating.git global_suite

# set some useful aliases
COPY bash_aliases $TF_HOME/.bash_aliases
# update welcome message
COPY WELCOME $TF_HOME/WELCOME
COPY README.md $TF_HOME/README.md

USER root

