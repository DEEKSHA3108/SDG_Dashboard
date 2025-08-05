import streamlit as st

# <--------------------- Data Gap Chart Description --------------------->

def heatmap_description():
    with st.expander("Chart Description"):
        st.markdown("""
        This dynamic heatmap provides a clear and intuitive visualization of missing values across the dataset, 
        where each row represents a record and each column corresponds to a feature. The white areas highlight 
        missing data points, making it easy to identify gaps, while red vertical lines outline the features that 
        contain missing values for enhanced visibility. The interactive nature of the chart allows users to explore 
        and analyze data completeness in real time, making it a valuable tool for identifying data quality issues 
        before conducting further analysis or building predictive models.
        """)

def india_germany_missing_description():
    with st.expander("Chart Description"):
        st.markdown("""
        This comparative bar chart highlights the number of missing values for each indicator in India and Germany. 
        Each horizontal bar represents an individual indicator, with the bar length corresponding to the total count 
        of missing values. By visually comparing both countries side by side, the chart provides valuable insight into 
        where data gaps exist, helping to pinpoint which indicators may require further data collection or cleaning. 
        This focused comparison supports better decision-making in cross-country data analysis and quality assurance.
        """)

def top_missing_countries_description():
    with st.expander("Chart Description"):
        st.markdown("""
        This bar chart showcases the top countries with the highest number of missing data fields across all indicators. 
        Each bar represents a country, with the height reflecting the total number of missing values. In this example, 
        India leads with 337 missing entries, followed by Germany with 273. This high-level overview helps quickly identify 
        countries with significant data quality issues, guiding efforts for data cleaning, imputation, or further investigation.
        """)

def stacked_missing_vs_available_description():
    with st.expander("Chart Description"):
        st.markdown("""
        This stacked bar chart presents a comparative overview of available versus missing data points for India and Germany. 
        Each bar is divided into two segments: the blue section represents the number of available (complete) data points, 
        while the red section indicates the number of missing values. This visual makes it easy to assess overall data coverage 
        and spot gaps at a glance. It effectively highlights the proportion of missing information relative to the total dataset 
        for each country, aiding in quick diagnostics and prioritization for data cleaning.
        """)


# <--------------------- Forcasting Chart Description --------------------->

def forcasting_description():
    with st.expander("Chart Description"):
        st.markdown("""
        This dual-panel chart presents historical and forecasted GDP growth for India and Germany from 2000 through 2028, including a five-year forecast horizon (2024–2028). The pink line represents projected GDP growth based on historical trends, while the shaded blue bands illustrate the 95% confidence intervals, capturing the uncertainty around those forecasts. A dashed green line indicates each country’s long-term trend. The vertical red dashed line marks the onset of the COVID-19 pandemic in 2020, highlighting a significant economic disruption for both nations. India’s growth path demonstrates higher average rates and wider uncertainty, reflecting its more dynamic but volatile economic environment. Germany, in contrast, shows more stable historical growth with sharper declines during crises but a consistent return to trend. The forecast suggests a gradual normalization for both economies post-pandemic, offering a forward-looking perspective on macroeconomic recovery and resilience through 2028.
        """)

def error_matrix_table_description():
    with st.expander("Chart Description"):
        st.markdown("""
        This section presents a comparative evaluation of the forecasting model’s performance for India and Germany using two key error metrics: **Root Mean Squared Error (RMSE)** and **Mean Absolute Error (MAE)**. RMSE captures the standard deviation of prediction errors, giving greater weight to large deviations, while MAE provides the average absolute difference between predicted and actual GDP growth values. The chart and accompanying table reveal that the forecasting model performs more accurately for Germany, with significantly lower RMSE and MAE values (2.83 and 1.91, respectively), compared to India (6.29 and 4.68). These discrepancies suggest that India’s GDP growth patterns are more volatile and harder to predict, likely due to greater exposure to structural shifts, policy variability, and external shocks. This comparison helps assess model reliability and highlights the differing levels of economic predictability between developed and emerging economies.
        """)

# <--------------------- EDA Chart Description -------------------------->

