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


## all_stunts.csv
all_stunts = pd.read_csv('test_csv.csv')
## big data bowl games.csv
games = pd.read_csv('games.csv')
games = games[['gameId','homeTeamAbbr','visitorTeamAbbr']]
all_stunts = all_stunts.merge(games,on='gameId',how = 'left')
all_stunts['yardsToEZ'] = all_stunts.absoluteYardlineNumber - 10
all_stunts['pointDifferential'] = np.where(all_stunts.possessionTeam == all_stunts.homeTeamAbbr,
                                   all_stunts.preSnapVisitorScore - all_stunts.preSnapHomeScore,
                                   all_stunts.preSnapHomeScore - all_stunts.preSnapVisitorScore)
all_stunts['min_sec'] = all_stunts.gameClock.map(lambda x:x.split(':'))
all_stunts['quarterTimeLeft'] = all_stunts.min_sec.map(lambda x:(int(x[0])*60)+int(x[1]))
all_stunts['gameTimeLeft'] = (4 - all_stunts.quarter)*15*60 + all_stunts.quarterTimeLeft
all_stunts = all_stunts.rename(columns = {"('blitz', 'mean')":"blitz",
                             "('blitz_class', '')":"blitz_class",
                             "('stunt', '')":"stunt",
                             "('stunt_class', '')":"stunt_class"})
# all_stunts = all_stunts.drop(all_stunts.index[0])
all_stunts['gameId'] = all_stunts.gameId.astype('int64')
all_stunts['playId'] = all_stunts.playId.astype('int64')
all_stunts = all_stunts.drop(['Unnamed: 0'], axis = 1)
all_stunts = all_stunts.dropna(subset = ['yardsToEZ'])
all_stunts['gameplayId'] = all_stunts.apply(lambda row:str(row.loc['gameId'])+"_"+str(row.loc['playId']), axis=1)
all_stunts = all_stunts.drop(['...1','possessionTeam','yardlineNumber','yardlineSide','playDescription','preSnapHomeScore',
                              'preSnapVisitorScore','offenseFormation', 'personnelO', 'defendersInBox','personnelD', 'dropBackType',
                              'pff_passCoverage','pff_passCoverageType','gameId','playId','penaltyYards','prePenaltyPlayResult','foulName1', 'foulNFLId1',
                              'foulName2','foulNFLId2', 'foulName3','foulNFLId3','absoluteYardlineNumber','pff_playAction','visitorTeamAbbr','homeTeamAbbr',
                              'min_sec'],axis = 1)
all_stunts.iloc[0]
     

