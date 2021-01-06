import os
import pathlib
import numpy as np
import datetime as dt
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import threading
from time import sleep

from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from scipy.stats import rayleigh
from db.db_api import select_people_by_id, select_sensor, select_traces, get_data


GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

server = app.server

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

params = [
    'L0', 'L1', 'L2', 'R0', 'R1', 'R2'
]

app.layout = html.Div(
    [
        # header
        html.Div(
            [
                html.Div(
                    [
                        html.H4("MONITORING THE PRESSURE OF THE FEET2", className="app__header__title"),
                        html.P(
                            "The application presents a graphical visualization of measurements of a device for monitoring walking habits and patterns and displays live charts of pressure and anomalies in moving.",
                            className="app__header__title--grey",
                        ),
                    ],
                    className="app__header__desc",
                ),
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("dash-new-logo.png"),
                            className="app__menu__img",
                        )
                    ],
                    className="app__header__logo",
                ),
            ],
            className="app__header",
        ),
        html.Div(
            [
                # wind speed
                html.Div(
                    [
                        html.Div(
                            [html.H6("LEFT FOOT", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="l0",
                            figure=dict(
                                layout=dict(
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                )
                            ),
                        ),
                        dcc.Graph(
                            id="l1",
                            figure=dict(
                                layout=dict(
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                )
                            ),
                        ),
                                                dcc.Graph(
                            id="l2",
                            figure=dict(
                                layout=dict(
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                )
                            ),
                        ),
                        dcc.Interval(
                            id="wind-speed-update",
                            interval=int(GRAPH_INTERVAL),
                            n_intervals=0,
                        ),
                    ],
                    className="one-third column wind__speed__container",
                ),
                # right foot
                html.Div(
                    [
                        html.Div(
                            [html.H6("RIGHT FOOT", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="r0",
                            figure=dict(
                                layout=dict(
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                )
                            ),
                        ),
                        dcc.Graph(
                            id="r1",
                            figure=dict(
                                layout=dict(
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                )
                            ),
                        ),
                            dcc.Graph(
                            id="r2",
                            figure=dict(
                                layout=dict(
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                )
                            ),
                        ),
                        dcc.Interval(
                            id="wind-speed-update2",
                            interval=int(GRAPH_INTERVAL),
                            n_intervals=0,
                        ),
                    ],
                    className="one-third column wind__speed__container",
                ),

                html.Div(
                    [
                        # histogram
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "PATIENT",
                                            className="graph__title",
                                        )
                                    ]
                                ),
                                
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id='person-dropdown',
                                            options=[
                                            {'label': 'Janek Grzegorczyk', 'value': '1'},
                                            {'label': 'Elżbieta Kochalska', 'value': '2'},
                                            {'label': 'Albert Lisowski', 'value': '3'},
                                            {'label': 'Ewelina Nosowska', 'value': '4'},
                                            {'label': 'Piotr Fokalski', 'value': '5'},
                                            {'label': 'Bartosz Moskalski', 'value': '6'}
                                            ],
                                            value='1'
                                        ),
                                    ],
                                    className="dropdown",
                                ),

                                html.Div(
                                    [
                                        html.H2(
                                            "NAME",
                                            className="graph__title",
                                            id="person-name"
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H2(
                                            "SURNAME",
                                            className="graph__title",
                                            id="person-surname"
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H2(
                                            "YEAR OF BIRTH",
                                            className="graph__title",
                                            id="person-year"
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H2(
                                            "DISABLED",
                                            className="graph__title",
                                            id="person-disabled"
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H2(
                                            "ELO",
                                            className="graph__title",
                                            id="elo"
                                        )
                                    ]
                                ),

                            ],
                            className="graph__container first",
                        ),
                        # wind direction
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "TABLE OF PRESSURE VALUES", className="graph__title"
                                        )
                                    ]
                                ),
                                dash_table.DataTable(
                                    id='table-editing-simple',
                                    columns=(
                                    [{'id': 'Model', 'name': 'SENSOR'}] +
                                    [{'id': p, 'name': p} for p in params]
                                    ),
                                    data=[
                                    dict(Model=i, **{param: 0 for param in params})
                                    for i in ["VALUE", "ANOMALY", "MEAN", "MIN", "MAX", "QARTILES", "RMS"]
                                    ],
                                    style_table={'border': 'thin lightgrey solid'},
                                                    style_header={'backgroundColor':'lightgrey','fontWeight':'bold'},
                                                    style_cell={'textAlign':'center','width':'12%'},
                                                    style_data_conditional=[{
                                                        'if' : {'filter':  'side eq "bid"' },
                                                        'color':'blue'
                                                                }
                                                        ]+[
                                                        {
                                                        'if' : {'filter': 'side eq "ask"' },
                                                        'color':'rgb(203,24,40)'
                                                    }]+[
                                                        { 'if': {'row_index':'odd'},
                                                        'backgroundColor':'rgb(242,242,242)'}
                                                    ]+[
                                                        {'if':{'column_id':'price'},
                                                        'fontWeight':'bold',
                                                        'border': 'thin lightgrey solid'}
                                                    ]+[{'if':{'column_id':'from_mid'},
                                                        'fontWeight':'bold'}
                                                    ],
                                                    style_as_list_view=True,
                                    editable=True,
                                ),
                            
                            ],
                            className="graph__container second",
                        ),
                    ],
                    className="one-third column histogram__direction",
                ),
            ],
            className="app__content",
        ),
    ],
    className="app__container",
)


