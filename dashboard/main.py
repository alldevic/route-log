import dash
from dash.dependencies import Input, Output
from plotly import graph_objs as go

from layout import base_layout


app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width"}
    ],
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
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=53.757607, lon=87.136101),
                bearing=0,
                zoom=12,
            ),
            updatemenus=[
                dict(
                    buttons=(
                        [
                            dict(
                                args=[
                                    {
                                        "mapbox.zoom": 12,
                                        "mapbox.center.lon": "87.136101",
                                        "mapbox.center.lat": "53.757607",
                                        "mapbox.bearing": 0,
                                        "mapbox.style": "open-street-map",
                                    }
                                ],
                                label="Reset Zoom",
                                method="relayout",
                            )
                        ]
                    ),
                    direction="left",
                    pad={"r": 0, "t": 0, "b": 0, "l": 0},
                    showactive=False,
                    type="buttons",
                    x=0.45,
                    y=0.02,
                    xanchor="left",
                    yanchor="bottom",
                    bgcolor="#323130",
                    borderwidth=1,
                    bordercolor="#6d6d6d",
                    font=dict(color="#FFFFFF"),
                )
            ],
        ),
    )


if __name__ == "__main__":
    app.run_server(debug=True)
