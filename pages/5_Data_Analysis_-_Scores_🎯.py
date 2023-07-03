import numpy as np
import pandas as pd
import altair as alt
import streamlit as st

st.set_page_config(layout='wide')
st.sidebar.success('Select a page above.')

st.sidebar.divider()

styles = ['All', 'AFB', 'BB', 'BH', 'CL', 'FS', 'HT', 'LB', 'PV', 'TB', 'TD', 'TXB', 'UL', 'XB']

classes = ['All', 'M', 'F']

bow = ['All', 'Traditional', 'Compound']

instinct = ['All', 'Instinctive', 'Sighted']

champs = ['All', '3Ds', 'Nationals']

option = st.sidebar.multiselect("Choose style(s)", styles, default=['All'])

gender = st.sidebar.multiselect("Choose class(es)", classes, default=['All'])

trad = st.sidebar.multiselect("Choose Traditional or Compound", bow, default=['All'])

sight = st.sidebar.multiselect("Choose Instinctive or Sighted", instinct, default=['All'])

championship = st.sidebar.multiselect("Choose which Champs", champs, default=['All'])

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

st.header("Data Analysis - Scores 🎯")

st.markdown("""Now the part we've possibly all been looking forward to, score trending! Time to look at max scores, 
            average per target, average kills per style, and possibly other interesting facts.""")

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
elif not championship:
    st.error("Please select at least one of Champs or All.")
elif 'All' in championship and len(championship) > 1:
    st.error("Please select All, or  individuals champs, not both.")
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
        for i in gender:
            filtered = selected[selected["Class"] == i]
            selected_1 = pd.concat([selected_1, filtered])

    selected_2 = pd.DataFrame()
    if trad[0] == 'All':
        selected_2 = selected_1.copy()
    else:
        for i in trad:
            filtered = selected_1[selected_1["Type"] == i]
            selected_2 = pd.concat([selected_2, filtered])

    selected_3 = pd.DataFrame()
    if sight[0] == 'All':
        selected_3 = selected_2.copy()
    else:
        for i in sight:
            filtered = selected_2[selected_2["Instinct"] == i]
            selected_3 = pd.concat([selected_3, filtered])

    final = pd.DataFrame()
    if championship[0] == 'All':
        final = selected_3.copy()
    else:
        for i in championship:
            filtered = selected_2[selected_2["Champs"] == i]
            final = pd.concat([final, filtered])

    max_scores = final[final["#"] == 1].copy()
    max_scores['combined'] = max_scores['Champs'] + ' ' + max_scores['Style'] + ' ' + max_scores['Class']

    st.subheader('Class and Style Max Scores')
    st.markdown("""The below chart is very confusing to look at unless you filter it with filters to the left 👈. It is
                best viewed either with one or two styles, or a single class. This is to look at change over the years. 
                The problem with this view is the courses are never the same. Not laid by the same people, in the same
                location etc so scores do fluctuate a fair amount. Also due to location, lifestyle etc the people
                attending every year changes, so peaks and troughs can be due to various competitors turning up/not 
                turning up.""")

    chart = (
        alt.Chart(max_scores).mark_line(point=True).encode(
            x=alt.X('Year:N'),
            y=alt.Y('Total', title='Max Score'),
            color=alt.Color('combined'),
        )
    )
    st.altair_chart(chart, use_container_width=True)

    average_scores = final[((final['#'] == 1) | (final['#'] == 2) | (final['#'] == 3))].copy()
    # st.table(average_scores)
    average_scores['combined'] = average_scores['Champs'] + ' ' + average_scores['Style'] + ' ' + average_scores[
        'Class']
    average_scores = average_scores.groupby(['Year', 'combined'])['Total'].mean().reset_index()
    # st.table(average_scores)
    average_scores['target_average'] = average_scores['Total'] / 80

    st.header('Average Scores/Target by Medalists')

    chart = (
        alt.Chart(average_scores).mark_line(point=True).encode(
            x=alt.X('Year:N'),
            y=alt.Y('target_average', title='Average Per Target'),
            color=alt.Color('combined'),
        )
    )
    st.altair_chart(chart, use_container_width=True)

    st.markdown("""For the most part this does mimic the max scores above, however this is an interesting one to look at
                as it incorporates (where possible) results for Gold, Silver and Bronze, mean averages them, then works
                out the average score by target. It gives people an idea of current targets to be aiming for if hoping
                to place in the medals of their category.""")

st.markdown("""Now that an initial look at scores and averages has been done, the first thing I'd like to look at is: 
            is there (for want of a better term) power creep becoming evident in any classes and styles? To do this, 
            I'm going to take the results from 2002 (or the first time the class and style appears) and 2023 and compare
            the max scores from each champs type (split as there does always seem to be a variance in score on 3Ds 
            verses paper faces) split by style and class.""")

top_scores = df[df['#'] == 1].copy()
max_scores_2002 = top_scores[top_scores['Year'] == 2002].copy()
max_scores_2023 = top_scores[((top_scores['Year'] == 2023) & (top_scores['Champs'] == '3Ds')) |
                             ((top_scores['Year'] == 2022) & (top_scores['Champs'] == 'Nationals'))].copy()

