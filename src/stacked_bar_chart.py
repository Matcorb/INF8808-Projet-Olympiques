import plotly.express as px

from template import MEDAL_COLORS

def get_plot(df, type):
    title = f"Top 5 Countries by {'Medal Count (Official Order)' if type == 'official' else type.capitalize() + ' Medals'}"
    
    if type in ["official", "total medals"]:
        fig = px.bar(df,
                     y="Country",
                     x=["Gold", "Silver", "Bronze"],
                     title=title,
                     labels={"value": "Medals", "variable": "Medal Type"},
                     color_discrete_map=MEDAL_COLORS,
                     orientation="h",
                     category_orders={"Country": df["Country"].tolist()})
        fig.update_layout(barmode="stack") 
    else:
        bar_color = MEDAL_COLORS.get(type.capitalize(), "black")
        fig = px.bar(df,
                     y="Country",
                     x=type.capitalize(),
                     title=title,
                     color_discrete_sequence=[bar_color],
                     orientation="h",
                     category_orders={"Country": df["Country"].tolist()})
    fig.update_layout(legend_orientation="h", legend=dict(y=-0.2, xanchor="center", x=0.5))
    return fig

