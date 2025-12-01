import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from tsp_solver import solve_tsp


# ----------------------------------------------------------
#                   CENTERED HEADERS
# ----------------------------------------------------------

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


# ----------------------------------------------------------
#           DEFAULT DISTANCE MATRIX (ALWAYS SHOWN FIRST)
# ----------------------------------------------------------

default_matrix = [
    [0,   233, 281, 260, 500, 250, 450],  # Delhi
    [233,   0, 240, 400, 335, 350, 260],  # Agra
    [281, 240,   0, 520, 590, 520, 570],  # Jaipur
    [260, 400, 520,   0, 650, 150, 700],  # Chandigarh
    [500, 335, 590, 650,   0, 530,  90],  # Lucknow
    [250, 350, 520, 150, 530,   0, 600],  # Dehradun
    [450, 260, 570, 700,  90, 600,   0],  # Kanpur
]

default_cities = ["Delhi", "Agra", "Jaipur", "Chandigarh", "Lucknow", "Dehradun", "Kanpur"]

distance_matrix = default_matrix
cities = default_cities
use_uploaded = False

st.markdown(
    "<h3 style='text-align:center;'>Default Distance Matrix (km)</h3>",
    unsafe_allow_html=True
)

df_default = pd.DataFrame(default_matrix, index=default_cities, columns=default_cities)
st.table(df_default)


# ----------------------------------------------------------
#               OPTIONAL CSV UPLOAD COMES AFTER DEFAULT
# ----------------------------------------------------------

st.markdown(
    "<h3 style='text-align:center;'>Upload Custom Distance Matrix (Optional)</h3>",
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload a CSV containing a square distance matrix",
    type=["csv"]
)

if uploaded_file is not None:
    df_uploaded = pd.read_csv(uploaded_file, header=None)

    if df_uploaded.shape[0] != df_uploaded.shape[1]:
        st.error("Uploaded matrix must be square (n×n).")
    else:
        st.success("Matrix uploaded successfully!")

        n = df_uploaded.shape[0]

        st.markdown(
            "<h4 style='text-align:center;'>Enter City Names (In Order)</h4>",
            unsafe_allow_html=True
        )

        cities = []
        for i in range(n):
            city = st.text_input(f"City {i+1} Name:", key=f"city_{i}")
            cities.append(city)

        if all(cities):
            distance_matrix = df_uploaded.values.tolist()
            use_uploaded = True


# ----------------------------------------------------------
#             SELECT STARTING CITY
# ----------------------------------------------------------

st.markdown(
    "<h4 style='text-align:center;'>Select Starting City</h4>",
    unsafe_allow_html=True
)

start_city = st.selectbox("", cities, index=0)
start_index = cities.index(start_city)


# ----------------------------------------------------------
#                   SOLVE BUTTON
# ----------------------------------------------------------

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    solve = st.button("Solve TSP")


# ----------------------------------------------------------
#         FUNCTION TO GENERATE VISUALIZATION COORDS
# ----------------------------------------------------------

def generate_coordinates(n):
    np.random.seed(42)
    return np.random.rand(n, 2) * 100


# ----------------------------------------------------------
#                     SOLVER OUTPUT
# ----------------------------------------------------------

if solve:

    if use_uploaded and any(c == "" for c in cities):
        st.error("Please enter all city names.")
    else:
        route, total_dist = solve_tsp(distance_matrix, start_node=start_index)

        if route is None:
            st.error("No feasible solution found.")
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

            # Route Table
            step_df = pd.DataFrame({
                "Step": list(range(len(route_names))),
                "City": route_names
            })

            st.markdown(
                "<h4 style='text-align:center;'>Route Details</h4>",
                unsafe_allow_html=True
            )
            st.table(step_df)


            # ----------------------------------------------------------
            #                ROUTE VISUALIZATION WITH NUMBERS
            # ----------------------------------------------------------

            st.markdown(
                "<h3 style='text-align:center;'>Route Visualization</h3>",
                unsafe_allow_html=True
            )

            coords = generate_coordinates(len(cities))

            route_x = [coords[i][0] for i in route]
            route_y = [coords[i][1] for i in route]

            # Labels: "1. Delhi", "2. Agra", ...
            arrival_labels = [f"{idx+1}. {cities[city]}" for idx, city in enumerate(route)]

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=route_x,
                y=route_y,
                mode='lines+markers+text',
                line=dict(width=3),
                marker=dict(size=12),
                text=arrival_labels,
                textposition="top center"
            ))

            fig.update_layout(
                width=750,
                height=500,
                showlegend=False,
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False)
            )

            st.plotly_chart(fig, use_container_width=True)
