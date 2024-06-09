# Import libraries
import streamlit as st
import pandas as pd
import numpy as np
import warnings

# Ignore warnings
warnings.filterwarnings('ignore')

# Title
st.title('Bill of Materials')
st.divider()
st.header('3-Season Tent')
st.divider()
st.subheader('Indented')
df = pd.read_excel("BOM_season.xlsx", na_filter=True)
# Replace NaN values with an empty string for display purposes
df = df.fillna('')
df['Quantity'] = df['Quantity'].round(1)

# Display the data
df.set_index('Part Number', inplace=True)
formatted_df = df.applymap(lambda x: f'{x:.1f}' if isinstance(x, float) else x)
# Display the formatted DataFrame
st.table(formatted_df)
st.divider()
st.subheader('Single-Level')
st.image('BOM_single_season.png')
st.divider()
st.subheader('Multi-Level')
st.image('BOM_multi_season.png')
st.divider()
st.header('Large Summer Tent')
st.divider()
st.subheader('Indented')
df = pd.read_excel("BOM_summer.xlsx", na_filter=True)
# Replace NaN values with an empty string for display purposes
df = df.fillna('')
df['Quantity'] = df['Quantity'].round(1)

# Display the data
df.set_index('Part Number', inplace=True)
formatted_df = df.applymap(lambda x: f'{x:.1f}' if isinstance(x, float) else x)
# Display the formatted DataFrame
st.table(formatted_df)
st.divider()
st.subheader('Single-Level')
st.image('BOM_single_sum.png')
st.divider()
st.subheader('Muti-Level')
st.image('BOM_multi_sum.png')




