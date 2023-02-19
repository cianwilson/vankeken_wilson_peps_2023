from dolfin import *
import numpy as np
import matplotlib
# set a display independent backend
matplotlib.use('Agg')
import matplotlib.pyplot as pl

def solve_poisson(nx):
  mesh = UnitIntervalMesh(nx)
  V = FunctionSpace(mesh, "Lagrange", 1)

  # Define Dirichlet boundary (x = 0)
  def boundary(x):
      return x[0] < DOLFIN_EPS

  # Define boundary condition
  T0 = Constant(0.0)
  bc = DirichletBC(V, T0, boundary)

  # Define variational problem
  T_a = TrialFunction(V)
  T_t = TestFunction(V)
  f = Constant(1.0)

  a = inner(grad(T_t), grad(T_a))*dx
  L = T_t*f*dx

  # Compute solution
  T_i = Function(V)
  solve(a == L, T_i, bc)

  # Save solution in XDMF format
  ofile = XDMFFile("poisson_{}.xdmf".format(nx,))
  ofile.write(T_i)
  ofile.close()

  return T_i

def evaluate_error(T_i):
  x  = SpatialCoordinate(T_i.function_space().mesh())
  Te = -0.5*x[0]**2 + x[0]

  l2err = assemble((T_i - Te)*(T_i - Te)*dx)**0.5

  return l2err

errors_l2_a = []
nxs = [10, 20, 40, 80, 160, 320]
for nx in nxs:
  T_i = solve_poisson(nx)
  l2error = evaluate_error(T_i)
  print('nx = ', nx, ', l2error = ', l2error)
  errors_l2_a.append(l2error)

hs = 1./np.array(nxs)
p = np.polyfit(np.log(hs), np.log(errors_l2_a),1)

# log-log plot of the error  
pl.figure()
pl.loglog(hs,errors_l2_a,'bo-')
pl.xlabel('h')
pl.ylabel('||e||_2')
pl.grid()

pl.title('h Convergence, p={0}'.format(p[0]))
pl.savefig('poisson_convergence.pdf')

print("***********  order of accuracy p=",p[0])
print("***********  convergence figure in poisson_convergence.pdf")

assert(p[0] > 1.9)

