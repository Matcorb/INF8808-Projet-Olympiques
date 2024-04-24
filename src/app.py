"""
 # @ Create Time: 2024-04-09 15:49:20.397484
"""

from dash import Dash, html, dcc, Input, Output, State, callback_context
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

# Raw dataframes
medals_df = pd.read_csv("./assets/data/medals.csv")
top_medal_athlete_df = pd.read_csv("./assets/data/top_medals_athlete.csv")
top_medal_country_df = pd.read_csv("./assets/data/top_medals_country.csv")
athletes = pd.read_csv("./assets/data/athletes.csv")
medals_total = pd.read_csv("./assets/data/medals_total.csv")

# Processed dataframes
medals_by_date_df = preprocess.extract_countries_from_athletes(medals_df)
medals_totals_by_date_df = preprocess.get_country_totals_per_date(medals_by_date_df)
line_bar_data = preprocess.line_bar_data(athletes, medals_total)
athletes = preprocess.athlete_age(athletes)
medals = preprocess.medal_athlete_age(medals_df, athletes)
dates = preprocess.get_dates(medals_totals_by_date_df)

# Dropdown options
order_types = ["official", "total medals", "gold", "silver", "bronze"]
order_types_top = ["total", "gold", "silver", "bronze"]
order_types_graph = ["athlete", "country"]

template.set_default_theme()

