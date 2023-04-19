#!/usr/bin/env python3

import os
import matplotlib.tri as tri
import matplotlib.pyplot as plt
import numpy as np
from buckettools import vtktools
from matplotlib.colors import LinearSegmentedColormap
import pickle
import json

# GMT colormap that is reproduced below (hopefully)
#0       0       0       255     100     34      34      255
#100     34      34      255     200     68      68      255
#200     68      68      255     300     102     102     255
#300     102     102     255     400     136     136     255
#400     136     136     255     500     170     170     255
#500     170     170     255     600     204     204     255
#600     204     204     255     700     238     238     255
#700     238     238     255     800     255     238     238
#800     255     238     238     900     255     204     204
#900     255     204     204     1000    255     170     170
#1000    255     170     170     1100    255     136     136
#1100    255     136     136     1200    255     102     102
#1200    255     102     102     1300    255     68      68
#1300    255     68      68      1400    255     34      34
#1400    255     34      34      1500    255     0       0

cdict = {'red':   [
                   [0.0,         0.0,        0.0],
                   [0.466666667, 0.93333333, 0.93333333],
                   [0.533333333, 1.0,        1.0],
                   [1.0,         1.0,        1.0]
                  ],
         'green': [
                   [0.0,         0.0,        0.0],
                   [0.466666667, 0.93333333, 0.93333333],
                   [0.533333333, 0.93333333, 0.93333333],
                   [0.6,         0.8,        0.8],
                   [1.0,         0.0,        0.0],
                  ],
         'blue':  [
                   [0.0,         1.0,        1.0],
                   [0.466666667, 1.0,        1.0],
                   [0.533333333, 0.93333333, 0.93333333],
                   [0.6,         0.8,        0.8],
                   [1.0,         0.0,        0.0]
                  ]
        }

gmtcmap = LinearSegmentedColormap('GMTCMap', segmentdata=cdict, N=256)

def extract_temperatures(filename1, filename2=None, slabfilename=None, index=-1):
  path = os.path.split(filename1)[0]

  vtu1 = vtktools.vtu(filename1, tindex=index)
  Tname1 = "temperature" if "temperature" in vtu1.GetFieldNames() else "Temperature::PotentialTemperature"
  vtudiff = vtu1
  if filename2 is not None:
    vtu2 = vtktools.vtu(filename2, tindex=index)
    Tname2 = "temperature" if "temperature" in vtu2.GetFieldNames() else "Temperature::PotentialTemperature"
    vtudiff = vtktools.VtuDiff(vtu1, vtu2, {Tname1:Tname2})
  
  coords = vtudiff.GetLocations()
  topo = [vtudiff.GetCellPoints(i) for i in range(vtudiff.ugrid.GetNumberOfCells())]
  # re-order topology to be anticlockwise
  for t in topo:
    if np.cross(coords[t[1],:2]-coords[t[0],:2], coords[t[2],:2]-coords[t[0],:2]).item() < 0.0: t[:] = t[[0,2,1]]
  T1 = vtu1.GetField(Tname1)[:,-1]
  deltaT = vtudiff.GetField(Tname1)[:,-1]

  mesh = tri.Triangulation(coords[:,0], coords[:,1], triangles=topo)

  if slabfilename is not None:
    with open(slabfilename, 'r') as f:
      slab = json.load(f)
    scoords = np.stack([slab["slab_x_98"], slab["slab_y_98"]])
    mcoords = np.stack([slab["slab_x_108"], slab["slab_y_108"]])
    cd = scoords[:,np.abs(scoords[-1,:]+float(slab["Dc"])).argmin()]

  if filename2 is not None:
    fig = plt.Figure(figsize=(6.4, 4.8))
    ax = fig.gca()
    absmaxdeltaT = np.abs(deltaT).max()
    Tc = ax.tripcolor(mesh, deltaT, shading='gouraud', vmin=-absmaxdeltaT, vmax=absmaxdeltaT, cmap=gmtcmap)
    if slabfilename is not None:
      ax.plot(scoords[0], scoords[1], 'k-')
      ax.plot(mcoords[0], mcoords[1], 'k--')
      ax.plot(cd[0], cd[1], 'k*')
    fig.colorbar(Tc, location='bottom', orientation='horizontal', shrink=0.9, label=r'$\Delta T$ (K)')
    ax.set_aspect('equal', 'box')
    ax.set_xlabel('$x$ (km)')
    fig.tight_layout()
    fig.savefig(os.path.join(path, "subduction_deltaT_plot.png"), dpi=300)

  fig = plt.Figure(figsize=(6.4, 4.8))
  ax = fig.gca()
  Tc = ax.tripcolor(mesh, T1, shading='gouraud', cmap=gmtcmap)
  if slabfilename is not None:
    ax.plot(scoords[0], scoords[1], 'k-')
    ax.plot(mcoords[0], mcoords[1], 'k--')
    ax.plot(cd[0], cd[1], 'k*')
  fig.colorbar(Tc, location='bottom', orientation='horizontal', shrink=0.9, label=r'$T$ (K)')
  ax.set_aspect('equal', 'box')
  ax.set_xlabel('$x$ (km)')
  ax.set_ylabel('$y$ (km)')
  fig.tight_layout()
  fig.savefig(os.path.join(path, "subduction_T_plot.png"), dpi=300)

if __name__ == "__main__":
  import argparse
  import os

  parser = argparse.ArgumentParser( \
                         description="""Plot the temperature for single or multiple xdmf \"subduction\" files.""")
  parser.add_argument('-f1', '--filename1', action='store', metavar='filename1', type=str, required=True,
                      help='specify first vtu, pvtu or xdmf filename')
  parser.add_argument('-f2', '--filename2', action='store', metavar='filename2', type=str, required=False, default=None,
                      help='specify second vtu, pvtu or xdmf filename')
  parser.add_argument('-s', '--slabfilename', action='store', metavar='slabfilename', type=str, required=False, default=None,
                      help='specify filename of json file to plot slab and moho on top of temperature')
  parser.add_argument('-i', '--index', action='store', metavar='index', type=int, default=-1,
                      help='index (time) of plot (defaults to -1, the last time-step)')
  args = parser.parse_args()

  filename1 = os.path.abspath(args.filename1)
  filename2 = None
  if args.filename2 is not None: filename2 = os.path.abspath(args.filename2)
  slabfilename = None
  if args.slabfilename is not None: slabfilename = os.path.abspath(args.slabfilename)

  extract_temperatures(filename1, filename2=filename2, slabfilename=slabfilename, index=args.index)