def gdp_vs_education_description(selected_feature):
    with st.expander("Chart Description", expanded=True):
        if selected_feature == "Female/male secondary enrollment":
            st.markdown("""
            This visualization compares GDP growth with the ratio of female to male secondary school enrollment in India and Germany. A ratio closer to 1 indicates gender parity. In India, we observe a gradual rise in the ratio toward parity, which aligns with steady economic growth, particularly post-2005. Germany, having already achieved near parity in the 1990s, shows minimal fluctuations, suggesting its stable educational equity. This plot helps illustrate how countries at different development stages reflect education gender parity in broader economic patterns.
            """)
        
        elif selected_feature == "Female/male tertiary enrollment":
            st.markdown("""
            This graph highlights the evolving gender dynamics in tertiary education and their relationship with GDP growth. India shows a significant improvement in female-to-male tertiary enrollment, even surpassing parity in recent years. Interestingly, this upward trend aligns with India's post-2010 economic growth spurts. Germany maintains steady GDP performance while also showing a slight dominance of female enrollment, which may signal advanced educational access. This comparison provides insights into how gender progress in higher education correlates with economic trajectories.
            """)

        elif selected_feature == "Secondary school enrollment, female":
            st.markdown("""
            Here, we analyze the percentage of girls enrolled in secondary school alongside GDP growth trends. In India, enrollment rates among girls have risen steadily over the decades, from under 50% to over 80%, mirroring a trajectory of economic development. In contrast, Germany already maintained a high and stable enrollment rate, with only minor variations. This chart underscores how improving access to secondary education for girls can be both a result and a driver of economic performance, particularly in emerging economies like India.
            """)

        elif selected_feature == "Tertiary school enrollment, female":
            st.markdown("""
            This visualization showcases the female tertiary enrollment rate and its correlation with GDP growth. India exhibits remarkable growth in women's higher education enrollment—from below 10% in the 1990s to over 30% recently—coinciding with periods of economic expansion. Germany, while starting at a much higher base, shows stable but fluctuating enrollment patterns with occasional dips. The graph offers a clear narrative of how expanding higher education for women can reflect broader socio-economic transformations.
            """)

        elif selected_feature == "education_index":
            st.markdown("""
            This chart compares GDP growth with the Education Index—a composite measure reflecting the average years of schooling and expected years of schooling. India's steady rise in the Education Index over the years mirrors its growing economy and educational infrastructure. Germany’s consistently high index scores reflect a matured education system with minimal year-to-year variation. This comparison allows for a holistic view of how broader education development aligns with long-term economic outcomes.
            """)

        elif selected_feature == "ed_progression_ratio":
            st.markdown("""
            This plot links GDP growth with the education progression ratio, which indicates the percentage of students progressing from primary to secondary education. India shows a sharp increase in this ratio over time, reflecting improvements in foundational educational access, which aligns with periods of GDP growth. Germany, on the other hand, maintains a high progression ratio with some variance. The comparison highlights how early educational transition plays a crucial role in shaping economic opportunities, particularly in developing nations.
            """)

        else:
            st.markdown("No description available for this selection.")


def gdp_vs_employment_description(selected_feature):
    with st.expander("Chart Description"):
        if selected_feature == "Employment to population ratio":
            st.markdown("""
            This chart compares the **employment-to-population ratio** (both male and female) with **GDP growth** in India and Germany. The chart highlights how economic growth may influence workforce participation rates over time. India shows a gradual increase in female employment alongside rising GDP, while Germany maintains consistently high employment ratios. The gender gap is more prominent in India but shows signs of narrowing in recent years. These trends reflect structural shifts in labor markets and the socio-economic factors influencing workforce inclusion.
            """)
        
        elif selected_feature == "Female employment in agriculture":
            st.markdown("""
            This graph visualizes the **female employment in agriculture** as a percentage of total female employment against **GDP growth**. In India, there is a steady decline in agricultural employment for women, suggesting a transition towards other sectors as the economy matures. Conversely, Germany's figures remain low and flat, indicating a minimal role of agriculture in female employment. This contrast emphasizes the ongoing economic transformation in developing economies and sectoral shifts in employment structures.
            """)
        
        elif selected_feature == "Female employment in senior and managerial positions":
            st.markdown("""
            This chart tracks the proportion of **female employment in senior and managerial roles** relative to **GDP growth**. While India shows virtually no change over time, Germany shows modest progress in women's representation in leadership positions, even during fluctuating economic conditions. This visualization highlights the challenges of upward mobility for women in India despite economic growth and underscores the importance of inclusive policies and organizational reforms to foster gender diversity in leadership.
            """)

        elif selected_feature == "Emp Gap (Female - Male)":
            st.markdown("""
            This chart presents the **employment gap between females and males** compared with **GDP growth**. India's employment gap is seen narrowing over the years, suggesting improved gender parity in labor force participation, especially in the last decade. On the other hand, Germany’s gender employment gap slightly widens, even with steady GDP growth. These trends provide insights into how economic development does not always equate to equal employment gains across genders, urging a closer look into gender-focused labor policies.
            """)


