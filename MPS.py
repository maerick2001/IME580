# Import libraries
import streamlit as st
import pandas as pd
import numpy as np
import warnings

# Ignore warnings
warnings.filterwarnings('ignore')

# Title
st.title('Master Production Schedule')
st.divider()
st.subheader('Level Production Schedule')
st.subheader('Make to Stock')
# Read data
df_mps = pd.read_excel('MPS.xlsx')

def force_remove_decimals(df):
    for column in df.columns:
        # Check if the column contains numeric data by trying to convert to float
        if df[column].dtype in [float, int]:
            df[column] = df[column].apply(lambda x: str(x).split('.')[0] if pd.notnull(x) else x)
    return df

# Function to calculate projected available
def calculate_projected_available(df):
    projected_available = []
    prev_projected_available = start_inv  # Initialize with starting inventory for Week 1
    for index, row in df.iterrows():
        projected_available.append(prev_projected_available - row['Forecast'] + row['Production Plan'])
        prev_projected_available = projected_available[-1]  # Update for next iteration
    return projected_available

def calculate_atp(df, time_fence):
    df['ATP'] = 0
    for index, row in df.iterrows():
        if row['Production Plan'] > 0:
            if index + 1 <= time_fence:
                total_demand = row['Customer Orders']  # Use customer orders if before or on the time fence
            else:
                total_demand = max(row['Customer Orders'], row['Forecast'])  # Use the higher of customer orders or forecast if after the time fence
  
            for future_index in range(index + 1, len(df)):
                future_row = df.iloc[future_index]
                if future_row['Production Plan'] > 0:
                    break
                if future_index + 1 <= time_fence:  # Accumulate customer orders before the time fence
                    total_demand += future_row['Customer Orders']
                else:  # Compare and accumulate the maximum of customer orders or forecast after the time fence
                    total_demand += max(future_row['Customer Orders'], future_row['Forecast'])

            # Subtract the larger of the accumulated demand or forecast (after time fence) from the current production plan
            df.at[index, 'ATP'] = row['Production Plan'] - total_demand

    return df
#Function to decide production and calculate projected available
def calculate_production_and_available(df_summer, df_season, summer_starting_inv, season_starting_inv):
    summer_proj_available = summer_starting_inv
    season_proj_available = season_starting_inv
    

    for index, (row_summer, row_season) in enumerate(zip(df_summer.itertuples(), df_season.itertuples())):
        forecast_summer = row_summer.Forecast
        forecast_season = row_season.Forecast

        # Calculate potential projected available if no production
        potential_proj_available_summer = summer_proj_available - forecast_summer
        potential_proj_available_season = season_proj_available - forecast_season

        if potential_proj_available_summer < potential_proj_available_season:
            # Summer has a lower projected available, so produce for summer
            summer_production = lot_size
            season_production = 0
            summer_proj_available = potential_proj_available_summer + summer_production
            season_proj_available = potential_proj_available_season
        else:
            # Season has a lower or equal projected available, so produce for season
            summer_production = 0
            season_production = lot_size
            # should_reset_summer_atp = True
            # should_reset_season_atp = False if season_production == 0 else True
            summer_proj_available = potential_proj_available_summer
            season_proj_available = potential_proj_available_season + season_production
        # Append results to DataFrames
        df_summer.at[index, 'Production Plan'] = summer_production
        df_season.at[index, 'Production Plan'] = season_production
        df_summer.at[index, 'Projected Available'] = summer_proj_available
        df_season.at[index, 'Projected Available'] = season_proj_available
    
    return df_summer, df_season
        



# Form for user inputs
with st.form('user_inputs'):
    st.markdown('Choose a starting inventory and lot size.')
    start_inv = st.number_input("Starting Inventory", min_value=0, value=100)
    lot_size = st.number_input("Lot Size", min_value=50,value=100,step=50)
    time_fence = st.number_input("Time Fence", min_value=1, max_value=12, value=6)
    submitted = st.form_submit_button()

# Check if form submitted
if submitted:
    df_mps['Production Plan'] = lot_size
    # Add 'Projected Available' column to DataFrame
    df_mps['Projected Available'] = calculate_projected_available(df_mps)

    # Transpose DataFrame
    df_transposed = df_mps.T

    # Show transposed DataFrame
    st.header("Master Production Schedule")
    st.table(df_transposed)

# Check if form submitted
if submitted:
    # Calculate starting inventories for summer and season
    summer_starting_inv = start_inv * 0.25
    season_starting_inv = start_inv * 0.75

    # Read data for summer and season
    df_mps_summer = pd.read_excel('MPS_summer.xlsx')
    df_mps_season = pd.read_excel('MPS_season.xlsx')


    # Calculate Production and Projected Available
    calculate_production_and_available(df_mps_summer, df_mps_season, summer_starting_inv, season_starting_inv)
    df_mps_summer = calculate_atp(df_mps_summer, time_fence)
    df_mps_season = calculate_atp(df_mps_season, time_fence)


    # Transpose DataFrames
    df_summer_transposed = df_mps_summer.T
    df_season_transposed = df_mps_season.T

    df_summer_transposed = force_remove_decimals(df_summer_transposed)
    df_season_transposed = force_remove_decimals(df_season_transposed)

    # Show transposed DataFrames with integer formatting
    st.subheader("Large Summer Tent MPS")
    st.table(df_summer_transposed)

    st.subheader("3-Season Tent MPS")
    st.table(df_season_transposed)


