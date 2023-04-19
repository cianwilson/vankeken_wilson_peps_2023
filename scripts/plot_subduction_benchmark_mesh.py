#!/usr/bin/env python3

import os
import matplotlib.tri as tri
import matplotlib.pyplot as plt
import numpy as np
from buckettools import vtktools
from matplotlib.colors import LinearSegmentedColormap
import pickle
import json
import glob

def annotate_axes(ax, text, fontsize=18):
    ax.text(0.5, 0.5, text, transform=ax.transAxes,
            ha="center", va="center", fontsize=fontsize, color="darkgrey")

def extract_mesh(filenames1):

  gs_kw = dict(width_ratios=[1]*len(filenames1), height_ratios=[1]*2)
  fig, axd = plt.subplot_mosaic([['mesh'+repr(i) for i in range(len(filenames1))],
                                 ['zoom'+repr(i) for i in range(len(filenames1))]],
                                gridspec_kw=gs_kw, figsize=(len(filenames1)*6.4,2*4.8))

  for i1, filename1 in enumerate(filenames1):
    path1 = os.path.split(filename1)[0]
    print(path1)

    vtu1 = vtktools.vtu(filename1)
  
    coords = vtu1.GetLocations()
    topo = [vtu1.GetCellPoints(i) for i in range(vtu1.ugrid.GetNumberOfCells())]
    # re-order topology to be anticlockwise
    for t in topo:
      if np.cross(coords[t[1],:2]-coords[t[0],:2], coords[t[2],:2]-coords[t[0],:2]).item() < 0.0: t[:] = t[[0,2,1]]

    mesh = tri.Triangulation(coords[:,0], coords[:,1], triangles=topo)

    scoords = None
    mcoords = None
    cd = None

    scoordsl = None
    mcoordsl = None
    cdl = None

    scoordy = None
    tcoordx = None

    slabfilename = os.path.join(path1, 'subduction_solid.json')
    if os.path.isfile(slabfilename):
      with open(slabfilename, 'r') as f:
        slab = json.load(f)

      scoordy = np.asarray(slab["slab_y"])
      scoordsl = np.stack([slab["slab_x"], slab["slab_y"]])
      cdl = scoordsl[:,np.abs(scoordsl[-1,:]+float(slab["Dc"])).argmin()]
      sT = np.asarray(slab["slab_T"])
      cdT = sT[np.abs(scoordsl[-1,:]+float(slab["Dc"])).argmin()]

      if "slab_x_108" in slab:
        mcoordsl = np.stack([slab["slab_x_108"], slab["slab_y_108"]])
        mT = np.asarray(slab["slab_T_108"])

    else:
      slabpaths = glob.glob1(path1, '*slabpaths.001')
      if len(slabpaths) > 0: 
        slabfilename = os.path.join(path1, slabpaths[0])
        slab = np.loadtxt(slabfilename)

        scoordy = slab[slab[:,4]==98][:,1]
        scoordsl = np.stack([slab[slab[:,4]==98][:,0], slab[slab[:,4]==98][:,1]])
        mcoordsl = np.stack([slab[slab[:,4]==108][:,0], slab[slab[:,4]==108][:,1]])
      elif os.path.isfile(os.path.join(path1, "slabT.dat")):
        slab = np.loadtxt(os.path.join(path1, "slabT.dat"))

        scoordy = slab[:,0]
        
    scoords = scoordsl
    mcoords = mcoordsl
    cd = cdl

    ax = axd['mesh'+repr(i1)]
    ax.triplot(mesh, 'k-', lw=0.5, color='0.2')
    if scoords is not None: ax.plot(scoords[0], scoords[1], 'r-')
    if mcoords is not None: ax.plot(mcoords[0], mcoords[1], 'r--')
    if cd is not None: ax.plot(cd[0], cd[1], '*', markeredgecolor='r', markerfacecolor='w', markersize=8)
    ax.set_aspect('equal')
    ax.set_xlabel('$x$ (km)')
    if i1==0: ax.set_ylabel('$y$ (km)')
    if i1 > 0: ax.yaxis.set_ticklabels([])

    ax = axd['zoom'+repr(i1)]
    ax.triplot(mesh, 'k-', lw=0.5, color='0.2')
    if scoords is not None: ax.plot(scoords[0], scoords[1], 'r-')
    if mcoords is not None: ax.plot(mcoords[0], mcoords[1], 'r--')
    if cd is not None: ax.plot(cd[0], cd[1], '*', markeredgecolor='r', markerfacecolor='w', markersize=8)
    ax.set_xlabel('$x$ (km)')
    if i1==0: ax.set_ylabel('$y$ (km)')
    if i1 > 0: ax.yaxis.set_ticklabels([])
    ax.set_xlim([75, 200])
    ax.set_ylim([-100, -25])
    ax.set_aspect('equal', 'box')

  fig.tight_layout()

  #for k in axd:
  #    annotate_axes(axd[k], f'axd["{k}"]', fontsize=14)
  fig.savefig(os.path.join("subduction_mesh_plot.pdf"), dpi=400)

if __name__ == "__main__":
  import argparse
  import os

  parser = argparse.ArgumentParser( \
                         description="""Plot the temperature of xdmf or vtu \"subduction\" files.""")
  parser.add_argument('filenames1', action='store', metavar='filenames1', type=str, nargs='+',
                      help='specify first vtu, pvtu or xdmf filenames')
  args = parser.parse_args()

  extract_mesh(args.filenames1)