def gdp_vs_leadership_description(selected_feature):
    with st.expander("Chart Description"):
        if selected_feature == "Parliament Representation (Female %)":
            st.markdown("""
            This visualization examines the relationship between **GDP growth** and **female representation in national parliaments** in India and Germany. India's chart reveals a modest but steady upward trend in women's parliamentary participation over the years, from below 5% to around 15%, which is mirrored by a relatively stable economic growth trajectory. Germany, on the other hand, shows consistently higher levels of female parliamentary representation, peaking above 30%, with minimal disruption across economic cycles. This comparison highlights different stages of gender inclusion in politics and how societal structures may influence leadership diversity alongside economic performance.
            """)

        elif selected_feature == "Female in Senior/Managerial Role":
            st.markdown("""
            This chart explores the evolution of **female employment in senior and managerial roles** against **GDP growth** in India and Germany. While Germany displays a visible and steady rise in women in leadership, surpassing 25%, India’s numbers remain critically low, hovering around 0%—indicating deep-rooted barriers to top-level gender inclusion. Despite comparable economic fluctuations, the disparity suggests that economic growth alone does not drive gender parity in leadership. The German case may reflect stronger institutional and corporate policies supporting women's advancement into executive roles.
            """)


def gdp_vs_labourforce_description(selected_feature):
    with st.expander("Chart Description"):
        if selected_feature == "Labor force participation rate":
            st.markdown("""
            This chart explores the relationship between **GDP growth** and the **labor force participation rate (LFPR)** for males and females in India and Germany. While male LFPR remains consistently high across both countries, the female participation rate in India shows a steady decline, even during periods of economic expansion. Germany demonstrates more stable and balanced participation trends between genders. These patterns underscore persistent gender disparities in labor force access in developing economies and prompt questions about structural and socio-cultural barriers limiting women's economic involvement in India.
            """)

        elif selected_feature == "LFP Gap (Female - Male)":
            st.markdown("""
            This visualization examines the **gender gap in labor force participation** (Female - Male) against **GDP growth**. In India, the gap initially widens but starts to narrow in recent years, although still remaining significant. Germany shows a consistent decline in the gap, stabilizing at much lower levels. The contrast highlights how inclusive labor market policies and progressive gender norms in developed economies like Germany contribute to workforce equality. India's persistent disparity, despite economic progress, suggests the need for focused gender-sensitive employment strategies.
            """)


def gdp_vs_unemployment_description(selected_feature):
    with st.expander("Chart Description"):
        if selected_feature == "Unemployment Rate":
            st.markdown("""
            This chart compares **GDP growth** with the **male and female unemployment rates** in India and Germany. In India, female unemployment consistently exceeds male unemployment, and the gap worsens in response to economic slowdowns, especially after 2020. Germany, on the other hand, shows a declining trend in unemployment for both genders, with a closer alignment to GDP changes. This contrast highlights structural differences in labor markets and the resilience of Germany’s employment systems compared to India’s gender-segmented labor market.
            """)

        elif selected_feature == "Unemployment Gap (Female - Male)":
            st.markdown("""
            This graph displays the **unemployment gender gap** (Female - Male) relative to GDP growth. In India, the gap is persistently positive and widens during downturns, revealing a disproportionate impact on female employment. Germany shows a near-zero or slightly negative gap across most years, indicating a more gender-equitable labor market. The data implies that India’s female workforce is more vulnerable to macroeconomic shocks, while Germany’s policy frameworks provide greater gender protection.
            """)

        elif selected_feature == "NEET Rate":
            st.markdown("""
            This visualization plots **GDP growth** against the **NEET (Not in Employment, Education, or Training) rate** for males and females. In India, female NEET rates are extremely high and remain largely unaffected by GDP fluctuations, indicating structural exclusion from both education and work. Male NEET rates are lower and relatively stable. Germany shows consistently low NEET rates for both genders, reflecting stronger education-to-work transitions and inclusive youth employment policies.
            """)

        elif selected_feature == "NEET Gap (Female - Male)":
            st.markdown("""
            This chart examines the **NEET gender gap** (Female - Male) alongside GDP growth. India displays a wide and persistent NEET gap, often exceeding 20%, with the gap expanding during periods of economic decline. This underscores deep-rooted gender disparities in youth engagement. Germany’s NEET gap remains minimal or even negative, suggesting that women are equally or more engaged than men in productive activity. The chart reveals critical gaps in gender equity and opportunity in India’s youth landscape.
            """)


