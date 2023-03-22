import pandas
import json

params = pandas.read_excel("Flow_Law_Parameter_Compilation.xlsx")

rheoli = {name:index for index,name in enumerate(params['PaperName']) if isinstance(name, str)}

rheols = {name:{'A':10**params.iloc[index]['log10A(MPa^-(n+r) s^-1 m^-m)'],  # convert from log10A to A
                'E':1.e-3*params.iloc[index]['E(J/mol)'],                    # convert from J/mol to kJ/mol
                'V':params.iloc[index]['V(m3/mol)'],
                'n':params.iloc[index]['n'],
                'r':params.iloc[index]['r']} for name,index in rheoli.items()}

with open("rheologies.json", "w") as f:
  json.dump(rheols, f, indent=4, separators=(",", ":"))
