import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
import requests


def get_options():
    resp = requests.get("http://nav_client/getAllDevices").json()
    res = []
    for x in resp:
        y = x['__values__']
        res.append(dict(
            label=y['name'],
            value=y['id'],
        ))
    return res


base_layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="three columns div-user-controls",
                    children=[
                        html.Img(
                            className="logo",
                            src="./assets/logo.png"
                        ),
                        html.H2("Маршрутный журнал"),
                        html.P(
                            """Выберите день, автомобиль и прочее"""
                        ),
                        html.Div(
                            className="div-for-options",
                            children=[
                                dcc.Checklist(
                                    id="options-checklist",
                                    options=[
                                        {'label': 'Границы площадок',
                                            'value': 'borders'},
                                    ],
                                    value=[]
                                )
                            ]
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    date=dt.now(),
                                    display_format="MMMM D, YYYY",
                                    style={"border": "0px solid black"},
                                )
                            ],
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.Dropdown(
                                    id="car-dropdown",
                                    placeholder="Выберите автомобиль",
                                    options=get_options()
                                )
                            ],
                        ),
                    ]
                ),
                # Column for app graphs and tables
                html.Div(
                    className="nine columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="map-graph"),
                        dcc.Graph(id="data-table"),
                    ],
                ),
            ]
        )
    ]
)
