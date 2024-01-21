# Usual Dash dependencies
from datetime import datetime
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from urllib.parse import urlparse, parse_qs

from app import app
from apps import dbconnect as db

# Store the layout objects into a variable named layout
layout = html.Div(
    [
        html.Div(
            [
                dcc.Store(id='attendance_toload', storage_type='memory', data=0),
            ]
        ),
        dbc.Card(
            [
                dbc.CardHeader(html.H2("Attendance")),
                html.Hr(),
                dbc.CardBody(
                    [
                        dbc.Alert(id='attendance_alert', is_open=False),
                        dbc.Form(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label("Member Name", width=1),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id='attendance_membername',
                                                placeholder="Member Name",
                                                value=''  # Add this line to initialize value
                                            ),
                                            width=5
                                        )
                                    ],
                                    className='mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Membership Type", width=1),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id='attendance_membershiptype',
                                                placeholder="Membership Type",
                                                value=''  # Add this line to initialize value
                                            ),
                                            width=5
                                        )
                                    ],
                                    className='mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Class Type", width=1),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id='attendance_classtype',
                                                placeholder="Class Attended",
                                                value=''  # Add this line to initialize value
                                            ),
                                            width=5
                                        )
                                    ],
                                    className='mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Amount Paid", width=1),
                                        dbc.Col(
                                            dcc.Input(
                                                id='attendance_amount_paid',
                                                type='number',
                                                placeholder='Enter Amount Paid'
                                            ),
                                            width=5
                                        ),
                                    ],
                                    className='mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Time-In", width=1),
                                        dbc.Col(
                                            html.Button("Log Time In", id='log-time-button', n_clicks=0, className="btn btn-success"),
                                            width=5
                                        )
                                    ],
                                    className='mb-3'
                                ),
                            ]
                        ),
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Delete Attendance", width=2),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='attendance_removerecord',
                                            options=[
                                                {
                                                    'label': "Mark for Deletion",
                                                    'value': 1
                                                }
                                            ],
                                            style={'fontWeight': 'bold'},
                                        ),
                                        width=7,
                                    ),
                                ],
                                className="mb-3",
                            ),
                            id='attendance_removerecord_div'
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(
                                    html.H4('Save Success')
                                ),
                                dbc.ModalBody(
                                    [
                                        'Attendance has been saved.'
                                    ], id='attendance_feedback_message'
                                ),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed",
                                        href='/attendance/attendance_home',
                                        id='attendance_list_btn_modal'
                                    )
                                )
                            ],
                            centered=True,
                            id='attendance_successmodal',
                            backdrop='static'
                        )
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    [
        Output('attendance_feedback_message', 'children'),
        Output('attendance_successmodal', 'is_open'),
    ],
    [
        Input('log-time-button', 'n_clicks')
    ],
    [
        State('attendance_membername', 'value'),
        State('attendance_membershiptype', 'value'),
        State('attendance_classtype', 'value'),
        State('attendance_removerecord', 'value'),
        State('url', 'search'),
        State('attendance_amount_paid', 'value'),
    ]
)
def log_time_in(n_clicks, member_id, membership_type, class_type, removerecord_div, search, amount_paid):
    if n_clicks == 0:
        raise PreventUpdate

    if not all(value for value in [membership_type, class_type, amount_paid]):
        print("Please fill in all fields")
        return ['Please fill in all fields'], False

    # Fetch member_name based on member_id
    member_name_sql = """
        SELECT CONCAT(m.member_fname, ' ', m.member_lname) AS label
        FROM member_info m
        WHERE m.member_id = %s;
    """
    member_name_values = [member_id]

    try:
        member_name_result = db.querydatafromdatabase(member_name_sql, member_name_values, ['label'])
        member_name = member_name_result.iloc[0]['label']
    except Exception as e:
        print("Error fetching member_name:", e)
        return ['Error fetching member_name'], False  # No modal, just display feedback

    # Record time in
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save to the database
    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query)['mode'][0]

    if create_mode == 'add':
        # Insert logic for add mode
        sql = """
            INSERT INTO attendance (member_id, typeid, class_id, timein, amount_paid)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = [member_id, membership_type, class_type, current_time, amount_paid]

        try:
            db.modifydatabase(sql, values)
            print(f'Time in recorded for {member_name} at {current_time}, Amount Paid: {amount_paid}')
            return [f'Time in recorded for {member_name} at {current_time}, Amount Paid: {amount_paid}'], True  # Show modal
        except Exception as e:
            print("Error:", e)
            return ['Error saving to the database'], False  # No modal, just display feedback

    else:
        raise PreventUpdate


@app.callback(
    [
        Output('attendance_membername', 'options'),
        Output('attendance_membershiptype', 'options'),
        Output('attendance_classtype', 'options'),
        Output('attendance_toload', 'data'),
        Output('attendance_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')    
    ],
    [
        State('url', 'search')
    ]
)
def attendance_loaddropdown(pathname, search):

    if pathname == '/attendance/attendance_list':
        # Load options for Member Name dropdown
        member_name_sql = """
            SELECT CONCAT(m.member_fname, ' ', m.member_lname) AS label, m.member_id AS value FROM member_info m;
        """
        member_name_values = []  # You might need to add relevant values here
        member_name_cols = ['label', 'value']
        member_name_df = db.querydatafromdatabase(member_name_sql, member_name_values, member_name_cols)
        member_name_options = member_name_df.to_dict('records')

        # Load options for Membership Type dropdown
        membership_type_sql = """
            SELECT membership AS label, s.typeid AS value FROM membershiptype s;
        """
        membership_type_values = []  # You might need to add relevant values here
        membership_type_cols = ['label', 'value']
        membership_type_df = db.querydatafromdatabase(membership_type_sql, membership_type_values, membership_type_cols)
        membership_type_options = membership_type_df.to_dict('records')

        # Load options for Class Type dropdown
        class_type_sql = """
            SELECT class_name AS label, class_id AS value FROM class_info;
        """
        class_type_values = []  # You might need to add relevant values here
        class_type_cols = ['label', 'value']
        class_type_df = db.querydatafromdatabase(class_type_sql, class_type_values, class_type_cols)
        class_type_options = class_type_df.to_dict('records')

        # Reuse the same df for all dropdowns
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return [
            member_name_options,
            membership_type_options,
            class_type_options,
            [{'label': current_time, 'value': current_time}],
            {'display': 'none'}  # Or provide the correct style
        ]

    else:
        raise PreventUpdate


