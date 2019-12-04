import dash
from dash.dependencies import Input, Output
from plotly import graph_objs as go

from .layout import base_layout

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

app.layout = base_layout


@app.callback(Output("map-graph", "figure"),
              [Input("car-dropdown", "value")])
def init_graph(vl):
    return go.Figure(
        data=go.Scattermapbox(),
        layout=go.Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, t=35, r=0, b=35),
            showlegend=False,
            mapbox_style="open-street-map",
        ),
    )
