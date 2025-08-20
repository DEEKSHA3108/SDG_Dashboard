import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots 
from dataLoading import loading_preprocessed_data  # Import the cached data function
import streamlit as st
import matplotlib.pyplot as plt
import chartDiscription as cd

def render():
    # Load the processed data
    data = loading_preprocessed_data()
    df = data.copy()
    df.columns = df.columns.str.strip()


# <--------- Radio buttons to toogle between graphs -------------------->
    st.sidebar.subheader("Data Visulisation")
    chart_type = st.sidebar.radio(
        "Choose a chart to visualize:",
        [
            "Education Category",
            "Employment category",
            "Leadership Category",
            "Labour Force Category",
            "Unemployment Category",
            "Fertility Category",
            "Well Being Category"
        ]
    )

# <----------------- Graphs render with Radio Button ------------------->
# <------------------------------ Education----------------------------->


    if chart_type == "Education Category":
        education_features = [
        "Female/male secondary enrollment",
        "Female/male tertiary enrollment",
        "Secondary school enrollment, female",
        "Tertiary school enrollment, female",
        "education_index",
        "ed_progression_ratio"
        ]
        countries = ["India", "Germany"]

        # Use Streamlit's clean native selectbox for dropdown
        #selected_feature = st.selectbox("Select an education feature:", education_features)
        col1, _ = st.columns([2, 5])  # 2 for dropdown, 5 as spacer
        with col1:
            selected_feature = st.selectbox(
                "Select an education feature:",
                options=education_features,
                key="edu_dropdown"
            )

        # Initialize subplot (2 rows: one per country)
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            subplot_titles=countries,
            row_heights=[0.5, 0.5],
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]]
        )

        for i, country in enumerate(countries):
            df_country = df[df['Country'] == country]
            row = i + 1

            # GDP growth
            fig.add_trace(go.Scatter(
            x=df_country["Year"],
            y=df_country["gdp_growth"],
            mode='lines',
            name=f"{country}: GDP Growth (%)",
            line=dict(color="rgba(0, 102, 204, 1)", width=2),
            fill="tozeroy",
            fillcolor="rgba(0, 102, 204, 0.3)",
            hoverinfo="x+y"
        ), row=row, col=1, secondary_y=False)


            # Education feature
            fig.add_trace(go.Scatter(
                x=df_country["Year"],
                y=df_country[selected_feature],
                mode="lines+markers",
                name=f"{country}: {selected_feature}",
                line=dict(color="red")
            ), row=row, col=1, secondary_y=True)

        # Layout cleanup
        fig.update_layout(
            yaxis2=dict(
                overlaying="y",
                side="right",
                showticklabels=True,  # hides tick labels
                showgrid=False,        # hides grid lines
                zeroline=True,        # hides zero line
                title="",              # removes title
            ),
            yaxis4=dict(
                overlaying="y3",
                side="right",
                showticklabels=True,
                showgrid=False,
                zeroline=True,
                title=""
            ),
            title="GDP Growth vs Female Education Indicators - India & Germany",
            height=600,
            template="plotly_white",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5
            )
        )

        # Y-axis titles
        fig.update_yaxes(title_text="GDP Growth (%)", row=1, col=1, color="blue")
        fig.update_yaxes(title_text=selected_feature, row=1, col=1, secondary_y=True, color="red")
        fig.update_yaxes(title_text="GDP Growth (%)", row=2, col=1, color="blue")
        fig.update_yaxes(title_text=selected_feature, row=2, col=1, secondary_y=True, color="red")
        
        # X-axis title (only bottom subplot needs it)
        fig.update_xaxes(title_text="Year", row=2, col=1)

        # Display chart
        st.plotly_chart(fig, use_container_width=True)
        cd.gdp_vs_education_description(selected_feature)

