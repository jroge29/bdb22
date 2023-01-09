from turtle import goto
import dash
from dash import html, dcc, dash_table
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import date, timedelta, datetime
from scipy import stats
import math
import re
import random


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
['3rd and Long',0,0,0,0], ['4th and Short',0,0,0,0], ['4th and Long',0,0,0,0], ['Goal to go',0,0,0,0], ['Red Zone',0,0,0,0, ],['FG Range',0,0,0,0],['Four Man Front',0,0,0,0]]
table10 = pd.DataFrame(t1,columns = ['Situation', '%Blitz', 'EPA/Blitz','%Stunt','EPA/Stunt'])
table1 = dash_table.DataTable(
    id = 'table1', data=table10.to_dict('records'),
    columns=[{'name': col, 'id': col} for col in table10.columns],
    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['Date', 'Region']
    ],
    style_data={
        'color': 'black',
        'backgroundColor': 'white'
    },
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }
    ],style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'color': 'black',
        'fontWeight': 'bold'
    }
)
graph = dcc.Graph(id='visual1',style={'width': '1vw', 'height': '1vh'})
t2 = [['Common Blitz 1', 0,0,0],['Common Blitz 2',0,0,0],['Common Blitz 3',0,0,0],['Common Stunt 1',0,0,0],['Common Stunt 2',0,0,0],['Common Stunt 3',0,0,0]]
table20 = pd.DataFrame(t2, columns = ['Most Common Blitzes/Stunts','%Rate','EPA/Play','Classification Number'])
table2 = dash_table.DataTable(
    id = 'table2', data=table20.to_dict('records'),
    columns=[{'name': col, 'id': col} for col in table20.columns],
    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['Date', 'Region']
    ],
    style_data={
        'color': 'black',
        'backgroundColor': 'white'
    },
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }
    ],style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'color': 'black',
        'fontWeight': 'bold'
    }
)

app.layout = html.Div([
    html.H1(children="Stunt & Blitz Guide", style={'textAlign': 'center', 'font-family': 'Verdana'}),
    html.P(
        children="Pick a defense to get a scouting report on their most common and effective blitz packages and stunts ran. Negative EPA means good defense.",
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
    html.Div(table1, style={'width': '45%', 'float': 'left'}),
    html.Div(graph, style = {'width': '50%', 'float': 'right'}),
    html.Div(table2, style = {'width': '33%'})

])


## all_stunts.csv
all_stunts = pd.read_csv('with_epa.csv')
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
                             "('stunt_class', '')":"stunt_class","('4manfront', '')":"manfront",
                             "('npos_list', '')":"npos_list"})
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
                              'min_sec','npos_list'],axis = 1)
all_stunts.iloc[0]

def visualize_blitz_stunt(play_type, team, common_vs_effective,num_plays,only_4man):
    cve = common_vs_effective ## for simplicity
    pt = play_type ## for simplicity
    if only_4man:
        tm = all_stunts.loc[(all_stunts.defensiveTeam == team) & (all_stunts.manfront == 1)]
    else:
        tm = all_stunts.loc[all_stunts.defensiveTeam == team]
    
    ## stunt/blitz rate section
    if pt == 'stunt':
        play_count = tm.loc[tm.stunt == 1].shape[0] ## delete .loc[tm.stunt == 1] if you want it stunt rate out of all plays
        if cve == 'common':
            tm = pd.DataFrame(tm.groupby('stunt_class').stunt.count())
            tm['stunt'] = tm.stunt/play_count
            tm = tm.drop(tm.index[0])
            tm = tm.sort_values(['stunt'],ascending=False)
            tm = tm.iloc[0:num_plays]
            play_class = tm.index.values
            play_rates = tm.stunt.values
        if cve == 'effective':
            tm = pd.DataFrame(tm.groupby('stunt_class').epa.mean())
            tm = tm.drop(tm.index[0])
            tm = tm.sort_values(['epa'])
            tm = tm.iloc[0:num_plays]
            play_class = tm.index.values
            play_rates = tm.epa.values
    elif pt == 'blitz':
        play_count = tm.loc[tm.blitz == 1].shape[0] ## delete .loc[tm.stunt == 1] if you want it stunt rate out of all plays
        if cve == 'common':
            tm = pd.DataFrame(tm.groupby('blitz_class').blitz.count())
            tm['blitz'] = tm.blitz/play_count
            tm = tm.drop(tm.index[0])
            tm = tm.sort_values(['blitz'],ascending=False)
            tm = tm.iloc[0:num_plays]
            play_class = tm.index.values
            play_rates = tm.blitz.values
        if cve == 'effective':
            tm = pd.DataFrame(tm.groupby('blitz_class').epa.mean())
            tm = tm.drop(tm.index[0])
            tm = tm.sort_values(['epa'])
            tm = tm.iloc[0:num_plays]
            play_class = tm.index.values
            play_rates = tm.epa.values
    
    ## visualization section
    if pt == 'blitz':
        stunts = pd.DataFrame(all_stunts.loc[(all_stunts.blitz_class == play_class[0])&(all_stunts.defensiveTeam == team)])
    if pt == 'stunt':
        stunts = pd.DataFrame(all_stunts.loc[(all_stunts.stunt_class == play_class[0])&(all_stunts.defensiveTeam == team)])
    if only_4man:
        stunts = stunts.loc[stunts.manfront == 1]
    ids = stunts.gameplayId.iloc[0].split('_')
    gameId = int(ids[0])
    playId = int(ids[1])
    classnum = play_class[0]
    fig_1 = animate_play(all_weeks,plays,players,pff,gameId,playId,classnum)
    
    return fig_1

