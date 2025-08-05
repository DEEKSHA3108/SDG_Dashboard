# Load the requried Libraries
import wbgapi as wb
import pandas as pd
import numpy as np
import streamlit as st
from fancyimpute import IterativeImputer
from sklearn.impute import IterativeImputer
from sklearn.metrics import mean_squared_error
from sklearn.experimental import enable_iterative_imputer

# <------------------------ List of the Indicators ---------------------------->
indicators =  [
    'FIN.ACC.OWN.FE', 'FIN.ACC.OWN.MA', 'FX.OWN.TOTL.FE.ZS', 'FX.OWN.TOTL.MA.ZS', 'IC.FRM.FEMM.ZS',
 'IC.FRM.FEMO.ZS', 'IC.REG.COST.FE.ZS', 'IT.CEL.SETS.FE.ZS', 'IT.CEL.SETS.MA.ZS',
    'IT.NET.USER.FE.ZS', 'IT.NET.USER.MA.ZS',
 'NY.GDP.MKTP.KD.ZG', 'NY.GDP.PCAP.KD.ZG', 'SE.SEC.ENRR.FE','SE.ENR.SECO.FM.ZS', 'SE.ENR.TERT.FM.ZS', 
    'SE.TER.ENRR.FE', 'SG.GEN.PARL.ZS',
 'SG.TIM.UWRK.FE', 'SG.TIM.UWRK.MA', 'SL.AGR.EMPL.FE.ZS', 'SL_DOM_TSPD', 'SL.EMP.SMGT.FE.ZS', 
 'SL.EMP.WORK.FE.ZS', 
 'SL.EMP.WORK.MA.ZS', 'SL.ISV.IFRM.FE.ZS', 'SL.ISV.IFRM.MA.ZS', 'SL.TLF.CACT.FE.ZS', 'SL.TLF.CACT.MA.ZS',
 'SL.UEM.NEET.FE.ZS', 'SL.UEM.NEET.MA.ZS', 'SL.UEM.TOTL.FE.ZS', 'SL.UEM.TOTL.MA.ZS', 'SL.WAG.010.FE.ZS',
 'SL_DOM_TSPDCW', 'SL_DOM_TSPDDC', 'SP.ADO.TFRT', 'SP.DYN.TFRT.IN', 'SP.M15.2024.FE.ZS',
 'SP.M18.2024.FE.ZS', 'SP.MARR.1524.FE.ZS'
]

# Countries: India (IND), Germany (DEU), Canada (CAN), South Africa (ZAF)
countries = ['IND', 'DEU']  #'CAN','ZAF']

# Years: 2000 to 2023
years = range(1995, 2024)

@st.cache_data
def load_world_bank_data():
# <---------------- Loading the data from world bank api ----------------------->
    # Fetch data from the world bank api 
    df = wb.data.DataFrame(indicators, economy=countries, time=years, labels=True)
    # Reset index
    df.reset_index(inplace=True)
    # Save to CSV
    df.to_csv('worldbank_extracted_data.csv', index=False)

# <----------------------- Pre processing the data ----------------------------->
    # Replace YR from the column names
    df.columns = [int(i.replace('YR', '')) if 'YR' in i else i for i in df.columns]
    # Copying the df to a new variable df_new, for interchanging the rows and columns for handling the NaN values
    df_new = df.copy()

    # Converting the Df from wider format to longer format, where creating all years column under a single column "Year"
    df_long = pd.melt(
        df_new,
        id_vars=["economy", "series", "Country"],
        value_vars= df.columns[4:33],
        var_name="Year",
        value_name="Value"
    )
    # Pivoting the DF where "series" column row unique values will become columns 
    df_pivoted = df_long.pivot_table(
        index=["economy", "Country", "Year"],
        columns="series",
        values="Value"
    ).reset_index()

    return df_pivoted

# <----------------------- Cleaning the data ----------------------------->
@st.cache_data
def cleaned_data():
    data = load_world_bank_data()
    df_pivoted = data.copy()
    df_pivoted = df_pivoted.drop(columns = ['economy', 'FX.OWN.TOTL.FE.ZS' ,'FX.OWN.TOTL.MA.ZS', 'IC.FRM.FEMM.ZS', 'IC.FRM.FEMO.ZS',
                                       'SG.TIM.UWRK.FE', 'SG.TIM.UWRK.MA', 'SP.M15.2024.FE.ZS', 'SP.M18.2024.FE.ZS' ], axis = 1)
    india_original_data = df_pivoted[df_pivoted['Country'] == 'India'].copy()
    germany_original_data = df_pivoted[df_pivoted['Country'] == 'Germany'].copy()

    india_temp_data = df_pivoted[df_pivoted['Country'] == 'India']
    germany_temp_data = df_pivoted[df_pivoted['Country'] == 'Germany']
    high_missing_cols = [
    'IT.NET.USER.FE.ZS',
    'IT.NET.USER.MA.ZS',
    'SL.EMP.SMGT.FE.ZS'
    ]
    india_temp_data[high_missing_cols] = 0

    columns_with_missing = [col for col in india_temp_data.select_dtypes(include=[np.number]).columns if india_temp_data[col].isnull().any()]
    print(columns_with_missing)


    print()
        
    # Select a larger numeric subset for imputation
    numeric_cols = india_temp_data.select_dtypes(include=[np.number]).columns.tolist()

    # Apply MICE on all numeric columns to use full context
    mice_imputer = IterativeImputer(random_state=42, max_iter=10)
    india_temp_data[numeric_cols] = mice_imputer.fit_transform(india_temp_data[numeric_cols])

