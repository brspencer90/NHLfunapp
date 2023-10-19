# %%
import requests as r
import pandas as pd
import streamlit as st
# %%
# # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # NHL API # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # #


teamsURL = 'https://statsapi.web.nhl.com/api/v1/teams'
scheduleURL = 'https://statsapi.web.nhl.com/api/v1/schedule'
gameURL = 'https://statsapi.web.nhl.com/api/v1/game'
standingsURL = 'https://statsapi.web.nhl.com/api/v1/standings'

def get_nhl_dataset(URL):
    response = r.get(URL)
    JSON = response.json()
    return JSON

def get_team_records():
    division_records = get_nhl_dataset(standingsURL)['records']

    team_records = pd.DataFrame()

    for div in division_records:
        team_list = div['teamRecords']
        
        team_dict = {}

        for team in team_list:
            team_dict['Team Name'] = team['team']['name']

            team_record = team['leagueRecord']

            team_dict['GP'] = 0
            team_dict['W'] = team_record['wins']
            team_dict['L'] = team_record['losses']
            team_dict['OTL'] = team_record['ot']

            team_dict['GP'] = team_record['wins'] + team_record['losses'] + team_record['ot']
            
            team_records = pd.concat([team_records,pd.DataFrame(team_dict,index=[0])],ignore_index=True)

    return team_records
# %% 
team_records = get_team_records()

aaron_list = ['Buffalo Sabres','Carolina Hurricanes','Minnesota Wild','Nashville Predators','Washington Capitals']
bryan_list = ['Arizona Coyotes','Colorado Avalanche','New York Rangers','Seattle Kraken','Tampa Bay Lightning']
chad_list = ['Edmonton Oilers','Los Angeles Kings','New York Islanders','Philadelphia Flyers','Toronto Maple Leafs']
collin_list = ['Boston Bruins','Calgary Flames','Florida Panthers','St. Louis Blues','Vegas Golden Knights']
jonah_list = ['Chicago Blackhawks','Columbus Blue Jackets','Dallas Stars','Pittsburgh Penguins','Winnipeg Jets']
robbie_list = ['New Jersey Devils','Detroit Red Wings','Ottawa Senators','Vancouver Canucks','Montréal Canadiens']

person_col_list = [[aaron_list,collin_list],[bryan_list,jonah_list],[chad_list,robbie_list]]
person_name_list = [['Aaron','Collin'],['Bryan','Jonah'],['Chad','Robbie']]
st.set_page_config(
   page_title='Cole Caulfield 4 Prez',
   layout="wide",
)

tab1, tab2 = st.tabs(['Ranking','Breakdown'])

with tab2:

    overall_scores_dict = {}

    col1,col2,col3 = st.columns(3)
    col_list = [col1,col2,col3]

    for i in range(0,3):
        col = col_list[i]

        person_list = person_col_list[i]
        name_list = person_name_list[i]
        for j in range(0,2):
            person = person_list[j]
            name = name_list[j]
            
            col.write(name + "'s Team")
            
            person_records = team_records[team_records['Team Name'].isin(person)]

            person_records_total = pd.DataFrame({
                '':'Total',
                'GP':person_records['GP'].sum(),
                'W':person_records['W'].sum(),
                'L':person_records['L'].sum(),
                'OTL':person_records['OTL'].sum()
            },index=[0])

            col.dataframe(person_records,use_container_width=True,hide_index=True)

            col.dataframe(person_records_total,use_container_width=True,hide_index=True)

            total_score = person_records_total['W'].values[0]*2 + person_records_total['OTL'].values[0]*1

            overall_scores_dict[name] = total_score

            col.write('Total score : ' + str(total_score))

            col.divider()

with tab1:

    score_ranking = pd.DataFrame(overall_scores_dict,index=[0]).T.sort_values(0,ascending=False)
    score_ranking.columns = ['Score']

    st.dataframe(score_ranking)