def calculate_epa_blitzes(team, all_stunts):
    tm = all_stunts.loc[all_stunts.defensiveTeam == team]
    
    ## when blitzing
    q = tm.loc[tm.blitz==1].groupby('quarter').epa.mean().values
    q1,q2,q3,q4 = q[0],q[1],q[2],q[3]

    first10 = tm.loc[(tm.down == 1)&(tm.yardsToGo==10)&(tm.blitz == 1)].epa.mean()
    secondShort = tm.loc[(tm.down == 2)&(tm.yardsToGo<5)&(tm.blitz == 1)].epa.mean()
    secondLong = tm.loc[(tm.down == 2)&(tm.yardsToGo>=5)&(tm.blitz == 1)].epa.mean()
    thirdShort = tm.loc[(tm.down == 3)&(tm.yardsToGo<5)&(tm.blitz == 1)].epa.mean()
    thirdLong = tm.loc[(tm.down == 3)&(tm.yardsToGo>=5)&(tm.blitz == 1)].epa.mean()
    fourthShort = tm.loc[(tm.down == 4)&(tm.yardsToGo<5)&(tm.blitz == 1)].epa.mean()
    fourthLong = tm.loc[(tm.down == 4)&(tm.yardsToGo>=5)&(tm.blitz == 1)].epa.mean()

    g2g = tm.loc[(tm.yardsToEZ < 10)&(tm.blitz==1)].epa.mean()
    redzone = tm.loc[(tm.yardsToEZ < 20)&(tm.blitz==1)].epa.mean()
    fgRange = tm.loc[(tm.yardsToEZ < 45)&(tm.blitz==1)].epa.mean()

    singleScoreW = tm.loc[(tm.pointDifferential <= 8)&(tm.pointDifferential > 0)&(tm.blitz == 1)].epa.mean()
    singleScoreL = tm.loc[(tm.pointDifferential >= -8)&(tm.pointDifferential < 0)&(tm.blitz == 1)].epa.mean()
    scoreT = tm.loc[(tm.pointDifferential == 0)&(tm.blitz == 1)].epa.mean()
    multScoreW = tm.loc[(tm.pointDifferential >= 8)&(tm.blitz == 1)].epa.mean()
    multScoreL = tm.loc[(tm.pointDifferential < -8)&(tm.blitz == 1)].epa.mean()

    epa_blitzing = np.array([first10,secondShort,secondLong,thirdShort,thirdLong,fourthShort,fourthLong,g2g,
                             redzone,fgRange,singleScoreW,singleScoreL,scoreT,multScoreW,multScoreL,q1,q2,q3,q4])

    ## when not blitzing
    q = tm.loc[tm.blitz==0].groupby('quarter').epa.mean().values
    q1,q2,q3,q4 = q[0],q[1],q[2],q[3]

    first10 = tm.loc[(tm.down == 1)&(tm.yardsToGo==10)&(tm.blitz == 0)].epa.mean()
    secondShort = tm.loc[(tm.down == 2)&(tm.yardsToGo<5)&(tm.blitz == 0)].epa.mean()
    secondLong = tm.loc[(tm.down == 2)&(tm.yardsToGo>=5)&(tm.blitz == 0)].epa.mean()
    thirdShort = tm.loc[(tm.down == 3)&(tm.yardsToGo<5)&(tm.blitz == 0)].epa.mean()
    thirdLong = tm.loc[(tm.down == 3)&(tm.yardsToGo>=5)&(tm.blitz == 0)].epa.mean()
    fourthShort = tm.loc[(tm.down == 4)&(tm.yardsToGo<5)&(tm.blitz == 0)].epa.mean()
    fourthLong = tm.loc[(tm.down == 4)&(tm.yardsToGo>=5)&(tm.blitz == 0)].epa.mean()

    g2g = tm.loc[(tm.yardsToEZ < 10)&(tm.blitz==0)].epa.mean()
    redzone = tm.loc[(tm.yardsToEZ < 20)&(tm.blitz==0)].epa.mean()
    fgRange = tm.loc[(tm.yardsToEZ < 45)&(tm.blitz==0)].epa.mean()

    singleScoreW = tm.loc[(tm.pointDifferential <= 8)&(tm.pointDifferential > 0)&(tm.blitz == 0)].epa.mean()
    singleScoreL = tm.loc[(tm.pointDifferential >= -8)&(tm.pointDifferential < 0)&(tm.blitz == 0)].epa.mean()
    scoreT = tm.loc[(tm.pointDifferential == 0)&(tm.blitz == 0)].epa.mean()
    multScoreW = tm.loc[(tm.pointDifferential >= 8)&(tm.blitz == 0)].epa.mean()
    multScoreL = tm.loc[(tm.pointDifferential < -8)&(tm.blitz == 0)].epa.mean()


    epa_not_blitzing = np.array([first10,secondShort,secondLong,thirdShort,thirdLong,fourthShort,fourthLong,g2g,
                             redzone,fgRange,singleScoreW,singleScoreL,scoreT,multScoreW,multScoreL,q1,q2,q3,q4])

    ## how much does the offense lose in epa when the defense blitzes vs. normal
    delta_epa = epa_blitzing - epa_not_blitzing

    return [epa_blitzing,epa_not_blitzing,delta_epa]
     