# <----------------------------- Employment ----------------------------->

    if chart_type == "Employment category":

        # Filter data
        countries = ["India", "Germany"]
        df_filtered = df[df["Country"].isin(countries)]

        base_features = {
            "Employment to population ratio": ["Employment to population ratio, female", "Employment to population ratio, male"],
            "Female employment in agriculture": ["Female employment in agriculture", None],
            "Female in senior/managerial role": ["Female employment in senior and managerial positions", None],
            "Emp Gap (Female - Male)": ["emp_gap"]
        }

        #initial_feature = "Employment to population ratio"

        col1, _ = st.columns([2, 5])  # 2 for dropdown, 5 as spacer
        with col1:
            initial_feature = st.selectbox(
                "Select an education feature:",
                options=base_features,
                key="edu_dropdown"
            )

        # Initialize subplot (2 rows: one per country)
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            subplot_titles=countries,
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
            vertical_spacing=0.12
        )

        for i, country in enumerate(countries):
            df_country = df_filtered[df_filtered["Country"] == country]
            row = i + 1

            # GDP Growth — bold area chart
            fig.add_trace(go.Scatter(
                x=df_country["Year"],
                y=df_country["gdp_growth"],
                mode='lines',
                name=f"{country}: GDP Growth (%)",
                line=dict(color="rgba(0, 102, 204, 1)", width=2),
                fill="tozeroy",
                fillcolor="rgba(0, 102, 204, 0.3)",
                hoverinfo="x+y"
            ), row=row, col=1, secondary_y=False)


            # Female (or gap) — red
            female_label = f"{country}: {initial_feature}, female" if "Gap" not in initial_feature else f"{country}: {initial_feature}"
            fig.add_trace(go.Scatter(
                x=df_country["Year"],
                y=df_country[base_features[initial_feature][0]],
                mode="lines+markers",
                name=female_label,
                line=dict(color="red", width=2)
            ), row=row, col=1, secondary_y=True)

            # Male — green
            if len(base_features[initial_feature]) > 1 and base_features[initial_feature][1]:
                fig.add_trace(go.Scatter(
                    x=df_country["Year"],
                    y=df_country[base_features[initial_feature][1]],
                    mode="lines+markers",
                    name=f"{country}: {initial_feature}, male",
                    line=dict(color="green", width=2)
                ), row=row, col=1, secondary_y=True)
            else:
                fig.add_trace(go.Scatter(
                    x=df_country["Year"],
                    y=[None] * len(df_country),
                    mode="lines+markers",
                    name=f"{country}: {initial_feature}, male (N/A)",
                    line=dict(color="green", width=2),
                    visible=False
                ), row=row, col=1, secondary_y=True)

        # Layout
        fig.update_layout(
            yaxis2=dict(
                overlaying="y",
                side="right",
                showticklabels=True,  # hides tick labels
                showgrid=False,        # hides grid lines
                zeroline=True,        # hides zero line
                title="",              # removes title
            ),
            yaxis4=dict(
                overlaying="y3",
                side="right",
                showticklabels=True,
                showgrid=False,
                zeroline=True,
                title=""
            ),
            title="GDP Growth vs Employment Indicators - India & Germany",
            height=600,
            template="plotly_white",
            xaxis=dict(title="Year"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5
            )
        )


        # Axis titles
        fig.update_yaxes(title_text="GDP Growth (%)", row=1, col=1, color="blue")
        fig.update_yaxes(title_text=f"{initial_feature} (%)", row=1, col=1, secondary_y=True, color="red")
        fig.update_yaxes(title_text="GDP Growth (%)", row=2, col=1, color="blue")
        fig.update_yaxes(title_text=f"{initial_feature} (%)", row=2, col=1, secondary_y=True, color="red")

        # X-axis title (only bottom subplot needs it)
        fig.update_xaxes(title_text="Year", row=2, col=1)

        # Display chart
        st.plotly_chart(fig, use_container_width=True)
        cd.gdp_vs_employment_description(initial_feature)
        
