import streamlit as st
from utils.movies import generate_stars, count_stars
from utils.constants import NOT_RATED, MOVIES_STATE, REVIEW_STATE
from utils.init import config_page

config_page()
st.title('Please Rate the following Movies:')

N_ROWS = 20
N_COLS = 5
RADIO_OPTIONS = [NOT_RATED] + [generate_stars(i) for i in range(1,5+1)]

def render(curr_reviews, movies):
    # Source: https://discuss.streamlit.io/t/table-of-media-pictures-or-audio/6925/2
    for i in range(N_ROWS):
        cols = st.columns(N_COLS)

        for j in range(N_COLS):
            col = cols[j]
            index = i*N_COLS + j
        
            col.text(movies['title'][index])
            col.image(
                movies['url'][index],
                use_container_width=True
            )

            id = str(movies['movie_id'][index])
            selected_option = col.radio(
                label='Please pick a Rating:',
                options = RADIO_OPTIONS,
                key = id,
                index = curr_reviews.get(id, 0)
            )

            if selected_option != NOT_RATED:
                st.session_state[REVIEW_STATE][id] = count_stars(selected_option)
            elif id in curr_reviews:
                del st.session_state[REVIEW_STATE][id]
        
        st.divider()

render(
    st.session_state[REVIEW_STATE],
    st.session_state[MOVIES_STATE]
)

columns = st.columns([1,10])
if columns[0].button('Return to Main', type='secondary'):
    st.switch_page('start.py')

if columns[-1].button('Submit List', type='primary'):
    st.switch_page('pages/3_result.py')
