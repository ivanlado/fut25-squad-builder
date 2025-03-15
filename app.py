import streamlit as st
from squad_solver import *
from utils_squads import *
st.set_page_config(layout="wide")

st.title("EA FC 25 Football Ultimate Team Squad Builder")
st.write("Welcome to the EA FC 25 Football Ultimate Team Squad Builder. This app will help you build the best squad within your budget. You can choose the formation and the budget you have. The app will then find the best squad for you. Enjoy!")

st.radio("Select the formation you want to play with", ["4-4-2", "4-3-3", "4-2-3-1", "4-1-2-1-2", "5-3-2", "5-2-1-2"], index=0)
st.slider("Select your budget (thousand of coins)", 15, 1000, 100)



squad_solver = SquadSolver()
ampl = squad_solver.get_ampl()
ampl.eval('option presolve 0;')

params = {
    "budget": 1000000,
    "number_of_defenders": 4,
    "number_of_midfielders": 3,
    "number_of_forwards": 3,
    "min_chemistry": 17,
    "M":11
}

data = squad_solver.read_csv_data("players.csv")
summary_squad(data)
squad_solver.set_ampl_data(params)

# General components of all formulations
general_components = "Avg_Global, PositionGK, PositionDEF, PositionMID, PositionFOR, Budget, R6"
general_components += ", y, natCount, chemistryNat1, chemistryNat2, chemistryNat3"
formulation_1 = "problem Formulation_1: " + general_components + ", " + "R31, R32, R33A, R33B, R33C, R6;"
results_formulation_1= squad_solver.solve("Formulation_1", print_results=False, print_summary=False)
squad_formulation_1 = squad_solver.get_squad()

st.write("The best squad for you is:")
st.write(squad_formulation_1)