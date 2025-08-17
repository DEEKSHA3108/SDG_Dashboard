import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import chartDiscription as cd

from dataLoading import load_world_bank_data  # Import the cached data function

def render():
   # Load the processed data
    data = load_world_bank_data()
    df_pivoted = data.copy()
    
    # Radio buttons to toogle between graphs
    st.sidebar.subheader("Data Gap Visuals")
    chart_type = st.sidebar.radio(
        "Choose a chart to visualize:",
        [
            "Heatmap for missing data",
            "Missing Values Country wise Per Indicator",
            "Country wise Total Missing Value",
            "Available vs Missing Values per Country"
        ]
    )

    data = df_pivoted.copy()
    # Renaming the indictors for proper understanding 
    data.rename(columns={
            "FX.OWN.TOTL.FE.ZS": "FX.OWN.TOTL.FE.ZS: Account holder, Female",
            "FX.OWN.TOTL.MA.ZS": "FX.OWN.TOTL.MA.ZS: Account holder, Male",
            "IC.FRM.FEMM.ZS": "IC.FRM.FEMM.ZS: Firms with female in ownership",
            "IC.FRM.FEMO.ZS": "IC.FRM.FEMO.ZS: Firms with female top manager",
            "IT.NET.USER.FE.ZS": "IT.NET.USER.FE.ZS: Internet users, female",
            "IT.NET.USER.MA.ZS": "IT.NET.USER.MA.ZS: Internet users, male",
            "NY.GDP.MKTP.KD.ZG": "NY.GDP.MKTP.KD.ZG: GDP growth",
            "NY.GDP.PCAP.KD.ZG": "NY.GDP.PCAP.KD.ZG: GDP per capita growth)",
            "SE.ENR.SECO.FM.ZS": "SE.ENR.SECO.FM.ZS: Secondary enrollment, female",
            "SE.ENR.TERT.FM.ZS": "SE.ENR.TERT.FM.ZS: Tertiary enrollment, female",
            "SE.SEC.ENRR.FE": "SE.SEC.ENRR.FE: Secondary enrollment ratio, female",
            "SE.TER.ENRR.FE": "SE.TER.ENRR.FE: Tertiary enrollment ratio, female",
            "SG.GEN.PARL.ZS": "SG.GEN.PARL.ZS: Women in parliament",
            "SG.TIM.UWRK.FE": "SG.TIM.UWRK.FE: Time-related underemployment, female",
            "SG.TIM.UWRK.MA": "SG.TIM.UWRK.MA: Time-related underemployment, male",
            "SL.AGR.EMPL.FE.ZS": "SL.AGR.EMPL.FE.ZS: Employment in agriculture, female",
            "SL.EMP.SMGT.FE.ZS": "SL.EMP.SMGT.FE.ZS: Women in senior and middle management",
            "SL.EMP.WORK.FE.ZS": "SL.EMP.WORK.FE.ZS: Wage/salaried workers, female",
            "SL.EMP.WORK.MA.ZS": "SL.EMP.WORK.MA.ZS: Wage/salaried workers, male",
            "SL.TLF.CACT.FE.ZS": "SL.TLF.CACT.FE.ZS: Labor force participation, female",
            "SL.TLF.CACT.MA.ZS": "SL.TLF.CACT.MA.ZS: Labor force participation, male",
            "SL.UEM.NEET.FE.ZS": "SL.UEM.NEET.FE.ZS: Youth disengagement(edu, job, training), female",
            "SL.UEM.NEET.MA.ZS": "SL.UEM.NEET.MA.ZS, Youth disengagement(edu, job, training, male",
            "SL.UEM.TOTL.FE.ZS": "SL.UEM.TOTL.FE.ZS: Unemployment rate, female",
            "SL.UEM.TOTL.MA.ZS": "SL.UEM.TOTL.MA.ZS: Unemployment rate, male",
            "SP.ADO.TFRT": "SP.ADO.TFRT: Adolescent fertility rate (births 1/1000 women ages 15–19)",
            "SP.DYN.TFRT.IN": "SP.DYN.TFRT.IN: Total fertility rate (births per woman)",
            "SP.M15.2024.FE.ZS": "SP.M15.2024.FE.ZS: Median age, female (age 15, 2024 est.)",
            "SP.M18.2024.FE.ZS": "SP.M18.2024.FE.ZS: Median age, female (age 18, 2024 est.)"
        }, inplace=True)
    