# <-----------------------------Leadership ------------------------------>

    if chart_type == "Leadership Category":
        countries = ["India", "Germany"]
        df_filtered = df[df["Country"].isin(countries)]

        leadership_features = {
            "Parliament Representation (Female %)": "Proportion parliament's female",
            "Female in Senior/Managerial Role": "Female employment in senior and managerial positions"
        }

        col1, _ = st.columns([2, 5])
        with col1:
            initial_feature_label = st.selectbox(
                "Select a leadership feature:",
                options=list(leadership_features.keys()),
                key="edu_dropdown"
            )

        # Column to use
        col = leadership_features[initial_feature_label]

        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            subplot_titles=[f"{c}" for c in countries],
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
            vertical_spacing=0.15
        )

        # Colors
        gdp_color = "rgba(255, 90, 95, 0.65)"     # Soft coral
        bar_color = "rgba(70, 130, 180, 0.5)"      # Steel blue (bars behind)
        text_color = "#FFFFFF"
        
        for i, country in enumerate(countries):
            df_country = df_filtered[df_filtered["Country"] == country]
            row_idx = i + 1
        
            # GDP Growth (blue, primary y-axis)
            fig.add_trace(go.Scatter(
                x=df_country["Year"],
                y=df_country["gdp_growth"],
                mode='lines',
                name="GDP Growth (%)",
                line=dict(color="rgba(0, 102, 204, 1)", width=2),
                fill="tozeroy",
                fillcolor="rgba(0, 102, 204, 0.3)",
                showlegend=(i == 0)
            ), row=row_idx, col=1, secondary_y=False)
        
            # Initial leadership feature (red, secondary y-axis)
            col = leadership_features[initial_feature_label]
            fig.add_trace(go.Scatter(
                x=df_country["Year"],
                y=df_country[col],
                mode='lines+markers',
                name=f"{country}: {initial_feature_label}",
                line=dict(color="red", width=2),
                showlegend=(i == 0)
            ), row=row_idx, col=1, secondary_y=True)

        fig.update_layout(
            yaxis2=dict(
                overlaying="y",
                side="right",
                showticklabels=True,  # hides tick labels
                showgrid=False,        # hides grid lines
                zeroline=True,        # hides zero line
                title="",              # removes title
            ),
            yaxis4=dict(
                overlaying="y3",
                side="right",
                showticklabels=True,
                showgrid=False,
                zeroline=True,
                title=""
            ),
            title="GDP Growth vs Labour Force Indicators - India & Germany",
            height=600,
            template="plotly_white",
            xaxis=dict(title="Year"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5
            )
        )

        # Y-axis labels
        fig.update_yaxes(title_text="GDP Growth (%)", row=1, col=1, color="blue")
        fig.update_yaxes(title_text=initial_feature_label, row=1, col=1, secondary_y=True, color="red")
        fig.update_yaxes(title_text="GDP Growth (%)", row=2, col=1, color="blue")
        fig.update_yaxes(title_text=initial_feature_label, row=2, col=1, secondary_y=True, color="red")

        # X-axis title (only bottom subplot needs it)
        fig.update_xaxes(title_text="Year", row=2, col=1)

        # Display chart
        st.plotly_chart(fig, use_container_width=True)
        cd.gdp_vs_leadership_description(initial_feature_label)
       
# <-----------------------------Labour Force ---------------------------->

    if chart_type == "Labour Force Category":

        # Filter data
        countries = ["India", "Germany"]
        df_filtered = df[df["Country"].isin(countries)]

        # Define LFP-related features
        lfp_features = {
            "Labor force participation rate": ["Labor force participation rate, female", "Labor force participation rate, male"],
            "LFP Gap (Female - Male)": ["lfp_gap", None],
        }

        # Dropdown selection
        col1, _ = st.columns([2, 5])
        with col1:
            selected_feature = st.selectbox(
                "Select a labor force participation feature:",
                options=list(lfp_features.keys()),
                key="lfp_dropdown"
            )

        female_col = lfp_features[selected_feature][0]
        male_col = lfp_features[selected_feature][1]

        # Create subplots
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            subplot_titles=countries,
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
            vertical_spacing=0.15
        )

        for i, country in enumerate(countries):
            row_idx = i + 1
            df_country = df_filtered[df_filtered["Country"] == country].copy()
            df_country.sort_values("Year", inplace=True)
            df_country.reset_index(drop=True, inplace=True)

            # GDP growth
            fig.add_trace(go.Scatter(
            x=df_country["Year"],
            y=df_country["gdp_growth"],
            mode='lines',
            name=f"{country}: GDP Growth (%)",
            line=dict(color="rgba(0, 102, 204, 1)", width=2),
            fill="tozeroy",
            fillcolor="rgba(0, 102, 204, 0.3)",
            hoverinfo="x+y"
            ), row=row_idx, col=1, secondary_y=False)

            # Female feature (red)
            fig.add_trace(go.Scatter(
                x=df_country["Year"],
                y=df_country[female_col],
                mode='lines+markers',
                name=f"{country} - {female_col}",
                line=dict(color="red")
            ), row=row_idx, col=1, secondary_y=True)

            # Male feature (green), only if available
            if male_col:
                fig.add_trace(go.Scatter(
                    x=df_country["Year"],
                    y=df_country[male_col],
                    mode='lines+markers',
                    name=f"{country} - {male_col}",
                    line=dict(color="green")
                ), row=row_idx, col=1, secondary_y=True)

        fig.update_layout(
            yaxis2=dict(
                overlaying="y",
                side="right",
                showticklabels=True,  # hides tick labels
                showgrid=False,        # hides grid lines
                zeroline=True,        # hides zero line
                title="",              # removes title
            ),
            yaxis4=dict(
                overlaying="y3",
                side="right",
                showticklabels=True,
                showgrid=False,
                zeroline=True,
                title=""
            ),
            title="GDP Growth vs Labour Force Indicators - India & Germany",
            height=600,
            template="plotly_white",
            xaxis=dict(title="Year"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5
            )
        )

        # Y-axis labels
        fig.update_yaxes(title_text="GDP Growth (%)", row=1, col=1, color="blue")
        fig.update_yaxes(title_text=selected_feature, row=1, col=1, secondary_y=True, color="red")
        fig.update_yaxes(title_text="GDP Growth (%)", row=2, col=1, color="blue")
        fig.update_yaxes(title_text=selected_feature, row=2, col=1, secondary_y=True, color="red")

        # X-axis title (only bottom subplot needs it)
        fig.update_xaxes(title_text="Year", row=2, col=1)

        # Display chart
        st.plotly_chart(fig, use_container_width=True)
        cd.gdp_vs_labourforce_description(selected_feature)

