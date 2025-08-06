import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import streamlit as st
import chartDiscription as cd

from dataLoading import cleaned_data  # Make sure this returns your cleaned DataFrame


def create_lag_features(df, target='gdp_growth', lags=3):
    for lag in range(1, lags + 1):
        df[f'{target}_lag{lag}'] = df[target].shift(lag)
    df['year_idx'] = df['Year'] - df['Year'].min()
    return df


def hybrid_forecast_plotly(df, country_name, forecast_horizon=10, show_legend=True):
    target = 'gdp_growth'
    country_df = df[df["Country"] == country_name].copy()
    country_df = country_df.drop(columns=["Country", "gdp_per_capita_growth"], errors="ignore")
    country_df = create_lag_features(country_df).dropna().reset_index(drop=True)

    train = country_df.iloc[:-forecast_horizon]
    test = country_df.iloc[-forecast_horizon:]
    feature_cols = [col for col in country_df.columns if 'lag' in col or col == 'year_idx']
    X_train, y_train = train[feature_cols], train[target]
    X_test, y_test = test[feature_cols], test[target]

    # XGBoost
    xgb = XGBRegressor(n_estimators=200, max_depth=3, learning_rate=0.1, random_state=42)
    xgb.fit(X_train, y_train)
    full_preds_xgb = xgb.predict(country_df[feature_cols])

    # ARIMA
    best_model = None
    best_aic = np.inf
    for p in [0, 1, 2]:
        for d in [0, 1]:
            for q in [0, 1, 2]:
                try:
                    model = ARIMA(train[target], order=(p, d, q))
                    res = model.fit()
                    if res.aic < best_aic:
                        best_model = res
                        best_aic = res.aic
                except:
                    continue

    arima_preds = best_model.forecast(len(country_df) - len(train))
    arima_full_preds = np.concatenate([best_model.fittedvalues, arima_preds])
    ensemble_preds = 0.6 * full_preds_xgb + 0.4 * arima_full_preds

    # Confidence Interval
    residuals = train[target] - best_model.fittedvalues
    std_resid = residuals.std()
    upper_ci = ensemble_preds + 1.96 * std_resid
    lower_ci = ensemble_preds - 1.96 * std_resid

    # Forecast Future
    full_df = country_df.copy()
    forecast_vals = list(ensemble_preds)

    for _ in range(forecast_horizon):
        year = full_df['Year'].max() + 1
        new_row = {'Year': year}
        for lag in range(1, 4):
            new_row[f'{target}_lag{lag}'] = full_df.iloc[-lag][target]
        new_row['year_idx'] = year - df['Year'].min()
        X_future = pd.DataFrame([new_row])[feature_cols]

        xgb_future = xgb.predict(X_future)[0]
        arima_future = best_model.forecast(1).iloc[0]
        hybrid_future = 0.6 * xgb_future + 0.4 * arima_future

        new_row[target] = hybrid_future
        full_df = pd.concat([full_df, pd.DataFrame([new_row])], ignore_index=True)
        forecast_vals.append(hybrid_future)
        upper_ci = np.append(upper_ci, hybrid_future + 1.96 * std_resid)
        lower_ci = np.append(lower_ci, hybrid_future - 1.96 * std_resid)

    # Trend Line
    trend_df = full_df[full_df['Year'] >= 1995]
    z = np.polyfit(trend_df['Year'], trend_df[target], 1)
    trend_line = np.polyval(z, full_df['Year'])

    # Plotly Traces
    traces = []

    traces.append(go.Scatter(
        x=country_df['Year'],
        y=country_df[target],
        name="Actual",
        mode='lines+markers',
        line=dict(color='white', width=2),
        marker=dict(symbol='circle', size=6),
        showlegend=show_legend
    ))

    traces.append(go.Scatter(
        x=full_df['Year'],
        y=forecast_vals,
        name="Forecast",
        mode='lines+markers',
        line=dict(color='crimson', width=3),
        marker=dict(symbol='circle', size=6),
        showlegend=show_legend
    ))

    traces.append(go.Scatter(
        x=full_df['Year'], y=upper_ci,
        line=dict(width=0),
        showlegend=False
    ))

    traces.append(go.Scatter(
        x=full_df['Year'], y=lower_ci,
        name="95% Confidence Interval",
        fill='tonexty',
        fillcolor='rgba(100,149,237,0.3)',
        line=dict(width=0),
        mode='lines',
        hoverinfo='skip',
        showlegend=show_legend
    ))

    traces.append(go.Scatter(
        x=full_df['Year'],
        y=trend_line,
        name="Trend Line",
        line=dict(color='green', width=2, dash='dash'),
        mode='lines',
        showlegend=show_legend
    ))

    return traces, y_test, ensemble_preds[-forecast_horizon:], residuals, forecast_vals, full_df, upper_ci, lower_ci

