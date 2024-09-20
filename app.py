# %%
import requests as r
import pandas as pd
import streamlit as st

from constants import Constants as c
# %%
# # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # NHL API # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # #


teamsURL = 'https://statsapi.web.nhl.com/api/v1/teams'
scheduleURL = 'https://statsapi.web.nhl.com/api/v1/schedule'
gameURL = 'https://statsapi.web.nhl.com/api/v1/game'
standingsURL = 'https://api-web.nhle.com/v1/standings/now'

def get_nhl_dataset(URL):
    response = r.get(URL)
    JSON = response.json()
    return JSON

def get_team_records():
    team_list = get_nhl_dataset(standingsURL)['standings']

    team_records = pd.DataFrame()

    for team in team_list:
        team_dict = {}

        team_dict['Team Name'] = team['teamName']['default']

        team_dict['GP'] = 0
        team_dict['W'] = team['wins']
        team_dict['L'] = team['losses']
        team_dict['OTL'] = team['otLosses']
        team_dict['P'] = team['wins']*2 + team['otLosses']*1

        team_dict['GP'] = team['wins'] + team['losses'] + team['otLosses']
        
        team_records = pd.concat([team_records,pd.DataFrame(team_dict,index=[0])],ignore_index=True)

    return team_records
# %% 
team_records = get_team_records()

aaron_list = ['BOS','TBL','MIN','CGY','ANA']
bryan_list = ['EDM','TOR','WPG','PHI','OTT']
chad_list = ['VAN','VGK','UTA','BUF','NJD']
collin_list = ['FLA','NSH','DET','NYI','STL']
jonah_list = ['COL','NYR','WSH','CBJ','SEA']
robbie_list = ['CAR','DAL','LAK','PIT','MTL']

team_dict = c.team_dict

aaron_list_full = [team_dict[abr] for abr in aaron_list]
bryan_list_full = [team_dict[abr] for abr in bryan_list]
chad_list_full = [team_dict[abr] for abr in chad_list]
collin_list_full = [team_dict[abr] for abr in collin_list]
jonah_list_full = [team_dict[abr] for abr in jonah_list]
robbie_list_full = [team_dict[abr] for abr in robbie_list]

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
            
            col.write(name + "'s Riding Chad's Dick Division")
            
            person_records = team_records[team_records['Team Name'].isin(person)]

            person_records_total = pd.DataFrame({
                '':'Total',
                'GP':person_records['GP'].sum(),
                'W':person_records['W'].sum(),
                'L':person_records['L'].sum(),
                'OTL':person_records['OTL'].sum(),
                'P':person_records['P'].sum()
            },index=[0])

            col.dataframe(person_records,use_container_width=True,hide_index=True)

            col.dataframe(person_records_total,use_container_width=True,hide_index=True)

            total_score = person_records_total['W'].values[0]*2 + person_records_total['OTL'].values[0]*1

        
            overall_scores_dict[name] = [person_records['GP'].sum(),
                                         total_score,
                                         round(total_score/person_records['GP'].sum(),3)]

            col.divider()

with tab1:

    score_ranking = pd.DataFrame(overall_scores_dict).T
    score_ranking.columns = ['GP','Score','PPGR']

    for col in ['GP','Score']:
        score_ranking[col] = score_ranking[col].astype(int)

    st.dataframe(score_ranking,width=400)


# %%
