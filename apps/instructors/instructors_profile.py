# Usual Dash dependencies
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd


from app import app

#for DB needs
from apps import dbconnect as db

#get the pair of keys and values from the url
from urllib.parse import urlparse, parse_qs

# store the layout objects into a variable named layout
layout = html.Div(
    [
        html.Div( # This div shall contain all dcc.Store objects
            [
                dcc.Store(id='instructorprofile_toload', storage_type='memory', data=0),
            ]
        ),
        
        dbc.Card(
            [
            dbc.CardHeader(html.H2('Instructor Details')),  # Card Header
            html.Hr(),
            dbc.CardBody(
                [
                    dbc.Alert(id='instructorprofile_alert', is_open=False), # For feedback purposes
            dbc.Form(
                [
                    dbc.Row(
                        [
                            dbc.Label("First Name", width=1),
                            dbc.Col(
                                dbc.Input(
                                    type='text',
                                    id='instructorprofile_fname',
                                    placeholder="First Name"
                                ),
                                width=5
                            )
                        ],
                        className='mb-3'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Last Name", width=1),
                            dbc.Col(
                                dbc.Input(
                                    type='text',
                                    id='instructorprofile_lname',
                                    placeholder="Last Name"
                                ),
                                width=5
                            )
                        ],
                        className='mb-3'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Address", width=1),
                            dbc.Col(
                                dbc.Input(
                                    type='text',
                                    id='instructorprofile_address',
                                    placeholder="Address"
                                ),
                                width=5
                            )
                        ],
                        className='mb-3'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Contact Number", width=1),
                            dbc.Col(
                                dbc.Input(
                                    type='text',
                                    id='instructorprofile_contactnumber',
                                    placeholder="Contact Number"
                                ),
                                width=5
                            )
                        ],
                        className='mb-3'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Birthdate", width=1),
                            dbc.Col(
                                dcc.DatePickerSingle(
                                    id='instructorprofile_birthdate',
                                    placeholder='Birthdate',
                                    month_format='MMM Do, YY',
                                ),
                                width=5
                            )
                        ],
                        className='mb-3'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Email", width=1),
                            dbc.Col(
                                dbc.Input(
                                    type='text',
                                    id='instructorprofile_email',
                                    placeholder="Email"
                                ),
                                width=5
                            )
                        ],
                        className='mb-3'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Sex", width=1),
                            dbc.Col(
                                dcc.Dropdown(
                                    id='instructorprofile_sex',
                                    placeholder='Sex'
                                ),
                                width=5
                            )
                        ],
                        className='mb-3'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Civil Status", width=1),
                            dbc.Col(
                                dcc.Dropdown(
                                    id='instructorprofile_civilstatus',
                                    placeholder='Civil Status'
                                ),
                                width=5
                            )
                        ],
                        className = 'mb-3'
                    ),
                ]
            ),
        html.Div(
            dbc.Row(
                [
                    dbc.Label("Delete Instructor", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='instructorprofile_removerecord',
                            options=[
                                {
                                    'label': "Mark for Deletion",
                                    'value': 1
                                }
                            ], # I want the label to be bold
                            style={'fontWeight':'bold'},
                        ),
                        width=7,
                    ),
                ],
                className="mb-3",
            ),
            id='instructorprofile_removerecord_div'
        ),
                    dbc.Button(
                        'Submit',
                        id='instructorprofile_submit',
                        n_clicks=0 # Initialize number of clicks
                    ),
                ]
            )
            ]
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(
                    html.H4('Save Success')
                ),
                 dbc.ModalBody(
                    [
                        'Instructor has been saved.'
                    ], id='instructorprofile_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/instructors/instructors_home',  # Clicking this would lead to a change of pages
                        id='instructorprofile_btn_modal'
                    )
                )
            ],
            centered=True,
            id='instructorprofile_successmodal',
            backdrop='static'  # Dialog box does not go away if you click at the background
        )
    ]
)

