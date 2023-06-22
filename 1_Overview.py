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
            all under x age classes) have been removed. This i due to the wildly varying results that were seen on 
            these, and the under subscription to them.""")
