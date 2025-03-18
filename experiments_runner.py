from squad_solver import *
from utils_squads import *


def run_experiment(squad_solver, csv_filename, params, formulation_name, formulation, print_results=True, print_summary=True):
    if squad_solver is None:
        squad_solver = SquadSolver()
    ampl = squad_solver.get_ampl()
    ampl.eval('option presolve 0;')
    data = squad_solver.read_csv_data(csv_filename)
    squad_solver.set_ampl_data(params)

    squad_solver.add_formulation(formulation_name, formulation)
    results = squad_solver.solve(formulation_name, print_results=print_results, print_summary=print_summary)
    squad = squad_solver.get_squad(print_squad=False)
    return results, squad  


def repeat_run_experiment(squad_solver, csv_filename, params, formulation_name, formulation, print_results=True, print_summary=True, n_repeats=10):
    results = []
    squads = []
    for i in range(n_repeats):
        result, squad = run_experiment(squad_solver, csv_filename, params, formulation_name, formulation, print_results=print_results, print_summary=print_summary)
        results.append(result)
        squads.append(squad)
    return results, squads