import io
import pandas as pd
import altair as alt
import streamlit as st

from st_aggrid import GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode

df = pd.concat(pd.read_excel('NFAS Results.xlsx', sheet_name=None), ignore_index=True)

st.set_page_config(layout='wide')
st.sidebar.success('Select a page above.')

st.header("Data Exploration 🗺️")

st.markdown("To start this project, as with any project, some initial data exploration is needed.")

buffer = io.StringIO()
df.info(buf=buffer)
s = buffer.getvalue()

st.text(s)

st.markdown("""First df.info() was run on the data and this is shown above. It shows there are some null values in 
            3 columns - Day 1, Day 2 and 24s. Unfortunately due to the age of the data, this isn't surprising. While
            this does limit the data that can be looked at and analysed, it does not prevent the analysis from going 
            forward. It will limit the years that can be looked at for max/min scores etc. I will not be dropping the 
            rows with nulls in these columns as this would drop entire years of data..""")

st.write(df.describe())

st.markdown("""Next df.describe() was run on the data to ensure no columns have values that appear to be out of the 
            realm of acceptable. Ignoring the year and ranking (#) column as analysis on these give irrelevant 
            information for the most part, most columns appear to have values within normal limits.""")
