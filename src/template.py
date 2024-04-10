import plotly.graph_objects as go
import plotly.io as pio

MEDAL_COLORS = {
    "Gold": "gold",
    "Silver": "silver",
    "Bronze": "#cd7f32"
}


def set_default_theme():
    pio.templates.default = "plotly_white"
