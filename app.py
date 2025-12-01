import streamlit as st
import pandas as pd
from tsp_solver import solve_tsp

# --------------------------- CENTERED HEADERS ---------------------------

st.markdown(
    """
    <h1 style='text-align: center;'>
        Travelling Salesman Problem (TSP)
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h3 style='text-align: center;'>
        Implemented Using Google OR-Tools Routing Model
    </h3>
    """,
    unsafe_allow_html=True
)

st.write("""
This application solves the Travelling Salesman Problem using Google OR-Tools.
The model ensures:
1. Each city has exactly one outgoing path  
2. Each city has exactly one incoming path  
3. All decision variables x(i,j) are binary  
Subtour elimination is handled internally by OR-Tools.
""")

# --------------------------- DISTANCE MATRIX ---------------------------

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

st.markdown(
    "<h3 style='text-align:center;'>Distance Matrix (km)</h3>",
    unsafe_allow_html=True
)

# Center the DataFrame
st.markdown(
    """
    <style>
        .center-table {
            margin-left: auto;
            margin-right: auto;
        }
    </style>
    """,
    unsafe_allow_html=True
)

df = pd.DataFrame(distance_matrix, index=cities, columns=cities)
st.table(df.style.set_table_attributes("class='center-table'"))

# --------------------------- SELECT START CITY ---------------------------

st.markdown(
    "<h4 style='text-align:center;'>Select Starting City</h4>",
    unsafe_allow_html=True
)

start_city = st.selectbox("", cities, index=0)
start_index = cities.index(start_city)

# --------------------------- CENTERED BUTTON ---------------------------

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    solve = st.button("Solve TSP")

# --------------------------- SOLUTION OUTPUT ---------------------------

if solve:
    route, total_dist = solve_tsp(distance_matrix, start_node=start_index)

    if route is None:
        st.error("No solution found.")
    else:
        route_names = [cities[i] for i in route]

        st.markdown(
            f"""
            <h3 style='text-align:center; color:green;'>
                Optimal Route (Starting from {start_city})
            </h3>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"<h4 style='text-align:center;'>{' → '.join(route_names)}</h4>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<h4 style='text-align:center;'>Total Distance: <b>{total_dist} km</b></h4>",
            unsafe_allow_html=True
        )

        # Centered Route Table
        st.markdown(
            "<h4 style='text-align:center;'>Route Details</h4>",
            unsafe_allow_html=True
        )

        step_df = pd.DataFrame({
            "Step": list(range(len(route_names))),
            "City": route_names
        })

        st.table(step_df.style.set_table_attributes("class='center-table'"))
