from dolfin import *
import numpy as np
import matplotlib
# set a display independent backend
matplotlib.use('Agg')
import matplotlib.pyplot as pl

def solve_poisson(nc, p):
  mesh = UnitIntervalMesh(nc)
  V = FunctionSpace(mesh, "Lagrange", p)

  # Define Dirichlet boundary (x = 0)
  def boundary(x):
      return x[0] < DOLFIN_EPS

  # Define boundary condition
  T0 = Constant(0.0)
  bc = DirichletBC(V, T0, boundary)

  # Define variational problem
  T_a = TrialFunction(V)
  T_t = TestFunction(V)
  x  = SpatialCoordinate(mesh)
  f = (pi**2)*sin(pi*x[0]/2)/4

  a = inner(grad(T_t), grad(T_a))*dx
  L = T_t*f*dx

  # Compute solution
  T_i = Function(V)
  solve(a == L, T_i, bc)

  # Save solution in XDMF format
  ofile = XDMFFile("poisson_{}.xdmf".format(nc,))
  ofile.write(T_i)
  ofile.close()

  return T_i

def evaluate_error(T_i):
  x  = SpatialCoordinate(T_i.function_space().mesh())
  Te = sin(pi*x[0]/2)

  l2err = assemble((T_i - Te)*(T_i - Te)*dx)**0.5

  return l2err

def test_convergence():
  pl.figure()

  ps = [1, 2]
  ncells = [10, 20, 40, 80, 160, 320]
  test_passes = True
  for p in ps:
    errors_l2_a = []
    for nc in ncells:
      T_i = solve_poisson(nc, p)
      l2error = evaluate_error(T_i)
      print('nc = ', nc, ', l2error = ', l2error)
      errors_l2_a.append(l2error)

    hs = 1./np.array(ncells)/p

    with open('convergence_p{}.csv'.format(p), 'w') as f:
      np.savetxt(f, np.c_[ncells, hs, errors_l2_a], delimiter=',', 
                 header='ncells, hs, l2errs')

    fit = np.polyfit(np.log(hs), np.log(errors_l2_a),1)
    print("***********  order of accuracy p={}, order={:.2f}".format(p,fit[0]))

    # log-log plot of the error  
    pl.loglog(hs,errors_l2_a,'o-',label='p={}, order={:.2f}'.format(p,fit[0]))

    test_passes = test_passes and fit[0] > p+0.9

  pl.xlabel('h')
  pl.ylabel('||e||_2')
  pl.grid()
  pl.title('Convergence')
  pl.legend()
  pl.savefig('poisson_convergence.pdf')

  print("***********  convergence figure in poisson_convergence.pdf")
  assert(test_passes)


if __name__ == "__main__":
  test_convergence()

