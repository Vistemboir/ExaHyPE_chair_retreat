import peano4, exahype2
import os, sys
import argparse, string

from exahype2.solvers.PDETerms import PDETerms

import subprocess

polynomials = exahype2.solvers.aderdg.Polynomials.Gauss_Legendre
  # exahype2.solvers.aderdg.Polynomials.Gauss_Lobatto


max_h = 1.1 * 120 / (3.0**5)
min_h = max_h / (3.0**0)

project = exahype2.Project(["exahype2", "aderdg", "euler"], ".", "AIRFOIL")

theSolver = exahype2.solvers.fv.rusanov.GlobalAdaptiveTimeStep(
  name  = "euler_airfoil", patch_size = 22,
  min_volume_h          = min_h,
  max_volume_h          = max_h,
  time_step_relaxation  = 0.1,
  unknowns              = 4,
  auxiliary_variables   = 0
)

theSolver.set_implementation(
  initial_conditions    = PDETerms.User_Defined_Implementation,
  boundary_conditions   = PDETerms.User_Defined_Implementation,
  eigenvalues = PDETerms.User_Defined_Implementation,
  flux        = PDETerms.User_Defined_Implementation,
  # ncp         = PDETerms.User_Defined_Implementation
)

project.set_output_path("solutions")

project.add_solver(theSolver)

project.set_global_simulation_parameters(
  dimensions = 2,
  offset  = [-10, -60],
  size    = [120, 120],
  min_end_time = 10.,
  max_end_time = 10.,
  first_plot_time_stamp = 0.0,
  time_in_between_plots = 0.5,
  periodic_BC = [False, False],
)

#
# So here's the parallel stuff. This is new compared to the serial
# prototype we did start off with.
#
project.set_load_balancing(
  "toolbox::loadbalancing::strategies::RecursiveBipartition",
  "new ::exahype2::LoadBalancingConfiguration()",
)
project.set_Peano4_installation("../../", peano4.output.CompileMode.Release)
peano4_project = project.generate_Peano4_project("False")

peano4_project.build(make_clean_first=True, number_of_parallel_builds=16)
