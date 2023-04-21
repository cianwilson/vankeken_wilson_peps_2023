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

def annotate_axes(ax, text, fontsize=18):
    ax.text(0.5, 0.5, text, transform=ax.transAxes,
            ha="center", va="center", fontsize=fontsize, color="darkgrey")

def extract_temperatures(filenames1, filenames2=None, indices1=[-1], indices2=[-1]):

  gs_kw = dict(width_ratios=[1]*len(filenames1), height_ratios=[1]*2)
  fig, axd = plt.subplot_mosaic([['T'+repr(i) for i in range(len(filenames1))],
                                 ['dT'+repr(i) for i in range(len(filenames1))]],
                                gridspec_kw=gs_kw, figsize=(len(filenames1)*6.4,2*4.8))

  lindices1 = list(indices1)
  if len(indices1) == 1: lindices1 = indices1*len(filenames1)
  lindices2 = list(indices2)
  if len(indices2) == 1: lindices2 = indices2*len(filenames2)
  
  Tmin = 6.e6
  Tmax = 0.0
  absmaxdeltaT = 0.0
  for i1, filename1 in enumerate(filenames1):
    path1 = os.path.split(filename1)[0]
    filename2 = None if filenames2 is None else filenames2[i1]
    path2 = None if filename2 is None else os.path.split(filename2)[0]
    print(path1)

    vtu1 = vtktools.vtu(filename1, tindex=lindices1[i1])
    Tname1 = "temperature" if "temperature" in vtu1.GetFieldNames() else "Temperature::PotentialTemperature"
    T1 = vtu1.GetField(Tname1)[:,-1]
    Tmin = min(Tmin, T1.min())
    Tmax = max(Tmax, T1.max())
    vtudiff = vtu1
    Tname2 = None
    if filename2 is not None:
      vtu2 = vtktools.vtu(filename2, tindex=lindices2[i1])
      Tname2 = "temperature" if "temperature" in vtu2.GetFieldNames() else "Temperature::PotentialTemperature"
      vtudiff = vtktools.VtuDiff(vtu1, vtu2, {Tname1:Tname2})
      deltaT = vtudiff.GetField(Tname1)[:,-1]
      absmaxdeltaT = max(absmaxdeltaT, np.abs(deltaT).max())
  
  for i1, filename1 in enumerate(filenames1):
    path1 = os.path.split(filename1)[0]
    filename2 = None if filenames2 is None else filenames2[i1]
    path2 = None if filename2 is None else os.path.split(filename2)[0]
    print(path1)

    vtu1 = vtktools.vtu(filename1, tindex=lindices1[i1])
    Tname1 = "temperature" if "temperature" in vtu1.GetFieldNames() else "Temperature::PotentialTemperature"
    vtudiff = vtu1
    Tname2 = None
    if filename2 is not None:
      vtu2 = vtktools.vtu(filename2, tindex=lindices2[i1])
      Tname2 = "temperature" if "temperature" in vtu2.GetFieldNames() else "Temperature::PotentialTemperature"
      vtudiff = vtktools.VtuDiff(vtu1, vtu2, {Tname1:Tname2})
  
    coords = vtu1.GetLocations()
    topo = [vtu1.GetCellPoints(i) for i in range(vtu1.ugrid.GetNumberOfCells())]
    # re-order topology to be anticlockwise
    for t in topo:
      if np.cross(coords[t[1],:2]-coords[t[0],:2], coords[t[2],:2]-coords[t[0],:2]).item() < 0.0: t[:] = t[[0,2,1]]
    T1 = vtu1.GetField(Tname1)[:,-1]
    deltaT = vtudiff.GetField(Tname1)[:,-1]

    mesh = tri.Triangulation(coords[:,0], coords[:,1], triangles=topo)

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
        if os.path.isfile(slabfilename):
          with open(slabfilename, 'r') as f:
            slab = json.load(f)
        else:
          continue

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
        slabpaths = glob.glob1(path, '*slabpaths.001')
        if len(slabpaths) > 0: 
          slabfilename = os.path.join(path, slabpaths[0])
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

      if i==0:
        scoords = scoordsl
        mcoords = mcoordsl
        cd = cdl

    if filename2 is not None:
      ax = axd['dT'+repr(i1)]
      Tc = ax.tripcolor(mesh, deltaT, shading='gouraud', vmin=-absmaxdeltaT, vmax=absmaxdeltaT, cmap=gmtcmap)
      #Tc = ax.tripcolor(mesh, deltaT, shading='gouraud', cmap=gmtcmap)
      if scoords is not None: ax.plot(scoords[0], scoords[1], 'k-')
      if mcoords is not None: ax.plot(mcoords[0], mcoords[1], 'k--')
      if cd is not None: ax.plot(cd[0], cd[1], 'k*')
      if i1==len(filenames1)-1: fig.colorbar(Tc, ax=ax, location='right', orientation='vertical', shrink=0.5, label=r'$\Delta T$ ($^\circ$C)')
      ax.set_aspect('equal', 'box')
      #if i1==len(filenames1)-1: ax.set_xlabel('$x$ (km)')
      ax.set_xlabel('$x$ (km)')
      if i1==0: ax.set_ylabel('$y$ (km)')
      if i1 > 0: ax.yaxis.set_ticklabels([])
      #if i1<len(filenames1)-1: ax.xaxis.set_ticklabels([])

    ax = axd['T'+repr(i1)]
    Tc = ax.tripcolor(mesh, T1, shading='gouraud', vmin=Tmin, vmax=Tmax, cmap=gmtcmap)
    if scoords is not None: ax.plot(scoords[0], scoords[1], 'k-')
    if mcoords is not None: ax.plot(mcoords[0], mcoords[1], 'k--')
    if cd is not None: ax.plot(cd[0], cd[1], 'k*')
    if i1==len(filenames1)-1: fig.colorbar(Tc, ax=ax, location='right', orientation='vertical', shrink=0.5, label=r'$T$ ($^\circ$C)')
    ax.set_aspect('equal')
    #if i1==len(filenames1)-1: ax.set_xlabel('$x$ (km)')
    ax.set_xlabel('$x$ (km)')
    if i1==0: ax.set_ylabel('$y$ (km)')
    if i1 > 0: ax.yaxis.set_ticklabels([])
    #if i1<len(filenames1)-1: ax.xaxis.set_ticklabels([])

  fig.tight_layout()

  xmin = 6.e6
  xmax = -6.e6
  ymin = 6.e6
  ymax = -6.e6
  for i1, filename1 in enumerate(filenames1):
    xlim = axd['T'+repr(i1)].get_xlim()
    xmin = min(xmin, xlim[0])
    xmax = max(xmax, xlim[1])
    ylim = axd['T'+repr(i1)].get_ylim()
    ymin = min(ymin, ylim[0])
    ymax = max(ymax, ylim[1])

  xticks = axd['T'+repr(0)].get_xticks()
  yticks = axd['T'+repr(0)].get_yticks()
  opTf  = axd['T'+repr(len(filenames1)-1)].get_position()
  opdTf = axd['dT'+repr(len(filenames1)-1)].get_position()
  for i1 in range(len(filenames1)-1, -1, -1):

    axd['T'+repr(i1)].tick_params(bottom=True, top=True, left=True, right=True)
    axd['T'+repr(i1)].set_xticks(xticks)
    axd['T'+repr(i1)].set_yticks(yticks)
    axd['T'+repr(i1)].set_xlim([xmin, xmax])
    axd['T'+repr(i1)].set_ylim([ymin, ymax])
    opT  = axd['T'+repr(i1)].get_position()
    axd['T'+repr(i1)].set_position([opT.x0, opTf.y0, opTf.x1-opTf.x0, opTf.y1-opTf.y0])

    axd['dT'+repr(i1)].tick_params(bottom=True, top=True, left=True, right=True)
    axd['dT'+repr(i1)].set_xticks(xticks)
    axd['dT'+repr(i1)].set_yticks(yticks)
    axd['dT'+repr(i1)].set_xlim([xmin, xmax])
    axd['dT'+repr(i1)].set_ylim([ymin, ymax])
    opdT  = axd['dT'+repr(i1)].get_position()
    axd['dT'+repr(i1)].set_position([opdT.x0, opdTf.y0, opdTf.x1-opdTf.x0, opdTf.y1-opdTf.y0])


  #for k in axd:
  #    annotate_axes(axd[k], f'axd["{k}"]', fontsize=14)
  fig.savefig(os.path.join("subduction_justT_plot.pdf"), dpi=400)

