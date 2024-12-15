import streamlit as st
from utils.init import config_page
from utils.constants import MOVIES_STATE, REVIEW_STATE

config_page()

# Set the title of the app
st.title('Project 4: Streamlit App for CS 598 - PSL')
st.subheader('Movie Recommendation')

st.markdown("""
### Team

- Kelvin Chong (kvchong2)
- Byunggeun BK Park (bpark14)
- Ildar Nasirov (nasirov2)
            
### Description
This project allows the user to rate 100 films on a scale of 1 to 5 and 
receive a recommendation of 10 films based on the Item-Based Collaborative Filtering Recommender System.

Please click **Start** to start reviewing movies.
""")

st.write('')

columns = st.columns([1,10])
if columns[0].button('Start Review', type='primary'):
    st.switch_page('pages/2_review.py')

if columns[-1].button(
    'Reset System', 
    type='secondary', 
    disabled=len(st.session_state[REVIEW_STATE]) == 0
):
    del st.session_state[REVIEW_STATE]
