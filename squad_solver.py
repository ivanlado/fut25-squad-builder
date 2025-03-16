from amplpy import AMPL
import pandas as pd
import numpy as np
import re

from utils_squads import *

class SquadSolver():
    
    def __init__(self, solver='gurobi'):
        self.ampl = AMPL()
        self.ampl.read('model.mod')
        self.ampl.setOption("solver", solver)
        self.ampl.setOption("show_stats", 1)
        self.formulations = {}
        self.already_declared_formulations = []
        
    def read_csv_data(self, csv_filename, limit_rows=None):
        self.data = pd.read_csv(csv_filename)
        if limit_rows:
            self.data = self.data.loc[:limit_rows]
        self.data["generic_position"] = self.data["position"].map(position_mapping)
        self.data = self.data[self.data["price"] > 200] # Remove "free" players, those that are no longer in the market
        return self.data
    
    def set_ampl_data(self, params):
        P = len(self.data)
        global_score = self.data['global_score']
        price = self.data['price']
        nationality = list(self.data['nation'])
        is_GK = list(self.data['position'] == 'GK')
        is_DEF = list(self.data['position'].isin(['LB', 'CB', 'RB', 'LWB', 'RWB']))
        is_MID = list(self.data['position'].isin(['CM', 'CDM', 'CAM', 'RM', 'LM']))
        is_FOR = list(self.data['position'].isin(['LW', 'RW', 'ST', 'CF']))
        is_icon = list(self.data['is_icon'])
        is_hero = list(self.data['is_hero'])
        budget = params['budget']
        number_of_defenders = params['number_of_defenders']
        number_of_midfielders = params['number_of_midfielders']
        number_of_forwards = params['number_of_forwards']
        min_chemistry = params['min_chemistry']
        m = params['M']
        # Insert data in AMPL        
        self.ampl.getParameter('P').set(P)
        self.ampl.getParameter('BUDGET').set(budget)
        self.ampl.getParameter('GLOBAL_SCORE').setValues(list(global_score))
        self.ampl.getParameter('PRICE').setValues(list(price))
        self.ampl.getParameter('NATIONALITY').setValues(nationality)
        self.ampl.getParameter("IS_ICON").setValues(is_icon)
        self.ampl.getParameter("IS_HERO").setValues(is_hero)
        self.ampl.getParameter('MIN_CHEMISTRY').set(min_chemistry)
        self.ampl.getParameter('NUMBER_DEF').set(number_of_defenders)
        self.ampl.getParameter('NUMBER_MID').set(number_of_midfielders)   
        self.ampl.getParameter('NUMBER_FOR').set(number_of_forwards)
        self.ampl.getParameter("IS_GK").setValues(is_GK)
        self.ampl.getParameter("IS_DEF").setValues(is_DEF)
        self.ampl.getParameter("IS_MID").setValues(is_MID)
        self.ampl.getParameter("IS_FOR").setValues(is_FOR)
        self.ampl.getParameter("M").set(m)
        
    def add_formulation(self, formulation_name, formulation):
        self.formulations[formulation_name] = formulation
        
    def get_ampl(self):
        return self.ampl
        
    def solve(self, formulation_name, print_results=True, print_summary=True):
        output = ''
        output += self.ampl.get_output("option presolve 0;")
        output += self.ampl.get_output("option reset_initial_guesses 1;")
        output += self.ampl.get_output("option show_stats 1;")
        output += self.ampl.get_output("option solver gurobi;")
        output += self.ampl.get_output('option gurobi_options $gurobi_options " outlev=1 presolve=0 cuts=0 bestbound=1";')
        output = '' # For the time being lets ignore the previous outputs
        if formulation_name in self.formulations:
            print(f"Solving formulation: {formulation_name}.")
            # output += self.ampl.get_output(self.formulations[formulation_name])
            if formulation_name not in self.already_declared_formulations:
                self.ampl.eval(self.formulations[formulation_name])
                self.already_declared_formulations.append(formulation_name)
            output += self.ampl.get_output(f"solve {formulation_name};")
        else:
            output += self.ampl.get_output("solve;")
        solve_result = self.ampl.solve_result
        # ampl.solve(solver="gurobi", gurobi_options="outlev=1 presolve=0 timing=1")
        # assert ampl.solve_result == "solved"
        vars_match = re.search(r'(\d+) variables:', output)
        constraints_match = re.search(r'(\d+) constraints,', output)
        gap_match = re.search(r'gap\s+([\d\.%]+)', output)
        simplex_iters_match = re.search(r'(\d+) simplex iterations', output)
        branching_nodes_match = re.search(r'(\d+) branching node', output)
        objective_match = re.search(r'; objective\s+(\d+\.\d+)', output)
        # Storing extracted values in variables
        num_vars = int(vars_match.group(1)) if vars_match else None
        num_constraints = int(constraints_match.group(1)) if constraints_match else None
        gap = float(gap_match.group(1).strip('%')) / 100 if gap_match else None  # Convert % to decimal
        simplex_iterations = int(simplex_iters_match.group(1)) if simplex_iters_match else None
        branching_nodes = int(branching_nodes_match.group(1)) if branching_nodes_match else None
        objective = float(objective_match.group(1)) if objective_match else None
        solve_elapsed_time = self.ampl.get_output("display _solve_elapsed_time;").strip()
        solve_elapsed_time_match = re.search(r'(\d+\.\d+)', solve_elapsed_time)
        solve_elapsed_time = float(solve_elapsed_time_match.group(1)) if solve_elapsed_time_match else None
        output = output.strip() 
        if print_results:
            print(output)
            print(solve_result)
        if print_summary:
            print("Solver result: ", solve_result)
            print(f"Number of Variables: {num_vars}")
            print(f"Number of Constraints: {num_constraints}")
            print(f"Gap: {gap}")
            print(f"Number of Simplex Iterations: {simplex_iterations}")
            print(f"Number of Branching Nodes: {branching_nodes}")
        result_dict = {
            "solve_result": solve_result,
            "num_vars": num_vars,
            "num_constraints": num_constraints,
            "gap": gap,
            "simplex_iterations": simplex_iterations,
            "branching_nodes": branching_nodes,
            "solve_elapsed_time": solve_elapsed_time,
            "output": output,
            "objective": objective
        }
        return result_dict
    
    
    def get_squad(self, print_squad=True):
        y = self.ampl.getVariable("y").getValues().toPandas().values.flatten()
        squad = get_squad(y, self.data, print_squad)
        return squad