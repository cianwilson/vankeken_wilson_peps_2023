#!/usr/bin/python3
import pandas
import warnings

t0 = 0.04216560072028045 # Myr : t0 = h/v0 = 1330645161290.3225 s = 0.042166755183119145 Myr
q0 = 3.1 # mW/m/mQ0*h : q0 = k0*T0/h = 3.1e-3 W/m/m

headerrowi = 2
paramcols = {
             "vconv" : (headerrowi, "speed"),  # mm/yr -> m/yr
             "tslab" : (headerrowi, "age"),  # Myr
             "type"  : (headerrowi, "type"),
             "_trenchdepth" : (headerrowi, "trench"), # km
             "deltazmoho" : (headerrowi, "top of wedge"),  # km - actually "top of wedge" not moho (differs for oceanic)
             "qs" : (headerrowi, "surface heatflow"),  # mW/m/m -> non-dim
             "_ftcrust" : (headerrowi-1, "final age"),  # Myr
             "finishtime" : (headerrowi, "time"), # Myr -> non-dim
             "z0" : (headerrowi, "at trench"), # km
             "z15" : (headerrowi, "depth"), # km
             "dirname" : (headerrowi+1, "directory name") # official Syracuse directory name
           }
# also need deltazuc for continental but it is not provided

allowedmissing = {
                  "continental" : ["tcrust"],
                  "oceanic"     : ["deltazuc", "qs"],
                 }


geomcols = {
             "trench" : ("trench", (1,2,)),
             "deltaxcoast" : ("coast", (1,)), 
             "_lr" : ("lower right", (1,2)), 
             "_moho" : ("Top of wedge", (2,)), 
             "deltazoutflow" : ("inflow/outflow (steady_Ol)", (2,)),
           }

def getparams(name: str, xls, steady=False):
  """Return the parameters from the supplied spreadsheet for a subduction zone with a given name."""

  # find the index of this subduction zone
  ni = int(name.split("_")[0])
  
  # dictionary mapping ni ranges to sheet name
  # note that we either consider "steady" sheets or not depending on the steady keyword
  ni2sheet = {tuple([int(si) for si in s.split() if si.isdigit()]):s \
              for s in xls.keys() if 'to' in s and s.startswith('steady') == steady}
  # the sheet name containing this name
  sheetname = ni2sheet[[k for k in ni2sheet.keys() if k[0] <= ni and k[1] >= ni][0]]

  # get the main parameter sheet and row
  paramsheet = xls['SZ56 parameters']
  paramsheet = paramsheet.where(paramsheet.notnull(), None)
  paramrow = paramsheet[paramsheet[0] == ni]

  # get some parameters from the parameter sheet
  # note hard coded column indices
  params = {}
  for k, col in paramcols.items():
    headerrow = paramsheet.iloc[col[0]]
    coli = headerrow[headerrow.str.startswith(col[1], na=False)].index[0]
    val = paramrow.iloc[0][coli]
    if isinstance(val, str):
      val = val.strip()
      if len(val)==0: val = None
    params[k] = val

  sztype = params["type"]

  # get the relevent "geometry" sheet and the row index that this name is on
  geomsheet = xls[sheetname]
  geomsheet = geomsheet.where(geomsheet.notnull(), None)
  gi = geomsheet[geomsheet[0]==name].index[0]

  # get some geometry parameters
  for k, col in geomcols.items():
    geomrow = geomsheet.iloc[gi:][geomsheet.iloc[gi:][0]==col[0]].iloc[0]
    if len(col[1]) > 1:
      params[k] = tuple([geomrow[i] for i in col[1]])
    else:
      params[k] = geomrow[col[1][0]]

  ftcrust = params.pop("_ftcrust")
  if ftcrust is None:
    params["tcrust"] = None
  else:
    if ftcrust > 100.0: ftcrust = 100.0
    params["tcrust"] = ftcrust - params["finishtime"]
  # rescale some parameters
  if params["tslab"] > 100.0: params["tslab"] = 100.0
  params["vconv"] = params["vconv"]/1000.
  params["finishtime"] = params["finishtime"]/t0
  if params["qs"] is not None: params["qs"] = params["qs"]/q0
  params["deltazuc"] = None
  if sztype == "continental": params["deltazuc"] = 15 # this doesn't seem to be provided (or vary where relevant)

  # get the slab points from the geometry sheet
  slabpoints = []
  ti = geomsheet.iloc[gi:][geomsheet.iloc[gi:][0]=="tie points"].index[0]+1
  while ti < geomsheet[0].size and \
        geomsheet.iloc[ti][0] is not None and \
        isinstance(geomsheet.iloc[ti][0], str) and \
        geomsheet.iloc[ti][0].startswith("p"):
    x = geomsheet.iloc[ti][1]
    y = geomsheet.iloc[ti][2]
    if x is not None and y is not None:
      slabpoints.append((geomsheet.iloc[ti][1], geomsheet.iloc[ti][2]))
    ti = ti+1
  params["slabpoints"] = slabpoints

  # calculate deltaxwidth from the lower right point
  lr = params.pop("_lr")
  params["deltaxwidth"] = lr[0]-slabpoints[-1][0]
  if params["deltazoutflow"] is not None: params["deltazoutflow"] = -params["deltazoutflow"]

  # perform some checks...

  # check the slab points are ordered
  if not all([slabpoints[i][-1] > slabpoints[i+1][-1] for i in range(len(slabpoints)-1)]):
    raise Exception("{}: slab points not ordered!".format(name,))

  # check the lower right point matches the spline
  if lr[1] != slabpoints[-1][1]:
    warnings.warn("{}: mismatched domain base locations ({}, {})!".format(name, lr[1], slabpoints[-1][1],))

  # check both moho depths are the same
  moho = -params.pop("_moho")
  if moho != params["deltazmoho"]:
    warnings.warn("{}: mismatched moho depth descriptions ({}, {})!".format(name, moho, params["deltazmoho"],))

  # check the trench depths
  td = params.pop("_trenchdepth")
  if td != -params["trench"][1]:
    raise Exception("{}: mismatched trench depths ({}, {})!".format(name, td, -params["trench"][1],))

  for k,v in params.items():
    if v is None and k not in allowedmissing[sztype]:
      warnings.warn("{}: unexpected missing parameter {}".format(szname, k,))

  return params

