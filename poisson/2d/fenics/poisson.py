# Import the dolfin library (a component of FEniCS)
from dolfin import *
# Other imports
import numpy as np
import matplotlib
# Set a display independent backend
matplotlib.use('Agg')
import matplotlib.pyplot as pl

def solve_poisson_2d(ne, p=1):
  """
  A python function to solve a two-dimensional Poisson problem
  on a unit square domain.
  Parameters:
    * ne - number of elements in each dimension
    * p  - polynomial order of the solution function space
  """
  # Describe the domain (a unit square)
  # and also the tesselation of that domain into ne 
  # equally spaced squares in each dimension which are
  # subdivided into two triangular elements each
  mesh = UnitSquareMesh(ne, ne, diagonal='right')
  # Define the solution functionspace using Lagrange polynomials
  # of order p
  V = FunctionSpace(mesh, "Lagrange", p)

  # Define the trial and test functions on the same functionspace (V)
  T_a = TrialFunction(V)
  T_t = TestFunction(V)

  # Define the location of the boundary condition, x=0 and y=0
  def boundary(x):
      return x[0] < DOLFIN_EPS or x[1] < DOLFIN_EPS
  # Specify the value and define a Dirichlet boundary condition (bc)
  gD = Expression("exp(x[0] + x[1]/2.)", degree=p)
  bc = DirichletBC(V, gD, boundary)

  # Get the coordinates
  x = SpatialCoordinate(mesh)
  # Define the Neumann boundary condition function
  gN = as_vector((exp(x[0] + x[1]/2.), 0.5*exp(x[0] + x[1]/2.)))
  # Define the right hand side function, rhsf
  rhsf = -5./4.*exp(x[0] + x[1]/2.)

  # Get the unit vector normal to the facets
  n = FacetNormal(mesh)
  # Define the integral to be assembled into the stiffness matrix
  S = inner(grad(T_t), grad(T_a))*dx
  # Define the integral to be assembled into the forcing vector,
  # incorporating the Neumann boundary condition weakly
  f = T_t*rhsf*dx + T_t*inner(gN, n)*ds

  # Define the solution and compute it (given the boundary condition, bc)
  T_i = Function(V)
  solve(S == f, T_i, bc)

  # Save solution to disk in XDMF format
  ofile = XDMFFile("poisson_{}_{}.xdmf".format(ne,p,))
  ofile.write(T_i)
  ofile.close()

  # Return the solution
  return T_i

def evaluate_error(T_i):
  """
  A python function to evaluate the l2 norm of the error in 
  the two dimensional Poisson problem given a known analytical
  solution.
  """
  # Define the exact solution
  x  = SpatialCoordinate(T_i.function_space().mesh())
  Te = exp(x[0] + x[1]/2.)

  # Define the error between the exact solution and the given
  # approximate solution
  l2err = assemble((T_i - Te)*(T_i - Te)*dx)**0.5

  # Return the l2 norm of the error
  return l2err

def test_convergence():
  """
  A python function to test the convergence between a series of
  higher dimensional or higher order solutions to the two-dimensional
  Poisson problem.
  """
  # Open a figure for plotting
  fig = pl.figure()

  # List of polynomial orders to try
  ps = [1, 2]
  # List of resolutions to try
  nelements = [10, 20, 40, 80, 160, 320]
  # Keep track of whether we get the expected order of convergence
  test_passes = True
  # Loop over the polynomial orders
  for p in ps:
    # Accumulate the errors
    errors_l2_a = []
    # Loop over the resolutions
    for ne in nelements:
      # Solve the 2D Poisson problem
      T_i = solve_poisson_2d(ne, p)
      # Evaluate the error in the approximate solution
      l2error = evaluate_error(T_i)
      # Print to screen and save
      print('ne = ', ne, ', l2error = ', l2error)
      errors_l2_a.append(l2error)

    # Work out the order of convergence at this p
    hs = 1./np.array(nelements)/p

    # Write the errors to disk
    with open('2d_poisson_convergence_p{}.csv'.format(p), 'w') as f:
      np.savetxt(f, np.c_[nelements, hs, errors_l2_a], delimiter=',', 
                 header='nelements, hs, l2errs')

    # Fit a line to the convergence data
    fit = np.polyfit(np.log(hs), np.log(errors_l2_a),1)
    print("***********  order of accuracy p={}, order={:.2f}".format(p,fit[0]))

    # log-log plot of the error  
    pl.loglog(hs,errors_l2_a,'o-',label='p={}, order={:.2f}'.format(p,fit[0]))

    # Test if the order of convergence is as expected
    test_passes = test_passes and fit[0] > p+0.9

  # Tidy up the ploy
  pl.xlabel('h')
  pl.ylabel('||e||_2')
  pl.grid()
  pl.title('Convergence')
  pl.legend()
  pl.savefig('poisson_convergence.pdf')

  print("***********  convergence figure in poisson_convergence.pdf")
  # Check if we passed the test
  assert(test_passes)

# When run as a script this is the starting point
if __name__ == "__main__":
  test_convergence()