colors = {
'ARI':"#97233F", 
'ATL':"#A71930", 
'BAL':'#241773', 
'BUF':"#00338D", 
'CAR':"#0085CA", 
'CHI':"#C83803", 
'CIN':"#FB4F14", 
'CLE':"#311D00", 
'DAL':'#003594',
'DEN':"#FB4F14", 
'DET':"#0076B6", 
'GB':"#203731", 
'HOU':"#03202F", 
'IND':"#002C5F", 
'JAX':"#9F792C", 
'KC':"#E31837", 
'LA':"#003594", 
'LAC':"#0080C6", 
'LV':"#000000",
'MIA':"#008E97", 
'MIN':"#4F2683", 
'NE':"#002244", 
'NO':"#D3BC8D", 
'NYG':"#0B2265", 
'NYJ':"#125740", 
'PHI':"#004C54", 
'PIT':"#FFB612", 
'SEA':"#69BE28", 
'SF':"#AA0000",
'TB':'#D50A0A', 
'TEN':"#4B92DB", 
'WAS':"#5A1414", 
'football':'#CBB67C'
}

plays = pd.read_csv('plays.csv')
# week1 = pd.read_csv('/kaggle/input/nfl-big-data-bowl-2023/week1.csv')
pff = pd.read_csv('pffScoutingData.csv')
players = pd.read_csv('players.csv')

week1 = pd.read_csv('week1.csv')
week2 = pd.read_csv('week2.csv')
week3 = pd.read_csv('week3.csv')
week4 = pd.read_csv('week4.csv')
week5 = pd.read_csv('week5.csv')
week6 = pd.read_csv('week6.csv')
week7 = pd.read_csv('week7.csv')
week8 = pd.read_csv('week8.csv')
all_weeks = pd.concat([week1,week2,week3,week4,week5,week6,week7,week8])

