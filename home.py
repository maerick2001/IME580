# Import libraries
import streamlit as st
import pandas as pd
import numpy as np
from st_pages import Page, show_pages
import warnings
warnings.filterwarnings('ignore')


show_pages(
    [
        Page("home.py", "Home", "🏠"),
        Page("MPS.py", "MPS", "📆"),
        Page("MRP.py", "MRP", "🧮"),
        Page("BOM.py", "BOM", "🔩"),
    ]
)

st.title('Application for Tent Manufacturing') 
st.divider()
st.markdown('Click on the tabs on the left-side to view MPS, MRP, and BOMs.')
st.divider()
st.subheader('Large Summer Tent')
st.image('large_summer.jpg', width = 700)
st.subheader('3-Season Tent')
st.image('season_tent.png', width = 700)
#