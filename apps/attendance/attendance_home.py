# Usual Dash dependencies
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

# callbacks here
from app import app

from apps import dbconnect as db

# store the layout objects into a variable named layout
layout = html.Div(
    [
        html.H1([html.Span("📋", style={'margin-right': '0.5em'}), "ATTENDANCE"],
                style={'background-color': '#ffc404', 'text-align': 'center'}),
        html.Hr(),
        dbc.Card(  # Card Container
            [
                dbc.CardHeader(  # Define Card Header
                    [
                        html.H3('Manage Attendance')
                    ]
                ),
                dbc.CardBody(  # Define Card Contents
                    [
                        html.Div(  # Add Entry Btn
                            [
                                dbc.Button(
                                    "Add Entry",
                                    color='warning',
                                    href='/attendance/attendance_list?mode=add'
                                ),
                            ]
                        ),
                        html.Hr(),
                        html.Div(  # Create section to show attendance list
                            [
                                html.H4('Attendance List'),
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='Attendancehome_memberfilter',
                                                        placeholder='Member Name'
                                                    ),
                                                ),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='Attendancehome_classtypefilter',
                                                        placeholder='Class Type'
                                                    ),
                                                ),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id='Attendancehome_membershiptypefilter',
                                                        options=[
                                                            {'label': 'Walk-in', 'value': 'Walk-in'},
                                                            {'label': 'Member', 'value': 'Member'}
                                                        ],
                                                        placeholder='Membership Type',
                                                        multi=False
                                                    ),
                                                ),
                                                dbc.Col(
                                                    dcc.DatePickerRange(
                                                        id='Attendancehome_datefilter',
                                                        start_date='',
                                                        end_date='',
                                                        display_format='YYYY-MM-DD',
                                                    ),
                                                ),
                                            ],
                                            className='mb-3',  # Add a margin-bottom to the row
                                            style={'margin-top': '20px'}  # Add a margin-top to the row
                                        ),
                                        dbc.Button(
                                            "Search",
                                            id='Attendancehome_searchbutton',
                                            color='primary',
                                            style={'margin-top': '10px'}  # Adjust margin-top for the search button
                                        ),
                                        html.Div(
                                            dbc.Table(id='attendancehome_attendancelist', striped=True, bordered=True,
                                                      hover=True, size='sm',
                                                      style={'margin-top': '20px'})  # Adjust margin-top for the table
                                        ),
                                    ],
                                ),
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)
# Table
@app.callback(
    [
        Output('attendancehome_attendancelist', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('Attendancehome_searchbutton', 'n_clicks'),
    ],
    [
        State('Attendancehome_memberfilter', 'value'),
        State('Attendancehome_classtypefilter', 'value'),
        State('Attendancehome_membershiptypefilter', 'value'),
        State('Attendancehome_datefilter', 'start_date'),
        State('Attendancehome_datefilter', 'end_date'),
    ]
)
def attendancehome_loadattendancelist(pathname, n_clicks, member_filter, classtype_filter, membershiptype_filter, start_date, end_date):
    if pathname == '/attendance/attendance_home':
        if n_clicks is None:
            raise PreventUpdate

        # Check if start_date and end_date are empty strings, and replace with None
        start_date = start_date if start_date else None
        end_date = end_date if end_date else None

        sql = """
            SELECT
                CONCAT(m.member_fname, ' ', m.member_lname) AS "Member Name",
                c.class_name AS "Class Type",
                s.membership AS "Membership Type",
                a.amount_paid AS "Amount Paid",
                TO_CHAR(a.timein, 'YYYY-MM-DD') AS "Date Logged In",
                TO_CHAR(a.timein, 'HH24:MI:SS') AS "Time Logged In"
            FROM
                attendance a
            LEFT JOIN
                member_info m ON a.member_id = m.member_id
            LEFT JOIN
                class_info c ON a.class_id = c.class_id
            LEFT JOIN
                membershiptype s ON a.typeid = s.typeid
            WHERE
                (COALESCE(%s::text, '') = '' OR COALESCE(m.member_fname, '') ILIKE %s
                OR COALESCE(m.member_lname, '') ILIKE %s)
                AND (COALESCE(%s::text, '') = '' OR COALESCE(c.class_name, '') ILIKE %s)
                AND (COALESCE(%s::text, '') = '' OR COALESCE(s.membership, '') ILIKE %s)
                AND (COALESCE(%s::date, '1900-01-01') = '1900-01-01' OR a.timein::date BETWEEN %s::date AND %s::date)
        """
        values = [member_filter, f"%{member_filter}%", f"%{member_filter}%",
                  classtype_filter, f"%{classtype_filter}%",
                  membershiptype_filter, f"%{membershiptype_filter}%",
                  start_date, start_date, end_date]

        cols = ['Member Name', 'Class Type', 'Membership Type', 'Amount Paid', 'Date Logged In', 'Time Logged In']

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape[0]:
            return [dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')]
        else:
            empty_df = pd.DataFrame(columns=cols)
            return [dbc.Table.from_dataframe(empty_df, striped=True, bordered=True, hover=True, size='sm')]
    else:
        raise PreventUpdate