def animate_play(tracking_df, play_df,players,pffScoutingData, gameId,playId,classnum):
       
    selected_play_df = play_df[(play_df.playId==playId)&(play_df.gameId==gameId)].copy()
    
    tracking_players_df = pd.merge(tracking_df,players,how="left",on = "nflId")
    tracking_players_df = pd.merge(tracking_players_df,pffScoutingData,how="left",on = ["nflId","playId","gameId"])
    selected_tracking_df = tracking_players_df[(tracking_players_df.playId==playId)&(tracking_players_df.gameId==gameId)].copy()

    sorted_frame_list = selected_tracking_df.frameId.unique()
    sorted_frame_list.sort()

    # get play General information 
    line_of_scrimmage = selected_play_df.absoluteYardlineNumber.values[0]
    first_down_marker = line_of_scrimmage + selected_play_df.yardsToGo.values[0]
    down = selected_play_df.down.values[0]
    quarter = selected_play_df.quarter.values[0]
    gameClock = selected_play_df.gameClock.values[0]
    playDescription = selected_play_df.playDescription.values[0]
    # Handle case where we have a really long Play Description and want to split it into two lines
    if len(playDescription.split(" "))>15 and len(playDescription)>115:
        playDescription = " ".join(playDescription.split(" ")[0:16]) + "<br>" + " ".join(playDescription.split(" ")[16:])

    # initialize plotly start and stop buttons for animation
    updatemenus_dict = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 100, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 0}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]
    # initialize plotly slider to show frame position in animation
    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Frame:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }
    frames = []
    for frameId in sorted_frame_list:
        data = []
        # Add Numbers to Field 
        data.append(
            go.Scatter(
                x=np.arange(20,110,10), 
                y=[5]*len(np.arange(20,110,10)),
                mode='text',
                text=list(map(str,list(np.arange(20, 61, 10)-10)+list(np.arange(40, 9, -10)))),
                textfont_size = 30,
                textfont_family = "Courier New, monospace",
                textfont_color = "#ffffff",
                showlegend=False,
                hoverinfo='none'
            )
        )
        data.append(
            go.Scatter(
                x=np.arange(20,110,10), 
                y=[53.5-5]*len(np.arange(20,110,10)),
                mode='text',
                text=list(map(str,list(np.arange(20, 61, 10)-10)+list(np.arange(40, 9, -10)))),
                textfont_size = 30,
                textfont_family = "Courier New, monospace",
                textfont_color = "#ffffff",
                showlegend=False,
                hoverinfo='none'
            )
        )
        # Add line of scrimage 
        data.append(
            go.Scatter(
                x=[line_of_scrimmage,line_of_scrimmage], 
                y=[0,53.5],
                line_dash='dash',
                line_color='blue',
                showlegend=False,
                hoverinfo='none'
            )
        )
        # Add First down line 
        data.append(
            go.Scatter(
                x=[first_down_marker,first_down_marker], 
                y=[0,53.5],
                line_dash='dash',
                line_color='yellow',
                showlegend=False,
                hoverinfo='none'
            )
        )
        # Plot Players
        for team in selected_tracking_df.team.unique():
            plot_df = selected_tracking_df[(selected_tracking_df.team==team)&(selected_tracking_df.frameId==frameId)].copy()
            if team != "football":
                hover_text_array=[]
                for nflId in plot_df.nflId:
                    selected_player_df = plot_df[plot_df.nflId==nflId]
                    hover_text_array.append("nflId:{}<br>displayName:{}<br>Position:{}<br>Role:{}".format(selected_player_df["nflId"].values[0],
                                                                                      selected_player_df["displayName"].values[0],
                                                                                      selected_player_df["pff_positionLinedUp"].values[0],
                                                                                      selected_player_df["pff_role"].values[0]))
                data.append(go.Scatter(x=plot_df["x"], y=plot_df["y"],mode = 'markers',marker_color=colors[team],name=team,hovertext=hover_text_array,hoverinfo="text"))
            else:
                data.append(go.Scatter(x=plot_df["x"], y=plot_df["y"],mode = 'markers',marker_color=colors[team],name=team,hoverinfo='none'))
        # add frame to slider
        slider_step = {"args": [
            [frameId],
            {"frame": {"duration": 100, "redraw": False},
             "mode": "immediate",
             "transition": {"duration": 0}}
        ],
            "label": str(frameId),
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)
        frames.append(go.Frame(data=data, name=str(frameId)))

    scale=10
    layout = go.Layout(
        autosize=False,
        width=120*scale,
        height=60*scale,
        xaxis=dict(range=[0, 120], autorange=False, tickmode='array',tickvals=np.arange(10, 111, 5).tolist(),showticklabels=False),
        yaxis=dict(range=[0, 53.3], autorange=False,showgrid=False,showticklabels=False),

        plot_bgcolor='#00B140',
        # Create title and add play description at the bottom of the chart for better visual appeal
        title=f"GameId: {gameId}, PlayId: {playId}<br>{gameClock} {quarter}Q<br>Most common stunt: {classnum}"+"<br>"*19+f"{playDescription}",
        updatemenus=updatemenus_dict,
        sliders = [sliders_dict]
    )

    fig = go.Figure(
        data=frames[0]["data"],
        layout= layout,
        frames=frames[1:]
    )
    # Create First Down Markers 
    for y_val in [0,53]:
        fig.add_annotation(
                x=first_down_marker,
                y=y_val,
                text=str(down),
                showarrow=False,
                font=dict(
                    family="Courier New, monospace",
                    size=16,
                    color="black"
                    ),
                align="center",
                bordercolor="black",
                borderwidth=2,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=1
                )

    return fig

