#!/usr/bin/env python3

import os
import matplotlib.tri as tri
import pickle
import numpy as np
import json
import importlib
from buckettools import xdmftools

def extract_temperatures(filename, index=-1):
  path = os.path.split(filename)[0]
  
  xdmf = xdmftools.XDMF(filename)

  slabf = open(os.path.join(path, 'subduction.slab'), 'rb')
  slab = pickle.load(slabf)
  slabf.close()

  # walk through directory tree looking for sediment_thickness file
  dirs = list(filter(None, os.path.normpath(path).split(os.sep)))
  for i in range(len(dirs), -1, -1):
    spath = os.path.join(os.sep, *dirs[:i], "sediment_thickness.py")
    if os.path.exists(spath): break
  
  try:
    spec = importlib.util.spec_from_file_location("st", spath)
    st = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(st)
    z0 = st.z0
    z15 = st.z15
  except:
    print("WARNING: sediment_thickness.py not found")
    z0, z15 = 0.0, 0.0

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
  Ti = tri.CubicTriInterpolator(mesh, T)

  # bounding box
  x0 = slab.x[0]
  y0 = slab.y[0]
  xf = slab.x[-1]
  yf = slab.y[-1]

  # vertices
  nc = 1  # number of sampling points per line segment along slab
  scoords = np.empty((2,0))
  for curve in slab.interpcurves:
    scoords = np.append(scoords, np.stack([np.linspace(curve.points[0].x, curve.points[1].x, nc, endpoint=False), \
                                           np.linspace(curve.points[0].y, curve.points[1].y, nc, endpoint=False)]), axis=1)

  # normals
  snormals = np.stack([-slab.cs(scoords[0,:], nu=1), np.ones(scoords.shape[1])], axis=0)
  snormags = np.sqrt(np.sum(snormals**2, axis=0))
  snormals = snormals/snormags

 # sediment thicknesses
  y = scoords[1,:]
  ssthicks = np.where(y>y0, z0, np.where(y<-15, z15, (z0-z15)*(y-y0)/(y0+15) + z0))

  # set up layers
  layer_names = [str(name) for name in range(88, 113)]
  layer_factors = [0.0]*11 + [-0.5] + [-1.0]*13
  layer_offsets = np.arange(9.5, 0.0, -1).tolist() + [0.0]*3 + [-0.15, -0.45, -1.4] + np.arange(-2.5, -11, -1).tolist()

  results = {}
  for i in range(len(layer_names)):
    nscoords = scoords + (layer_factors[i]*ssthicks + layer_offsets[i])*snormals
    nmask = (nscoords[0,:] >= x0) & (nscoords[0,:] <= xf) & (nscoords[1,:] <= y0) & (nscoords[1,:] >= yf)
    nscoords = nscoords[:,nmask]

    name = layer_names[i]
    results['slab_x_'+name] = nscoords[0,:].tolist()
    results['slab_y_'+name] = nscoords[1,:].tolist()
    results['slab_T_'+name] = Ti(nscoords[0,:], nscoords[1,:]).data.tolist()

  with open(os.path.join(path, "subduction_solid_from_xdmf"+suffix+".json"), 'w') as f:
    json.dump(results, f, indent=4, separators=(",", ": "))

if __name__ == "__main__":
  import argparse
  import os

  parser = argparse.ArgumentParser( \
                         description="""Extract the temperature along, above and below the slab from xdmf \"subduction\" files.""")
  parser.add_argument('file', action='store', metavar='file', type=str, nargs='+',
                      help='specify filename(s)')
  parser.add_argument('-i', '--index', action='store', metavar='index', type=int, default=-1,
                      help='index (time) of plot (defaults to -1, the last time-step)')
  args = parser.parse_args()

  
  filenames = [os.path.abspath(f) for f in args.file]

  for filename in filenames:
    extract_temperatures(filename, index=args.index)
