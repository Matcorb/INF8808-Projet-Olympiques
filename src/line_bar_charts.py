import plotly.graph_objects as go

def get_plot(line_bar_data):
    title="Countries with the most Athletes and their Medal Count"
    
    bar_chart = go.Bar(
        x=line_bar_data.index,
        y=line_bar_data['count'],
        name='athletes',
        yaxis='y1'
    )
    line_chart = go.Scatter(
        x=line_bar_data.index,
        y=line_bar_data['Total'],
        mode='lines+markers',
        marker=dict(size=8, symbol='diamond'),
        name='medals',
        yaxis='y2'
    )
    data = [bar_chart, line_chart]

    layout = go.Layout(
        title=title,
        hovermode='x',
        xaxis=dict(tickangle=-60),
        yaxis=dict(side='left', range=[0, 250], title=dict(text='Number of athletes')),
        yaxis2=dict(side='right', range=[0, 50], title=dict(text='Nomber of medals'), overlaying='y')
    )
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(plot_bgcolor="#FFC0CB", paper_bgcolor="#FFC0CB")
    return fig