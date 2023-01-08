import dash
from dash import html, dcc, dash_table
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np


# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash()


teams = {
    'Arizona Cardinals': 'ARI','Atlanta Falcons': 'ATL','Baltimore Ravens': 'BAL','Buffalo Bills': 'BUF','Carolina Panthers': 'CAR','Chicago Bears': 'CHI',
    'Cincinnati Bengals': 'CIN','Cleveland Browns': 'CLE','Dallas Cowboys': 'DAL','Denver Broncos': 'DEN','Detroit Lions': 'DET',
    'Green Bay Packers': 'GB','Houston Texans': 'HOU','Indianapolis Colts': 'IND','Jacksonville Jaguars': 'JAX','Kansas City Chiefs': 'KC','Las Vegas Raiders': 'LV',
    'Los Angeles Chargers': 'LAC','Los Angeles Rams': 'LAR','Miami Dolphins': 'MIA','Minnesota Vikings': 'MIN','New England Patriots': 'NE',
    'New Orleans Saints': 'NO','New York Giants': 'NYG','New York Jets': 'NYJ','Philadelphia Eagles': 'PHI','Pittsburgh Steelers': 'PIT','San Francisco 49ers': 'SF',
    'Seattle Seahawks': 'SEA','Tampa Bay Buccaneers': 'TB', 'Tennessee Titans': 'TEN','Washington Commanders': 'WAS'
}
t1 = [['1st Quarter',0,0,0,0], ['2nd Quarter',0,0,0,0], ['3rd Quarter',0,0,0,0], ['4th Quarter',0,0,0,0],
['Winning by 9+',0,0,0,0], ['Winning by 1-8',0,0,0,0], ['Tied',0,0,0,0], ['Losing by 1-8',0,0,0,0], ['Losing by 9+',0,0,0,0],
['1st and 10',0,0,0,0], ['2nd and Short',0,0,0,0], ['2nd and Long',0,0,0,0], ['3rd and Short',0,0,0,0], 
['3rd and Long',0,0,0,0], ['4th and Short',0,0,0,0], ['4th and Long',0,0,0,0], ['Goal to go',0,0,0,0], ['Red Zone',0,0,0,0, ],['FG Range',0,0,0,0]]
table10 = pd.DataFrame(t1,columns = ['Situation', 'Blitz%', 'EPA/Blitz','Stunt%','EPA/Stunt'])
table1 = dash_table.DataTable(
    id = 'table1', data=table10.to_dict('records'),
    columns=[{'name': col, 'id': col} for col in table10.columns]
)


app.layout = html.Div([
    html.H1(children="Stunt & Blitz Guide", style={'textAlign': 'center', 'font-family': 'Verdana'}),
    html.P(
        children="Pick a defense to get a scouting report on their blitz packages and stunts ran. (Negative epa = good defense)",
        style={'textAlign': 'center', 'font-family': 'Verdana'}
    ),
    dcc.Dropdown(
        ['Arizona Cardinals','Atlanta Falcons','Baltimore Ravens','Buffalo Bills','Carolina Panthers','Chicago Bears','Cincinnati Bengals','Cleveland Browns',
        'Dallas Cowboys','Denver Broncos','Detroit Lions','Green Bay Packers','Houston Texans','Indianapolis Colts','Jacksonville Jaguars','Kansas City Chiefs',
        'Las Vegas Raiders','Los Angeles Chargers','Los Angeles Rams','Miami Dolphins','Minnesota Vikings','New England Patriots','New Orleans Saints','New York Giants',
        'New York Jets','Philadelphia Eagles','Pittsburgh Steelers','San Francisco 49ers','Seattle Seahawks','Tampa Bay Buccaneers','Tennessee Titans','Washington Commanders'],
        'Arizona Cardinals', id='demo-dropdown', style={'textAlign': 'center', 'font-family': 'Verdana'}
    ),
    html.Div(id='dd-output-container'),
    html.Div(table1, style={'width': '40%', 'float': 'left'}),
    # html.Div(table2, style={'width': '33%', 'float': 'left'}),
    # html.Div(table3, style={'width': '33%', 'float': 'left'}),
])