# <----------------------------- Unemployment --------------------------->

    if chart_type == "Unemployment Category":
        # Filter data for selected countries
        countries = ["India", "Germany"]
        df_filtered = df[df["Country"].isin(countries)]

        # Define Unemployment & NEET features
        unemp_neet_features = {
            "Unemployment Rate": ["Unemployment rate, female", "Unemployment rate, male"],
            "Unemployment Gap (Female - Male)": ["unemp_gap", None],
            "NEET Rate": ["NEET rate, female", "NEET rate, male"],
            "NEET Gap (Female - Male)": ["neet_gap", None],
        }

        #initial_feature = "Unemployment Rate"
        col1, _ = st.columns([2, 5])  # 2 for dropdown, 5 as spacer
        with col1:
            initial_feature = st.selectbox(
                "Select an education feature:",
                options=unemp_neet_features,
                key="edu_dropdown"
            )

        # Create subplot
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            subplot_titles=countries,
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
            vertical_spacing=0.15
        )

        # Add initial traces
        for i, country in enumerate(countries):
            df_country = df_filtered[df_filtered["Country"] == country]
            row_idx = i + 1

            # # GDP line (primary y-axis)
            # fig.add_trace(go.Scatter(
            #     x=df_country["Year"],
            #     y=df_country["gdp_growth"],
            #     mode='lines+markers',
            #     name=f"{country}: GDP Growth (%)",
            #     line=dict(color="blue"),
            #     showlegend=(i == 0)
            # ), row=row_idx, col=1, secondary_y=False)
            # GDP growth
            fig.add_trace(go.Scatter(
            x=df_country["Year"],
            y=df_country["gdp_growth"],
            mode='lines',
            name=f"{country}: GDP Growth (%)",
            line=dict(color="rgba(0, 102, 204, 1)", width=2),
            fill="tozeroy",
            fillcolor="rgba(0, 102, 204, 0.3)",
            hoverinfo="x+y"
            ), row=row_idx, col=1, secondary_y=False)

            # Female (red)
            fig.add_trace(go.Scatter(
                x=df_country["Year"],
                y=df_country[unemp_neet_features[initial_feature][0]],
                mode='lines+markers',
                name="Female",
                line=dict(color="red"),
                showlegend=(i == 0)
            ), row=row_idx, col=1, secondary_y=True)

            # Male (green) if applicable
            male_col = unemp_neet_features[initial_feature][1]
            fig.add_trace(go.Scatter(
                x=df_country["Year"],
                y=df_country[male_col] if male_col else [None] * len(df_country),
                mode='lines+markers',
                name="Male",
                line=dict(color="green"),
                showlegend=(i == 0 and male_col is not None),
                visible=male_col is not None
            ), row=row_idx, col=1, secondary_y=True)

        # Final layout
        fig.update_layout(
            yaxis2=dict(
                overlaying="y",
                side="right",
                showticklabels=True,  # hides tick labels
                showgrid=False,        # hides grid lines
                zeroline=True,        # hides zero line
                title="",              # removes title
            ),
            yaxis4=dict(
                overlaying="y3",
                side="right",
                showticklabels=True,
                showgrid=False,
                zeroline=True,
                title=""
            ),
            title="GDP Growth vs Unemployment & NEET - India & Germany",
            height=600,
            template="plotly_white",
            xaxis=dict(title="Year"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5
            )
        )

        # Y-axis labels
        fig.update_yaxes(title_text="GDP Growth (%)", row=1, col=1, color="blue")
        fig.update_yaxes(title_text="Unemployment Rate (%)", row=1, col=1, secondary_y=True, color = "red")
        fig.update_yaxes(title_text="GDP Growth (%)", row=2, col=1, color="blue")
        fig.update_yaxes(title_text="Unemployment Rate (%)", row=2, col=1, secondary_y=True, color = "red")

        # X-axis title (only bottom subplot needs it)
        fig.update_xaxes(title_text="Year", row=2, col=1)

        # Display chart
        st.plotly_chart(fig, use_container_width=True)

        cd.gdp_vs_unemployment_description(initial_feature)


