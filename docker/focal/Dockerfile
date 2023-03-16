# Copyright (C) 2023 Carnegie Institution for Science and others.
#
# Builds a Docker image with a full installation of TerraFERMA and the
# materials for van Keken & Wilson, PEPS, 2023.  
# The built image can be found at:
#
#   https://github.com/users/cianwilson/packages/container/package/vankeken_wilson_peps_2023
#


# build using the TerraFERMA v1.0.1
FROM ghcr.io/terraferma/dev:fenics-2019.1.0-focal
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

# install the source repo
RUN git clone -q https://github.com/cianwilson/vankeken_wilson_peps_2023.git

# set some useful aliases
COPY bash_aliases $TF_HOME/.bash_aliases
# update welcome message
COPY WELCOME $TF_HOME/WELCOME
COPY README.md $TF_HOME/README.md

USER root

