import plotly.express as px
from datetime import datetime

from template import MEDAL_COLORS


def get_plot(df, type, day):

    if type in ["official", "total medals"]:
        fig = px.bar(
            df,
            y="Country",
            x=["Gold", "Silver", "Bronze"],
            labels={"value": "Medals", "variable": "Medal Type"},
            color_discrete_map=MEDAL_COLORS,
            orientation="h",
            category_orders={"Country": df["Country"].tolist()},
        )
        fig.update_layout(barmode="stack")
    else:
        bar_color = MEDAL_COLORS.get(type.capitalize(), "black")
        fig = px.bar(
            df,
            y="Country",
            x=type.capitalize(),
            color_discrete_sequence=[bar_color],
            orientation="h",
            category_orders={"Country": df["Country"].tolist()},
        )
    fig.update_layout(
        legend_orientation="h", legend=dict(y=-0.2, xanchor="center", x=0.5), plot_bgcolor="#f9f0f0", paper_bgcolor="#f9f0f0", font=dict(family="Roboto Slab, serif")
    )
    return fig


def get_top_plot(df, type, graph_type):
    hover_column = "athlete_name" if graph_type == "athlete" else "country"

    if type == "total":
        hover_template = (
            "<b>%{customdata[0]}</b><br>"
            f"{type.capitalize()} Medals: %{{x}}<br>"
            f"Gold: %{{customdata[2]}}<br>"
            f"Silver: %{{customdata[3]}}<br>"
            f"Bronze: %{{customdata[4]}}<br>"
            f"Represents %{{customdata[1]:.2f}}% of all medals in %{{y}}"
        )
    else:
        hover_template = (
            "<b>%{customdata[0]}</b><br>"
            f"{type.capitalize()} Medals: %{{x}}<br>"
            f"Represents %{{customdata[1]:.2f}}% of all medals in %{{y}}"
        )

    fig = px.bar(
        df,
        y="discipline",
        x=type,
        orientation="h",
        category_orders={"Discipline": df["discipline"].unique()},
        hover_data={hover_column: True},
        color=type,
        color_continuous_scale=px.colors.sequential.Pinkyl,
        labels={
            type: f"Number of {type.capitalize()} Medals per {graph_type.capitalize()}",
        },
    )
    fig.update_traces(
        hovertemplate=hover_template,
        customdata=df[[hover_column, "percent", "gold", "silver", "bronze"]],
        marker_line_color="black",
        marker_line_width=1.5,
        opacity=1,
    )
    fig.update_xaxes(
        title_text=f"{type.capitalize()} Medals Distribution by Discipline",
    )
    fig.update_yaxes(
        autorange="reversed",
        title_text="Discipline",
    )
    fig.update_layout(showlegend=False, plot_bgcolor="#84c1ff", paper_bgcolor="#84c1ff", font=dict(family="Roboto Slab, serif"))
    return fig
