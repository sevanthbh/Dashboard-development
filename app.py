import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

# Sample RCB IPL Performance Data (Last 5 Years)
data = {
    'Year': [2019, 2020, 2021, 2022, 2023],
    'Wins': [5, 7, 9, 8, 10],
    'Losses': [9, 7, 5, 6, 4],
    'Top Scorer': ['Kohli', 'ABD', 'Maxwell', 'DK', 'Faf'],
    'Total Runs': [1700, 2100, 1900, 2050, 2250],
    'Run Rate': [7.8, 8.2, 8.5, 8.0, 8.7]
}
df = pd.DataFrame(data)

# Initialize Dash app
app = dash.Dash(__name__)

# Layout with Stylish Full-Screen Design
app.layout = html.Div(style={
    'backgroundColor': '#121212', 'color': 'white', 'padding': '20px',
    'height': '100vh', 'width': '100vw', 'overflow': 'hidden'
}, children=[
    html.H1("🔥 RCB IPL Performance Dashboard (Last 5 Years) 🔥", 
            style={'textAlign': 'center', 'color': '#ff0037', 'fontSize': '36px'}),
    
    dcc.Dropdown(
        id='stat-dropdown',
        options=[
            {'label': 'Wins vs Losses', 'value': 'wins_losses'},
            {'label': 'Total Runs Per Year', 'value': 'runs'},
            {'label': 'Run Rate Trend', 'value': 'run_rate'},
            {'label': 'Win % Comparison', 'value': 'win_percentage'}
        ],
        value='wins_losses',
        style={'color': 'black', 'width': '50%', 'margin': 'auto', 'fontSize': '18px'}
    ),
    
    html.Div([
        dcc.Graph(id='rcb-chart', style={'height': '70vh', 'marginTop': '20px'}),
    ], style={'display': 'flex', 'justifyContent': 'center'}),
])

# Callback to Update Graph
@app.callback(
    Output('rcb-chart', 'figure'),
    [Input('stat-dropdown', 'value')]
)
def update_chart(selected_stat):
    if selected_stat == 'wins_losses':
        fig = px.bar(df, x='Year', y=['Wins', 'Losses'], 
                     title='🏆 RCB Wins vs Losses (Last 5 Years)', 
                     barmode='group', color_discrete_sequence=['#ff0037', '#ffcc00'])
    elif selected_stat == 'runs':
        fig = px.area(df, x='Year', y='Total Runs', markers=True, 
                      title='🏏 RCB Total Runs Per Year', color_discrete_sequence=['#00ffcc'])
    elif selected_stat == 'win_percentage':
        df['Win Percentage'] = (df['Wins'] / (df['Wins'] + df['Losses'])) * 100
        fig = px.pie(df, names='Year', values='Win Percentage', 
                     title='🎯 RCB Win % Comparison', color_discrete_sequence=px.colors.sequential.Reds)
    else:
        fig = px.scatter(df, x='Year', y='Run Rate', size='Run Rate', 
                         title='🚀 RCB Run Rate Trend', color='Run Rate',
                         color_continuous_scale='reds')
    
    fig.update_layout(plot_bgcolor='#1e1e30', paper_bgcolor='#121212', font_color='white')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
