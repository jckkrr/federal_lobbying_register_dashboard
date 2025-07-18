############## Constistuent.Online #################
####### Code-free analysis for curious folk. ######

### An application for ...

## streamlit run "C:\Users\Jack\Documents\Python_projects\greenpeace\lobbyists\streamlit_app.py"

### --------------------------------------- IMPORTS 

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import customChartDefaultStyling

pd.set_option('display.max_columns', None)

### 
headers = {
    "content-type": "application/json"
}

css = 'body, html, p, h1, .st-emotion-cache-1104ytp h1, [class*="css"] {font-family: "Inter", sans-serif;}'
st.set_page_config(layout="wide")
st.markdown( f'<style>{css}</style>' , unsafe_allow_html= True)


### ---------------------------------------- FUNCTIONS 

### Get a person's comany and clients
def get_l2c():
    df_l2c = df_lobbyists.merge(df_clients[['Parent Organisation', 'Org ABN', 'Client Name', 'Client ABN', 'is_energy', 'Date Published']], on = ['Parent Organisation', 'Org ABN'], how = 'outer')
    
    return df_l2c


### ----------------------------------------  RUN

st.markdown("**Open Investigation Tools** | [constituent.online](%s)" % 'http://www.constituent.online')
    
st.title('Australian Federal Government Lobbying Register Dashboard')
st.write('Data downloaded: 18 July 2025')

### Get DFs ### 

df_organisations = pd.read_csv('https://raw.githubusercontent.com/jckkrr/federal_lobbying_register_dashboard/refs/heads/main/df_organisations.csv')
df_lobbyists = pd.read_csv('https://raw.githubusercontent.com/jckkrr/federal_lobbying_register_dashboard/refs/heads/main/df_lobbyists.csv')
df_clients = pd.read_csv('https://raw.githubusercontent.com/jckkrr/federal_lobbying_register_dashboard/refs/heads/main/df_clients.csv')

col1, col2, col3, col4, col5 = st.columns([1,2,1,1,1])

df_l2c = get_l2c()

with col1: 
    available_search_column = [None, 'Lobbyist Name', 'Parent Organisation', 'Previous Position', 'Client Name'] 
    chosen_search_column = st.selectbox('Search column:', (available_search_column))
    
with col2: 
    
    if chosen_search_column != None:
        available_search_terms = [None] + sorted(df_l2c[chosen_search_column].dropna().unique())
        chosen_search_term = st.selectbox('Search term:', (available_search_terms))
    else:
        chosen_search_term = None
        st.write('...')
        
    if chosen_search_column != None and chosen_search_term != None:
        df_l2c = df_l2c.loc[df_l2c[chosen_search_column] == chosen_search_term] 

with col3:
    available_only_exgov = [False, True]
    only_exgov = st.selectbox('Ex govt reps only', (available_only_exgov))
    
    if only_exgov == True:
        df_l2c = df_l2c.loc[df_l2c['Former Govt. Representative'] == 'Yes']
    
with col4:
    available_only_energy = [False, True]
    only_energy = st.selectbox('Enegry clients only', (available_only_energy))
    
    if only_energy == True:
        df_l2c = df_l2c.loc[df_l2c['is_energy'] == 'Yes']
    
with col5:
    available_inc_public_servants = [False, True]
    inc_public_servants = st.selectbox('Inc public servants as govt reps', (available_only_energy))
    
    if inc_public_servants == False:
        exclude_positions = ['Employed under the Public Service Act 1999', 'Contractor/consultant for an agency whose staff are employed under the Public Service Act 1999', 'Public Servant']
        df_l2c['Former Govt. Representative'] = np.where(df_l2c['Previous Position'].isin(exclude_positions), 'No', df_l2c['Former Govt. Representative'])

        
df_l2c = df_l2c.sort_values(by = ['is_energy', 'Former Govt. Representative', 'Cessation Year', 'Lobbyist Name'], ascending = [True, False, False, True])
df_l2c = df_l2c[['Lobbyist Name', 'Job Title', 'Parent Organisation', 'Org ABN', 'Former Govt. Representative', 'Previous Position', 'Cessation Year', 'Client Name', 'Client ABN', 'is_energy']]
    
df_l2c['Cessation Year'] = df_l2c['Cessation Year'].astype(float)
    
st.dataframe(df_l2c.style.format(precision=0)) 
        
