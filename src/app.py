'''
 # @ Create Time: 2024-04-09 15:49:20.397484
'''

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

import preprocess
import stacked_bar_chart
import template

app = Dash(__name__, title="Olympic-app")

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server


medals_total_df = pd.read_csv("./assets/data/medals_total.csv")
order_types = ["official", "total medals", "gold", "silver", "bronze"]

template.set_default_theme()

app.layout = html.Div(children=[
    html.H1(children='Olympic Dashboard'),

    html.Div([
        html.Div([
            dcc.Dropdown(
                id='order-type-dropdown',
                options=[{'label': i.capitalize(), 'value': i} for i in order_types],
                value='total medals',
                clearable=False,
                style={'width': '200px', 'marginBottom': '10px'}
            )
        ], style={'paddingRight': '10px'}),

        html.Div([
            dcc.Graph(id='medals-graph')
        ], style={'flex': '1'})
    ], style={'display': 'flex', 'flexDirection': 'column'}),

], style={'padding': '20px'}) 


@app.callback(
    Output('medals-graph', 'figure'),
    [Input('order-type-dropdown', 'value')]
)
def update_figure(selected_order_type):
    filtered_df = preprocess.get_top5_medals(medals_total_df, selected_order_type)
    fig = stacked_bar_chart.get_plot(filtered_df, selected_order_type)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
