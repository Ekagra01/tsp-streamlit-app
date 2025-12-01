import streamlit as st
import pandas as pd
from tsp_solver import solve_tsp

st.title("Travelling Salesman Problem – Flexible Start City")
st.write("""
This app uses **OR-Tools RoutingModel** to solve the TSP.

The model satisfies:
1. Each city is departed from exactly once  
2. Each city is arrived at exactly once  
3. Decision variables x(i,j) are binary  
Subtours are eliminated internally by OR-Tools.  
""")

# Distance matrix (Your data)
distance_matrix = [
    [0,   233, 281, 260, 500, 250, 450],  # Delhi
    [233,   0, 240, 400, 335, 350, 260],  # Agra
    [281, 240,   0, 520, 590, 520, 570],  # Jaipur
    [260, 400, 520,   0, 650, 150, 700],  # Chandigarh
    [500, 335, 590, 650,   0, 530,  90],  # Lucknow
    [250, 350, 520, 150, 530,   0, 600],  # Dehradun
    [450, 260, 570, 700,  90, 600,   0],  # Kanpur
]

cities = ["Delhi", "Agra", "Jaipur", "Chandigarh", "Lucknow", "Dehradun", "Kanpur"]

st.subheader("Distance Matrix (km)")
st.dataframe(pd.DataFrame(distance_matrix, index=cities, columns=cities))

# New Feature: Select start city
start_city = st.selectbox("Select the starting city", cities)
start_index = cities.index(start_city)

if st.button("Solve TSP"):
    route, total_dist = solve_tsp(distance_matrix, start_node=start_index)

    if route is None:
        st.error("No solution found!")
    else:
        route_names = [cities[i] for i in route]

        st.success(f"Optimal route starting from {start_city}:")
        st.write(" → ".join(route_names))
        st.write(f"Total distance: **{total_dist} km**")

        st.subheader("Route Steps")
        st.table(pd.DataFrame({
            "Step": list(range(len(route_names))),
            "City": route_names
        }))
