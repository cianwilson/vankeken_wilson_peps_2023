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

def extract_temperatures(filename1, filename2=None, title=None, index=-1):
  path1 = os.path.split(filename1)[0]
  path2 = None if filename2 is None else os.path.split(filename2)[0]

  vtu1 = vtktools.vtu(filename1, tindex=index)
  Tname1 = "temperature" if "temperature" in vtu1.GetFieldNames() else "Temperature::PotentialTemperature"
  vtudiff = vtu1
  Tname2 = None
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

  gs_kw = dict(width_ratios=[2, 1, 2], height_ratios=[1, 2])
  fig, axd = plt.subplot_mosaic([['q', '.', '.'],
                                 ['T', 'sT', 'dT']],
                                gridspec_kw=gs_kw, figsize=(2.5*6.4,1.5*4.8))

  cs = ['k', 'r']
  lss = ['k-', 'ok']
  lsm = ['k--', 'ok']
  lsq = ['k-', 'ok']
  skip = [1, 30]
  scoords = None
  mcoords = None
  cd = None
  for i, (Tname, path) in enumerate(zip([Tname1, Tname2], \
                                        [path1,  path2])):
    if path is None: continue
    scoordsl = None
    mcoordsl = None
    cdl = None

    sT = None
    cdT = None
    mT = None
    scoordy = None
    tcoordx = None
    tq = None
    cdq = None
    if Tname == "Temperature::PotentialTemperature":
      slabfilename = os.path.join(path, 'subduction_solid.json')
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

      tcoordx = np.asarray(slab["surface_x"])
      tq = np.asarray(slab["surface_q"])
      cdx = scoordsl[0,np.abs(scoordsl[-1,:]+float(slab["Dc"])).argmin()]
      cdq = [cdx, tq[np.abs(tcoordx-cdx).argmin()]]

    else:
      slabpaths = sorted(glob.glob1(path, '*slabpaths.*'), key=lambda f: int(f.split('.')[-1]))
      if len(slabpaths) > 0: 
        slabfilename = os.path.join(path, slabpaths[-1])
        slab = np.loadtxt(slabfilename)

        scoordy = slab[slab[:,4]==98][:,1]
        scoordsl = np.stack([slab[slab[:,4]==98][:,0], slab[slab[:,4]==98][:,1]])
        sT = slab[slab[:,4]==98][:,2]
        mcoordsl = np.stack([slab[slab[:,4]==108][:,0], slab[slab[:,4]==108][:,1]])
        mT = slab[slab[:,4]==108][:,2]
      elif os.path.isfile(os.path.join(path, "slabT.dat")):
        slab = np.loadtxt(os.path.join(path, "slabT.dat"))

        scoordy = slab[:,0]
        sT = slab[:,1]
      else:
        continue
        

      topfilename = os.path.join(path, 'dtdx.001')
      if os.path.isfile(topfilename):
        top = np.loadtxt(topfilename)
        tcoordx = top[:,0]
        tq = top[:,2]*1.e-3
      elif os.path.isfile(os.path.join(path, 'heatflow.dat')):
        top = np.loadtxt(os.path.join(path, 'heatflow.dat'))
        tcoordx = top[:,0][::-1]
        tq = top[:,1][::-1]*1.e-3

    ax = axd['sT']
    ax.plot(sT[:-1:skip[i]], scoordy[:-1:skip[i]], lss[i], fillstyle='none', markersize=5)
    if mcoordsl is not None: ax.plot(mT[:-3:skip[i]], mcoordsl[-1][:-3:skip[i]], lsm[i], fillstyle='none', markersize=5)
    if cdT is not None: ax.plot(cdT, -float(slab["Dc"]), 'k*')
    ax.set_xlabel('$T$ ($^\circ$C)')
    ax.yaxis.set_ticklabels([])

    ax = axd['q']
    if tcoordx is not None: ax.plot(tcoordx[::skip[i]], tq[::skip[i]], lsq[i], fillstyle='none', markersize=5)
    if cdq is not None: ax.plot(cdq[0], cdq[1], 'k*')
    ax.set_ylabel('$q$ (W/m$^2$)')
    ax.xaxis.set_ticklabels([])

    if i==0:
      scoords = scoordsl
      mcoords = mcoordsl
      cd = cdl

  if filename2 is not None:
    ax = axd['dT']
    absmaxdeltaT = np.abs(deltaT).max()
    Tc = ax.tripcolor(mesh, deltaT, shading='gouraud', vmin=-absmaxdeltaT, vmax=absmaxdeltaT, cmap=gmtcmap)
    if scoords is not None: ax.plot(scoords[0], scoords[1], 'k-')
    if mcoords is not None: ax.plot(mcoords[0], mcoords[1], 'k--')
    if cd is not None: ax.plot(cd[0], cd[1], 'k*')
    fig.colorbar(Tc, ax=ax, location='bottom', orientation='horizontal', shrink=0.9, label=r'$\Delta T$ ($^\circ$C)')
    ax.set_aspect('equal', 'box')
    ax.set_xlabel('$x$ (km)')
    ax.yaxis.set_ticklabels([])

  ax = axd['T']
  Tc = ax.tripcolor(mesh, T1, shading='gouraud', cmap=gmtcmap)
  if scoords is not None: ax.plot(scoords[0], scoords[1], 'k-')
  if mcoords is not None: ax.plot(mcoords[0], mcoords[1], 'k--')
  if cd is not None: ax.plot(cd[0], cd[1], 'k*')
  fig.colorbar(Tc, ax=ax, location='bottom', orientation='horizontal', shrink=0.9, label=r'$T$ ($^\circ$C)')
  ax.set_aspect('equal')
  ax.set_xlabel('$x$ (km)')
  ax.set_ylabel('$y$ (km)')

  if title is not None: fig.suptitle(title)
  fig.tight_layout()

  axd['T'].tick_params(bottom=True, top=True, left=True, right=True)
  axd['sT'].tick_params(bottom=True, left=True, right=True)
  opT = axd['T'].get_position()
  opq = axd['q'].get_position()
  axd['q'].set_position([opT.x0, opq.y0, opT.x1-opT.x0, opq.y1-opq.y0])
  axd['q'].set_xticks(axd['T'].get_xticks())
  axd['q'].set_xlim(axd['T'].get_xlim())
  opsT = axd['sT'].get_position()
  axd['sT'].set_position([opsT.x0, opT.y0, opsT.x1-opsT.x0, opT.y1-opT.y0])
  axd['sT'].set_yticks(axd['T'].get_yticks())
  axd['sT'].set_ylim(axd['T'].get_ylim())
  axd['dT'].set_yticks(axd['T'].get_yticks())
  axd['dT'].set_ylim(axd['T'].get_ylim())
  axd['dT'].set_xticks(axd['T'].get_xticks())
  axd['dT'].set_xlim(axd['T'].get_xlim())

  fig.savefig(os.path.join(path1, "subduction_allT_plot.pdf"), dpi=400)

if __name__ == "__main__":
  import argparse
  import os

  parser = argparse.ArgumentParser( \
                         description="""Plot the temperature of xdmf or vtu \"subduction\" files.""")
  parser.add_argument('-f1', '--filename1', action='store', metavar='filename1', type=str, required=True,
                      help='specify first vtu, pvtu or xdmf filename')
  parser.add_argument('-f2', '--filename2', action='store', metavar='filename2', type=str, required=False, default=None,
                      help='specify second vtu, pvtu or xdmf filename')
  parser.add_argument('-t', '--title', action='store', metavar='index', type=str, default=None,
                      help='title to put on figure')
  parser.add_argument('-i', '--index', action='store', metavar='index', type=int, default=-1,
                      help='index (time) of plot (defaults to -1, the last time-step)')
  args = parser.parse_args()

  filename1 = os.path.abspath(args.filename1)
  filename2 = None
  if args.filename2 is not None: filename2 = os.path.abspath(args.filename2)

  extract_temperatures(filename1, filename2=filename2, title=args.title, index=args.index)

