import streamlit as st
import pandas as pd 
import numpy as np
import time
from PIL import Image
import requests
from bs4 import BeautifulSoup as bs
from fuzzywuzzy import process
# Define a function to be triggered on button click

url = "https://fbref.com/en/squads/c7a9f859/2023-2024/matchlogs/c20/schedule/Bayer-Leverkusen-Scores-and-Fixtures-Bundesliga"
r = requests.get(url)
soup = bs(r.content)
league_table = soup.find_all("table", id="matchlogs_for")
league_table = pd.read_html(str(league_table))[0]
league_table = league_table[['Date', 'Venue', 'Result', 'GF', 'GA', 'Opponent', 'xG', 'xGA', 'Poss', 'Attendance', 'Formation', 'Opp Formation']]

st.set_page_config(page_title="Bayer Leverkusen Passing Data", page_icon="📈")
#st.markdown("# Bundeslig Season 23/24")
st.header("Bayer Leverkusen Passing Data")
def click_button():
    st.session_state.clicked = True

# Check if 'clicked' exists in session state, if not, initialize it
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

# Button in the main content area
st.button('Generate Map', on_click=click_button)

# Inputs inside the sidebar
with st.sidebar:
    on = st.toggle("For individual minute")
    if on:
        st.write("Choose Bayern Leverkusen's Opponent")
        opponent = st.selectbox('Select Opponent', ['Augsburg', 
                                                    'Bayern-Munich', 
                                                    'Bochum', 
                                                    'Borussia-Dortmund', 
                                                    'Borussia-Monchengladbach',
                                                    'Darmstadt-98',
                                                    'Eintracht-Frankfurt',
                                                    'FC-Heidenheim',
                                                    'FC-Köln',
                                                    'Freiburg',
                                                    'FSV-Mainz05',
                                                    'Hoffenheim',
                                                    'RB-Leipzig',
                                                    'Union-Berlin',
                                                    'VfB-Stuttgart',
                                                    'Werder-Bremen',
                                                    'Wolfsburg']) 
        home_away = st.selectbox('Home or Away?', ['Home', 'Away'])
        minute = st.text_input("Select Minute", placeholder="0")
        minute = str(minute)
    else:
        st.write("Choose Bayern Leverkusen's Opponent")
        opponent = st.selectbox('Select Opponent', ['Augsburg', 
                                                    'Bayern-Munich', 
                                                    'Bochum', 
                                                    'Borussia-Dortmund', 
                                                    'Borussia-Monchengladbach',
                                                    'Darmstadt-98',
                                                    'Eintracht-Frankfurt',
                                                    'FC-Heidenheim',
                                                    'FC-Köln',
                                                    'Freiburg',
                                                    'FSV-Mainz05',
                                                    'Hoffenheim',
                                                    'RB-Leipzig',
                                                    'Union-Berlin',
                                                    'VfB-Stuttgart',
                                                    'Werder-Bremen',
                                                    'Wolfsburg'])  
        home_away = st.selectbox('Home or Away?', ['Home', 'Away'])
# Validate and format the minute input
home_away = home_away.capitalize()
actual_names = ['Augsburg',
                'Bayern-Munich', 
                'Bochum', 
                'Borussia-Dortmund',
                'Borussia-Monchengladbach',
                'Darmstadt-98', 
                'Eintracht-Frankfurt', 
                'FC-Heidenheim',
                'FC-Köln',
                'Freiburg',
                'FSV-Mainz05',
                'Hoffenheim',
                'RB-Leipzig',
                'Union-Berlin',
                'VfB-Stuttgart',
                'Werder-Bremen',
                'Wolfsburg']


def find_best_match(player, choices):
    best_match = process.extractOne(player, choices)
    return best_match[0] if best_match[1] > 50 else None 

st.header("Game Result and Stats")
# Apply the matching function
league_table['Opponent'] = league_table['Opponent'].apply(find_best_match, choices=actual_names)        
filtered_row = league_table.loc[(league_table['Opponent'] == opponent) & (league_table['Venue'] == home_away)]

st.write(filtered_row)
## THIS IS FOR GIF EXTRACTION BELOW
if on:
    # Only display the image after the button is clicked
    if minute.isdigit():
        minute = int(minute)
        minute_str = f"{minute:02}"  # Format minute to always have two digits

        # Only display the image after the button is clicked
        if st.session_state.clicked:
            # Construct the Cloudinary URL based on user input
            cloud_name = "dmvgm3jgz"  # Your Cloudinary cloud name
            public_id = f"{opponent}_{home_away}_map_minute_{minute}"
            image_url = f"https://res.cloudinary.com/{cloud_name}/image/upload/v1729790662/{opponent}/{home_away}/{public_id}"

            # Display the image in the main content area
            st.image(image_url)

## THIS IS FOR INDIVIDUAL GAME MINUTE EXTRACTION BELOW
else:
    if st.session_state.clicked:
        # Construct the Cloudinary URL based on user input
        cloud_name = "dmvgm3jgz"  # Your Cloudinary cloud name
        public_id = f"{opponent}_{home_away}.gif"
        gif_url = f"https://res.cloudinary.com/dmvgm3jgz/image/upload/v1729963428/images/{public_id}"

        # Display the image in the main content area
        st.image(gif_url)
    else:
        st.write("Please enter a valid minute (0-90)")

st.markdown("""
        <style>
               .block-container {
                    padding-top: 2.5rem;
                }
        </style>
        """, unsafe_allow_html=True)
logo = Image.open('bayer.png')
st.sidebar.image(logo)