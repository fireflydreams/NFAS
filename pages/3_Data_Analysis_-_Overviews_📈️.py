import pandas as pd
import altair as alt
import streamlit as st

from st_aggrid import GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode


st.set_page_config(layout='wide')
st.sidebar.success('Select a page above.')

df = pd.concat(pd.read_excel('NFAS Results.xlsx', sheet_name=None), ignore_index=True)

st.header("Data Analysis 📈️")

st.markdown("Now onto the data analysis.")

st.markdown("""Initially I'm going to look at the rise and fall of bow styles/classes. Initially not all bow styles are
            available, as through the years that we have data for (2002-2023) may new styles have been added. Below is 
            a table showing how styles have grown:""")

styles_per_year = (df.groupby('Year')['Style'].nunique()).reset_index()
styles_per_year.loc[styles_per_year.Year == 2007, "New Styles"] = 'PV'
styles_per_year.loc[styles_per_year.Year == 2018, "New Styles"] = 'TB'
styles_per_year.loc[styles_per_year.Year == 2022, "New Styles"] = 'TD'
styles_per_year.loc[styles_per_year.Year == 2023, "New Styles"] = 'TXB'
styles_per_year = styles_per_year.astype(str)

gb = GridOptionsBuilder.from_dataframe(styles_per_year)
gb.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=10)
gb.configure_side_bar()
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
gridOptions1 = gb.build()
st.caption('Number of Styles per year')
AgGrid(styles_per_year, gridOptions=gridOptions1, columns_auto_size_mode=ColumnsAutoSizeMode.NO_AUTOSIZE,
       allow_unsafe_jscode=Truee)

st.markdown("""This may not be accurate, however I have made the assumption that the first year a style appears in the 
            results is the year it was added.""")

st.markdown("""Champs attendance. Please remember, this is adults only. It does include NC and retires.""")

attendance = df.groupby(['Year', 'Champs']).size().reset_index(name='count')

st.subheader('Attendance by Year')
chart = (
    alt.Chart(attendance).mark_line(point=True).encode(
        x=alt.X('Year:N'),
        y=alt.Y('count', title='Entrants'),
        color=alt.Color('Champs'),
    )
)
st.altair_chart(chart, use_container_width=True)

st.markdown("""Looking at the above it is fairly obvious that the 3Ds has gained in popularity massively over the years,
            conversely the Nationals has declined. The Nationals and 3Ds popularity swapped in 2008. Prior to that the
            Nationals was the bigger competition, however 2008 and later, the 3Ds became the more subscribed 
            competition.""")

clubs = df.groupby(['Year', 'Champs'])['Club'].nunique().reset_index()

st.subheader('Club Representation')
chart = (
    alt.Chart(clubs).mark_line(point=True).encode(
        x=alt.X('Year:N'),
        y=alt.Y('Club', title='Clubs'),
        color=alt.Color('Champs'),
    )
)
st.altair_chart(chart, use_container_width=True)
