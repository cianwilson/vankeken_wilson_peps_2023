#!/usr/bin/python3
import os
import libspud
import shutil

def updatetfml(filename, params, outfilename=None):
  libspud.load_options(filename)

  tfml_options = [
    [["/system::Solid/coefficient::ConvergenceSpeed/type/rank/value/constant", \
      "/system::Stokes/coefficient::ConvergenceSpeed/type/rank/value/constant"], params["vconv"]], \
    [["/system::Solid/coefficient::TrenchDepth/type/rank/value/constant", \
      "/system::Stokes/coefficient::TrenchDepth/type/rank/value/constant"], \
       -params["trench"][1] if params["trench"] is not None else None], \
    [["/system::Solid/coefficient::CoastDistance/type/rank/value/constant", \
      "/system::Stokes/coefficient::CoastDistance/type/rank/value/constant"], 
       params.get("deltaxcoast", None)], \
    [["/system::Solid/coefficient::UpperCrustThickness/type/rank/value/constant", \
      "/system::Stokes/coefficient::UpperCrustThickness/type/rank/value/constant"], 
       params.get("deltazuc", None)], \
    [["/system::Solid/coefficient::LowerCrustThickness/type/rank/value/constant", \
      "/system::Stokes/coefficient::LowerCrustThickness/type/rank/value/constant"], \
      params["deltazmoho"]-params["deltazuc"] \
      if params.get("deltazmoho", None) is not None and params.get("deltazuc", None) is not None \
      else None], \
    [["/system::Solid/coefficient::SurfaceHeatFlux/type/rank/value/constant", \
      "/system::Temperature/coefficient::SurfaceHeatFlux/type/rank/value/constant"], params["qs"]], \
    [["/system::Solid/coefficient::SlabAge/type/rank/value/constant", \
      "/system::Temperature/coefficient::SlabAge/type/rank/value/constant"], params["tslab"]], \
    [["/system::Solid/coefficient::CrustAge/type/rank/value/constant", \
      "/system::Temperature/coefficient::CrustAge/type/rank/value/constant"], params["tcrust"]], \
    [["/timestepping/finish_time"], params["finishtime"]], \
    ]

  changed = False
  for paths, val in tfml_options:
    if val is not None:
      for path in paths:
        if libspud.have_option(path):
          libspud.set_option(path, float(val))
          changed = True
          break

  if changed:
    if outfilename is None: outfilename = filename
    if os.path.exists(outfilename): shutil.copy2(outfilename, outfilename+".bak")
    libspud.write_options(outfilename)

  libspud.clear_options()


if __name__ == "__main__":
  import argparse

  parser = argparse.ArgumentParser(description='Update a subduction global suite tfml file from the command line.')
  parser.add_argument('filename', nargs='+', metavar='filename', type=str, help='specify the name of the tfml file')
  parser.add_argument('--smml', metavar='smml', type=str, required=False, default=None, \
                      help='specify the name of the corresponding smml geometry file')
  parser.add_argument('--vconv', metavar='vconv', type=float, required=False, default=None, \
                      help='specify the convergence speed (m/yr)')
  parser.add_argument('--tslab', metavar='tslab', type=float, required=False, default=None, \
                      help='specify the slab age (Myr)')
  parser.add_argument('--tcrust', metavar='tcrust', type=float, required=False, default=None, \
                      help='specify the crust age (Myr; oceanic-oceanic subduction only)')
  parser.add_argument('--qs', metavar='qs', type=float, required=False, default=None, \
                      help='specify the surface heat flux (non-dim; oceanic-continental subduction only)')
  parser.add_argument('--finishtime', metavar='finishtime', type=float, required=False, default=None, \
                      help='specify the finish time (non-dim)')
  parser.add_argument('-o', '--output', metavar='filename', type=str, required=False, default=None,
                      help='specify the name of the output tfml file (if different to input')
  args = parser.parse_args()

  smml_options = {
    "deltaztrench" : "/slab/slab_surface/points/point::trench", \
    "deltazuc"     : "/domain/location::UpperCrustBase/depth", \
    "deltazmoho"   : "/domain/location::MohoBase/depth", \
    "deltaxcoast"  : "/domain/location::DomainSurface/coast_distance", \
    }

  smmlparams = {}
  if args.smml is not None:
    libspud.load_options(args.smml)
    
    for k,v in smml_options.items():
      try:
        smmlparams[k] = libspud.get_option(v)
      except libspud.SpudKeyError:
        pass

    libspud.clear_options()

  params = dict(vars(args), **smmlparams)
  params.pop("output")

  for filename in args.filename: updatetfml(filename, params, outfilename=args.output)