# <--------------------- Handling Missing Values too much deflecting ------------------------>
    india_temp_data['SL.UEM.NEET.FE.ZS'] = india_original_data['SL.UEM.NEET.FE.ZS']
    india_temp_data['SL.UEM.NEET.MA.ZS'] = india_original_data['SL.UEM.NEET.MA.ZS']
    # <====================== India =========================>
    # Set seed for reproducibility
    np.random.seed(42)

    # List of columns to impute
    cols_to_impute = ['SL.UEM.NEET.FE.ZS', 'SL.UEM.NEET.MA.ZS']

    for col in cols_to_impute:
        # Get non-null values from the column
        non_null_values = india_temp_data[col].dropna().values

        # Get the indices where values are NaN
        null_indices = india_temp_data[india_temp_data[col].isna()].index

        # Randomly sample (with replacement) from non-null values
        imputed_values = np.random.choice(non_null_values, size=len(null_indices), replace=True)

        # Assign imputed values back
        india_temp_data.loc[null_indices, col] = imputed_values

    # <===================== Germany ==========================>
    np.random.seed(42)
    na_cols = germany_temp_data.columns[germany_temp_data.isnull().any()].tolist()

    # Add missing indicators
    for col in na_cols:
        germany_temp_data[col + '_missing'] = germany_temp_data[col].isnull().astype(int)

    # Numeric columns (including indicators)
    numeric_cols = germany_temp_data.select_dtypes(include=np.number).columns

    # Random Imputation
    for col in na_cols:
        col_data = germany_temp_data[col]
        missing_mask = col_data.isnull()
        observed = col_data[~missing_mask]
        
        # Use normal distribution based on real data
        mu = observed.mean()
        sigma = observed.std()

        # Generate random values, clipped to observed range
        noise = np.random.normal(loc=mu, scale=sigma, size=missing_mask.sum())
        noise = np.clip(noise, observed.min(), observed.max())

        # Fill in missing values with noise
        germany_temp_data.loc[missing_mask, col] = noise

    # Drop the temporary _missing columns
    germany_temp_data.drop(columns=[col + '_missing' for col in na_cols], inplace=True)

    # Updating in the original dataset 
    df_pivoted.loc[germany_temp_data.index, germany_temp_data.columns ] = germany_temp_data
    df_pivoted.loc[india_temp_data.index, india_temp_data.columns ] = india_temp_data