app.layout = html.Div(
    children=[
        html.H1(children="Beijing 2022 Olympic Winter Games"),
        html.Div(
            [
                html.H3(
                    children=[
                        "The Olympics are one of the most viewed sporting events as it attracts fans from all over the world. The 2022 Winter Olympics were set in Beijing and saw 2893 athletes from 84 different countries competing for medals in 15 different disciplines. The following visualizations present an in depth analysis on the countries' and athletes' performances across the various sports.",
                        html.Br(),
                        html.Br(),
                        "We did the work so you don't have to. Scroll down and enjoy!",
                    ],
                    style={"textAlign": "center"},
                ),
            ],
            style={
                "paddingTop": "30px",
                "width": "70%",
                "margin": "auto",
                "textAlign": "center",
            },
        ),
        html.Img(
            src="/assets/images/olympic-rings.jpg",
            style={
                "mixBlendMode": "multiply",
                "width": "60%",
                "display": "block",
                "margin": "auto",
            },
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H2(children="Most Medaled Countries Through Time"),
                        html.Div(
                            [
                                html.H3(
                                    children=[
                                        "How well a country performed at the Olympics is often determined by its amount of medals earned. ",
                                        "Therefore, let's look at which countries got the most medals.",
                                        html.Br(),
                                        html.Br(),
                                        "The following bar chart presents the top 5 countries in terms of number of medals earned (total, gold, silver or bronze) and ",
                                        "even in terms of official rankings (determined by most golds followed by most silvers and finally most bronzes). ",
                                        "You can also use the slider available below the chart to visualize the top 5 countries at any date throughout the competition.",
                                    ],
                                    style={"textAlign": "center"},
                                ),
                            ],
                            style={
                                "paddingTop": "20px",
                                "width": "70%",
                                "margin": "auto",
                                "textAlign": "center",
                            },
                        ),
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
                                    style={
                                        "width": "200px",
                                        "marginBottom": "10px",
                                        "marginLeft": "10px",
                                        "backgroundColor": "lightgrey",
                                        "fontFamily": "Roboto Slab, serif",
                                    },
                                ),
                            ],
                            style={"paddingRight": "10px"},
                        ),
                        html.Div(
                            [
                                dcc.Graph(id="medals-graph"),
                                html.H3(
                                    children="Interact with the slider below to view the top countries at any date:"
                                ),
                                dcc.Slider(
                                    id="date-slider",
                                    min=dates[0].day,
                                    max=dates[-1].day,
                                    value=dates[-1].day,
                                    marks={
                                        date.day: "February " + str(date.day) + "th"
                                        for date in dates
                                    },
                                    step=None,
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": True,
                                        "template": "February {value}th 2022",
                                    },
                                ),
                            ],
                            style={"flex": "1", "backgroundColor": "#f9f0f0"},
                        ),
                    ],
                    style={"backgroundColor": "#f9f0f0", "paddingBottom": "50px"},
                ),
                html.Div(
                    [
                        html.H2(
                            children="Most Medaled Athletes and Countries per Event"
                        ),
                        html.Div(
                            [
                                html.H3(
                                    children=[
                                        "Certain countries and even athletes can also dominate specific disciplines without being one of the most medaled overall.",
                                        html.Br(),
                                        html.Br(),
                                        "The bar chart below presents the most decorated athletes and countries in the various events. ",
                                        "More information on a square can be seen by hovering over it.",
                                    ],
                                    style={"textAlign": "center"},
                                ),
                            ],
                            style={
                                "paddingTop": "20px",
                                "width": "70%",
                                "margin": "auto",
                                "textAlign": "center",
                            },
                        ),
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
                                            style={
                                                "width": "200px",
                                                "marginBottom": "10px",
                                                "marginLeft": "10px",
                                                "backgroundColor": "lightgrey",
                                            },
                                        ),
                                        dcc.Checklist(
                                            id="sort-method-checkbox",
                                            options=[
                                                {
                                                    "label": " Sort by Weighted Medal Values",
                                                    "value": "weighted",
                                                }
                                            ],
                                            value=[],
                                            style={
                                                "display": "none",
                                                "fontSize": "16px",
                                            },
                                        ),
                                        dcc.RadioItems(
                                            id="graph-type-selection",
                                            options=[
                                                {
                                                    "label": i.capitalize(),
                                                    "value": i,
                                                }
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
                                    [dcc.Graph(id="top-medals-graph")],
                                    style={"flex": "1"},
                                ),
                                html.Div(
                                    id="hover-data-box",
                                    style={
                                        "backgroundColor": "#84c1ff",
                                        "paddingBottom": "50px",
                                    },
                                ),
                            ],
                            style={"display": "flex", "flexDirection": "column"},
                        ),
                    ],
                    style={"backgroundColor": "#84c1ff", "paddingBottom": "50px"},
                ),
                html.Div(
                    [
                        html.H2(children="Athlete Age and Gender Distribution"),
                        html.Div(
                            [
                                html.H3(
                                    children=[
                                        "It can also be interesting to see how different age groups and genders were represented.",
                                        html.Br(),
                                        html.Br(),
                                        "The numerous violin charts found in this visualization present the age distribution ",
                                        "according to gender and either discipline or country of origin. With these charts, ",
                                        "we can see which age groups were the most represented in number of athletes and which age groups won the most medals.",
                                    ],
                                    style={"textAlign": "center"},
                                ),
                            ],
                            style={
                                "paddingTop": "20px",
                                "width": "70%",
                                "margin": "auto",
                                "textAlign": "center",
                            },
                        ),
                        html.Div(
                            [
                                html.Div(
                                    dcc.Dropdown(
                                        id="violin_graphs_filter",
                                        # options=['Discipline', 'Country'],
                                        options=["Discipline"],
                                        value="Discipline",
                                        clearable=False,
                                        style={
                                            "width": "200px",
                                            "marginBottom": "10px",
                                            "marginLeft": "10px",
                                            "backgroundColor": "lightgrey",
                                        },
                                    )
                                ),
                                html.Div(dcc.Graph(id="violin_graphs")),
                            ]
                        ),
                    ],
                    style={"backgroundColor": "#FFFFE0", "paddingBottom": "50px"},
                ),
                html.Div(
                    [
                        html.H2(
                            children="Country Performance Relative to Representation"
                        ),
                        html.Div(
                            [
                                html.H3(
                                    children=[
                                        "Every country is represented by a different amount of athletes. Thus, is can be interesting to ",
                                        "compare a country's amount of medals to its number of athletes.",
                                        html.Br(),
                                        html.Br(),
                                        "The ensuing chart presents just that. The blue bars represent a country's number of athletes ",
                                        "and the red dot its number of medals earned throughout the competition. ",
                                        "We can therefore see that, as an example, the Netherlands gained many medals despite its low representation (17 medals for 41 athletes) ",
                                        "and that Czech Republic on the other hand didn't see the same success (2 medals for 115 athletes).",
                                    ],
                                    style={"textAlign": "center"},
                                ),
                            ],
                            style={
                                "paddingTop": "20px",
                                "width": "70%",
                                "margin": "auto",
                                "textAlign": "center",
                            },
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="line_bar_graph_filter",
                                            # options=['All', 'Won medals'],
                                            options=["All"],
                                            value="All",
                                            clearable=False,
                                            style={
                                                "width": "200px",
                                                "marginBottom": "10px",
                                                "marginLeft": "10px",
                                                "backgroundColor": "lightgrey",
                                            },
                                        ),
                                        # dcc.RadioItems(
                                        #     id='relative_medal_filter',
                                        #     options=['Medals', 'Medals per 100'],
                                        #     value='Medals',
                                        #     labelStyle={
                                        #         'display': 'inline-block',
                                        #         'marginRight': '20px',
                                        #     },
                                        # )
                                    ]
                                ),
                                html.Div(dcc.Graph(id="line_bar_graph")),
                            ]
                        ),
                    ],
                    style={"backgroundColor": "#C0D9AF", "paddingBottom": "50px"},
                ),
            ],
            style={"display": "flex", "flexDirection": "column"},
        ),
    ],
    style={"padding": "20px", "backgroundColor": "#f9f0f0"},
)


