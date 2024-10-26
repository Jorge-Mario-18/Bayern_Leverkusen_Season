import streamlit as st
import pandas as pd 
import numpy as np
import streamlit as st 
from pandas import json_normalize
import requests
import numpy as np
from bs4 import BeautifulSoup as bs
from fuzzywuzzy import process
from PIL import Image

url = "https://fbref.com/en/squads/c7a9f859/2023-2024/Bayer-Leverkusen-Stats"
r = requests.get(url)
soup = bs(r.content)
table_stats = soup.find_all("table", id="stats_standard_20")
table_stats = pd.read_html(str(table_stats), header=1)[0]
table_stats = table_stats[['Player', 'Min', 'Gls', 'Ast', 'xG', 'PrgC', 'PrgR', 'PrgP']]

pass_team_a2= pd.read_csv('player_passes_BL.csv')
unique_names = pass_team_a2['Passing Player'].unique()
player_list_a = unique_names.tolist()

def find_best_match(player, choices):
    best_match = process.extractOne(player, choices)
    return best_match[0] if best_match[1] > 80 else None 

# Apply the matching function
pass_team_a2['matched_name'] = pass_team_a2['Passing Player'].apply(find_best_match, choices=table_stats['Player'])

# Merge the dataframes based on the matched names
merged_df = pd.merge(pass_team_a2, table_stats, left_on='matched_name', right_on='Player', how='inner')

st.header("Passing Chart")
with st.sidebar:
    on = st.toggle("Individual Player")
    if on:
        player = st.selectbox(
        "Pick a player",
        (player_list_a))
        selection_2 = st.radio("Selected Player as passing or recieving", ["Passing", "Receving"], horizontal=True)
    
if on:
    if selection_2 == "Passing":
        pass_player = pass_team_a2[pass_team_a2["Passing Player"] == player]
        pass_player = pass_player.drop(columns=['matched_name'])
        pass_player.reset_index(drop=True)
        player_stat = merged_df[merged_df["Passing Player"] == player]
        player_stat = player_stat[["Player", "Min", "Gls", "Ast", "xG", "PrgC", "PrgR", "PrgP"]]
        st.dataframe(pass_player.head(11))
        st.write(player_stat.head(1))
        
    if selection_2 == "Receving":
        pass_recipient = pass_team_a2[pass_team_a2["Pass Recipient"] == player]
        pass_recipient = pass_recipient.drop(columns=['matched_name'])
        pass_recipient.reset_index(drop=True)
        player_stat_1 = merged_df[merged_df["Passing Player"] == player]
        player_stat_1 = player_stat_1[["Player", "Min", "Gls", "Ast", "xG", "PrgC", "PrgR", "PrgP"]]
        st.dataframe(pass_recipient.head(11))
        st.write(player_stat_1.head(1))
else: 
    st.write("Avergae Starting 11 Passing")
    pass_team_a2 = pass_team_a2.drop(columns=['matched_name'])
    pass_team_a2 = pass_team_a2.reset_index(drop=True)
    st.dataframe(pass_team_a2.head(11))
    merged_df_2 = merged_df.drop(columns=['Passing Player', 'Pass Recipient', 'Number of passes'])
    merged_df_2 = merged_df_2.drop_duplicates()
    st.write("Average Starting 11 Player Stats")
    merged_df_2 = merged_df_2.drop(columns=['matched_name'])
    merged_df_2 = merged_df_2.reset_index(drop=True)
    st.dataframe(merged_df_2)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 3rem;
                }
        </style>
        """, unsafe_allow_html=True)

logo = Image.open('bayer.png')
st.sidebar.image(logo)