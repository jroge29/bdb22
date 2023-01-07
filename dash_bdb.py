import dash
from dash import html, dcc, dash_table
import pandas as pd
import pandas as pd

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
['3rd and Long',0,0,0,0], ['4th and Short',0,0,0,0], ['4th and Long',0,0,0,0], ['Goal to go',0,0,0,0]]
table10 = pd.DataFrame(t1,columns = ['Situation', 'Blitz%', 'EPA/Blitz','Stunt%','EPA/Stunt'])
table1 = dash_table.DataTable(
    id = 'table1', data=table10.to_dict('records'),
    columns=[{'name': col, 'id': col} for col in table10.columns]
)

# t2 = []
# table20 = pd.DataFrame(t2,columns = ['Situation', 'Blitz%', 'EPA/Blitz','Stunt%','EPA/Stunt'])
# table2 = dash_table.DataTable(
#     id = 'table2', data=table20.to_dict('records'),
#     columns=[{'name': col, 'id': col} for col in table20.columns]
# )

# t3 = []
# table30 = pd.DataFrame(t3,columns = ['Down & Distance', 'Blitz%', 'EPA/Blitz','Stunt%','EPA/Stunt'])
# table3 = dash_table.DataTable(
#     id = 'table3',data=table30.to_dict('records'),
#     columns=[{'name': col, 'id': col} for col in table30.columns]
# )

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
        ' ', id='demo-dropdown', style={'textAlign': 'center', 'font-family': 'Verdana'}
    ),
    html.Div(id='dd-output-container'),
    html.Div(table1, style={'width': '33%', 'float': 'left'}),
    # html.Div(table2, style={'width': '33%', 'float': 'left'}),
    # html.Div(table3, style={'width': '33%', 'float': 'left'}),
])


vikings = [1]*69
vikings[0] = 'MIN'
bears = [2]*69
bears[0] = 'CHI'


@app.callback( 
    dash.dependencies.Output('table1', 'data'),
    dash.dependencies.Input('demo-dropdown', 'value')
)


def update_tables(value):
    team = bears #turn into helper function that finds team from it, then changes all of the values
    #we want to alter the dataframe, then send it back
    data_list = [['1st Quarter',bears[3],bears[4],bears[5],bears[6]], ['2nd Quarter',0,0,0,0], ['3rd Quarter',0,0,0,0], ['4th Quarter',0,0,0,0],
['Winning by 9+',0,0,0,0], ['Winning by 1-8',0,0,0,0], ['Tied',0,0,0,0], ['Losing by 1-8',0,0,0,0], ['Losing by 9+',0,0,0,0],
['1st and 10',0,0,0,0], ['2nd and Short',0,0,0,0], ['2nd and Long',0,0,0,0], ['3rd and Short',0,0,0,0], 
['3rd and Long',0,0,0,0], ['4th and Short',0,0,0,0], ['4th and Long',0,0,0,0], ['Goal to go',0,0,0,0]]
    data_frame = pd.DataFrame(data_list,columns = ['Situation', 'Blitz%', 'EPA/Blitz','Stunt%','EPA/Stunt'])
    return data_frame.to_dict('records')

def team(val): #helper method for finding which list to pick and use
    list = []
    return list

if __name__ == '__main__':
    app.run_server(debug=True)

