import streamlit as st
from utils.ibcf import myIBCF, parse_recomendations
from utils.init import config_page
from utils.constants import MOVIES_STATE, REVIEW_STATE

config_page(init_cache=False)

st.title('List of Recommended Movies:')

N_ROWS = 2
N_COLS = 5

def render(reviews, movies):
    recommendations = parse_recomendations(myIBCF(reviews))

    for i in range(N_ROWS): # number of rows
        cols = st.columns(N_COLS) # number of columns in each row

        for j in range(N_COLS):
            col = cols[j]
            index = i*N_COLS + j
            movie_id = recommendations[index]
            recommendation = movies[movies['movie_id'] == movie_id]

            col.text(recommendation.at[recommendation.index[0], 'title'])
            col.image(
                recommendation.at[recommendation.index[0], 'url'],
                caption=f"Rank: {index+1}",
                use_container_width=True
            )
        
        st.divider()

if REVIEW_STATE in st.session_state and MOVIES_STATE in st.session_state:
    render(
        st.session_state[REVIEW_STATE],
        st.session_state[MOVIES_STATE]
    )
else:
    st.markdown("""
        Please provide your movie recommendations on the Reviews page
    """)

if st.button('Return to Reviews', type='secondary'):
    st.switch_page("pages/2_review.py")
