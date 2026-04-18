# %%
import requests as r
import pandas as pd
import streamlit as st
from IPython.display import display

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

def get_team_records(
        points_rw = 2, 
        points_otw = 2, 
        points_sow = 2,
        points_sol = 1,
        points_otl = 1
        ):
    team_list = get_nhl_dataset(standingsURL)['standings']

    team_records = pd.DataFrame()

    for team in team_list:
        team_dict = {}

        team_dict['Team Name'] = team['teamName']['default']
        team_dict['Conference'] = team['conferenceName']
        team_dict['ConferenceAbbr'] = team['conferenceAbbrev']
        team_dict['Division'] = team['divisionName']
        team_dict['DivisionAbbr'] = team['divisionAbbrev']
        team_dict['GP'] = 0
        team_dict['W'] = team['wins']
        team_dict['RW'] = team['regulationWins']
        team_dict['OTW'] = team['regulationPlusOtWins'] - team['regulationWins']
        team_dict['SOW'] = team['shootoutWins']
        team_dict['OTW_T'] = team_dict['OTW'] + team_dict['SOW']
        team_dict['L'] = team['losses']
        team_dict['RL'] = team['losses'] - team['otLosses']
        team_dict['OTL_T'] = team['otLosses']
        team_dict['OTL'] = team['otLosses'] - team['shootoutLosses']
        team_dict['SOL'] = team['shootoutLosses']
        team_dict['TOT'] = team_dict['OTL_T'] + team_dict['OTW_T']
        team_dict['P'] = team_dict['RW']* points_rw + team_dict['OTW'] * points_otw + team_dict['SOW'] * points_sow \
                            + team_dict['SOL'] * points_sol + team_dict['OTL'] * points_otl

        team_dict['GP'] = team['wins'] + team['losses'] + team['otLosses']
        
        team_records = pd.concat([team_records,pd.DataFrame(team_dict,index=[0])],ignore_index=True)

    return team_records


# %% 
team_records = get_team_records()

aaron_list = ['VGK','STL','LAK','CHI'] #['BOS','TBL','MIN','CGY','ANA']
bryan_list = ['DAL','NJD','OTT','VAN'] #['EDM','TOR','WPG','PHI','OTT']
chad_list = ['WPG','TOR','CGY','DET'] #['VAN','VGK','UTA','BUF','NJD']
collin_list = ['EDM','CAR','BOS','PIT'] #['FLA','NSH','DET','NYI','STL']
jonah_list = ['TBL','NYR','MTL','SJS'] #['COL','NYR','WSH','CBJ','SEA']
robbie_list = ['FLA','WSH','MIN','CBJ'] #['CAR','DAL','LAK','PIT','MTL']
emily_list = ['COL','UTA','ANA','SEA']

team_dict = c.team_dict

aaron_list_full = [team_dict[abr] for abr in aaron_list]
bryan_list_full = [team_dict[abr] for abr in bryan_list]
chad_list_full = [team_dict[abr] for abr in chad_list]
collin_list_full = [team_dict[abr] for abr in collin_list]
jonah_list_full = [team_dict[abr] for abr in jonah_list]
robbie_list_full = [team_dict[abr] for abr in robbie_list]
emily_list_full = [team_dict[abr] for abr in emily_list]

person_col_list = [[aaron_list,collin_list,emily_list],[bryan_list,jonah_list],[chad_list,robbie_list],[emily_list]]
person_name_list = [['Aaron','Collin','Emily'],['Bryan','Jonah'],['Chad','Robbie']]
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

        team_list = person_col_list[i]
        name_list = person_name_list[i]
        for j in range(0,len(team_list)):
            teams_abbr = team_list[j]
            teams = [team_dict[abr] for abr in teams_abbr]
            name = name_list[j]
            
            col.write(name + "'s Riding Chad's Dick Division")
            
            person_records = team_records[team_records['Team Name'].isin(teams)]

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

    st.dataframe(score_ranking.sort_values('Score',ascending=False),width=400)


