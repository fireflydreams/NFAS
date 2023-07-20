import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout='wide',
)

st.sidebar.success('Select a page above.')

st.write("# Welcome to my National Field Archery Society (NFAS) champs analysis! 👋")

st.markdown("""For the past 8 years I have been doing field archery after being introduced to it by friends. I started
            competing locally, before progressing to national competitions (the 3Ds and the National Champs.) Having
            found there is a lot of data on the society site showing the history of the results, I decided to 
            investigate the history of the scores and look for any trends.""")

st.markdown("""Before we dive into the data, a quick preface to this. Anyone not classed as adult (Juniors, Cubs, and 
            all under x age classes) have been removed. This is due to the wildly varying results that were seen on 
            these, and the under subscription to them.""")

st.markdown("""The questions that I posed to the data are:
Overview
- How have styles evolved over the years?
- What has attendance looked like at both the 3D Champs and the Nationals?
- How many clubs are typically represented at each event?

Breakowns
- How has the popularity of classes & styles changed over the years?
- How has the popularity of Compounds vs Traditional bows changed over the years?
- How has the popularity of Instinctive vs Sighted changed over the years?""")