def writesedthick(params, outfilename):
  import os
  if os.path.exists(outfilename): shutil.copy2(outfilename, outfilename+".bak")

  options = [
    ["z0", params["z0"]], \
    ["z15", params["z15"]], \
    ]

  with open(outfilename, 'w') as f:
    for name, val in options:
      f.write(str(name)+" = {v:f}".format(v=val)+os.linesep)

if __name__ == "__main__":
  import argparse
  import math
  from lxml import etree
  from updatetfml import updatetfml
  from updatesmml import updatesmml
  import os
  import shutil

  parser = argparse.ArgumentParser(description='Update a subduction global suite tfml file from the command line.')
  parser.add_argument('template', metavar='filename', type=str, nargs='+',
                      help="""Specify the name of the template tfml file.  
                              This filename will be found in the templates directory of the appropriate type.
                              It does not need to include a full filepath and if it does this will be ignored.""")
  parser.add_argument('-n', '--name', metavar='name', type=str, required=False, default=None, nargs='+',
                      help="""Specify the standardized name of a subduction zone in number_name format.
                              If left unspecified all subduction zones (as described in the spreadsheet) will be processed.""")
  parser.add_argument('-s', '--steady', action='store_true',
                      help="""Use the steady state spreadsheet tabs.
                              If left unspecified the default time-dependent spreadsheet descriptions will be used.""")
  args = parser.parse_args()

  repopath = os.path.realpath(os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.pardir))
  templatepath = os.path.join(repopath, "templates")
  knownextensions = [".tfml", ".smml"]
  knownfilenames = ["sediment_thickness.py"]

  # open the xls file and read all sheets, ignoring the header since there is none
  xls = pandas.ExcelFile(os.path.join(templatepath, "T2 SZ56.xlsx")).parse(sheet_name=None, header=None)
  # get the main parameter sheet
  paramsheet = xls['SZ56 parameters']

  i = paramsheet[paramsheet[0]==1].index[0]
  allowednames = []
  while not math.isnan(paramsheet.iloc[i][0]):
    allowednames.append(repr(paramsheet.iloc[i][0]).zfill(2)+'_'+'_'.join(paramsheet.iloc[i][1].split()))
    i = i + 1

  if args.name is None:
    sznames = allowednames
  else:
    sznames = []
    for name in args.name:
      if name in allowednames:
        sznames.append(name)
      else:
        raise Warning("Unrecognized subduction zone name {}".format(name))

  # process shmls first (shmls don't depend on type so are assumed to be in the base templates directory)
  templatenames = []
  for template in args.template:
    path, filename = os.path.split(template)
    basename, ext = os.path.splitext(filename)

    templatenames.append(filename)
    if ext == ".shml":
      tree = etree.parse(os.path.join(templatepath, filename))
      inputfiles = tree.findall("//input_file")+tree.findall("//required_input")
      for ele in inputfiles:
        ifilename = ele.find(".//string_value").text
        iext = os.path.splitext(ifilename)[1]
        if iext in knownextensions or ifilename in knownfilenames: templatenames.append(ifilename)

  templatenames = list(set(templatenames))
  print("sznames = ", sznames)
  print("templatenames = ", templatenames)
  for szname in sznames:
    try:
      params = getparams(szname, xls, args.steady)
    except IndexError as e:
      print(e)
      warnings.warn("Skipping {}".format(szname))
      continue
    sztype = params.pop("type")
    dirname = params.pop("dirname")
    if not os.path.exists(os.path.join(repopath, dirname)): os.makedirs(os.path.join(repopath, dirname))
    print("Processing {} (in directory {})".format(szname, dirname))
    for templatename in templatenames:
      ext = os.path.splitext(templatename)[1]
      if ext == ".tfml":
        updatetfml(os.path.join(templatepath, sztype, templatename), params, 
                   outfilename=os.path.join(repopath, dirname, templatename))
      elif ext == ".smml":
        updatesmml(os.path.join(templatepath, sztype, templatename), params, 
                   outfilename=os.path.join(repopath, dirname, templatename))
      elif ext == ".shml":
        shutil.copy2(os.path.join(templatepath, templatename), os.path.join(repopath, dirname, templatename))
      elif templatename == "sediment_thickness.py":
        writesedthick(params, os.path.join(repopath, dirname, templatename))
      else:
        raise Exception("Unknown template file extension {}".format(templatename))
        
  

  