@app.callback(
    Output("sort-method-checkbox", component_property="style"),
    [Input("order-type-top-dropdown", "value")],
)
def show_hide_top_checkbox(visibility_state):
    return {"display": "block" if visibility_state == "total" else "none"}


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
        Input("sort-method-checkbox", "value"),
    ],
)
def update_top_figure(selected_top_order_type, graph_type, sort_method):
    filtered_df = preprocess.get_top_medals(
        top_medal_athlete_df if graph_type == "athlete" else top_medal_country_df,
        selected_top_order_type,
        graph_type,
        sort_method,
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
    [State("hover-data-box", "children")],
)
def display_hover_data(hover_data, order_type, graph_type, current_data):
    ctx = callback_context

    if not ctx.triggered or not hover_data or ctx.triggered[0]["prop_id"] in (
        "order-type-top-dropdown.value",
        "graph-type-selection.value",
    ):
        return html.Div(
            [
                html.H3("Hover over a bar to see detailed data"),
            ],
            style={
                "padding": "10px",
                "margin-top": "5px",
                "backgroundColor": "#84c1ff",
                "paddingBottom": "50px",
            },
        )
    
    data = hover_data["points"][0]
    country_or_athlete = data["customdata"][0]
    discipline = data["y"]
    percent = data["customdata"][1]
    medals = data["customdata"][2:5]  # gold, silver, bronze
    medal_names = ["Gold", "Silver", "Bronze"]
    medal_texts = [f"{name}: {count}" for name, count in zip(medal_names, medals)]

    medal_type = "" if order_type == "total" else order_type
    header_text = f"{country_or_athlete} - {discipline}"
    info_text = f"This {graph_type} has won {percent:.2f}% of the {medal_type} medals in {discipline}"

    return html.Div(
        [
            html.H3(header_text),
            *map(html.P, medal_texts),
            html.P(info_text),
        ],
        style={
            "padding": "10px",
            "margin-top": "5px",
            "backgroundColor": "#84c1ff",
            "paddingBottom": "50px",
        },
    )



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