def blitz_stunt_summary(play_type, team,only_4man):
    pt = play_type ## for simplicity
    if only_4man:
        tm = all_stunts.loc[(all_stunts.defensiveTeam == team) & (all_stunts.fourManFront == 1)]
    else:
        tm = all_stunts.loc[all_stunts.defensiveTeam == team]
    
    ## stunt/blitz rate section
    if pt == 'stunt':
        play_count = tm.loc[tm.stunt == 1].shape[0] ## delete .loc[tm.stunt == 1] if you want it stunt rate out of all plays
        tm = pd.DataFrame(tm.groupby('stunt_class').agg({'stunt':'count','epa':np.mean}))
        tm['stunt'] = tm.stunt/play_count
        tm = tm.drop(tm.index[0])
        tm = tm.sort_values(['stunt'],ascending=False)
        tm = tm.iloc[0:3]
        play_class = tm.index.values
        play_rates = tm.stunt.values
        play_epa = tm.epa.values
    elif pt == 'blitz':
        play_count = tm.loc[tm.blitz == 1].shape[0] ## delete .loc[tm.stunt == 1] if you want it stunt rate out of all plays
        tm = pd.DataFrame(tm.groupby('blitz_class').agg({'blitz':'count','epa':np.mean}))
        tm['blitz'] = tm.blitz/play_count
        tm = tm.drop(tm.index[0])
        tm = tm.sort_values(['blitz'],ascending=False)
        tm = tm.iloc[0:3]
        play_class = tm.index.values
        play_rates = tm.blitz.values
        play_epa = tm.epa.values
    
    return play_class,play_rates,play_epa    

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
    fourman = tm.loc[(tm.manfront == 1)&(tm.blitz == 1)].epa.mean()

    epa_blitzing = np.array([first10,secondShort,secondLong,thirdShort,thirdLong,fourthShort,fourthLong,g2g,
                             redzone,fgRange,singleScoreW,singleScoreL,scoreT,multScoreW,multScoreL,q1,q2,q3,q4,fourman])

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
                             redzone,fgRange,singleScoreW,singleScoreL,scoreT,multScoreW,multScoreL,q1,q2,q3,q4,0])

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
    fourman = tm.loc[(tm.manfront == 1)&(tm.stunt == 1)].epa.mean()

    epa_stunting = np.array([first10,secondShort,secondLong,thirdShort,thirdLong,fourthShort,fourthLong,g2g,
                             redzone,fgRange,singleScoreW,singleScoreL,scoreT,multScoreW,multScoreL,q1,q2,q3,q4,fourman])

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
                             redzone,fgRange,singleScoreW,singleScoreL,scoreT,multScoreW,multScoreL,q1,q2,q3,q4,0])

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
    sr_fourman = tm[(tm.stunt == 1) & (tm.manfront == 4)].stunt.count()/total_plays

    stunt_rates = [sr_first10,sr_secondShort,sr_secondLong,sr_thirdShort,sr_thirdLong,
            sr_fourthShort,sr_fourthLong,sr_G2G,sr_redzone,sr_fgRange,sr_singleScoreW,
            sr_singleScoreL,sr_singleScoreT,sr_multScoreW,sr_multScoreL,sr_quarterOne,
            sr_quarterTwo,sr_quarterThree,sr_quarterFour,sr_fourman]
    
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
    br_fourman = tm[(tm.blitz == 1) & (tm.manfront == 1)].blitz.count()/total_plays
    
    blitz_rates = [br_first10,br_secondShort,br_secondLong,br_thirdShort,br_thirdLong,
            br_fourthShort,br_fourthLong,br_G2G,br_redzone,br_fgRange,br_singleScoreW,
            br_singleScoreL,br_singleScoreT,br_multScoreW,br_multScoreL,br_quarterOne,
            br_quarterTwo,br_quarterThree,br_quarterFour,br_fourman]
    
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
    (dash.dependencies.Output('table1', 'data'),dash.dependencies.Output('visual1','figure'), dash.dependencies.Output('table2','data')), 
    [dash.dependencies.Input('demo-dropdown', 'value')])

