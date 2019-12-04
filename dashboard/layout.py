import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt

base_layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="three columns div-user-controls",
                    children=[
                        # html.Img(
                        #     className="logo",
                        #     src=app.get_asset_url("logo.png")
                        # ),
                        html.H2("Маршрутный журнал"),
                        html.P(
                            """Выберите день, автомобиль и прочее"""
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    min_date_allowed=dt(2019, 4, 1),
                                    max_date_allowed=dt(2019, 9, 30),
                                    initial_visible_month=dt(2019, 4, 1),
                                    date=dt(2019, 4, 1).date(),
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
