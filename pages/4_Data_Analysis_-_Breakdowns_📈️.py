import numpy as np
import pandas as pd
import altair as alt
import streamlit as st

from st_aggrid import GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode

st.set_page_config(layout='wide')
st.sidebar.success('Select a page above.')

st.sidebar.divider()

styles = ['All', 'AFB', 'BB', 'BH', 'CL', 'FS', 'HT', 'LB', 'PV', 'TB', 'TD', 'TXB', 'UL', 'XB']

classes = ['All', 'M', 'F']

bow = ['All', 'Traditional', 'Compound']

instinct = ['All', 'Instinctive', 'Sighted']

option = st.sidebar.multiselect("Choose style(s)", styles, default=['All'])

gender = st.sidebar.multiselect("Choose class(es)", classes, default=['All'])

trad = st.sidebar.multiselect("Choose Traditional or Compound", bow, default=['All'])

sight = st.sidebar.multiselect("Choose Instinctive or Sighted", instinct, default=['All'])


df = pd.concat(pd.read_excel('NFAS Results.xlsx', sheet_name=None), ignore_index=True)

conditions = [
    (df['Style'] == 'AFB'),
    (df['Style'] == 'BB'),
    (df['Style'] == 'BH'),
    (df['Style'] == 'CL'),
    (df['Style'] == 'FS'),
    (df['Style'] == 'HT'),
    (df['Style'] == 'LB'),
    (df['Style'] == 'PV'),
    (df['Style'] == 'TB'),
    (df['Style'] == 'TD'),
    (df['Style'] == 'TXB'),
    (df['Style'] == 'UL'),
    (df['Style'] == 'XB')
]

values = ['Traditional', 'Traditional', 'Compound', 'Compound', 'Traditional', 'Traditional', 'Traditional',
          'Traditional', 'Traditional', 'Traditional', 'Traditional', 'Compound', 'Traditional']

df['Type'] = np.select(conditions, values)

conditions = [
    (df['Style'] == 'AFB'),
    (df['Style'] == 'BB'),
    (df['Style'] == 'BH'),
    (df['Style'] == 'CL'),
    (df['Style'] == 'FS'),
    (df['Style'] == 'HT'),
    (df['Style'] == 'LB'),
    (df['Style'] == 'PV'),
    (df['Style'] == 'TB'),
    (df['Style'] == 'TD'),
    (df['Style'] == 'TXB'),
    (df['Style'] == 'UL'),
    (df['Style'] == 'XB')
]

values = ['Instinctive', 'Instinctive', 'Instinctive', 'Sighted', 'Sighted', 'Instinctive', 'Instinctive',
          'Instinctive', 'Instinctive', 'Instinctive', 'Instinctive', 'Sighted', 'Sighted']

df['Instinct'] = np.select(conditions, values)

st.header("Data Analysis 📈️")

if not option:
    st.error("Please select at least one bow style, or All.")
elif 'All' in option and len(option) > 1:
    st.error("Please select All, or bow styles, not both.")
elif not gender:
    st.error("Please select at least one class, or All.")
elif 'All' in gender and len(gender) > 1:
    st.error("Please select All, or bow classes, not both.")
elif not trad:
    st.error("Please select at least one of Traditional, Sighted or All.")
elif 'All' in trad and len(trad) > 1:
    st.error("Please select All, or Traditional/Sighted, not both.")
elif not sight:
    st.error("Please select at least one of Instinctive, Sighted or All.")
elif 'All' in sight and len(sight) > 1:
    st.error("Please select All, or Instinctive/Sighted, not both.")
else:
    selected = pd.DataFrame()
    if option[0] == 'All':
        selected = df.copy()
    else:
        for i in option:
            filtered = df[df["Style"] == i]
            selected = pd.concat([selected, filtered])

    selected_1 = pd.DataFrame()
    if gender[0] == 'All':
        selected_1 = selected.copy()
    else:
        for i in sight:
            filtered = selected[selected["Class"] == i]
            selected_1 = pd.concat([selected_1, filtered])

    selected_2 = pd.DataFrame()
    if trad[0] == 'All':
        selected_2 = selected_1.copy()
    else:
        for i in trad:
            filtered = selected_1[selected_1["Type"] == i]
            selected_2 = pd.concat([selected_2, filtered])

    final = pd.DataFrame()
    if sight[0] == 'All':
        final = selected_2.copy()
    else:
        for i in sight:
            filtered = selected_2[selected_2["Instinct"] == i]
            final = pd.concat([final, filtered])

    class_counts = final.groupby(['Year', 'Style', 'Class']).size().reset_index(name='count')
    class_counts['combined'] = class_counts['Style'] + ' ' + class_counts['Class']

    st.subheader('Class and Style Popularity')
    st.markdown("""The below chart is very confusing to look at unless you filter it with filters to the left 👈. It is
                best viewed either with one or two styles, or a single class.""")
    chart = (
        alt.Chart(class_counts).mark_line(point=True).encode(
            x=alt.X('Year:N'),
            y=alt.Y('count', title='Entrants'),
            color=alt.Color('combined'),
        )
    )
    st.altair_chart(chart, use_container_width=True)

    st.markdown("""I could go into detail about each style and class, and it's increase or decrease in popularity, however 
                this can easily be seen by filtering the above for yourself. """)

st.markdown("""A couple of generalizations can be pulled from the data however:
- Once a class is announced it typically sees a spike in popularity the year after it is added, with a steady increase 
to a plateau a few years later.
- Overall attendance is dropping at each champs type. COVID certainly seems to have impacted this more, as 2021 and 2022
champs had very large drops in attendance. Cost of living could also factor into this, with less people choosing to 
travel to one or more champs.""")

st.markdown("""2023 has seen a surge in attendance, however there is only one champs this year. This will have had an 
            effect on the attendance. Until further years can be seen, it is hard to qualify whether this is an anomaly
            or a trend. Further information will become available as more years of champs (either single or double) are
            available.""")

df_traditional = df[['Year', 'Type', 'Archer']].copy()
df_traditional = df_traditional.groupby(['Year', 'Type']).nunique().reset_index()

df_attendance = df[['Year', 'Archer']].copy()
df_attendance = df_attendance.groupby(['Year']).nunique().reset_index()

df_traditional = df_traditional.merge(df_attendance, on='Year', how='left')
df_traditional['percent_attendance'] = (df_traditional['Archer_x']/df_traditional['Archer_y'])*100

st.header("Percent attendance Compound vs Traditional")
chart = (
    alt.Chart(df_traditional).mark_line(point=True).encode(
        x=alt.X('Year:N'),
        y=alt.Y('percent_attendance', title='Entrants'),
        color=alt.Color('Type'),
    )
)
st.altair_chart(chart, use_container_width=True)

st.markdown("""Now having a look at the """)

df_sight = df[['Year', 'Instinct', 'Archer']].copy()

df_sight = df_sight.groupby(['Year', 'Instinct']).nunique().reset_index()
df_sight = df_sight.merge(df_attendance, on='Year', how='left')
df_sight['percent_attendance'] = (df_sight['Archer_x']/df_sight['Archer_y'])*100

chart = (
    alt.Chart(df_sight).mark_line(point=True).encode(
        x=alt.X('Year:N'),
        y=alt.Y('percent_attendance', title='Entrants'),
        color=alt.Color('Instinct'),
    )
)
st.altair_chart(chart, use_container_width=True)
