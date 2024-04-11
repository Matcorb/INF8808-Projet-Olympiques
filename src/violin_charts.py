import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
colors = px.colors.qualitative.Plotly # Plotly base colors

def get_plot(athletes, medals):
    
    # Define figure and layout
    fig = make_subplots(rows=2, cols=17, vertical_spacing=0.1, horizontal_spacing=0.005)
    layout = go.Layout(
        yaxis=dict(title=dict(text='Athlete age'), range=[10,55], tickvals=np.linspace(10, 55, 10).astype(int)),
        yaxis3=dict(range=[10,55], tickvals=np.linspace(10, 55, 10).astype(int)),

        yaxis18=dict(title=dict(text='Athlete age'), range=[10,55], tickvals=np.linspace(10, 55, 10).astype(int)),
        yaxis20=dict(range=[10,55], tickvals=np.linspace(10, 55, 10).astype(int)),
    )
    fig.update_layout(layout)
    
    for row in range(1, 3):
        for col in range(4, 18):
            fig.update_yaxes(
                range=[10,55], tickvals=np.linspace(10, 55, 10).astype(int), showticklabels=False,
                row=row, col=col
            )
    
    for col in range(1, 18):
        fig.update_xaxes(showticklabels=False, row=1, col=col)
        fig.update_xaxes(tickangle=-30, row=2, col=col)
    
    # -----------------------------------------------------------------------------
    # 1. Athlete age plots
    # -----------------------------------------------------------------------------
    # Add violin plots for all athletes
    violin_male = go.Violin(
        x=['Global']*len(athletes),
        y=athletes['age'][athletes['gender'] == 'Male'],
        side='negative',
        name='Men',
        points=False,
        meanline_visible=True,
        line_color=colors[0]
    )
    violin_female = go.Violin(
        x=['Global']*len(athletes),
        y=athletes['age'][athletes['gender'] == 'Female'],
        side='positive',
        name='Woman',
        points=False,
        meanline_visible=True,
        line_color=colors[1]
    )
    fig.add_trace(violin_male, row=1, col=1)
    fig.add_trace(violin_female, row=1, col=1)
    
    # Add a violin plot for each discipline
    disciplines = athletes['discipline'].unique()
    subplots = [(1,3), (1,4), (1,5), (1,6), (1,7), (1,8), (1,9), (1,10), (1,11),
                (1,12), (1,13), (1,14), (1,15), (1,16), (1,17)]
    for discipline, subplot in zip(disciplines, subplots):
        athletes_filtered = athletes[athletes['discipline'] == discipline]

        if len(athletes_filtered['age'][athletes_filtered['gender'] == 'Female']) > 0:
            violin_male = go.Violin(
                x=[discipline]*len(athletes_filtered),
                y=athletes_filtered['age'][athletes_filtered['gender'] == 'Male'],
                side='negative',
                showlegend=False,
                points=False,
                meanline_visible=True,
                line_color=colors[0]
            )
            violin_female = go.Violin(
                x=[discipline]*len(athletes_filtered),
                y=athletes_filtered['age'][athletes_filtered['gender'] == 'Female'],
                side='positive',
                showlegend=False,
                points=False,
                meanline_visible=True,
                line_color=colors[1]
            )
            fig.add_trace(violin_male, row=subplot[0], col=subplot[1])
            fig.add_trace(violin_female, row=subplot[0], col=subplot[1])

        else:
            violin = go.Violin(
                x=[discipline]*len(athletes_filtered),
                y=athletes_filtered['age'],
                showlegend=False,
                points=False,
                meanline_visible=True,
                line_color=colors[0]
            )
            fig.add_trace(violin, row=subplot[0], col=subplot[1])

    # -----------------------------------------------------------------------------
    # 2. Medal athlete age plots
    # -----------------------------------------------------------------------------
    # Add violin plots for all athletes
    violin_male = go.Violin(
        x=['Global']*len(medals),
        y=medals['age'][medals['gender'] == 'Male'],
        side='negative',
        showlegend=False,
        points=False,
        meanline_visible=True,
        line_color=colors[0]
    )
    violin_female = go.Violin(
        x=['Global']*len(medals),
        y=medals['age'][medals['gender'] == 'Female'],
        side='positive',
        showlegend=False,
        points=False,
        meanline_visible=True,
        line_color=colors[1]
    )
    fig.add_trace(violin_male, row=2, col=1)
    fig.add_trace(violin_female, row=2, col=1)
    
    # Add a violin plot for each discipline
    subplots = [(2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (2,9), (2,10), (2,11),
                (2,12), (2,13), (2,14), (2,15), (2,16), (2,17)]
    for discipline, subplot in zip(disciplines, subplots):
        medals_filtered = medals[medals['discipline'] == discipline]

        if len(medals_filtered['age'][medals_filtered['gender'] == 'Female']) > 0:
            violin_male = go.Violin(
                x=[discipline]*len(medals_filtered),
                y=medals_filtered['age'][medals_filtered['gender'] == 'Male'],
                side='negative',
                showlegend=False,
                points=False,
                meanline_visible=True,
                line_color=colors[0]
            )
            violin_female = go.Violin(
                x=[discipline]*len(medals_filtered),
                y=medals_filtered['age'][medals_filtered['gender'] == 'Female'],
                side='positive',
                showlegend=False,
                points=False,
                meanline_visible=True,
                line_color=colors[1]
            )
            fig.add_trace(violin_male, row=subplot[0], col=subplot[1])
            fig.add_trace(violin_female, row=subplot[0], col=subplot[1])

        else:
            violin = go.Violin(
                x=[discipline]*len(medals_filtered),
                y=medals_filtered['age'],
                showlegend=False,
                points=False,
                meanline_visible=True,
                line_color=colors[0]
            )
            fig.add_trace(violin, row=subplot[0], col=subplot[1])
    
    fig.update_layout(annotations=[
        dict(
            x=0.5, y=1.05,
            xref='paper', yref='paper',
            text='Number of athletes',
            font=dict(size=16, color='black'),
            showarrow=False
        ),
        dict(
            x=0.5, y=0.45,
            xref='paper', yref='paper',
            text='Number of medals',
            font=dict(size=16, color='black'),
            showarrow=False
        )
    ])
    return fig