def update_table_and_graph(value):
    nfl_team = teams[value]
    list = when_they_blitz(nfl_team, all_stunts)
    epa_stunt = calculate_epa_stunts(nfl_team, all_stunts)
    epa_blitz = calculate_epa_blitzes(nfl_team, all_stunts)

    data_list = [['1st Quarter',round(list[1][15]*100,2),round(epa_blitz[0][15],3),round(list[0][15]*100,2),round(epa_stunt[0][15],3)], ['2nd Quarter',round(list[1][16]*100,2),round(epa_blitz[0][16],3),round(list[0][16]*100,2),round(epa_stunt[0][16],3)], ['3rd Quarter',round(list[1][17]*100,2),round(epa_blitz[0][17],3),round(list[0][17]*100,2),round(epa_stunt[0][17],3)], ['4th Quarter',round(list[0][18]*100,2),round(epa_blitz[0][18],3),round(list[1][18]*100,2),round(epa_stunt[0][18],3)],
['Winning by 9+',round(list[1][13]*100,2),round(epa_blitz[0][13],3),round(list[0][13]*100,2),round(epa_stunt[0][13],3)], ['Winning by 1-8',round(list[1][10]*100,2),round(epa_blitz[0][10],3),round(list[0][10]*100,2),round(epa_stunt[0][13],3)], ['Tied',round(list[1][12]*100,2),round(epa_blitz[0][12],3),round(list[0][12]*100,2),round(epa_stunt[0][12],3)], ['Losing by 1-8',round(list[1][11]*100,2),round(epa_blitz[0][11],3),round(list[0][11]*100,2),round(epa_stunt[0][11],3)], ['Losing by 9+',round(list[1][14]*100,2),round(epa_blitz[0][14],3),round(list[0][14]*100,2),round(epa_stunt[0][14],3)],
['1st and 10',round(list[1][0]*100,2),round(epa_blitz[0][0],3),round(list[0][0]*100,2),round(epa_stunt[0][0],3)], ['2nd and Short',round(list[1][1]*100,2),round(epa_blitz[0][1],3),round(list[0][1]*100,2),round(epa_stunt[0][1],3)], ['2nd and Long',round(list[1][2]*100,2),round(epa_blitz[0][2],3),round(list[0][2]*100,2),round(epa_stunt[0][2],3)], 
['3rd and Short',round(list[1][3]*100,2),round(epa_blitz[0][3],3),round(list[0][3]*100,2),round(epa_stunt[0][3],3)], ['3rd and Long',round(list[1][4]*100,2),round(epa_blitz[0][4],3),round(list[0][4]*100,2),round(epa_stunt[0][4],3)], ['4th and Short',round(list[1][5]*100,2),round(epa_blitz[0][5],3),round(list[0][5]*100,2),round(epa_stunt[0][5],3)], 
['4th and Long',round(list[1][6]*100,2),round(epa_blitz[0][6],3),round(list[0][6]*100,2),round(epa_stunt[0][6],3)], ['Goal to go',round(list[1][7]*100,2),round(epa_blitz[0][7],3),round(list[0][7]*100,2),round(epa_stunt[0][7],3)], ['Red Zone', round(list[1][8]*100,2),round(epa_blitz[0][8],3),round(list[0][8]*100,2),round(epa_stunt[0][8],3)],['FG Range', round(list[1][9]*100,2),round(epa_blitz[0][9],3),round(list[0][9]*100,2),round(epa_stunt[0][9],3)],['Four Man Front',round(list[1][19]*100,2),round(epa_blitz[0][19],3),round(list[0][9]*100,2),round(epa_stunt[0][9],3)]]
    data_frame = pd.DataFrame(data_list,columns = ['Situation', '%Blitz', 'EPA/Blitz','%Stunt','EPA/Stunt'])

    stunt_epa_table = visualize_blitz_stunt('stunt',nfl_team,'common',3,False)

    cs = blitz_stunt_summary('stunt',nfl_team,False)
    cb = blitz_stunt_summary('blitz',nfl_team,False)

    d2 = [['Common Blitz 1', round(cb[1][0]*100,2),round(cb[2][0],3),cb[0][0]],['Common Blitz 2',round(cb[1][1]*100,2),round(cb[2][1],3),cb[0][1]],['Common Blitz 3',round(cb[1][2]*100,2),round(cb[2][2],3),cb[0][2]],
    ['Common Stunt 1',round(cs[1][0]*100,2),round(cs[2][0],3),cs[0][0]],['Common Stunt 2',round(cs[1][1]*100,2),round(cs[2][1],3),cs[0][1]],['Common Stunt 3',round(cs[1][2]*100,2),round(cs[2][2],3),cs[0][2]]]
    table2_frame = pd.DataFrame(d2, columns = ['Most Common Blitzes/Stunts','%Rate','EPA/Play','Classification Number'])


    return data_frame.to_dict('records'), stunt_epa_table, table2_frame.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)


