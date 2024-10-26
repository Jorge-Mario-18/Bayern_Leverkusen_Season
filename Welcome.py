import streamlit as st
from PIL import Image



st.header("Bayer Leverkusen Passing Stats")
logo = Image.open('bayer.png')
st.sidebar.image(logo)
st.markdown("""
                This dashboard showcases data and visual maps of Bayer Leverkusen's passing. 
            You can explore each game, minute-by-minute, through GIFs or standalone images, 
            selecting the opponent, venue (home or away), and specific minute. The player 
            stats page displays connected passes for each individual player, along with season 
            stats. You can also filter by individual players for more detailed insights.
            """)
st.write("By Jorge Mario Restrepo")

st.image("bayer_trophy.jpg")
st.write("""Event and Coordinate Data is provide by Hudlstatsbomb's free API. Game and player stats is 
         provided by Sports Reference. The images are hosted on Cloudinary""")
st.write("""
         Email: coachjorgemario@gmail.com""")