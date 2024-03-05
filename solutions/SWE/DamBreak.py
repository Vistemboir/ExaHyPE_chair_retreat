import peano4, exahype2


"""
Here we define an ExaHyPE2 solver, specifically an ADER-DG solver.
  It takes as arguments a name, a polynomial order,
  the number of unknowns and the allowable cell sizes for the refinement.
"""

theSolver = exahype2.solvers.aderdg.rusanov.GlobalAdaptiveTimeStep(
  name  = "damBreak", order = 5,
  min_cell_h = 0.008, max_cell_h = 0.1,
  time_step_relaxation  = 0.9,
  unknowns              = {"h": 1, "hu": 2, "b": 1},
  auxiliary_variables   = {},
  flux = exahype2.solvers.PDETerms.User_Defined_Implementation,
  ncp  = exahype2.solvers.PDETerms.User_Defined_Implementation,
  refinement_criterion = exahype2.solvers.PDETerms.User_Defined_Implementation
)


"""
Here we define a Peano project that the ExaHyPE solver will be bound to.
  This takes a namespace for the C++-code, as well as a name for the executable.
  We then add our solver to this project and, just for cleanliness, set an output
  path for our results
"""

project = exahype2.Project( ["exahype2", "aderdg", "swe"], ".", executable="DAM_BREAK")
project.add_solver(theSolver)

project.set_output_path("solutions")


"""
Now that we have a Peano project, let's populate it with some information:
  this is essentially the domain our solver will run in. 
  The project needs to know the domain size, how long the simulation should run,
  how often it should plot the solution, and what type of boundary we are using 
"""

project.set_global_simulation_parameters(
  dimensions = 2,
  offset  = [-1.0, -1.0],
  size    = [ 2.0,  2.0],
  min_end_time = 0.5,
  max_end_time = 0.5,
  first_plot_time_stamp = 0.0,
  time_in_between_plots = 0.1,
  periodic_BC = [False, False],
)


"""
  Finally, we specify some optimizations for parallel runs, and compile the project
"""

project.set_load_balancing("toolbox::loadbalancing::strategies::RecursiveBipartition", "new ::exahype2::LoadBalancingConfiguration()")
project.set_Peano4_installation("../../", peano4.output.CompileMode.Release)
peano4_project = project.generate_Peano4_project()

peano4_project.build(make_clean_first=True, number_of_parallel_builds=16)