def calculate_epa_stunts(team, all_stunts):
    tm = all_stunts.loc[all_stunts.defensiveTeam == team]
    
    ## when stunting
    q = tm.loc[tm.stunt==1].groupby('quarter').epa.mean().values
    q1,q2,q3,q4 = q[0],q[1],q[2],q[3]

    first10 = tm.loc[(tm.down == 1)&(tm.yardsToGo==10)&(tm.stunt == 1)].epa.mean()
    secondShort = tm.loc[(tm.down == 2)&(tm.yardsToGo<5)&(tm.stunt == 1)].epa.mean()
    secondLong = tm.loc[(tm.down == 2)&(tm.yardsToGo>=5)&(tm.stunt == 1)].epa.mean()
    thirdShort = tm.loc[(tm.down == 3)&(tm.yardsToGo<5)&(tm.stunt == 1)].epa.mean()
    thirdLong = tm.loc[(tm.down == 3)&(tm.yardsToGo>=5)&(tm.stunt == 1)].epa.mean()
    fourthShort = tm.loc[(tm.down == 4)&(tm.yardsToGo<5)&(tm.stunt == 1)].epa.mean()
    fourthLong = tm.loc[(tm.down == 4)&(tm.yardsToGo>=5)&(tm.stunt == 1)].epa.mean()

    g2g = tm.loc[(tm.yardsToEZ < 10)&(tm.stunt==1)].epa.mean()
    redzone = tm.loc[(tm.yardsToEZ < 20)&(tm.stunt==1)].epa.mean()
    fgRange = tm.loc[(tm.yardsToEZ < 45)&(tm.stunt==1)].epa.mean()

    singleScoreW = tm.loc[(tm.pointDifferential <= 8)&(tm.pointDifferential > 0)&(tm.stunt == 1)].epa.mean()
    singleScoreL = tm.loc[(tm.pointDifferential >= -8)&(tm.pointDifferential < 0)&(tm.stunt == 1)].epa.mean()
    scoreT = tm.loc[(tm.pointDifferential == 0)&(tm.stunt == 1)].epa.mean()
    multScoreW = tm.loc[(tm.pointDifferential >= 8)&(tm.stunt == 1)].epa.mean()
    multScoreL = tm.loc[(tm.pointDifferential < -8)&(tm.stunt == 1)].epa.mean()

    epa_stunting = np.array([first10,secondShort,secondLong,thirdShort,thirdLong,fourthShort,fourthLong,g2g,
                             redzone,fgRange,singleScoreW,singleScoreL,scoreT,multScoreW,multScoreL,q1,q2,q3,q4])

    ## when not stunting
    q = tm.loc[tm.stunt==0].groupby('quarter').epa.mean().values
    q1,q2,q3,q4 = q[0],q[1],q[2],q[3]

    first10 = tm.loc[(tm.down == 1)&(tm.yardsToGo==10)&(tm.stunt == 0)].epa.mean()
    secondShort = tm.loc[(tm.down == 2)&(tm.yardsToGo<5)&(tm.stunt == 0)].epa.mean()
    secondLong = tm.loc[(tm.down == 2)&(tm.yardsToGo>=5)&(tm.stunt == 0)].epa.mean()
    thirdShort = tm.loc[(tm.down == 3)&(tm.yardsToGo<5)&(tm.stunt == 0)].epa.mean()
    thirdLong = tm.loc[(tm.down == 3)&(tm.yardsToGo>=5)&(tm.stunt == 0)].epa.mean()
    fourthShort = tm.loc[(tm.down == 4)&(tm.yardsToGo<5)&(tm.stunt == 0)].epa.mean()
    fourthLong = tm.loc[(tm.down == 4)&(tm.yardsToGo>=5)&(tm.stunt == 0)].epa.mean()

    g2g = tm.loc[(tm.yardsToEZ < 10)&(tm.stunt==0)].epa.mean()
    redzone = tm.loc[(tm.yardsToEZ < 20)&(tm.stunt==0)].epa.mean()
    fgRange = tm.loc[(tm.yardsToEZ < 45)&(tm.stunt==0)].epa.mean()

    singleScoreW = tm.loc[(tm.pointDifferential <= 8)&(tm.pointDifferential > 0)&(tm.stunt == 0)].epa.mean()
    singleScoreL = tm.loc[(tm.pointDifferential >= -8)&(tm.pointDifferential < 0)&(tm.stunt == 0)].epa.mean()
    scoreT = tm.loc[(tm.pointDifferential == 0)&(tm.stunt == 0)].epa.mean()
    multScoreW = tm.loc[(tm.pointDifferential >= 8)&(tm.stunt == 0)].epa.mean()
    multScoreL = tm.loc[(tm.pointDifferential < -8)&(tm.stunt == 0)].epa.mean()


    epa_not_stunting = np.array([first10,secondShort,secondLong,thirdShort,thirdLong,fourthShort,fourthLong,g2g,
                             redzone,fgRange,singleScoreW,singleScoreL,scoreT,multScoreW,multScoreL,q1,q2,q3,q4])

    ## how much does the offense lose in epa when the defense stunts vs. normal
    delta_epa = epa_stunting - epa_not_stunting
    
    return [epa_stunting,epa_not_stunting,delta_epa]
     

