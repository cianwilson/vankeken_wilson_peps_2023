#!/usr/bin/env python3
import os
import glob

output = """\\documentclass{article}
\\usepackage{graphicx}
\\usepackage{multirow}
\\usepackage{fullpage}
\\usepackage{longtable}
\\usepackage{array}

\\setlength{\\tabcolsep}{1pt}
\\renewcommand{\\arraystretch}{0.1}

\\begin{document}

\\begin{longtable}{m{\\textwidth}}
\hline""".split(os.linesep)

sorted(glob.glob('??_*'))

minres='1.0'
cfl='1.0'

repodir = os.path.join(os.path.dirname(__file__), os.path.pardir)
subdirs = sorted([os.path.basename(d) for d in glob.glob(os.path.join(repodir, '??_*'))])
for subdir in subdirs:
  subpath = os.path.join(repodir, subdir, 'subduction_linearized_p2p1p2.tfml.run', 'Dc_80.0', 'minres_'+minres, 'cfl_'+cfl, 'run_0')
  print(subdir)
  print(subpath)
  subentry = [""]
  plot_found = False
  if os.path.exists(os.path.join(subpath, 'subduction_allT_plot.pdf')):
    subentry[-1] += '\\includegraphics[width=\\textwidth]{'+os.path.join(subpath, 'subduction_allT_plot.pdf')+'}'
    plot_found = True
  subentry[-1] += ' \\\\ \hline'
  if plot_found: output += subentry

output += """\\end{longtable}

\\end{document}""".split(os.linesep)

with open(os.path.join('all_temperature_diffs.tex'), 'w') as f:
  f.write(os.linesep.join(output))


