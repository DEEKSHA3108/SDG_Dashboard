import streamlit as st

def render():
    # Anchor to scroll to Overview
    # Add a spacer
    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("<h3 id='overview'>Welcome to the SDG Dashboard: Gender Inequality & Economic Growth</h3>", unsafe_allow_html=True)
    st.markdown("""

    In today’s data-driven landscape, understanding the **intersection of gender equality and economic performance** is critical for shaping inclusive policies and sustainable development strategies. This dashboard is designed to visually explore key insights from the **Sustainable Development Goals (SDG)**, specifically:

    - **Goal 5**: *Gender Equality*  
    - **Goal 8**: *Decent Work & Economic Growth*

    We focus on two representative countries — **India** and **Germany**, across a wide historical range (**1995 to 2023**) to provide meaningful context and comparisons.
    """)

    # Add a spacer
    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)

    # Anchor to scroll to About
    st.markdown("<h3 id='about'>What Can You Do With This Dashboard?</h3>", unsafe_allow_html=True)
    st.markdown("""

    - **Data Gap Analysis**: Identify where and how much data is missing across different indicators and countries.
    - **Exploratory Data Analysis (EDA)**: Dive into category-wise gender and economic indicators to discover patterns and trends.
    - **Forecasting Models**: Leverage statistical models to project **future 5-year GDP growth**.

    This dashboard is built to be intuitive and insightful — whether you're a policymaker, researcher, or someone simply passionate about sustainable development.

    Let’s dive in and explore the data that shapes progress.
    """)