# %%
# def generate_nhl_standings(team_records, top_division_teams=3, wildcard_teams=2):
#     standings = {}
#     for conf in team_records['Conference'].dropna().unique():
#         conf_df = team_records[team_records['Conference'] == conf]
#         divisions = conf_df['DivisionAbbr'].unique()
#         division_playoff_teams = []
#         wildcard_candidates = []
#         for div in divisions:
#             div_df = conf_df[conf_df['DivisionAbbr'] == div].sort_values('P', ascending=False)
#             div_top = div_df.head(top_division_teams).copy()
#             div_top['PlayoffStatus'] = 'Division'
#             division_playoff_teams.append(div_top)
#             div_rest = div_df.iloc[top_division_teams:].copy()
#             if not div_rest.empty:
#                 wildcard_candidates.append(div_rest)
#         if wildcard_candidates:
#             wildcard_df = pd.concat(wildcard_candidates)
#             wildcard_df = wildcard_df.sort_values('P', ascending=False)
#             wildcards = wildcard_df.head(wildcard_teams).copy()
#             wildcards['PlayoffStatus'] = 'Wildcard'
#             out_df = wildcard_df.iloc[wildcard_teams:].copy()
#             out_df['PlayoffStatus'] = 'Out'
#         else:
#             wildcards = pd.DataFrame()
#             out_df = pd.DataFrame()
#         conf_table = pd.concat(division_playoff_teams + [wildcards, out_df], ignore_index=True)
#         conf_table['PlayoffStatus'] = pd.Categorical(
#             conf_table['PlayoffStatus'], categories=['Division', 'Wildcard', 'Out'], ordered=True
#         )
#         conf_table = conf_table.sort_values(['PlayoffStatus', 'P'], ascending=[True, False])
#         standings[conf] = conf_table.reset_index(drop=True)
#     return standings

# def style_standings_table(df, conference):
#     df['Division'] = df['Division'].astype(str).str[:5]
#     # Select and order columns as specified
#     columns = [
#         'Team Name', 'Division', 'W', 'RW', 'OTW', 'SOW', 'L', 'RL', 'OTL', 'SOL', 'P', 'PlayoffStatus'
#     ]
#     for col in columns:
#         if col not in df.columns:
#             df[col] = 0 if col not in ['Team Name', 'Division', 'PlayoffStatus'] else ''
#     df = df[columns].copy()
#     df.index = df.index + 1  # 1-based index

#     # Define background colors for playoff status
#     colors = {
#         'Division': 'background-color: #b3e6b3;',
#         'Wildcard': 'background-color: #ffe699;',
#         'Out': 'background-color: #f4cccc;'
#     }
#     def highlight_status(row):
#         return [colors.get(row['PlayoffStatus'], '')] * len(row)

#     styled = (
#         df.style
#         .apply(highlight_status, axis=1)
#         .set_caption(f"NHL Playoff Standings - {conference} Conference")
#         .set_table_styles([
#             {'selector': 'th', 'props': [('background-color', '#003366'), ('color', 'white'), ('font-size', '14px')]},  # column headers
#             {'selector': 'caption', 'props': [('caption-side', 'top'), ('font-size', '16px'), ('font-weight', 'bold'), ('color', 'white')]},
#             {'selector': 'td', 'props': [('color', 'black')]},  # table cells
#             {'selector': 'thead th', 'props': [('color', 'white')]},  # column headers
#             {'selector': 'tbody th', 'props': [('color', 'white'), ('background-color', '#003366')]}  # row labels
#         ])
#         .format({'P': '{:.0f}', 'W': '{:.0f}', 'RW': '{:.0f}', 'OTW': '{:.0f}', 'SOW': '{:.0f}', 'L': '{:.0f}', 'RL': '{:.0f}', 'OTL': '{:.0f}', 'SOL': '{:.0f}'})
#     )
#     return styled

# # Example usage:
# team_records = get_team_records(
#     points_rw = 2, 
#     points_otw = 2, 
#     points_sow = 2,
#     points_sol = 1,
#     points_otl = 0
# )
# standings = generate_nhl_standings(
#     team_records, 
#     top_division_teams=3, 
#     wildcard_teams=2
# )

# for conf, df in standings.items():
#     display(style_standings_table(df, conf))  # Use display() in Jupyter, or .to_html() for web
# %%
