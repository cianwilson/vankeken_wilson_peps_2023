#!/usr/bin/env python3

import os
import matplotlib.tri as tri
import matplotlib.pyplot as plt
import numpy as np
from buckettools.statfile import parser as statparser
import matplotlib.colors as mcolors
from buckettools.threadlibspud import *
import pickle
import json
import glob
from itertools import cycle
from math import cos, atan

def annotate_axes(ax, text, fontsize=18):
    ax.text(0.5, 0.5, text, transform=ax.transAxes,
            ha="center", va="center", fontsize=fontsize, color="darkgrey")

def extract_temperatures(filename, ssfilename=None, indices=None):

  gs_kw = dict(width_ratios=[1, 1], height_ratios=[1])
  fig, axd = plt.subplot_mosaic([['sT', 'mT']],
                                gridspec_kw=gs_kw, figsize=(6.4,4.8))

  axs = axd['sT']
  axm = axd['mT']

  lines = []

  yd = -150.

  if ssfilename is not None:
    sspath = os.path.split(ssfilename)[0]
    threadlibspud.load_options(ssfilename)
    ssbasename = libspud.get_option("/io/output_base_name")
    cd = libspud.get_option("/system::Stokes/coefficient::CouplingDepth/type/rank/value/constant")
    threadlibspud.clear_options()

    ssdet = statparser(os.path.join(sspath, ssbasename+".det"))

    ss_slab_y = ssdet['SlabLayer98']['position_1'][:,-1]
    ss_slab_T = ssdet['Temperature']['Temperature']['SlabLayer98']
    ss_moho_y = ssdet['SlabLayer108']['position_1'][:,-1]
    ss_moho_T = ssdet['Temperature']['Temperature']['SlabLayer108']

    cdi = np.abs(ss_slab_y+cd).argmin()

    sssxind = ss_slab_y > yd
    ssmxind = ss_moho_y > yd
    sT = ss_slab_T[:,-1]
    lines.append(axs.plot(sT[sssxind], ss_slab_y[sssxind], 'k--', linewidth=1, label='steady')[0])
    axm.plot(ss_moho_T[:,-1][ssmxind], ss_moho_y[ssmxind], 'k--', linewidth=1)
    axs.plot(sT[cdi], ss_slab_y[cdi], 'k*')

  path = os.path.split(filename)[0]
  threadlibspud.load_options(filename)
  basename = libspud.get_option("/io/output_base_name")
  cd = libspud.get_option("/system::Stokes/coefficient::CouplingDepth/type/rank/value/constant")
  v0 = libspud.get_option("/system::Stokes/coefficient::VelocityScale/type/rank/value/constant")
  vconv = libspud.get_option("/system::Stokes/coefficient::ConvergenceSpeed/type/rank/value/constant") # m/yr
  h  = libspud.get_option("/system::Stokes/coefficient::LengthScale/type/rank/value/constant")
  threadlibspud.clear_options()
    
  t0 = h/v0
  
  det = statparser(os.path.join(path, basename+".det"))

  times = det['ElapsedTime']['value']
  slab_x = det['SlabLayer98']['position_0'][:,-1]
  slab_y = det['SlabLayer98']['position_1'][:,-1]
  slab_T = det['Temperature']['Temperature']['SlabLayer98']
  moho_x = det['SlabLayer108']['position_0'][:,-1]
  moho_y = det['SlabLayer108']['position_1'][:,-1]
  moho_T = det['Temperature']['Temperature']['SlabLayer108']

  if indices is None: indices = list(range(2, slab_T.shape[-1]))

  colors_cycle = cycle(mcolors.BASE_COLORS)

  for i in indices:
    xd = vconv*times[i]*t0*cos(atan(0.5))/1.e3
    sxind = np.logical_and(slab_x < xd, slab_y > yd)
    mxind = np.logical_and(moho_x < xd, moho_y > yd)
    sT = slab_T[:,i]
    color = next(colors_cycle)
    lines.append(axs.plot(sT[sxind], slab_y[sxind], color=color, linestyle='-', linewidth=1, \
                 label="{:2.1f} Myr".format(times[i]*t0/1.e6,))[0])
    axm.plot(moho_T[:,i][mxind], moho_y[mxind], color=color, linestyle='-', linewidth=1)


  axs.tick_params(bottom=True, top=True, left=True, right=True)
  axm.tick_params(bottom=True, top=True, left=True, right=True)
  axs.set_ylabel('$y$ (km)')
  axm.set_yticklabels([])
  axm.set_yticks(axs.get_yticks())
  axm.set_ylim(axs.get_ylim())
  axm.set_xlabel('$T$ ($^\circ$C)')
  axs.set_xlabel('$T$ ($^\circ$C)')

  fig.legend(handles=lines)
  fig.tight_layout()

  fig.savefig(os.path.join("subduction_slabT_plot.pdf"), dpi=400)

if __name__ == "__main__":
  import argparse
  import os

  argparser = argparse.ArgumentParser( \
                         description="""Plot the slab temperature given a tfml file in a run directory.""")
  argparser.add_argument('filename', action='store', metavar='filename', type=str,
                      help='specify time-dependent tfml file')
  argparser.add_argument('-ss', '--ssfilename', action='store', metavar='ssfilename', type=str, required=False,
                      default=None, help='specify steady state tfml file')
  argparser.add_argument('-i', '--indices', action='store', metavar='index', type=int, default=None, nargs='+',
                      help='indices of times to plot')
  args = argparser.parse_args()

  extract_temperatures(args.filename, ssfilename=args.ssfilename, indices=args.indices)