@st.cache_resource
def render():
    df = cleaned_data()
    df.columns = df.columns.str.strip()

# <----------------- Radio buttons to toogle between graphs ----------------------->
    st.sidebar.subheader("Data Visualization")
    chart_type = st.sidebar.radio(
        "Choose a chart to visualize:",
        [
            "Forcasting Model",
            "Error Metrics Table"
        ]
    )

    # Get forecasting results for India (used in all diagnostic plots)
    #india_traces, y_test, test_preds, residuals, forecast_vals, full_df, upper_ci, lower_ci = hybrid_forecast_plotly(df, "India", forecast_horizon=5, show_legend=True)
    india_traces, _, _, _, _, _, _, _ = hybrid_forecast_plotly(df, "India", forecast_horizon=5, show_legend=True)

# <--------------------- Graphs render with Radio Button ----------------------->
    if chart_type == "Forcasting Model":
        germany_traces, *_ = hybrid_forecast_plotly(df, "Germany", forecast_horizon=5, show_legend=False)

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                            subplot_titles=["India", "Germany"])

        for trace in india_traces:
            fig.add_trace(trace, row=1, col=1)
        for trace in germany_traces:
            fig.add_trace(trace, row=2, col=1)

        for row in [1, 2]:
            fig.add_vline(
                x=2020,
                line=dict(color='red', dash='dash', width=2),
                annotation_text="COVID-19 Impact",
                annotation_position="top right",
                annotation_font=dict(color='red'),
                row=row, col=1
            )

        fig.update_layout(
            height=600,
            title="GDP Growth Forecasts (India & Germany) with 95% Confidence Intervals",
            showlegend=True,
            template="plotly_white",
            hovermode="x unified",
            legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center"),
            margin=dict(l=60, r=60, t=80, b=150)
        )
        fig.update_yaxes(title_text="GDP Growth (%)", row=1, col=1)
        fig.update_yaxes(title_text="GDP Growth (%)", row=2, col=1)
        fig.update_xaxes(title_text="Year", tickmode='linear', tick0=1995, dtick=5,
                         tickformat='.0f', row=2, col=1)

        st.plotly_chart(fig, use_container_width=True)
        cd.forcasting_description()

    elif chart_type == "Error Metrics Table":
        st.markdown("### Error Metrics for India and Germany")

        # Forecast + Metrics for India
        _, y_test_india, preds_india, _, _, _, _, _ = hybrid_forecast_plotly(df, "India", forecast_horizon=5)
        rmse_india = np.sqrt(mean_squared_error(y_test_india, preds_india))
        mae_india = mean_absolute_error(y_test_india, preds_india)

        # Forecast + Metrics for Germany
        _, y_test_ger, preds_ger, _, _, _, _, _ = hybrid_forecast_plotly(df, "Germany", forecast_horizon=5)
        rmse_ger = np.sqrt(mean_squared_error(y_test_ger, preds_ger))
        mae_ger = mean_absolute_error(y_test_ger, preds_ger)

        # Metrics DataFrame
        metrics_df = pd.DataFrame({
            "Country": ["India", "Germany"],
            "RMSE": [rmse_india, rmse_ger],
            "MAE": [mae_india, mae_ger]
        })

        st.dataframe(metrics_df.set_index("Country").round(3))

        # Plotly Interactive Bar Chart
        import plotly.graph_objs as go

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=metrics_df["Country"],
            y=metrics_df["RMSE"],
            name='RMSE',
            marker_color='skyblue',
            text=[f"{val:.2f}" for val in metrics_df["RMSE"]],
            textposition='outside'
        ))

        fig.add_trace(go.Bar(
            x=metrics_df["Country"],
            y=metrics_df["MAE"],
            name='MAE',
            marker_color='lightcoral',
            text=[f"{val:.2f}" for val in metrics_df["MAE"]],
            textposition='outside'
        ))

        fig.update_layout(
            height=400,
            barmode='group',
            title="RMSE & MAE for India and Germany",
            xaxis_title="Country",
            yaxis_title="Error Value",
            template='plotly_dark',
            legend=dict(orientation="h", y=-0.2, x=0.5, xanchor='center'),
            margin=dict(l=60, r=60, t=60, b=80)
        )

        st.plotly_chart(fig, use_container_width=True)
        cd.error_matrix_table_description()

