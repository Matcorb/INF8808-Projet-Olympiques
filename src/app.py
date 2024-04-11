"""
 # @ Create Time: 2024-04-09 15:49:20.397484
"""

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
medals_df = pd.read_csv("./assets/data/medals.csv")
medals_by_date_df = preprocess.extract_countries_from_athletes(medals_df)
medals_totals_by_date_df = preprocess.get_country_totals_per_date(medals_by_date_df)
dates = preprocess.get_dates(medals_totals_by_date_df)

order_types = ["total medals", "gold", "silver", "bronze"]

top_medal_athlete_df = pd.read_csv("./assets/data/top_medals_athlete.csv")
top_medal_country_df = pd.read_csv("./assets/data/top_medals_country.csv")
order_types_top = ["total", "gold", "silver", "bronze"]
order_types_graph = ["athlete", "country"]

template.set_default_theme()

app.layout = html.Div(
    children=[
        html.H1(children="Olympic Dashboard"),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="order-type-dropdown",
                            options=[
                                {"label": i.capitalize(), "value": i}
                                for i in order_types
                            ],
                            value="total medals",
                            clearable=False,
                            style={"width": "200px", "marginBottom": "10px"},
                        ),
                    ],
                    style={"paddingRight": "10px"},
                ),
                html.Div(
                    [
                        dcc.Graph(id="medals-graph"),
                        dcc.Slider(
                            id="date-slider",
                            min=dates[0].day,
                            max=dates[-1].day,
                            value=dates[-1].day,
                            marks={
                                date.day: str(date.day) + " février 2022"
                                for date in dates
                            },
                            step=None,
                            tooltip={
                                "placement": "bottom",
                                "always_visible": True,
                                "template": "{value} février 2022",
                            },
                        ),
                    ],
                    style={"flex": "1"},
                ),
                html.H1(children="Dominating medals"),
                html.Div(
                    [
                        html.Div(
                            [
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
                                    style={"width": "200px", "marginBottom": "10px"},
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
                            ],
                            style={"paddingRight": "10px"},
                        ),
                        html.Div(
                            [dcc.Graph(id="top-medals-graph")], style={"flex": "1"}
                        ),
                    ],
                    style={"display": "flex", "flexDirection": "column"},
                ),
            ],
            style={"display": "flex", "flexDirection": "column"},
        ),
    ],
    style={"padding": "20px"},
)


@app.callback(
    Output("medals-graph", "figure"),
    [Input("order-type-dropdown", "value"), Input("date-slider", "value")],
)
def update_figure(selected_order_type, selected_date):
    filtered_df = preprocess.get_top5_medals_by_date(
        medals_totals_by_date_df, selected_date, selected_order_type
    )
    fig = stacked_bar_chart.get_plot(filtered_df, selected_order_type)
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


if __name__ == "__main__":
    app.run_server(debug=True)