def gdp_vs_fertility_description(selected_feature):
    with st.expander("Chart Description"):
        if selected_feature == "Adolescent Fertility Rate (15–19)":
            st.markdown("""
            This chart visualizes the relationship between **GDP growth** and the **Adolescent Fertility Rate (ages 15–19)** for India and Germany. India exhibits a steep decline in adolescent fertility over the years, especially from the early 2000s onward, even as GDP growth shows cyclical fluctuations. The most notable drop occurs post-2010, indicating socio-economic shifts and improved access to education and healthcare. In contrast, Germany maintains a consistently low adolescent fertility rate, with only gradual reductions, suggesting that the indicator is largely decoupled from economic changes due to established reproductive health systems. The inverse correlation in India highlights progress in gender health indicators during economic development.
            """)

        elif selected_feature == "Total Fertility Rate":
            st.markdown("""
            This graph compares **Total Fertility Rate (TFR)** with **GDP growth** in India and Germany. India's TFR shows a continuous and substantial decline, from above 3.5 in the 1990s to below 2.0 by 2022, mirroring the demographic transition typical of developing economies. The fall persists despite GDP fluctuations, suggesting that fertility reductions are driven by broader structural changes like urbanization, female literacy, and access to contraception. Germany's TFR remains low and stable, hovering around 1.4–1.6, and appears largely insulated from short-term economic variation. This chart underscores differing demographic maturities and the long-term societal shifts influencing fertility trends across both nations.
            """)

        elif selected_feature == "Fertility x Secondary Education":
            st.markdown("""
            This chart compares **GDP growth** with the interaction of **fertility rate and female secondary school enrollment** for India and Germany. In India, a clear inverse trend emerges — as more girls enroll in secondary education, fertility rates drop, and economic growth generally sustains upward momentum. Germany, already having low fertility and high education rates, shows less dramatic fluctuations, with smaller variations in the combined metric. This visualization captures how **educational attainment at the secondary level can significantly influence reproductive behavior and long-term economic outcomes** in developing countries. The interaction term amplifies this effect by tying together both social and economic progress in a single composite measure.
            """)

        elif selected_feature == "Fertility x Tertiary Education":
            st.markdown("""
            This graph illustrates the connection between **GDP growth** and the interaction of **fertility rate and female tertiary (higher) education enrollment**. For India, the declining trend in the interaction value reflects expanding access to higher education among women and a parallel decline in fertility — key indicators of a maturing economy. In Germany, the metric remains relatively stable, indicating an already saturated system with consistent educational and fertility behavior. This interaction term helps quantify the dual impact of education and reproductive trends on economic momentum, particularly highlighting the role of tertiary education in empowering women and reducing fertility over time.
            """)


def gdp_vs_wellbeing_description(selected_indicator):
    with st.expander("Chart Description"):
        if selected_indicator == "Labor Equity & Inclusion Score (LEIS)":
            st.markdown("""
            This chart visualizes the relationship between **GDP Growth (%)** and the **Labor Equity & Inclusion Score (LEIS)** for **India and Germany** over time. In India, LEIS demonstrates a sharp upward trend despite economic fluctuations, reflecting strong national efforts toward equitable and inclusive labor practices. Germany maintains consistently high LEIS values, with smaller fluctuations and a stable economic backdrop. This suggests that while economic growth is important, policy-driven equity improvements can progress independently of GDP variations.
            """)

        elif selected_indicator == "Inclusive Bank Index (IBI)":
            st.markdown("""
            This dynamic graph compares **GDP Growth (%)** with the **Inclusive Bank Index (IBI)** for **India and Germany**. India's IBI trajectory is marked by volatility and occasional disconnect from GDP trends, signaling uneven progress in financial inclusion. Germany, meanwhile, shows a declining IBI despite relatively stable GDP growth, raising critical questions about long-term access to financial services. The visualization emphasizes how inclusive banking development may not always move in tandem with economic expansion.
            """)

        elif selected_indicator == "Empowerment Progress Index (EPI)":
            st.markdown("""
            The chart illustrates the correlation between **GDP Growth (%)** and the **Empowerment Progress Index (EPI)** in **India and Germany**. India showcases a steady and substantial rise in EPI, particularly in recent years, aligning with moderate GDP growth and reflecting strong gains in societal empowerment. Germany shows consistent EPI growth with minor dips, largely independent of economic variations. This trend reveals that social empowerment can advance even during periods of slow or stagnant GDP growth, underscoring the role of sustained policy efforts.
            """)

        else:
            st.markdown("Please select a valid well-being indicator to view a detailed description.")




