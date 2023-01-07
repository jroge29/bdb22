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
t1 = [['1st Quarter',0,0,0,0], ['2nd Quarter',0,0,0,0], ['3rd Quarter',0,0,0,0], ['4th Quarter',0,0,0,0]]
table10 = pd.DataFrame(t1,columns = ['Quarter', 'Blitz%', 'EPA/Blitz','Stunt%','EPA/Stunt'])
table1 = dash_table.DataTable(
    data=table10.to_dict('records'),
    columns=[{'name': col, 'id': col} for col in table10.columns]
)

t2 = [['Winning by 9+',0,0,0,0], ['Winning by 1-8',0,0,0,0], ['Tied',0,0,0,0], ['Losing by 1-8',0,0,0,0], ['Losing by 9+',0,0,0,0]]
table20 = pd.DataFrame(t2,columns = ['Situation', 'Blitz%', 'EPA/Blitz','Stunt%','EPA/Stunt'])
table2 = dash_table.DataTable(
    data=table20.to_dict('records'),
    columns=[{'name': col, 'id': col} for col in table20.columns]
)

t3 = [['1st and 10',0,0,0,0], ['2nd and Short',0,0,0,0], ['2nd and Long',0,0,0,0], ['3rd and Short',0,0,0,0], ['3rd and Long',0,0,0,0], ['4th and Short',0,0,0,0], ['4th and Long',0,0,0,0], ['Goal to go',0,0,0,0]]
table30 = pd.DataFrame(t3,columns = ['Down & Distance', 'Blitz%', 'EPA/Blitz','Stunt%','EPA/Stunt'])
table3 = dash_table.DataTable(
    id = 'table3',data=table30.to_dict('records'),
    columns=[{'name': col, 'id': col} for col in table30.columns]
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
        ' ', id='demo-dropdown', style={'textAlign': 'center', 'font-family': 'Verdana'}
    ),
    html.Div(id='dd-output-container'),
    html.Div(table1, id='table1', style={'width': '33%', 'float': 'left'}),
    html.Div(table2, id='table2', style={'width': '33%', 'float': 'left'}),
    html.Div(table3, id='table3', style={'width': '33%', 'float': 'left'}),
])


vikings = [1]*69
vikings[0] = 'MIN'
bears = [2]*69
bears[0] = 'CHI'


@app.callback( #this is where the errors are happening. the 'dash_table' does not match what it should be, 'data' does not work either
    [dash.dependencies.Output('table1', 'dash_table'), dash.dependencies.Output('table2', 'dash_table'), dash.dependencies.Output('table3','dash_table')],
    dash.dependencies.Input('demo-dropdown', 'value')
)


def update_tables(value):
    team = bears #turn into helper function that finds team from it, then changes all of the values
    t1 = [['1st Quarter',0,0,2,0], ['2nd Quarter',1,1,1,1], ['3rd Quarter',0,0,0,0], ['4th Quarter',0,0,0,0]] #new instances of the data tables, would have new values
    table10 = pd.DataFrame(t1,columns = ['Quarter', 'Blitz%', 'EPA/Blitz','Stunt%','EPA/Stunt'])
    

    t2 = [['Winning by 9+',0,0,0,0], ['Winning by 1-8',0,1,0,0], ['Tied',0,0,0,0], ['Losing by 1-8',0,0,0,0], ['Losing by 9+',0,0,0,0]]
    table20 = pd.DataFrame(t2,columns = ['Situation', 'Blitz%', 'EPA/Blitz','Stunt%','EPA/Stunt'])
    

    t3 = [['1st and 10',0,0,3,0], ['2nd and Short',0,0,0,0], ['2nd and Long',0,0,0,0], ['3rd and Short',0,0,0,0], ['3rd and Long',0,0,0,0], ['4th and Short',0,0,0,0], ['4th and Long',0,0,0,0], ['Goal to go',0,0,0,0]]
    table30 = pd.DataFrame(t3,columns = ['Down & Distance', 'Blitz%', 'EPA/Blitz','Stunt%','EPA/Stunt'])
    
    return table10.to_dict('rows'), table20.to_dict('rows'), table30.to_dict("rows") #unsure if this return statement works
    # list = get_team(defteam)
    # blitz_rates = ["Blitz Rates:\n"]
    # stunt_rates = "Stunt Rates:\n"
    
    # blitz_rates += f"First down: {percentages[1]*100}%\n"
    # blitz_rates += f"Second down, short yardage: {percentages[2]*100}%\n"
    # blitz_rates += f"Second down, long yardage: {percentages[3]*100}%\n"
    # # continue adding lines for the remaining percentages
    
    # stunt_rates += f"First down: {percentages[4]*100}%\n"
    # stunt_rates += f"Second down, short yardage: {percentages[5]*100}%\n"
    # stunt_rates += f"Second down, long yardage: {percentages[6]*100}%\n"
    # continue adding lines for the remaining percentages
    # return [blitz_rates, stunt_rates]



if __name__ == '__main__':
    app.run_server(debug=True)