def get_current_time():
    """ Helper function to get the current time in seconds. """

    now = dt.datetime.now()
    total_time = (now.hour * 3600) + (now.minute * 60) + (now.second)
    return total_time


@app.callback(
    Output("wind-speed", "figure"), [Input("wind-speed-update", "n_intervals")]
)

@app.callback(
    Output('elo', 'children'),
    Output('person-name', 'children'),
    Output('person-surname', 'children'),
    Output('person-year', 'children'),
    Output('person-disabled', 'children'),
    [dash.dependencies.Input('person-dropdown', 'value')])
def update_output(value):
    df = select_people_by_id(value)
    print(df)
    return 'You have selected person with id: {}'.format(value), 'NAME: {}'.format(df["name"][0]), 'SURNAME: {}'.format(df["surname"][0]), 'YEAR OF BIRTH: {}'.format(df["birth_year"][0]), 'DISABLED: {}'.format(bool(df["disabled"][0]))


def gen_wind_speed(interval):
    """
    Generate the wind speed graph.

    :params interval: update the graph based on an interval
    """

    total_time = get_current_time()
    df = get_wind_data(total_time - 200, total_time)

    trace = dict(
        type="scatter",
        y=df["Speed"],
        line={"color": "#42C4F7"},
        hoverinfo="skip",
        error_y={
            "type": "data",
            "array": df["SpeedError"],
            "thickness": 1.5,
            "width": 2,
            "color": "#B4E8FC",
        },
        mode="lines",
    )

    layout = dict(
        plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        font={"color": "#fff"},
        height=700,
        xaxis={
            "range": [0, 200],
            "showline": True,
            "zeroline": False,
            "fixedrange": True,
            "tickvals": [0, 50, 100, 150, 200],
            "ticktext": ["200", "150", "100", "50", "0"],
            "title": "Time Elapsed (sec)",
        },
        yaxis={
            "range": [
                min(0, min(df["Speed"])),
                max(45, max(df["Speed"]) + max(df["SpeedError"])),
            ],
            "showgrid": True,
            "showline": True,
            "fixedrange": True,
            "zeroline": False,
            "gridcolor": app_color["graph_line"],
            "nticks": max(6, round(df["Speed"].iloc[-1] / 10)),
        },
    )

    return dict(data=[trace], layout=layout)


@app.callback(
    Output("wind-direction", "figure"), [Input("wind-speed-update", "n_intervals")]
)

def gen_wind_direction(interval):
    """
    Generate the wind direction graph.

    :params interval: update the graph based on an interval
    """

    total_time = get_current_time()
    df = get_wind_data_by_id(total_time)
    val = df["Speed"].iloc[-1]
    direction = [0, (df["Direction"][0] - 20), (df["Direction"][0] + 20), 0]

    traces_scatterpolar = [
        {"r": [0, val, val, 0], "fillcolor": "#084E8A"},
        {"r": [0, val * 0.65, val * 0.65, 0], "fillcolor": "#B4E1FA"},
        {"r": [0, val * 0.3, val * 0.3, 0], "fillcolor": "#EBF5FA"},
    ]

    data = [
        dict(
            type="scatterpolar",
            r=traces["r"],
            theta=direction,
            mode="lines",
            fill="toself",
            fillcolor=traces["fillcolor"],
            line={"color": "rgba(32, 32, 32, .6)", "width": 1},
        )
        for traces in traces_scatterpolar
    ]

    layout = dict(
        height=350,
        plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        font={"color": "#fff"},
        autosize=False,
        polar={
            "bgcolor": app_color["graph_line"],
            "radialaxis": {"range": [0, 45], "angle": 45, "dtick": 10},
            "angularaxis": {"showline": False, "tickcolor": "white"},
        },
        showlegend=False,
    )

    return dict(data=data, layout=layout)