# <-----------------------------Fertility ------------------------------->

    if chart_type == "Fertility Category":
        # Filter for countries
        countries = ["India", "Germany"]
        df_filtered = df[df["Country"].isin(countries)]

        # Fertility-related feature labels
        fertility_features = {
            "Adolescent Fertility Rate (15–19)": "Adolescent fertility rate (births per 1,000 women ages 15–19)",
            "Total Fertility Rate": "Total fertility rate (births per woman)",
            "Fertility x Secondary Education": "fertility_secondary_edu_interaction",
            "Fertility x Tertiary Education": "fertility_tertiary_edu_interaction"
        }
        #initial_feature_label = list(fertility_features.keys())[0]
        col1, _ = st.columns([2, 5])  # 2 for dropdown, 5 as spacer
        with col1:
            initial_feature_label = st.selectbox(
                "Select an education feature:",
                options=fertility_features,
                key="edu_dropdown"
            )
        # Create subplot
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            subplot_titles=countries,
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
            vertical_spacing=0.15
        )

        # Add traces for initial feature
        for i, country in enumerate(countries):
            df_country = df_filtered[df_filtered["Country"] == country]
            row_idx = i + 1

            # # GDP Growth trace (blue)
            # fig.add_trace(go.Scatter(
            #     x=df_country["Year"],
            #     y=df_country["gdp_growth"],
            #     mode="lines+markers",
            #     name=f"{country}: GDP Growth (%)",
            #     line=dict(color="blue"),
            #     showlegend=(i == 0)
            # ), row=row_idx, col=1, secondary_y=False)
            # GDP growth
            fig.add_trace(go.Scatter(
            x=df_country["Year"],
            y=df_country["gdp_growth"],
            mode='lines',
            name=f"{country}: GDP Growth (%)",
            line=dict(color="rgba(0, 102, 204, 1)", width=2),
            fill="tozeroy",
            fillcolor="rgba(0, 102, 204, 0.3)",
            hoverinfo="x+y"
            ), row=row_idx, col=1, secondary_y=False)

            # Initial fertility feature trace (red)
            col = fertility_features[initial_feature_label]
            fig.add_trace(go.Scatter(
                x=df_country["Year"],
                y=df_country[col],
                mode="lines+markers",
                name=f"{country}: {initial_feature_label}",
                line=dict(color="red"),
                showlegend=(i == 0)
            ), row=row_idx, col=1, secondary_y=True)

        # Layout
        fig.update_layout(
            yaxis2=dict(
                overlaying="y",
                side="right",
                showticklabels=True,  # hides tick labels
                showgrid=False,        # hides grid lines
                zeroline=True,        # hides zero line
                title="",              # removes title
            ),
            yaxis4=dict(
                overlaying="y3",
                side="right",
                showticklabels=True,
                showgrid=False,
                zeroline=True,
                title=""
            ),
            title="GDP Growth vs Fertility & Education - India & Germany",
            height=600,
            template="plotly_white",
            xaxis=dict(title="Year"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5
            )
        )

        # Y-axis titles
        fig.update_yaxes(title_text="GDP Growth (%)", row=1, col=1, color="blue")
        fig.update_yaxes(title_text=initial_feature_label, row=1, col=1, secondary_y=True, color = "red")
        fig.update_yaxes(title_text="GDP Growth (%)", row=2, col=1, color="blue")
        fig.update_yaxes(title_text=initial_feature_label, row=2, col=1, secondary_y=True, color = "red")

        # X-axis title (only bottom subplot needs it)
        fig.update_xaxes(title_text="Year", row=2, col=1)

        # Display chart
        st.plotly_chart(fig, use_container_width=True)
        cd.gdp_vs_fertility_description(initial_feature_label)

