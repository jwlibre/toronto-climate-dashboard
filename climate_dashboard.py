import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(layout="wide")
st.title('Toronto Climate Dashboard')
st.subheader("""The SSP2-4.5 and SSP5-8.5 climate scenarios are part of the Shared Socioeconomic Pathways (SSPs) framework used in climate modeling. They describe different possible futures based on socioeconomic trends and greenhouse gas (GHG) emissions.""")

scenarios_table_dataframe = pd.DataFrame()

with open('data/scenarios.json', mode='r') as f:
    scenarios_table_data = json.load(f)

scenarios_table_data = pd.DataFrame.from_dict(scenarios_table_data["Scenarios"]).transpose()
scenarios_table_data = scenarios_table_data.rename(columns=scenarios_table_data.iloc[0]).drop(scenarios_table_data.index[0])
st.table(data = scenarios_table_data)

st.multiselect("Scenarios", ["SSP2-4.5", "SSP5-8.5"], key="scenarios", default="SSP2-4.5")


DATA_URL = ('https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/current-and-future-climate/resource/dcb799c6-8eb0-432d-8188-f3aeff5ddaf3/download/Climate%20Variables.csv')
TEMPERATURE_VARIABLES = [
    "ANNUAL_MEAN_TEMPERATURE",
    "WINTER_MEAN_TEMPERATURE",
    "SPRING_MEAN_TEMPERATURE",
    "SUMMER_MEAN_TEMPERATURE",
    "FALL_MEAN_TEMPERATURE",
    "ANNUAL_MAXIMUM_TEMPERATURE",
    "WINTER_MAXIMUM_TEMPERATURE",
    "SPRING_MAXIMUM_TEMPERATURE",
    "SUMMER_MAXIMUM_TEMPERATURE",
    "FALL_MAXIMUM_TEMPERATURE",
    "ANNUAL_MINIMUM_TEMPERATURE",
    "WINTER_MINIMUM_TEMPERATURE",
    "SPRING_MINIMUM_TEMPERATURE",
    "SUMMER_MINIMUM_TEMPERATURE",
    "FALL_MINIMUM_TEMPERATURE",
    "DAYS_ABOVE_35C",
    "DAYS_ABOVE_30C",
    "DAYS_ABOVE_25C",
    "DAYS_ABOVE_20C_TROPICAL_NIGHTS",
    "HOTTEST_DAY_TEMPERATURE",
    "TEMPERATURE_BASED_HEAT_WARNING_FREQUENCY",
    "MAXIMUM_CONSECUTIVE_TEMPERATURE_BASED_HEAT_WARNING_DAYS",
]
PRECIPITATION_VARIABLES = [
    "ANNUAL_TOTAL_PRECIPITATION",
    "WINTER_TOTAL_PRECIPITATION",
    "SPRING_TOTAL_PRECIPITATION",
    "SUMMER_TOTAL_PRECIPITATION",
    "FALL_TOTAL_PRECIPITATION",
    "MAXIMUM_1DAY_PRECIPITATION",
    "MAXIMUM_3DAY_PRECIPITATION",
    "SIMPLE_DAILY_INTENSITY_INDEX",
    "95TH_PERCENTILE_PRECIPITATION",
    "99TH_PERCENTILE_PRECIPITATION",
    "MAXIMUM_CONSECUTIVE_WET_DAYS",
    "ANNUAL_TOTAL_DRY_DAYS",
    "MAXIMUM_CONSECUTIVE_DRY_DAYS",
]

col1, col2 = st.columns(2)

def load_data():
    data = pd.read_csv(DATA_URL)
    data = data[data.Distribution != "OVERALL_TREND"]
    colname_mapping = {}
    for name in data.columns:
        colname_mapping[name] = name.replace(" ", "_")
    data = data.rename(columns=colname_mapping)
    return data


@st.fragment()
def create_timeseries_plot(variable_type):
    if len(st.session_state["scenarios"]) == 0:
        st.text("Select at least one scenario")
    else:
        # , show_percentiles: bool
        data_to_plot = pd.DataFrame()
        for scenario in st.session_state.scenarios:
            data_to_plot = pd.concat([data_to_plot, dataset[dataset.Climate_Scenario == scenario]])
            data_to_plot_median = data_to_plot[data_to_plot.Distribution == "MEDIAN"]
            data_to_plot_10 = data_to_plot[data_to_plot.Distribution == "10th_PERCENTILE"]
            data_to_plot_90 = data_to_plot[data_to_plot.Distribution == "90th_PERCENTILE"]
        if variable_type == "temperature":
            plot = px.line(data_to_plot_median, x="Time_Horizon", y=st.session_state["temperature_variable"], color="Climate_Scenario")
        elif variable_type == "precipitation":
            plot = px.line(data_to_plot_median, x="Time_Horizon", y=st.session_state["precipitation_variable"], color="Climate_Scenario")
        st.plotly_chart(plot)
        # graph = st.scatter_chart(data_to_plot_median, x="Time_Horizon", y="ANNUAL_MEAN_TEMPERATURE", color="Climate_Scenario")


dataset = load_data()




with col1:
    st.selectbox("Temperature Variable", TEMPERATURE_VARIABLES, key="temperature_variable")
    create_timeseries_plot("temperature")
with col2:
    st.selectbox("Precipitation Variable", PRECIPITATION_VARIABLES, key="precipitation_variable")
    create_timeseries_plot("precipitation")
    
    