if __name__ == "__main__":
  import argparse
  import os

  parser = argparse.ArgumentParser( \
                         description="""Plot the temperature of xdmf or vtu \"subduction\" files.""")
  parser.add_argument('-f1', '--filenames1', action='store', metavar='filenames1', type=str, required=True, nargs='+',
                      help='specify first vtu, pvtu or xdmf filenames')
  parser.add_argument('-f2', '--filenames2', action='store', metavar='filenames2', type=str, required=False, nargs='+', 
                      default=None, help='specify second vtu, pvtu or xdmf filenames')
  parser.add_argument('-i1', '--indices1', action='store', metavar='index1', type=int, default=[-1], nargs='+',
                      help='index (time) of filename 1 (defaults to -1, the last time-step)')
  parser.add_argument('-i2', '--indices2', action='store', metavar='index2', type=int, default=[-1], nargs='+',
                      help='index (time) of filename 2 (defaults to -1, the last time-step)')
  args = parser.parse_args()

  if args.filenames2 is not None:  assert(len(args.filenames1)==len(args.filenames2))
  assert(len(args.indices1)==len(args.filenames1) or len(args.indices1)==1)
  assert(len(args.indices2)==len(args.filenames2) or len(args.indices2)==1)

  extract_temperatures(args.filenames1, filenames2=args.filenames2, indices1=args.indices1, indices2=args.indices2)