late_adds = top_scores[((top_scores['Year'] == 2007) & (top_scores['Style'] == 'PV'))].copy()
late_adds_1 = top_scores[((top_scores['Year'] == 2022) & (top_scores['Style'] == 'TD'))].copy()
late_adds_2 = top_scores[((top_scores['Year'] == 2023) & (top_scores['Style'] == 'TXB'))].copy()
late_adds_3 = top_scores[((top_scores['Year'] == 2018) & (top_scores['Style'] == 'TB'))].copy()
late_adds_4 = top_scores[((top_scores['Year'] == 2019) & (top_scores['Style'] == 'TB') & (top_scores['Class'] == 'F') &
                          (top_scores['Champs'] == '3Ds'))].copy()
late_adds_5 = top_scores[((top_scores['Year'] == 2003) & (top_scores['Style'] == 'XB')
                          & (top_scores['Class'] == 'F'))].copy()

top_max_scores = pd.concat([max_scores_2002, max_scores_2023, late_adds, late_adds_1, late_adds_2, late_adds_3,
                            late_adds_4, late_adds_5])

top_max_scores['combined'] = top_max_scores['Style'] + ' ' + top_max_scores['Class'] + ' ' + top_max_scores['Champs']

domain = ['2000', '2025']
colors = ['skyblue', 'mediumorchid']

st.header('Score Change, First recorded -> 2023')

lines = alt.Chart(top_max_scores).mark_line(point=True).encode(
    x='Total',
    y='combined',
    detail='combined',
    color=alt.value('lightskyblue'),
)

points = alt.Chart(top_max_scores).mark_circle(size=100).encode(
    x=alt.X('Total', title='Max Score'),
    y=alt.Y('combined', title='Style/Class/Champs'),
    color=alt.Color('Year', scale=alt.Scale(domain=domain, range=colors))
)

st.altair_chart(lines + points, use_container_width=True)

st.markdown("""Looking at the above graph, it is clear that scores are creeping up... although in some categories, not 
            so much creeping as jumping! There's very few class/style combos where the score hasn't jumped up. The ones
            to note that haven't changed much:""")
st.markdown("""
- 3Ds Female Compound Limited
- 3Ds Female Compound Unlimited
- Nationals Male Traditional Bowhunter""")
st.markdown("""No commentary can be made on:
- Nationals Male Thumbdraw
- 3Ds Traditional Crossbow""")
st.markdown("""As both of these have only had one set of results released.""")
st.markdown("""So are courses getting easier, or are archers at the top of their style continually getting better? Is 
            technology in bows and bow making improving? The same for arrows and arrow making? Are arrows being sold
            with less tolerance, so more consistency across sets? Is it all of the above? I'll leave you to decide that 
            one for yourselves.""")


box_and_whisker = df.copy()
box_and_whisker['combined'] = box_and_whisker['Style'] + ' ' + \
                              box_and_whisker['Class'] + ' ' + box_and_whisker['Champs']

box_and_whisker = box_and_whisker.dropna(subset=['Day 1', 'Day 2'])
box_and_whisker = box_and_whisker[box_and_whisker['Day 1'] != 0]
box_and_whisker = box_and_whisker[box_and_whisker['Day 2'] != 0]
box_and_whisker = box_and_whisker[box_and_whisker['Day 1'] >= 160]
box_and_whisker = box_and_whisker[box_and_whisker['Day 2'] >= 160]
box_and_whisker = box_and_whisker[box_and_whisker['Total'] >= 320]

st.header("Outlier Results")

st.markdown("""*A box plot (or boxplot) is a method for graphically demonstrating the locality, spread and skewness 
            groups of numerical data through their quartiles. In addition to the box on a box plot, there can be lines 
            (which are called whiskers) extending from the box indicating variability outside the upper and lower 
            quartiles (25% - 75%), thus, the plot is also called the box-and-whisker plot. Outliers that differ 
            significantly from the rest of the dataset may be plotted as individual points beyond the whiskers on the
            box-plot.*""")
st.markdown("""For the below, I advise reviewing the data for individual years. There's so much variation across the 
            full data that there becomes a very large number of outliers.""")
year = st.selectbox(
        "Which year?",
        ("2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015",
         "2016", "2017", "2018", "2019", "2021", "2022", "2023")
)

box_and_whisker = box_and_whisker.astype(str)
box_and_whisker = box_and_whisker[box_and_whisker['Year'] == year]

chart = (
    alt.Chart(box_and_whisker).mark_boxplot(extent=0.5, outliers={'size': 5}).encode(
        x=alt.X('combined', title='Style/Class/Champs', axis=alt.Axis(labels=True, ticks=False),
                scale=alt.Scale(padding=1)),
        y='Total:Q',
        color=alt.Color('combined', legend=None)
    )
    .properties(height=500)
)

st.altair_chart(chart, use_container_width=True)




