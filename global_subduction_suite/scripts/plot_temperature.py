#!/usr/bin/env python3

import os
import matplotlib.tri as tri
import matplotlib.pyplot as plt
import numpy as np
from buckettools import xdmftools

def extract_temperatures(filename, index=-1):
  path = os.path.split(filename)[0]

  xdmf = xdmftools.XDMF(filename)
  
  index = index%len(xdmf.grids)  # deal with negative indices for filename purposes
  suffix = ''
  if len(xdmf.grids) > 1: suffix = '_'+repr(index)

  coords = xdmf.getlocations(tindex=index)
  topo = xdmf.gettopology(tindex=index)
  # re-order topology to be anticlockwise
  for t in topo:
    if np.cross(coords[t[1],:]-coords[t[0],:], coords[t[2],:]-coords[t[0],:]).item() < 0.0: t[:] = t[[0,2,1]]
  T = xdmf.getfield("Temperature::Temperature", tindex=index)[:,-1]

  mesh = tri.Triangulation(coords[:,0], coords[:,1], triangles=topo)

  ax = plt.gca()
  Tc = ax.tripcolor(mesh, T, shading='gouraud')
  fig = plt.gcf()
  fig.colorbar(Tc)
  ax.set_aspect('equal', 'box')
  fig.savefig(os.path.join(path, "subduction_T_plot"+suffix+".png"))
  plt.show()

if __name__ == "__main__":
  import argparse
  import os

  parser = argparse.ArgumentParser( \
                         description="""Plot the temperature for single or multiple xdmf \"subduction\" files.""")
  parser.add_argument('file', action='store', metavar='file', type=str, nargs='+',
                      help='specify filename(s)')
  parser.add_argument('-i', '--index', action='store', metavar='index', type=int, default=-1,
                      help='index (time) of plot (defaults to -1, the last time-step)')
  args = parser.parse_args()

  
  filenames = [os.path.abspath(f) for f in args.file]

  for filename in filenames:
    extract_temperatures(filename, index=args.index)