# <----------------------------- Well Being------------------------------>

    if chart_type == "Well Being Category":
        # Filter for India and Germany
        countries = ["India", "Germany"]
        df_filtered = df[df["Country"].isin(countries)]

        # Mapping: Pretty labels (user sees) → actual DataFrame column names
        well_being_features = {
            "Inclusive Bank Index (IBI)": "IBI",
            "Labor Equity & Inclusion Score (LEIS)": "LEIS",
            "Empowerment Progress Index (EPI)": "EPI"
        }

        # UI: Selectbox for feature
        col1, _ = st.columns([2, 5])
        with col1:
            selected_label = st.selectbox(
                "Select a well-being indicator:",
                options=list(well_being_features.keys()),
                key="edu_dropdown"
            )

        selected_column = well_being_features[selected_label]  # Actual column name

        # Subplots setup
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            subplot_titles=countries,
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
            vertical_spacing=0.15
        )

        # Add traces
        for i, country in enumerate(countries):
            df_country = df_filtered[df_filtered["Country"] == country]
            row_idx = i + 1

            # # GDP Growth trace (blue)
            # fig.add_trace(go.Scatter(
            #     x=df_country["Year"],
            #     y=df_country["gdp_growth"],
            #     mode="lines+markers",
            #     name=f"{country}: GDP Growth (%)",
            #     line=dict(color="blue"),
            #     showlegend=(i == 0)
            #), row=row_idx, col=1, secondary_y=False)

            # GDP growth
            fig.add_trace(go.Scatter(
            x=df_country["Year"],
            y=df_country["gdp_growth"],
            mode='lines',
            name=f"{country}: GDP Growth (%)",
            line=dict(color="rgba(0, 102, 204, 1)", width=2),
            fill="tozeroy",
            fillcolor="rgba(0, 102, 204, 0.3)",
            hoverinfo="x+y"
            ), row=row_idx, col=1, secondary_y=False)

            # Well-being indicator trace (red)
            fig.add_trace(go.Scatter(
                x=df_country["Year"],
                y=df_country[selected_column],
                mode="lines+markers",
                name=f"{country}: {selected_label}",
                line=dict(color="red"),
                showlegend=(i == 0)
            ), row=row_idx, col=1, secondary_y=True)

        # Layout
        fig.update_layout(
            yaxis2=dict(
                overlaying="y",
                side="right",
                showticklabels=True,
                showgrid=False,
                zeroline=True,
                title=""
            ),
            yaxis4=dict(
                overlaying="y3",
                side="right",
                showticklabels=True,
                showgrid=False,
                zeroline=True,
                title=""
            ),
            title="GDP Growth vs Index & Wellbeing Indicators - India & Germany",
            height=600,
            template="plotly_white",
            xaxis=dict(title="Year"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5
            )
        )

        # Y-axis titles
        fig.update_yaxes(title_text="GDP Growth (%)", row=1, col=1, color="blue")
        fig.update_yaxes(title_text=selected_label, row=1, col=1, secondary_y=True, color="red")
        fig.update_yaxes(title_text="GDP Growth (%)", row=2, col=1, color="blue")
        fig.update_yaxes(title_text=selected_label, row=2, col=1, secondary_y=True, color="red")

        # X-axis title
        fig.update_xaxes(title_text="Year", row=2, col=1)

        # Display chart
        st.plotly_chart(fig, use_container_width=True)
        cd.gdp_vs_wellbeing_description(selected_label)