def when_they_blitz(team):
#     %xmode Verbose
    df = pd.read_csv('temp.csv')
    all_stunts = pd.read_csv('test_csv.csv')
    all_stunts = all_stunts.rename(columns = {"('blitz', 'mean')":"blitz",
                                 "('blitz_class', '')":"blitz_class",
                                 "('stunt', '')":"stunt",
                                 "('stunt_class', '')":"stunt_class"})
    # all_stunts = all_stunts.drop(all_stunts.index[0])
    all_stunts['gameId'] = all_stunts.gameId.astype('int64')
    all_stunts['playId'] = all_stunts.playId.astype('int64')
    all_stunts = all_stunts.drop(['Unnamed: 0'], axis = 1)
    all_stunts['gameplayId'] = all_stunts.apply(lambda row:str(row.loc['gameId'])+"_"+str(row.loc['playId']), axis=1)
    all_stunts = all_stunts.drop(['...1','possessionTeam','yardlineNumber','yardlineSide','playDescription','preSnapHomeScore', 'preSnapVisitorScore','offenseFormation', 'personnelO', 'defendersInBox',
           'personnelD', 'dropBackType', 'pff_passCoverage',
           'pff_passCoverageType','gameId','playId'], axis=1)
    merge_df = df[['rushers','blitz_pff_dummy','defendersInBox','gameplayId','yardsToEZ', 'pointDifferential','DL', 'LB', 'DB', 'quarterTimeLeft','gameTimeLeft']]
    all_stunts = all_stunts.merge(merge_df,on='gameplayId',how = 'left')
    all_stunts = all_stunts.drop(['penaltyYards', 'prePenaltyPlayResult', 'playResult',
           'foulName1', 'foulNFLId1', 'foulName2', 'foulNFLId2', 'foulName3',
           'foulNFLId3', 'absoluteYardlineNumber', 'pff_playAction'], axis=1)
    all_stunts = all_stunts.dropna(subset = ['blitz_pff_dummy'])
    all_stunts['dummyStunt'] = np.where(all_stunts.stunt_class > 0,1,0)
    all_stunts['dummyBlitz'] = np.where(all_stunts.blitz_class > 0,1,0)

    tm = all_stunts.loc[all_stunts.defensiveTeam == team]
    tm.loc[(tm.down == 1)&(tm.yardsToGo==10), 'first10'] = 1
    tm.loc[(tm.down == 2)&(tm.yardsToGo<5), 'secondShort'] = 1
    tm.loc[(tm.down == 2)&(tm.yardsToGo>=5), 'secondLong'] = 1
    tm.loc[(tm.down == 3)&(tm.yardsToGo<5), 'thirdShort'] = 1
    tm.loc[(tm.down == 3)&(tm.yardsToGo>=5), 'thirdLong'] = 1
    tm.loc[(tm.down == 4)&(tm.yardsToGo<5), 'fourthShort'] = 1
    tm.loc[(tm.down == 4)&(tm.yardsToGo>=5), 'fourthLong'] = 1

    
    total_plays = tm.shape[0]
    
    ## stunt rates
    sr_first10 = tm[tm.dummyStunt == 1].first10.sum()/total_plays
    sr_secondShort = tm[tm.dummyStunt == 1].secondShort.sum()/total_plays
    sr_secondLong = tm[tm.dummyStunt == 1].secondLong.sum()/total_plays
    sr_thirdShort = tm[tm.dummyStunt == 1].thirdShort.sum()/total_plays
    sr_thirdLong = tm[tm.dummyStunt == 1].thirdLong.sum()/total_plays
    sr_fourthShort = tm[tm.dummyStunt == 1].fourthShort.sum()/total_plays
    sr_fourthLong = tm[tm.dummyStunt == 1].fourthLong.sum()/total_plays
    
    sr_G2G = tm[(tm.dummyStunt == 1) & (tm.yardsToEZ <= 10)].dummyStunt.count()/total_plays
    sr_redzone = tm[(tm.dummyStunt == 1) & (tm.yardsToEZ <= 20)].dummyStunt.count()/total_plays
    sr_fgRange = tm[(tm.dummyStunt == 1) & (tm.yardsToEZ <= 45)].dummyStunt.count()/total_plays
    
    sr_singleScoreW = tm[(tm.dummyStunt == 1) &
                         (tm.pointDifferential <= 8) &
                         (tm.pointDifferential > 0)].dummyStunt.count()/total_plays
    sr_singleScoreL = tm[(tm.dummyStunt == 1) &
                         (tm.pointDifferential >= -8) &
                         (tm.pointDifferential < 0)].dummyStunt.count()/total_plays
    sr_singleScoreT = tm[(tm.dummyStunt == 1) &
                         (tm.pointDifferential == 0)].dummyStunt.count()/total_plays
    sr_multScoreW = tm[(tm.dummyStunt == 1) & (tm.pointDifferential > 8)].dummyStunt.count()/total_plays
    sr_multScoreL = tm[(tm.dummyStunt == 1) & (tm.pointDifferential < -8)].dummyStunt.count()/total_plays
                       
    sr_quarterOne = tm[(tm.dummyStunt == 1) & (tm.quarter == 1)].dummyStunt.count()/total_plays
    sr_quarterTwo = tm[(tm.dummyStunt == 1) & (tm.quarter == 2)].dummyStunt.count()/total_plays
    sr_quarterThree = tm[(tm.dummyStunt == 1) & (tm.quarter == 3)].dummyStunt.count()/total_plays
    sr_quarterFour = tm[(tm.dummyStunt == 1) & (tm.quarter == 4)].dummyStunt.count()/total_plays
    stunt_rates = [sr_first10,sr_secondShort,sr_secondLong,sr_thirdShort,sr_thirdLong,
            sr_fourthShort,sr_fourthLong,sr_G2G,sr_redzone,sr_fgRange,sr_singleScoreW,
            sr_singleScoreL,sr_singleScoreT,sr_multScoreW,sr_multScoreL,sr_quarterOne,
            sr_quarterTwo,sr_quarterThree,sr_quarterFour]
    
    ## blitz rates
    br_first10 = tm[tm.dummyBlitz == 1].first10.sum()/total_plays
    br_secondShort = tm[tm.dummyBlitz == 1].secondShort.sum()/total_plays
    br_secondLong = tm[tm.dummyBlitz == 1].secondLong.sum()/total_plays
    br_thirdShort = tm[tm.dummyBlitz == 1].thirdShort.sum()/total_plays
    br_thirdLong = tm[tm.dummyBlitz == 1].thirdLong.sum()/total_plays
    br_fourthShort = tm[tm.dummyBlitz == 1].fourthShort.sum()/total_plays
    br_fourthLong = tm[tm.dummyBlitz == 1].fourthLong.sum()/total_plays
    
    br_G2G = tm[(tm.dummyBlitz == 1) & (tm.yardsToEZ <= 10)].dummyBlitz.count()/total_plays
    br_redzone = tm[(tm.dummyBlitz == 1) & (tm.yardsToEZ <= 20)].dummyBlitz.count()/total_plays
    br_fgRange = tm[(tm.dummyBlitz == 1) & (tm.yardsToEZ <= 45)].dummyBlitz.count()/total_plays
    
    br_singleScoreW = tm[(tm.dummyBlitz == 1) &
                         (tm.pointDifferential <= 8) &
                         (tm.pointDifferential > 0)].dummyBlitz.count()/total_plays
    br_singleScoreL = tm[(tm.dummyBlitz == 1) &
                         (tm.pointDifferential >= -8) &
                         (tm.pointDifferential < 0)].dummyBlitz.count()/total_plays
    br_singleScoreT = tm[(tm.dummyBlitz == 1) &
                         (tm.pointDifferential == 0)].dummyBlitz.count()/total_plays
    br_multScoreW = tm[(tm.dummyBlitz == 1) & (tm.pointDifferential > 8)].dummyBlitz.count()/total_plays
    br_multScoreL = tm[(tm.dummyBlitz == 1) & (tm.pointDifferential < -8)].dummyBlitz.count()/total_plays
                       
    br_quarterOne = tm[(tm.dummyBlitz == 1) & (tm.quarter == 1)].dummyBlitz.count()/total_plays
    br_quarterTwo = tm[(tm.dummyBlitz == 1) & (tm.quarter == 2)].dummyBlitz.count()/total_plays
    br_quarterThree = tm[(tm.dummyBlitz == 1) & (tm.quarter == 3)].dummyBlitz.count()/total_plays
    br_quarterFour = tm[(tm.dummyBlitz == 1) & (tm.quarter == 4)].dummyBlitz.count()/total_plays
    blitz_rates = [br_first10,br_secondShort,br_secondLong,br_thirdShort,br_thirdLong,
            br_fourthShort,br_fourthLong,br_G2G,br_redzone,br_fgRange,br_singleScoreW,
            br_singleScoreL,br_singleScoreT,br_multScoreW,br_multScoreL,br_quarterOne,
            br_quarterTwo,br_quarterThree,br_quarterFour]
    # print("Stunt Rates: {}".format(stunt_rates))
    # print('-----')
    # print("Blitz Rates: {}".format(blitz_rates))
    
    # plt.bar([1,2,3,4],stunt_rates[-4:])
    # plt.xlabel("Quarter")
    # plt.ylabel("Stunt Rate")
    # ax = plt.gca()
    # ax.set_xticks(np.arange(1,5,1))
    # plt.show()
    
    # plt.bar([1,2,3,4],blitz_rates[-4:])
    # plt.xlabel("Quarter")
    # plt.ylabel("Blitz Rate")
    # ax = plt.gca()
    # ax.set_xticks(np.arange(1,5,1))
    # plt.show()
    
    return [stunt_rates,blitz_rates]