## team is abbreviation, all_stunts is all_stunts.csv
def when_they_blitz(team,all_stunts):
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
    sr_first10 = tm[tm.stunt == 1].first10.sum()/total_plays
    sr_secondShort = tm[tm.stunt == 1].secondShort.sum()/total_plays
    sr_secondLong = tm[tm.stunt == 1].secondLong.sum()/total_plays
    sr_thirdShort = tm[tm.stunt == 1].thirdShort.sum()/total_plays
    sr_thirdLong = tm[tm.stunt == 1].thirdLong.sum()/total_plays
    sr_fourthShort = tm[tm.stunt == 1].fourthShort.sum()/total_plays
    sr_fourthLong = tm[tm.stunt == 1].fourthLong.sum()/total_plays
    
    sr_G2G = tm[(tm.stunt == 1) & (tm.yardsToEZ <= 10)].stunt.count()/total_plays
    sr_redzone = tm[(tm.stunt == 1) & (tm.yardsToEZ <= 20)].stunt.count()/total_plays
    sr_fgRange = tm[(tm.stunt == 1) & (tm.yardsToEZ <= 45)].stunt.count()/total_plays
    
    sr_singleScoreW = tm[(tm.stunt == 1) &
                         (tm.pointDifferential <= 8) &
                         (tm.pointDifferential > 0)].stunt.count()/total_plays
    sr_singleScoreL = tm[(tm.stunt == 1) &
                         (tm.pointDifferential >= -8) &
                         (tm.pointDifferential < 0)].stunt.count()/total_plays
    sr_singleScoreT = tm[(tm.stunt == 1) &
                         (tm.pointDifferential == 0)].stunt.count()/total_plays
    sr_multScoreW = tm[(tm.stunt == 1) & (tm.pointDifferential > 8)].stunt.count()/total_plays
    sr_multScoreL = tm[(tm.stunt == 1) & (tm.pointDifferential < -8)].stunt.count()/total_plays
                       
    sr_quarterOne = tm[(tm.stunt == 1) & (tm.quarter == 1)].stunt.count()/total_plays
    sr_quarterTwo = tm[(tm.stunt == 1) & (tm.quarter == 2)].stunt.count()/total_plays
    sr_quarterThree = tm[(tm.stunt == 1) & (tm.quarter == 3)].stunt.count()/total_plays
    sr_quarterFour = tm[(tm.stunt == 1) & (tm.quarter == 4)].stunt.count()/total_plays
    stunt_rates = [sr_first10,sr_secondShort,sr_secondLong,sr_thirdShort,sr_thirdLong,
            sr_fourthShort,sr_fourthLong,sr_G2G,sr_redzone,sr_fgRange,sr_singleScoreW,
            sr_singleScoreL,sr_singleScoreT,sr_multScoreW,sr_multScoreL,sr_quarterOne,
            sr_quarterTwo,sr_quarterThree,sr_quarterFour]
    
    ## blitz rates
    br_first10 = tm[tm.blitz == 1].first10.sum()/total_plays
    br_secondShort = tm[tm.blitz == 1].secondShort.sum()/total_plays
    br_secondLong = tm[tm.blitz == 1].secondLong.sum()/total_plays
    br_thirdShort = tm[tm.blitz == 1].thirdShort.sum()/total_plays
    br_thirdLong = tm[tm.blitz == 1].thirdLong.sum()/total_plays
    br_fourthShort = tm[tm.blitz == 1].fourthShort.sum()/total_plays
    br_fourthLong = tm[tm.blitz == 1].fourthLong.sum()/total_plays
    
    br_G2G = tm[(tm.blitz == 1) & (tm.yardsToEZ <= 10)].blitz.count()/total_plays
    br_redzone = tm[(tm.blitz == 1) & (tm.yardsToEZ <= 20)].blitz.count()/total_plays
    br_fgRange = tm[(tm.blitz == 1) & (tm.yardsToEZ <= 45)].blitz.count()/total_plays
    
    br_singleScoreW = tm[(tm.blitz == 1) &
                         (tm.pointDifferential <= 8) &
                         (tm.pointDifferential > 0)].blitz.count()/total_plays
    br_singleScoreL = tm[(tm.blitz == 1) &
                         (tm.pointDifferential >= -8) &
                         (tm.pointDifferential < 0)].blitz.count()/total_plays
    br_singleScoreT = tm[(tm.blitz == 1) &
                         (tm.pointDifferential == 0)].blitz.count()/total_plays
    br_multScoreW = tm[(tm.blitz == 1) & (tm.pointDifferential > 8)].blitz.count()/total_plays
    br_multScoreL = tm[(tm.blitz == 1) & (tm.pointDifferential < -8)].blitz.count()/total_plays
                       
    br_quarterOne = tm[(tm.blitz == 1) & (tm.quarter == 1)].blitz.count()/total_plays
    br_quarterTwo = tm[(tm.blitz == 1) & (tm.quarter == 2)].blitz.count()/total_plays
    br_quarterThree = tm[(tm.blitz == 1) & (tm.quarter == 3)].blitz.count()/total_plays
    br_quarterFour = tm[(tm.blitz == 1) & (tm.quarter == 4)].blitz.count()/total_plays
    
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
    nfl_team = teams[value]
    list = when_they_blitz(nfl_team, all_stunts)
    epa_stunt = calculate_epa_stunts(nfl_team, all_stunts)
    epa_blitz = calculate_epa_blitzes(nfl_team, all_stunts)

    data_list = [['1st Quarter',round(list[1][15]*100,2),round(epa_blitz[0][15],3),round(list[0][15]*100,2),round(epa_stunt[0][15],3)], ['2nd Quarter',round(list[1][16]*100,2),round(epa_blitz[0][16],3),round(list[0][16]*100,2),round(epa_stunt[0][16],3)], ['3rd Quarter',round(list[1][17]*100,2),round(epa_blitz[0][17],3),round(list[0][17]*100,2),round(epa_stunt[0][17],3)], ['4th Quarter',round(list[0][18]*100,2),round(epa_blitz[0][18],3),round(list[1][18]*100,2),round(epa_stunt[0][18],3)],
['Winning by 9+',round(list[1][13]*100,2),round(epa_blitz[0][13],3),round(list[0][13]*100,2),round(epa_stunt[0][13],3)], ['Winning by 1-8',round(list[1][10]*100,2),round(epa_blitz[0][10],3),round(list[0][10]*100,2),round(epa_stunt[0][13],3)], ['Tied',round(list[1][12]*100,2),round(epa_blitz[0][12],3),round(list[0][12]*100,2),round(epa_stunt[0][12],3)], ['Losing by 1-8',round(list[1][11]*100,2),round(epa_blitz[0][11],3),round(list[0][11]*100,2),round(epa_stunt[0][11],3)], ['Losing by 9+',round(list[1][14]*100,2),round(epa_blitz[0][14],3),round(list[0][14]*100,2),round(epa_stunt[0][14],3)],
['1st and 10',round(list[1][0]*100,2),round(epa_blitz[0][0],3),round(list[0][0]*100,2),round(epa_stunt[0][0],3)], ['2nd and Short',round(list[1][1]*100,2),round(epa_blitz[0][1],3),round(list[0][1]*100,2),round(epa_stunt[0][1],3)], ['2nd and Long',round(list[1][2]*100,2),round(epa_blitz[0][2],3),round(list[0][2]*100,2),round(epa_stunt[0][2],3)], 
['3rd and Short',round(list[1][3]*100,2),round(epa_blitz[0][3],3),round(list[0][3]*100,2),round(epa_stunt[0][3],3)], ['3rd and Long',round(list[1][4]*100,2),round(epa_blitz[0][4],3),round(list[0][4]*100,2),round(epa_stunt[0][4],3)], ['4th and Short',round(list[1][5]*100,2),round(epa_blitz[0][5],3),round(list[0][5]*100,2),round(epa_stunt[0][5],3)], 
['4th and Long',round(list[1][6]*100,2),round(epa_blitz[0][6],3),round(list[0][6]*100,2),round(epa_stunt[0][6],3)], ['Goal to go',round(list[1][7]*100,2),round(epa_blitz[0][7],3),round(list[0][7]*100,2),round(epa_stunt[0][7],3)], ['Red Zone', round(list[1][8]*100,2),round(epa_blitz[0][8],3),round(list[0][8]*100,2),round(epa_stunt[0][8],3)],['FG Range', round(list[1][9]*100,2),round(epa_blitz[0][9],3),round(list[0][9]*100,2),round(epa_stunt[0][9],3)]]
    data_frame = pd.DataFrame(data_list,columns = ['Situation', 'Blitz%', 'EPA/Blitz','Stunt%','EPA/Stunt'])
    return data_frame.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)