@app.callback(
    Output("wind-histogram", "figure"),
    [Input("wind-speed-update", "n_intervals")],
    [
        State("wind-speed", "figure"),
        State("bin-slider", "value"),
        State("bin-auto", "value"),
    ],
)
def gen_wind_histogram(interval, wind_speed_figure, slider_value, auto_state):
    """
    Genererate wind histogram graph.

    :params interval: upadte the graph based on an interval
    :params wind_speed_figure: current wind speed graph
    :params slider_value: current slider value
    :params auto_state: current auto state
    """

    wind_val = []

    try:
        # Check to see whether wind-speed has been plotted yet
        if wind_speed_figure is not None:
            wind_val = wind_speed_figure["data"][0]["y"]
        if "Auto" in auto_state:
            bin_val = np.histogram(
                wind_val,
                bins=range(int(round(min(wind_val))), int(round(max(wind_val)))),
            )
        else:
            bin_val = np.histogram(wind_val, bins=slider_value)
    except Exception as error:
        raise PreventUpdate

    avg_val = float(sum(wind_val)) / len(wind_val)
    median_val = np.median(wind_val)

    pdf_fitted = rayleigh.pdf(
        bin_val[1], loc=(avg_val) * 0.55, scale=(bin_val[1][-1] - bin_val[1][0]) / 3
    )

    y_val = (pdf_fitted * max(bin_val[0]) * 20,)
    y_val_max = max(y_val[0])
    bin_val_max = max(bin_val[0])

    trace = dict(
        type="bar",
        x=bin_val[1],
        y=bin_val[0],
        marker={"color": app_color["graph_line"]},
        showlegend=False,
        hoverinfo="x+y",
    )

    traces_scatter = [
        {"line_dash": "dash", "line_color": "#2E5266", "name": "Average"},
        {"line_dash": "dot", "line_color": "#BD9391", "name": "Median"},
    ]

    scatter_data = [
        dict(
            type="scatter",
            x=[bin_val[int(len(bin_val) / 2)]],
            y=[0],
            mode="lines",
            line={"dash": traces["line_dash"], "color": traces["line_color"]},
            marker={"opacity": 0},
            visible=True,
            name=traces["name"],
        )
        for traces in traces_scatter
    ]

    trace3 = dict(
        type="scatter",
        mode="lines",
        line={"color": "#42C4F7"},
        y=y_val[0],
        x=bin_val[1][: len(bin_val[1])],
        name="Rayleigh Fit",
    )
    layout = dict(
        height=350,
        plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        font={"color": "#fff"},
        xaxis={
            "title": "Wind Speed (mph)",
            "showgrid": False,
            "showline": False,
            "fixedrange": True,
        },
        yaxis={
            "showgrid": False,
            "showline": False,
            "zeroline": False,
            "title": "Number of Samples",
            "fixedrange": True,
        },
        autosize=True,
        bargap=0.01,
        bargroupgap=0,
        hovermode="closest",
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "xanchor": "center",
            "y": 1,
            "x": 0.5,
        },
        shapes=[
            {
                "xref": "x",
                "yref": "y",
                "y1": int(max(bin_val_max, y_val_max)) + 0.5,
                "y0": 0,
                "x0": avg_val,
                "x1": avg_val,
                "type": "line",
                "line": {"dash": "dash", "color": "#2E5266", "width": 5},
            },
            {
                "xref": "x",
                "yref": "y",
                "y1": int(max(bin_val_max, y_val_max)) + 0.5,
                "y0": 0,
                "x0": median_val,
                "x1": median_val,
                "type": "line",
                "line": {"dash": "dot", "color": "#BD9391", "width": 5},
            },
        ],
    )
    return dict(data=[trace, scatter_data[0], scatter_data[1], trace3], layout=layout)


@app.callback(
    Output("bin-auto", "value"),
    [Input("bin-slider", "value")],
    [State("wind-speed", "figure")],
)
def deselect_auto(slider_value, wind_speed_figure):
    """ Toggle the auto checkbox. """

    # prevent update if graph has no data
    if "data" not in wind_speed_figure:
        raise PreventUpdate
    if not len(wind_speed_figure["data"]):
        raise PreventUpdate

    if wind_speed_figure is not None and len(wind_speed_figure["data"][0]["y"]) > 5:
        return [""]
    return ["Auto"]


@app.callback(
    Output("bin-size", "children"),
    [Input("bin-auto", "value")],
    [State("bin-slider", "value")],
)

def show_num_bins(autoValue, slider_value):
    """ Display the number of bins. """

    if "Auto" in autoValue:
        return "# of Bins: Auto"
    return "# of Bins: " + str(int(slider_value))


if __name__ == "__main__":
    #t = threading.Thread(target=get_data, args=[])
    #t.start()
    #sleep(10)
    #help(t)
    #time.sleep(2) 
    #t.raise_exception() 
    #t.join() 
    app.run_server()
    