@app.callback( 
    dash.dependencies.Output('table1', 'data'),
    dash.dependencies.Input('demo-dropdown', 'value')
)


def update_tables(value):
    print(value)
    nfl_team = teams[value]
    list = when_they_blitz(nfl_team)
    # for i in list[0]:
    #     i *= 100
    #     i = round(i,2)
    # for i in list[1]:
    #     i *= 100
    #     i = round(i,2)
    data_list = [['1st Quarter',round(list[1][15]*100,2),0,round(list[0][15]*100,2),0], ['2nd Quarter',round(list[1][16]*100,2),0,round(list[0][16]*100,2),0], ['3rd Quarter',round(list[1][17]*100,2),0,round(list[0][17]*100,2),0], ['4th Quarter',round(list[0][18]*100,2),0,round(list[1][18]*100,2),0],
['Winning by 9+',round(list[1][13]*100,2),0,round(list[0][13]*100,2),0], ['Winning by 1-8',round(list[1][10]*100,2),0,round(list[0][10]*100,2),0], ['Tied',round(list[1][12]*100,2),0,round(list[0][12]*100,2),0], ['Losing by 1-8',round(list[1][11]*100,2),0,round(list[0][11]*100,2),0], ['Losing by 9+',round(list[1][14]*100,2),0,round(list[0][14]*100,2),0],
['1st and 10',round(list[1][0]*100,2),0,round(list[0][0]*100,2),0], ['2nd and Short',round(list[1][1]*100,2),0,round(list[0][1]*100,2),0], ['2nd and Long',round(list[1][2]*100,2),0,round(list[0][2]*100,2),0], 
['3rd and Short',round(list[1][3]*100,2),0,round(list[0][3]*100,2),0], ['3rd and Long',round(list[1][4]*100,2),0,round(list[0][4]*100,2),0], ['4th and Short',round(list[1][5]*100,2),0,round(list[0][5]*100,2),0], 
['4th and Long',round(list[1][6]*100,2),0,round(list[0][6]*100,2),0], ['Goal to go',round(list[1][7]*100,2),0,round(list[0][7]*100,2),0], ['Red Zone', round(list[1][8]*100,2),0,round(list[0][8]*100,2),0],['FG Range', round(list[1][9]*100,2),0,round(list[0][9]*100,2),0]]
    data_frame = pd.DataFrame(data_list,columns = ['Situation', 'Blitz%', 'EPA/Blitz','Stunt%','EPA/Stunt'])
    return data_frame.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)


