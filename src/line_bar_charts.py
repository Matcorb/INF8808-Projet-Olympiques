import numpy as np
import plotly.graph_objects as go

def get_plot(line_bar_data, line_bar_graph_filter, relative_medal_filter):
    
    # Filter out countries that haven't won medals if needed
    if line_bar_graph_filter == "Won medals":
        line_bar_data = line_bar_data[line_bar_data['Total'] > 0]
    
    bar_chart = go.Bar(
        x=line_bar_data.index,
        y=line_bar_data['count'],
        name='athletes',
        yaxis='y1'
    )
    
    # Adjust for absolute or relative medals display
    if relative_medal_filter == 'Medals':
        medal_column = 'Total'
        yaxis_name = 'Medals'
        medal_trace_name = 'medals'
    elif relative_medal_filter == 'Medals per 100':
        medal_column = 'medals_per_100'
        yaxis_name = 'Medals per 100'
        medal_trace_name = 'medals per 100'
        
    line_chart = go.Scatter(
        x=line_bar_data.index,
        y=line_bar_data[medal_column],
        mode='lines+markers',
        marker=dict(size=8, symbol='diamond'),
        name=medal_trace_name,
        yaxis='y2'
    )
    data = [bar_chart, line_chart]

    layout = go.Layout(
        height=600,
        hovermode='x',
        xaxis=dict(tickangle=-60),
        yaxis=dict(side='left', range=[0, 255], title=dict(text='Number of athletes')),
        yaxis2=dict(side='right', range=[0, 51], title=dict(text=yaxis_name), overlaying='y')
    )
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(plot_bgcolor="#C0D9AF", paper_bgcolor="#C0D9AF", font=dict(size=16, family="Roboto Slab, serif"))
    return fig