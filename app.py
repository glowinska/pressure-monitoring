import datetime as dt
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import threading
from time import sleep
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from db.db_api import *

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

server = app.server

app_color = {"graph_bg": "#082255", "graph_line": "#309ADE"}

params = [
    'L0', 'L1', 'L2', 'R0', 'R1', 'R2'
]

figs = { 
    'L0': go.Figure(), 'L1': go.Figure(), 'L2': go.Figure(), 'R0': go.Figure(), 'R1': go.Figure(), 'R2': go.Figure()
}



app.layout = html.Div(
    [
        # header
        html.Div(
            [
                html.Div(
                    [
                        html.H4("MONITORING WALKING HABITS", className="app__header__title"),
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
                # wind date
                html.Div(
                    [
                        html.Div(
                            [html.H6("LEFT FOOT", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="l0",
                            figure=figs['L0'],
                            animate=True,
                        ),
                        dcc.Graph(
                            id="l1",
                            figure=figs['L1'],
                            animate=True,
                        ),
                        dcc.Graph(
                            id="l2",
                            figure=figs['L2'],
                            animate=True,
                        ),
                    ],
                    className="one-third column wind__date__container",
                ),
                # right foot
                html.Div(
                    [
                        html.Div(
                            [html.H6("RIGHT FOOT", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="r0",
                            figure=figs['R0'],
                            animate=True,
                        ),
                        dcc.Graph(
                            id="r1",
                            figure=figs['R1'],
                            animate=True,
                        ),
                            dcc.Graph(
                            id="r2",
                            figure=figs['R2'],
                            animate=True,
                        ),
                    ],
                    className="one-third column wind__date__container",
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


def get_current_date():
    now = dt.datetime.now()
    total_date = (now.hour * 3600) + (now.minute * 60) + (now.second)
    return total_date

@app.callback(
    Output('person-name', 'children'),
    Output('person-surname', 'children'),
    Output('person-year', 'children'),
    Output('person-disabled', 'children'),
    [dash.dependencies.Input('person-dropdown', 'value')])
def update_output(value):
    df = select_people_by_id(value)
    print(df)
    return 'NAME: {}'.format(df["name"][0]), 'SURNAME: {}'.format(df["surname"][0]), 'YEAR OF BIRTH: {}'.format(df["birth_year"][0]), 'DISABLED: {}'.format(bool(df["disabled"][0]))

def gen_diag(sensor_name, person_id):
    total_date = get_current_date()
    traces = select_traces(None, person_id)
    df = pd.DataFrame()
    for index, row in traces.iterrows():
        df = df.append(select_sensor_for_trace(None, row['id'], sensor_name))
    return df

@app.callback(
    Output("l0", "figure"),
    Output("l1", "figure"),
    Output("l2", "figure"),
    Output("r0", "figure"),
    Output("r1", "figure"),
    Output("r2", "figure"),
    [dash.dependencies.Input('person-dropdown', 'value')])
def draw_diag_for_person(value):
    for sensor_name in params:
        df = gen_diag(sensor_name, value)
        figs[sensor_name] = go.Figure()
        figs[sensor_name].update_layout(title=sensor_name, xaxis_title="Time", yaxis_title="Value")
        style=dict(
            plot_bgcolor=app_color["graph_bg"],
            paper_bgcolor=app_color["graph_bg"],
        )
        figs[sensor_name].update_layout(style)
        figs[sensor_name].add_trace(go.Scatter(x=df['date'], y=df['value'], mode="markers", name=sensor_name,))
    return figs["L0"], figs["L1"], figs["L2"], figs["R0"], figs["R1"], figs["R2"]

if __name__ == "__main__":
    #t = threading.Thread(target=get_data, args=[])
    #t.start()
    #draw_diag_for_person(1)
    app.run_server()
    
