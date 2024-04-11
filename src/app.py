"""
 # @ Create Time: 2024-04-09 15:49:20.397484
"""

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

import preprocess
import stacked_bar_chart
import violin_charts
import line_bar_charts
import template

app = Dash(__name__, title="Olympic-app")

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server


medals_total_df = pd.read_csv("./assets/data/medals_total.csv")
medals_df = pd.read_csv("./assets/data/medals.csv")
medals_by_date_df = preprocess.extract_countries_from_athletes(medals_df)
medals_totals_by_date_df = preprocess.get_country_totals_per_date(medals_by_date_df)
dates = preprocess.get_dates(medals_totals_by_date_df)

order_types = ["official", "total medals", "gold", "silver", "bronze"]

top_medal_athlete_df = pd.read_csv("./assets/data/top_medals_athlete.csv")
top_medal_country_df = pd.read_csv("./assets/data/top_medals_country.csv")
order_types_top = ["total", "gold", "silver", "bronze"]
order_types_graph = ["athlete", "country"]

# Preprocess line bar chart data
athletes = pd.read_csv('./assets/data/athletes.csv')
medals_total = pd.read_csv("./assets/data/medals_total.csv")
line_bar_data = preprocess.line_bar_data(athletes, medals_total)

# Import and preprocess athlete age data
athletes = pd.read_csv('./assets/data/athletes.csv')
athletes = preprocess.athlete_age(athletes)

# Import and preprocess medal athlete age data
medals = pd.read_csv('./assets/data/medals.csv')
medals = preprocess.medal_athlete_age(medals, athletes)

template.set_default_theme()

app.layout = html.Div(
    children=[
        html.H1(children="Beijing 2022 Olympic Winter Games"),
        html.Div([html.H3(children=["The Olympics are one of the most viewed sporting events as it attracts fans from all over the world. The 2022 Winter Olympics were set in Beijing and saw 2893 athletes from 84 different countries competing for medals in 15 different disciplines. The following visualizations present an in depth analysis on the countries' and athletes' performances across the various sports.",
                                    html.Br(),
                                    html.Br(),
                                    "We did the work so you don't have to. Scroll down and enjoy!"]),
        ], style={"paddingTop": "30px", "width": "70%", "margin": "auto", "textAlign": "center"}),
        html.Img(src="/assets/images/olympic-rings.jpg", style={"mixBlendMode":"multiply", "width": "60%", "display": "block", "margin": "auto"}),
        html.Div([
            html.Div([
                html.H2(children="Dominating Countries Through Time"),
                html.Div([
                    dcc.Dropdown(
                        id="order-type-dropdown",
                        options=[
                            {"label": i.capitalize(), "value": i}
                            for i in order_types
                        ],
                        value="total medals",
                        clearable=False,
                        style={"width": "200px", "marginBottom": "10px", "marginLeft": "10px", "backgroundColor": "lightgrey"},
                    ),
                ], style={"paddingRight": "10px"},),
                html.Div([
                    dcc.Graph(id="medals-graph"),
                    dcc.Slider(
                        id="date-slider",
                        min=dates[0].day,
                        max=dates[-1].day,
                        value=dates[-1].day,
                        marks={
                            date.day: "February " + str(date.day) + "th 2022"
                            for date in dates
                        },
                        step=None,
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True,
                            "template": "February {value}th 2022",
                        },
                    ),
                ], style={"flex": "1", "backgroundColor": "#f9f0f0"},),
            ], style={"backgroundColor": "#f9f0f0", "paddingBottom": "50px"}),
            html.Div([
                html.H2(children="Dominating Athletes and Countries"),
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id="order-type-top-dropdown",
                            options=[
                                {
                                    "label": i.capitalize(),
                                    "value": i,
                                }
                                for i in order_types_top
                            ],
                            value="total",
                            clearable=False,
                            style={"width": "200px", "marginBottom": "10px", "marginLeft": "10px", "backgroundColor": "lightgrey"},
                        ),
                        dcc.RadioItems(
                            id="graph-type-selection",
                            options=[
                                {"label": i.capitalize(), "value": i}
                                for i in order_types_graph
                            ],
                            value="athlete",
                            labelStyle={
                                "display": "inline-block",
                                "marginRight": "20px",
                            },
                        ),
                    ], style={"paddingRight": "10px"},),
                    html.Div(
                        [dcc.Graph(id="top-medals-graph")], style={"flex": "1"}
                    ),
                ], style={"display": "flex", "flexDirection": "column"},),
            ], style={"backgroundColor": "#FFC0CB", "paddingBottom": "50px"}),
            html.Div([
                html.H2(children="Athlete Age and Gender Distribution"),
                html.Div([
                    html.Div(
                        dcc.Dropdown(
                            id='violin_graphs_filter',
                            options=['Discipline', 'Country'],
                            value='Discipline',
                            clearable=False,
                            style={'width': '200px', 'marginBottom': '10px', "marginLeft": "10px", "backgroundColor": "lightgrey"}
                        )
                    ),
                    html.Div(
                        dcc.Graph(
                            id='violin_graphs'
                        )
                    )
                ]),
            ], style={"backgroundColor": "#f9f0f0", "paddingBottom": "50px"}),
            html.Div([
                html.H2(children="Relative Country Performance"),
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='line_bar_graph_filter',
                            options=['All', 'Won medals'],
                            value='All',
                            clearable=False,
                            style={'width': '200px', 'marginBottom': '10px', "marginLeft": "10px", "backgroundColor": "lightgrey"}
                        ),
                        dcc.RadioItems(
                            id='relative_medal_filter',
                            options=['Medals', 'Medals per 100'],
                            value='Medals',
                            labelStyle={
                                'display': 'inline-block',
                                'marginRight': '20px',
                            },
                        )
                    ]),
                    html.Div(
                        dcc.Graph(
                            id='line_bar_graph'
                        )
                    )
                ])
            ], style={"backgroundColor": "#FFC0CB", "paddingBottom": "50px"}),
        ], style={"display": "flex", "flexDirection": "column"},),
    ], style={"padding": "20px", "backgroundColor": "#f9f0f0"},
)


@app.callback(
    Output("medals-graph", "figure"),
    [Input("order-type-dropdown", "value"), Input("date-slider", "value")],
)
def update_figure(selected_order_type, selected_date):
    filtered_df = preprocess.get_top5_medals_by_date(
        medals_totals_by_date_df, selected_date, selected_order_type
    )
    fig = stacked_bar_chart.get_plot(filtered_df, selected_order_type, selected_date)
    return fig


@app.callback(
    Output("top-medals-graph", "figure"),
    [
        Input("order-type-top-dropdown", "value"),
        Input("graph-type-selection", "value"),
    ],
)
def update_top_figure(selected_top_order_type, graph_type):
    filtered_df = preprocess.get_top_medals(
        top_medal_athlete_df if graph_type == "athlete" else top_medal_country_df,
        selected_top_order_type,
        graph_type,
    )

    return stacked_bar_chart.get_top_plot(
        filtered_df, selected_top_order_type, graph_type
    )

# Viz 1
@app.callback(
    Output('violin_graphs', 'figure'),
    [Input('violin_graphs_filter', 'value')]
)
def update_figure(violin_graphs_filter):
    fig = violin_charts.get_plot(athletes, medals)
    return fig

# Viz 4
@app.callback(
    Output('line_bar_graph', 'figure'),
    [Input('line_bar_graph_filter', 'value')]
)
def update_figure(violin_graphs_filter):
    fig = line_bar_charts.get_plot(line_bar_data)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
