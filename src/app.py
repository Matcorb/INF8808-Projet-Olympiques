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

order_types = ["total medals", "gold", "silver", "bronze"]

top_medal_athlete_df = pd.read_csv("./assets/data/top_medals_athlete.csv")
top_medal_country_df = pd.read_csv("./assets/data/top_medals_country.csv")
order_types_top = ["total", "gold", "silver", "bronze"]
order_types_graph = ["athlete", "country"]

# Preprocess line bar chart data
athletes = pd.read_csv("./assets/data/athletes.csv")
medals_total = pd.read_csv("./assets/data/medals_total.csv")
line_bar_data = preprocess.line_bar_data(athletes, medals_total)

# Import and preprocess athlete age data
athletes = pd.read_csv("./assets/data/athletes.csv")
athletes = preprocess.athlete_age(athletes)

# Import and preprocess medal athlete age data
medals = pd.read_csv("./assets/data/medals.csv")
medals = preprocess.medal_athlete_age(medals, athletes)

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
                html.Div(id="hover-data-box"),
                html.H1(children="Athlete age and gender distribution"),
                html.Div(
                    [
                        html.Div(
                            dcc.Dropdown(
                                id="violin_graphs_filter",
                                options=["Discipline", "Country"],
                                value="Discipline",
                                clearable=False,
                                style={"width": "200px", "marginBottom": "10px"},
                            )
                        ),
                        html.Div(dcc.Graph(id="violin_graphs")),
                    ]
                ),
                html.H1(children="Relative country performance"),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="line_bar_graph_filter",
                                    options=["All", "Won medals"],
                                    value="All",
                                    clearable=False,
                                    style={"width": "200px", "marginBottom": "10px"},
                                ),
                                dcc.RadioItems(
                                    id="relative_medal_filter",
                                    options=["Medals", "Medals per 100"],
                                    value="Medals",
                                    labelStyle={
                                        "display": "inline-block",
                                        "marginRight": "20px",
                                    },
                                ),
                            ]
                        ),
                        html.Div(dcc.Graph(id="line_bar_graph")),
                    ]
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


@app.callback(
    Output("hover-data-box", "children"),
    [
        Input("top-medals-graph", "hoverData"),
        Input("order-type-top-dropdown", "value"),
        Input("graph-type-selection", "value"),
    ],
)
def display_hover_data(
    hover_data,
    medal_type,
    top_graph_type,
):
    if hover_data:
        data = hover_data["points"][0]
        print(data)
        discipline = data["y"]
        country = data["customdata"][0]
        percent = data["customdata"][1]
        gold = data["customdata"][2]
        silver = data["customdata"][3]
        bronze = data["customdata"][4]

        return html.Div(
            [
                html.H3(f"{country} in {discipline}"),
                html.P(f"Gold: {gold}"),
                html.P(f"Silver: {silver}"),
                html.P(f"Bronze: {bronze}"),
                html.P(
                    f"This {top_graph_type} has won {percent:.2f}% of {medal_type} medals in {discipline}"
                ),
            ]
        )
    else:
        return "Hover over a bar to see detailed data"


# Viz 1
@app.callback(
    Output("violin_graphs", "figure"), [Input("violin_graphs_filter", "value")]
)
def update_figure(violin_graphs_filter):
    fig = violin_charts.get_plot(athletes, medals)
    return fig


# Viz 4
@app.callback(
    Output("line_bar_graph", "figure"), [Input("line_bar_graph_filter", "value")]
)
def update_figure(violin_graphs_filter):
    fig = line_bar_charts.get_plot(line_bar_data)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
