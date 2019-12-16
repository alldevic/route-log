import dash
import requests
from dash.dependencies import Input, Output
from plotly import graph_objs as go
import datetime
from layout import base_layout


app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width"}
    ],
)

app.layout = base_layout


@app.callback(Output("map-graph", "figure"),
              [Input("options-checklist", "value"),
               Input("date-picker", "date"),
               Input("car-dropdown", "value")
               ])
def init_graph(vl, date, car):
    fig = go.Figure(
        data=go.Scattermapbox(),
        layout=go.Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, t=0, r=0, b=50),
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

    if car is not None:
        try:
            dt = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
        except Exception:
            dt = datetime.datetime.strptime(date, '%Y-%m-%d')

        resp = requests.get(
            f"http://nav_client:8080/getFlatTableSimple/{car},{dt.year},{dt.month},{dt.day}").json()

        lat_b = []
        lon_b = []
        name_b = []

        for x in resp["__values__"]["rows"]:
            for y in x["__values__"]["values"]:
                lat_b.append(y["__values__"]["pointValue"]
                             ["__values__"]["lat"])
                lon_b.append(y["__values__"]["pointValue"]
                             ["__values__"]["lon"])
                name_b.append(x["__values__"]["utc"])

        fig.add_trace(
            go.Scattermapbox(
                mode="markers+lines",
                lon=lon_b,
                lat=lat_b,
                marker={"size": 8, "color": "blue"},
                showlegend=False,
                text=name_b,
                hoverinfo='text',
            ))

    if "borders" in vl:
        resp = requests.get("http://nav_client:8080/getAllGeoZones").json()
        lat_a = []
        lon_a = []
        name_a = []

        for x in resp:
            y = x["__values__"]
            for z in y["points"]:
                zz = z["__values__"]
                lat_a.append(zz["lat"])
                lon_a.append(zz["lon"])
                name_a.append(f"{y['id']}, {y['name']}")
            lat_a.append(None)
            lon_a.append(None)
            name_a.append(None)

        fig.add_trace(
            go.Scattermapbox(
                fill="toself",
                lon=lon_a,
                lat=lat_a,
                marker={"size": 1, "color": "orange"},
                showlegend=False,
                text=name_a,
                hoverinfo='text',
            ))

    return fig


if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8050, debug=True)
