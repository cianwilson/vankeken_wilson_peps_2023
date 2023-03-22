#!/usr/bin/python3
import os
import libspud
import shutil

def updatesmml(filename, params, outfilename=None):
  libspud.load_options(filename)

  smml_options = [
    ["/domain/location::DomainSurface/coast_distance", params["deltaxcoast"]], \
    ["/domain/location::UpperCrustBase/depth", params["deltazuc"]], \
    ["/domain/location::MohoBase/depth", params["deltazmoho"]], \
    ["/domain/location::UpperWedgeBase/depth", params["deltazoutflow"]], \
    ["/domain/location::DomainRight/extra_width", params["deltaxwidth"]], \
    ]

  changed = False
  for path, val in smml_options:
    if libspud.have_option(path) and val is not None: 
      libspud.set_option(path, float(val))
      changed = True

  if params["trench"] is not None:
    libspud.set_option("/slab/slab_surface/points/point::trench", [float(p) for p in params["trench"]])

  if params["slabpoints"] is not None:
    p = 5
    basepath = "/slab/slab_surface/points/point::p"
    for point in params["slabpoints"]:
      path = basepath+repr(p)
      try:
        libspud.set_option(path, [float(p) for p in point])
        changed = True
      except libspud.SpudNewKeyWarning:
        try:
          libspud.set_option_attribute(path+"/__value/dim1", "dim")
        except libspud.SpudNewKeyWarning:
          pass
        pass
      p = p + 1

  if changed:
    if outfilename is None: outfilename = filename
    if os.path.exists(outfilename): shutil.copy2(outfilename, outfilename+".bak")
    libspud.write_options(outfilename)

  libspud.clear_options()
  

if __name__ == "__main__":
  import argparse

  parser = argparse.ArgumentParser(description='Update a subduction global suite smml file from the command line.')
  parser.add_argument('filename', nargs='+', metavar='filename', type=str, help='specify the name of the smml file')
  parser.add_argument('--trench', metavar=('x', 'y'), nargs=2, type=float, required=False, default=None,
                      help='specify the trench coordinates (non-dim)')
  parser.add_argument('--point', metavar=('x', 'y'), nargs=2, type=float, required=False, default=None, action='append',
                      help='specify spline point (non-dim)')
  parser.add_argument('--deltaxcoast', metavar='deltax', type=float, required=False, default=None,
                      help='specify the coast distance (non-dim)')
  parser.add_argument('--deltazuc', metavar='deltaz', type=float, required=False, default=None,
                      help='specify the upper crust thickness (non-dim)')
  parser.add_argument('--deltazmoho', metavar='deltaz', type=float, required=False, default=None,
                      help='specify the moho depth (non-dim)')
  parser.add_argument('--deltazoutflow', metavar='deltaz', type=float, required=False, default=None,
                      help='specify the depth of outflow on the rhs (non-dim)')
  parser.add_argument('--deltaxwidth', metavar='deltax', type=float, required=False, default=None,
                      help='specify the extra width on the right of the domain (non-dim)')
  parser.add_argument('-o', '--output', metavar='filename', type=str, required=False, default=None,
                      help='specify the name of the output smml file (if different to input')
  args = parser.parse_args()

  params = vars(args)
  params.pop("output")

  points = params.pop("point")
  if points is not None:
    points.sort(key=lambda p: p[1], reverse=True)
    if len(points) < 3:
      raise Warning("Modifying slab points but less than 3 points specified.")
  params["slabpoints"] = points

  for filename in args.filename: updatesmml(filename, params, outfilename=args.output)