@app.callback(
    [
        # dbc.Alert Properties
        Output('instructorprofile_alert', 'color'),
        Output('instructorprofile_alert', 'children'),
        Output('instructorprofile_alert', 'is_open'),
        # dbc.Modal Properties
        Output('instructorprofile_successmodal', 'is_open'),
        Output('instructorprofile_feedback_message', 'children'),
        Output('instructorprofile_btn_modal', 'href'),
    ],
    [
        # for buttons, the property n_clicks
        Input('instructorprofile_submit', 'n_clicks'),
        Input('instructorprofile_btn_modal', 'n_clicks'),
    ],
    [
        State('instructorprofile_fname', 'value'),
        State('instructorprofile_lname', 'value'),
        State('instructorprofile_address', 'value'),
        State('instructorprofile_contactnumber', 'value'),
        State('instructorprofile_birthdate', 'date'),
        State('instructorprofile_email', 'value'),
        State('instructorprofile_sex', 'value'),
        State('instructorprofile_civilstatus', 'value'),
        State('url', 'search'),
        State('instructorprofile_removerecord', 'value'),
    ]
)
def instructorprofile_saveprofile(submitbtn, instructorid, instructorfname, instructorlname, instructoraddress, instructorcontactnumber, instructorbirthdate,
                                instructoremail, instructorsex, instructorcivilstatus, search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    
        if eventid == 'instructorprofile_submit' and submitbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            feedbackmessage = ''
            okay_href = None

            if not instructorfname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the instructor first name.'
            elif not instructorlname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the instructor last name.'
            elif not instructoraddress:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the instructor address.'
            elif not instructorcontactnumber:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the instructor contact number.'
            elif len(str(instructorcontactnumber)) != 10:
                alert_open = True
                alert_color = 'warning'
                alert_text = 'Contact number should be 10 digits.'
            elif not instructorbirthdate:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the instructor birthdate.'
            elif not instructoremail:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the instructor email.'
            elif not instructorsex:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the instructor sex.'
            elif not instructorcivilstatus:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the instructor civil status'

            else:
                # Add the data into the db
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]
                
                if create_mode == 'add':
                    sql = """
                        INSERT INTO instructor_info (instructor_fname, instructor_lname, instructor_address, instructor_contactnumber,
                        instructor_birthdate, instructor_email, instructor_sex_id, instructor_civilstatus_id, instructor_delete_ind)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    values = [instructorfname, instructorlname, instructoraddress, instructorcontactnumber, instructorbirthdate,
                            instructoremail, instructorsex, instructorcivilstatus, False]
                    
                    db.modifydatabase(sql, values)

                    feedbackmessage = "Instructor has been saved"
                    okay_href = '/instructors/instructors_home'
                    modal_open = True

                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    instructorid = parse_qs(parsed.query)['id'][0]

                    sqlcode = """UPDATE instructor_info
                    SET
                        instructor_fname = %s,
                        instructor_lname = %s,
                        instructor_address = %s,
                        instructor_contactnumber = %s,
                        instructor_birthdate = %s,
                        instructor_email = %s,
                        instructor_sex_id = %s,
                        instructor_civilstatus_id = %s,
                        instructor_delete_ind = %s
                    WHERE
                        instructor_id = %s
                    """

                    to_delete = bool(removerecord)

                    values = [instructorfname, instructorlname, instructoraddress, instructorcontactnumber, instructorbirthdate,
                            instructoremail, instructorsex, instructorcivilstatus, to_delete, instructorid]
                    db.modifydatabase(sqlcode, values)

                    if to_delete:
                        sql_soft_delete = """
                            UPDATE instructor_info
                            SET instructor_delete_ind = TRUE
                            WHERE instructor_id = %s
                        """
                        db.modifydatabase(sql_soft_delete, [instructorid])

                        feedbackmessage = "Instructor has been marked for deletion."
                        okay_href = '/instructors/instructors_home'
                        modal_open = True

                    feedbackmessage = "Instructor information has been updated."
                    okay_href = '/instructors/instructors_home'
                    modal_open = True

                else:
                    raise PreventUpdate

            return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]

        else:
            raise PreventUpdate
    else:
         raise PreventUpdate


@app.callback(
    [
        Output('instructorprofile_sex', 'options'),
        Output('instructorprofile_civilstatus', 'options'),
        Output('instructorprofile_toload', 'data'),
        Output('instructorprofile_removerecord_div', 'style')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)

def instructorprofile_loaddropdown(pathname, search):

    if pathname == '/instructors/instructors_profile':
        sql = """
            SELECT sex_name as label, sex_id as value from member_sex
        """
        values =[]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        sex_options = df.to_dict('records')

        sql = """
            SELECT civil_status as label, civilstatus_id as value from civilstatus
        """
        values =[]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        civilstatusid_options = df.to_dict('records')

        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        removerecord_div = None if to_load else {'display': 'none'}

    else:
        raise PreventUpdate
    
    return [sex_options, civilstatusid_options, to_load, removerecord_div]

@app.callback(
    [
        Output('instructorprofile_fname', 'value'),
        Output('instructorprofile_lname', 'value'),
        Output('instructorprofile_address', 'value'),
        Output('instructorprofile_contactnumber', 'value'),
        Output('instructorprofile_birthdate', 'date'),
        Output('instructorprofile_email', 'value'),
        Output('instructorprofile_sex', 'value'),
        Output('instructorprofile_civilstatus', 'value'),
    ],
    [
        Input('instructorprofile_toload', 'modified_timestamp'),
    ],
    [
        State('instructorprofile_toload', 'data'),
        State('url', 'search'),
    ]
)

def instructorprofile_loadinstructordetails(timestamp, to_load, search):
    if to_load == 1:        

        parsed = urlparse(search)
        instructorid = parse_qs(parsed.query)['id'][0]

        sql = """
            SELECT instructor_fname, instructor_lname, instructor_address, instructor_contactnumber,
                    instructor_birthdate, instructor_email, instructor_sex_id, instructor_civilstatus_id
            FROM instructor_info
            WHERE instructor_id = %s
        """
        values = [instructorid]
        col = ['First Name', 'Last Name', 'Address', 'Contact Number', 'Date of Birth', 'Email',
                'Sex', 'Civil Status' ]
        
        df = db.querydatafromdatabase(sql, values, col)

        
        firstname = df['First Name'][0]
        lastname = df['Last Name'][0]
        address = df['Address'][0]
        contactnumber = df['Contact Number'][0]
        dateofbirth = df['Date of Birth'][0]
        email = df['Email'][0]
        sexid = int(df['Sex'][0])
        civilstatusid = int(df['Civil Status'][0])
        
        return [firstname, lastname, address, contactnumber, dateofbirth, email, sexid, civilstatusid]
    
    else:
        raise PreventUpdate


