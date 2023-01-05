from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1(children="Stunt & Blitz Guide", style={'textAlign': 'center', 'font-family': 'Verdana'}),
    html.P(
        children="Pick a team to get a scouting report on their blitz packages and stunts ran.",
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
    dbc.Row(
        [
            dbc.Col(html.P(id='blitz-rate')),
            dbc.Col(html.P(id='stunt-rate'))
        ],
        style={'textAlign': 'center', 'font-family': 'Verdana'}
    )
])



@app.callback(
    [Output('blitz-rate', 'children'), Output('stunt-rate', 'children')],
    Input('demo-dropdown', 'value')
)
def update_output(value):
    percentages = [.5,.6] #placeholders before actual csv values
    return [f'Blitz Rate: {percentages[0]*100}%',
            f'Stunt Rate: {percentages[1]*100}%']



if __name__ == '__main__':
    app.run_server(debug=True)