# <--------------------- Graphs render with Radio Button ----------------------->
    if chart_type == "Heatmap for missing data":
        # Compute null matrix and metadata
        null_matrix = data.isnull()
        z = null_matrix.astype(int).values
        feature_names = data.columns.tolist()
        missing_counts = null_matrix.sum().values  # Total missing per feature
        n_rows, n_features = z.shape

        # Custom text for each cell in the heatmap
        custom_text = [
            [f"Feature: {feature_names[col]}<br>Missing Count: {missing_counts[col]}" if z[row][col] == 1 else ""
            for col in range(n_features)]
            for row in range(n_rows)
        ]

        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=z,
            x=feature_names,
            text=custom_text,
            hoverinfo='text',  # only use the custom text
            colorscale=[[0, 'black'], [1, 'white']],
            showscale=False
        ))

        # Add red vertical lines between features
        for x in range(1, n_features):
            fig.add_shape(
                type="line",
                x0=x - 0.5, x1=x - 0.5,
                y0=-0.5, y1=n_rows - 0.5,
                line=dict(color="red", width=1)
            )

        # Layout with rotated labels and extra margin
        fig.update_layout(
            title="Missing Values Heatmap with Red Lines Around Missing Features",
            xaxis_title="Features",
            yaxis_title="Records",
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(n_features)),
                ticktext=feature_names,
                tickangle=45
            ),
            yaxis=dict(showticklabels=False),
            margin=dict(l=60, r=30, t=80, b=200),
            width=600,
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)
        cd.heatmap_description()

    elif chart_type == "Missing Values Country wise Per Indicator":
        # Filter for India and Germany
        countries = ['India', 'Germany']
        country_data = data[data['Country'].isin(countries)]

        # Create subplot (1 row, 2 columns)
        fig = make_subplots(
            rows=1, cols=2,
            shared_yaxes=True,
            subplot_titles=[f"{country} - Missing Values" for country in countries]
        )

        # Loop through countries and generate bar charts
        for i, country in enumerate(countries, start=1):
            subset = country_data[country_data['Country'] == country]
            
            # Drop irrelevant columns
            subset = subset.drop(columns=['Country', 'Year'], errors='ignore')
            
            # Calculate missing values per column
            missing_counts = subset.isnull().sum()
            missing_counts = missing_counts[missing_counts > 0].sort_values(ascending=True)

            # Add horizontal bar to subplot
            fig.add_trace(
                go.Bar(
                    x=missing_counts.values,
                    y=missing_counts.index,
                    orientation='h',
                    marker=dict(color='tomato'),
                    name=country,
                    showlegend=False
                ),
                row=1, col=i
            )

        # Update layout
        fig.update_layout(
            height=600,
            width=1200,
            title_text="India vs Germany - Missing Values Per Indicator",
            template="plotly_white"
        )

        fig.update_xaxes(title_text="Number of Missing Values", row=1, col=1)
        fig.update_xaxes(title_text="Number of Missing Values", row=1, col=2)
        fig.update_yaxes(title_text="Indicator", row=1, col=1)

        st.plotly_chart(fig, use_container_width=True)
        cd.india_germany_missing_description()

    
    elif chart_type == "Country wise Total Missing Value":
        # Filter only India and Germany
        subset = data[data['Country'].isin(['India', 'Germany'])]

        # Count total missing values for each country
        missing_by_country = subset.groupby('Country').apply(lambda x: x.isnull().sum().sum()).reset_index()
        missing_by_country.columns = ['Country', 'Total Missing Fields']

        # Create the bar chart with fixed color and larger figure size
        fig = px.bar(
            missing_by_country.sort_values('Total Missing Fields', ascending=False),
            x='Country',
            y='Total Missing Fields',
            title='Top Countries with Most Missing Values',
            text='Total Missing Fields',
            color_discrete_sequence=['skyblue']  # Same color for all bars
        )

        fig.update_traces(textposition='outside')

        # Customize layout for wider figure
        fig.update_layout(
            width=900,  # Increase width
            height=600,
            xaxis_title='Country',
            yaxis_title='Total Missing Fields',
            showlegend=False,
            template='plotly_white'
        )

        st.plotly_chart(fig, use_container_width=True)
        cd.top_missing_countries_description()


    elif chart_type == "Available vs Missing Values per Country":
        # Ensure columns are clean
        data.columns = data.columns.str.strip()

        # Define indicators (excluding identifiers)
        indicators = data.columns.difference(['economy', 'Country', 'Year'])

        # Count missing and available values per country
        missing_counts = data[indicators].isnull().groupby(data['Country']).sum().sum(axis=1)
        available_counts = data[indicators].notnull().groupby(data['Country']).sum().sum(axis=1)

        # Combine into DataFrame
        df_gap = pd.DataFrame({
            'Country': available_counts.index,
            'Available': available_counts.values,
            'Missing': missing_counts.reindex(available_counts.index, fill_value=0).values
        })

        # Optional: filter specific countries like Germany and India
        df_gap = df_gap[df_gap['Country'].isin(['Germany', 'India'])]

        # Plotly stacked bar chart
        fig = go.Figure(data=[
            go.Bar(name='Available', x=df_gap['Country'], y=df_gap['Available'],
                marker_color='royalblue'),
            go.Bar(name='Missing', x=df_gap['Country'], y=df_gap['Missing'],
                marker_color='tomato')
        ])

        fig.update_layout(
            height=600,
            barmode='stack',
            title='Stacked Bar: Available vs Missing Values per Country',
            xaxis_title='Country',
            yaxis_title='Number of Data Points'
        )

        st.plotly_chart(fig, use_container_width=True)
        cd.stacked_missing_vs_available_description()