# <-------------------------- Pre-processing Data --------------------------->

    # Gender gap in employment rate (male - female)
    df_pivoted['emp_gap'] = df_pivoted['SL.EMP.WORK.MA.ZS'] - df_pivoted['SL.EMP.WORK.FE.ZS']

    # Ratio of female to male employment rate
    df_pivoted['emp_ratio'] = df_pivoted['SL.EMP.WORK.FE.ZS'] / df_pivoted['SL.EMP.WORK.MA.ZS']

    # Gender gap in labor force participation (male - female)
    df_pivoted['lfp_gap'] = df_pivoted['SL.TLF.CACT.MA.ZS'] - df_pivoted['SL.TLF.CACT.FE.ZS']

    # Ratio of female to male labor force participation
    df_pivoted['lfp_ratio'] = df_pivoted['SL.TLF.CACT.FE.ZS'] / df_pivoted['SL.TLF.CACT.MA.ZS']

    # Gender gap in unemployment (female - male) — positive means female unemployment is higher
    df_pivoted['unemp_gap'] = df_pivoted['SL.UEM.TOTL.FE.ZS'] - df_pivoted['SL.UEM.TOTL.MA.ZS']

    # Ratio of male to female unemployment — closer to 1 is better equality
    df_pivoted['unemp_ratio'] = df_pivoted['SL.UEM.TOTL.MA.ZS'] / df_pivoted['SL.UEM.TOTL.FE.ZS']

    # Gender gap in NEET (Not in Employment, Education or Training)
    df_pivoted['neet_gap'] = df_pivoted['SL.UEM.NEET.FE.ZS'] - df_pivoted['SL.UEM.NEET.MA.ZS']

    # Ratio of male to female NEET rate
    df_pivoted['neet_ratio'] = df_pivoted['SL.UEM.NEET.MA.ZS'] / df_pivoted['SL.UEM.NEET.FE.ZS']

    ratio_cols = [
    'emp_ratio', 'lfp_ratio', 'unemp_ratio',
    'neet_ratio'
    ]
    df_pivoted[ratio_cols] = df_pivoted[ratio_cols].replace([np.inf, -np.inf], np.nan).fillna(0)


    # 2. EMPOWERMENT, EDUCATION & DEMOGRAPHICS 

    # Combined leadership indicator: women in parliament + women in senior management
    df_pivoted['female_leadership'] = df_pivoted['SG.GEN.PARL.ZS'] #+ df_pivoted['SL.EMP.SMGT.FE.ZS']

    # Composite education index: average of secondary and tertiary female enrollment
    df_pivoted['education_index'] = df_pivoted[['SE.SEC.ENRR.FE', 'SE.TER.ENRR.FE']].mean(axis=1)

    # Interaction of fertility rate and secondary education (higher when fertility is high and education low)
    df_pivoted['fertility_secondary_edu_interaction'] = df_pivoted['SP.DYN.TFRT.IN'] * (1 - (df_pivoted['SE.SEC.ENRR.FE'] / 100))

    df_pivoted['fertility_tertiary_edu_interaction'] = df_pivoted['SP.DYN.TFRT.IN'] * (1 - (df_pivoted['SE.TER.ENRR.FE'] / 100))

    # Ratio of tertiary to secondary enrollment — indicates progression of female education
    df_pivoted['ed_progression_ratio'] = df_pivoted['SE.TER.ENRR.FE'] / df_pivoted['SE.SEC.ENRR.FE']


    # 3. COMPOSITE INDICES 

    # Inequality Burden Index (IBI): sum of employment, labor, NEET and unemployment gender gaps
    df_pivoted['IBI'] = (
        df_pivoted['emp_gap'] +
        df_pivoted['lfp_gap'] +
        df_pivoted['neet_gap'] +
        df_pivoted['unemp_gap']
    )

    #  Extended IBI: adds adolescent fertility rate as an added burden dimension
    # Normalize fertility rate
    df_pivoted['SP.ADO.TFRT_NORM'] = df_pivoted['SP.ADO.TFRT'] / (df_pivoted['SP.ADO.TFRT'].max())
    # IBI extended
    df_pivoted['IBI_extended'] = df_pivoted['IBI'] + df_pivoted['SP.ADO.TFRT_NORM']


    # Leadership & Education Inclusion Score (LEIS): positive indicator combining leadership, education, and internet access
    df_pivoted['LEIS'] = (
        df_pivoted['female_leadership'] +
        df_pivoted['SE.SEC.ENRR.FE'] +
        df_pivoted['IT.NET.USER.FE.ZS']
    )


    df_pivoted['EPI'] = (
        df_pivoted['SL.EMP.WORK.FE.ZS'] +
        df_pivoted['SL.TLF.CACT.FE.ZS'] -
        df_pivoted['SL.UEM.TOTL.FE.ZS']
    )

    # <== Renaming the column ===>
    df_pivoted = df_pivoted.rename({'NY.GDP.PCAP.KD.ZG': 'gdp_per_capita_growth', 
                  'NY.GDP.MKTP.KD.ZG' : 'gdp_growth'}, axis = 1)
    
    df_pivoted.rename(columns={
    "IT.NET.USER.FE.ZS": "Internet users, female",
    "IT.NET.USER.MA.ZS": "Internet users, male",
    "NY.GDP.MKTP.KD.ZG": "GDP growth",
    "NY.GDP.PCAP.KD.ZG": "GDP per capita growth",
    "SE.ENR.SECO.FM.ZS": "Female/male secondary enrollment",
    "SE.ENR.TERT.FM.ZS": "Female/male tertiary enrollment",
    "SE.SEC.ENRR.FE": "Secondary school enrollment, female",
    "SE.TER.ENRR.FE": "Tertiary school enrollment, female",
    "SG.GEN.PARL.ZS": "Proportion parliament's female",
    "SL.AGR.EMPL.FE.ZS": "Female employment in agriculture",
    "SL.EMP.SMGT.FE.ZS": "Female employment in senior and managerial positions",
    "SL.EMP.WORK.FE.ZS": "Employment to population ratio, female",
    "SL.EMP.WORK.MA.ZS": "Employment to population ratio, male",
    "SL.TLF.CACT.FE.ZS": "Labor force participation rate, female",
    "SL.TLF.CACT.MA.ZS": "Labor force participation rate, male",
    "SL.UEM.NEET.FE.ZS": "NEET rate, female",
    "SL.UEM.NEET.MA.ZS": "NEET rate, male",
    "SL.UEM.TOTL.FE.ZS": "Unemployment rate, female",
    "SL.UEM.TOTL.MA.ZS": "Unemployment rate, male",
    "SP.ADO.TFRT": "Adolescent fertility rate (births per 1,000 women ages 15–19)",
    "SP.DYN.TFRT.IN": "Total fertility rate (births per woman)",
    }, inplace=True)

    return df_pivoted
