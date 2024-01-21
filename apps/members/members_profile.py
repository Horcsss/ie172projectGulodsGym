# Usual Dash dependencies
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import re

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
                dcc.Store(id='memberprofile_toload', storage_type='memory', data=0),
            ]
        ),
        dbc.Card(
            [
            dbc.CardHeader(html.H2('Member Details')),  # Card Header
            html.Hr(),
            dbc.CardBody(
                [
                    dbc.Alert(id='memberprofile_alert', is_open=False), # For feedback purposes
            dbc.Form(
                [
                    dbc.Row(
                        [
                            dbc.Label("First Name", width=1),
                            dbc.Col(
                                dbc.Input(
                                    type='text',
                                    id='memberprofile_fname',
                                    placeholder="First Name"
                                ),
                                width=5
                            )
                        ],
                        className = 'mb-3'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Middle Name", width=1),
                            dbc.Col(
                                dbc.Input(
                                    type='text',
                                    id='memberprofile_mname',
                                    placeholder="Middle Name"
                                ),
                                width=5
                            )
                        ],
                        className = 'mb-3'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Last Name", width=1),
                            dbc.Col(
                                dbc.Input(
                                    type='text',
                                    id='memberprofile_lname',
                                    placeholder="Last Name"
                                ),
                                width=5
                            )
                        ],
                        className = 'mb-3'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Address", width=1),
                            dbc.Col(
                                dbc.Input(
                                    type='text',
                                    id='memberprofile_address',
                                    placeholder="Address"
                                ),
                                width=5
                            )
                        ],
                        className = 'mb-3'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Contact Number", width=1),
                            dbc.Col(
                                dbc.Input(
                                    type='text',
                                    id='memberprofile_contactnumber',
                                    placeholder="eg. 9123456789"
                                ),
                                width=5
                            )
                        ],
                        className = 'mb-3'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Birthdate", width=1),
                            dbc.Col(
                                dcc.DatePickerSingle(
                                    id='memberprofile_birthdate',
                                    placeholder='Birthdate',
                                    month_format='MMM Do, YY',
                                ),
                                width=5
                            )
                        ],
                        className = 'mb-3'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Email", width=1),
                            dbc.Col(
                                dbc.Input(
                                    type='text',
                                    id='memberprofile_email',
                                    placeholder="Email"
                                ),
                                width=5
                            )
                        ],
                        className = 'mb-3'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Medical Details", width=1),
                            dbc.Col(
                                dbc.Input(
                                    type='text',
                                    id='memberprofile_medicaldetails',
                                    placeholder="Medical Details. Type NA if none"
                                ),
                                width=5
                            )
                        ],
                        className = 'mb-3'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Emergency Contact", width=1),
                            dbc.Col(
                                dbc.Input(
                                    type='text',
                                    id='memberprofile_emergencycontact',
                                    placeholder="Emergency Contact"
                                ),
                                width=5
                            )
                        ],
                        className = 'mb-3'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Emergency Contact Number", width=1),
                            dbc.Col(
                                dbc.Input(
                                    type='text',
                                    id='memberprofile_emergencycontactnumber',
                                    placeholder="eg. 9123456789"
                                ),
                                width=5
                            )
                        ],
                        className = 'mb-3'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Sex", width=1),
                            dbc.Col(
                                dcc.Dropdown(
                                    id='memberprofile_sex',
                                    placeholder='Sex'
                                ),
                                width=5
                            )
                        ],
                        className = 'mb-3'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Civil Status", width=1),
                            dbc.Col(
                                dcc.Dropdown(
                                    id='memberprofile_civilstatus',
                                    placeholder='Civil Status'
                                ),
                                width=5
                            )
                        ],
                        className = 'mb-3'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Membership Type", width=1),
                            dbc.Col(
                                dcc.Dropdown(
                                    id='memberprofile_membertypeid',
                                    placeholder='Membership Type'
                                ),
                                width=5
                            )
                        ],
                        className = 'mb-3'
                        ),
                                dbc.Row(
                                    [
                                        dbc.Label("Amount Paid for Subscription (Leave blank if Walk-in)", width=1),
                                        dbc.Col(
                                            dcc.Input(
                                                type='number',
                                                id='memberprofile_subscription_amount_paid',
                                                placeholder='Enter Amount Paid'
                                            ),
                                            width=5
                                        ),
                                    ],
                                    className='mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Date Added", width=1),
                                        dbc.Col(
                                            dcc.DatePickerSingle(
                                                id='memberprofile_date_added',
                                                placeholder='Date Added',
                                                month_format='MMM Do, YY',
                                            ),
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
                    dbc.Label("Delete Member", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='memberprofile_removerecord',
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
            id='memberprofile_removerecord_div'
        ),
                    dbc.Button(
                        'Submit',
                        id='memberprofile_submit',
                        n_clicks=0 # Initialize number of clicks
                    ),
                ]
            )
            ]
        ),
        dbc.Modal( # Modal = dialog box; feedback for successful saving.
            [
                dbc.ModalHeader(
                    html.H4('Save Success')
                ),
                dbc.ModalBody(
                    [
                        'Member has been saved.'
                    ], id = 'memberprofile_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/members/members_home', # Clicking this would lead to a change of pages
                        id = 'memberprofile_btn_modal'
                    )
                )
            ],
            centered=True,
            id='memberprofile_successmodal',
            backdrop='static' # Dialog box does not go away if you click at the background
        )
    ]
)



@app.callback(
    [
        Output('memberprofile_alert', 'color'),
        Output('memberprofile_alert', 'children'),
        Output('memberprofile_alert', 'is_open'),
        Output('memberprofile_successmodal', 'is_open'),
        Output('memberprofile_feedback_message', 'children'),
        Output('memberprofile_btn_modal', 'href'),
    ],
    [
        Input('memberprofile_submit', 'n_clicks'),
        Input('memberprofile_btn_modal', 'n_clicks'),
    ],
    [
        State('memberprofile_fname', 'value'),
        State('memberprofile_mname', 'value'),
        State('memberprofile_lname', 'value'),
        State('memberprofile_address', 'value'),
        State('memberprofile_contactnumber', 'value'),
        State('memberprofile_birthdate', 'date'),
        State('memberprofile_email', 'value'),
        State('memberprofile_medicaldetails', 'value'),
        State('memberprofile_emergencycontact', 'value'),
        State('memberprofile_emergencycontactnumber', 'value'),
        State('memberprofile_sex', 'value'),
        State('memberprofile_civilstatus', 'value'),
        State('memberprofile_membertypeid', 'value'),
        State('memberprofile_subscription_amount_paid', 'value'),
        State('memberprofile_date_added', 'date'),
        State('url', 'search'),
        State('memberprofile_removerecord', 'value'),
    ]
)
def memberprofile_saveprofile(submitbtn, memberid, memberfname, membermname, memberlname, memberaddress, membercontactnumber, memberbirthdate,
                              memberemail, membermedicaldetails, memberemergencycontact, memberemergencycontactnumber,
                              membersex, membercivilstatus, membertypeid, subscription_amount_paid, date_added, search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    
        if eventid == 'memberprofile_submit' and submitbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            feedbackmessage = ''
            okay_href = None
            
            if not memberfname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the member first name.'
            elif not memberlname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the member last name.'
            elif not memberaddress:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the member last name.'
            elif not membercontactnumber:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the member contact number.'
            elif not memberbirthdate:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the member birthdate.'
            elif not memberemail:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the member email.'
            elif not membermedicaldetails:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the member medical details.'
            elif not memberemergencycontact:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the member emergency contact.'
            elif not memberemergencycontactnumber:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the member emergency contact number.'
            elif not membersex:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the member sex.'
            elif not membercivilstatus:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the member civil status.'
            elif not membertypeid:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the membership type.'
            elif len(str(membercontactnumber)) != 10:
                alert_open = True
                alert_color = 'warning'
                alert_text = 'Contact number should be 10 digits.'
            elif len(str(memberemergencycontactnumber)) != 10:
                alert_open = True
                alert_color = 'warning'
                alert_text = 'Contact number should be 10 digits.'
            
            else:
                # Add the data into the db
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]
                
                if create_mode == 'add':
                    sql = """
                        INSERT INTO member_info (member_fname, member_mname, member_lname, member_address, member_contactnumber,
                        member_birthdate, member_email, member_medicaldetails, member_emergencycontact, 
                        member_emergencycontactnumber, sex_id, civilstatus_id, typeid, member_delete_ind, subscription_amount_paid, date_added)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    values = [memberfname, membermname, memberlname, memberaddress, membercontactnumber, memberbirthdate,
                              memberemail, membermedicaldetails, memberemergencycontact, memberemergencycontactnumber,
                              membersex, membercivilstatus, membertypeid, False, subscription_amount_paid, date_added]

                    db.modifydatabase(sql, values)

                    feedbackmessage = "Member has been saved"
                    okay_href = '/members/members_home'
                    modal_open = True
                    
                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    memberid = parse_qs(parsed.query)['id'][0]

                    sqlcode = """UPDATE member_info
                    SET
                        member_fname = %s,
                        member_mname = %s,
                        member_lname = %s,
                        member_address = %s,
                        member_contactnumber = %s,
                        member_birthdate = %s,
                        member_email = %s,
                        member_medicaldetails = %s,
                        member_emergencycontact = %s,
                        member_emergencycontactnumber = %s,
                        sex_id = %s,
                        civilstatus_id = %s,
                        typeid = %s,
                        member_delete_ind = %s,
                        subscription_amount_paid = %s,
                        date_added = %s
                    WHERE
                        member_id = %s
                    """

                    to_delete = bool(removerecord)

                    values = [memberfname, membermname, memberlname, memberaddress, membercontactnumber, memberbirthdate,
                              memberemail, membermedicaldetails, memberemergencycontact, memberemergencycontactnumber,
                              membersex, membercivilstatus, membertypeid, to_delete, subscription_amount_paid, date_added, memberid]
                    db.modifydatabase(sqlcode, values)

                    if to_delete:
                        sql_soft_delete = """
                            UPDATE member_info
                            SET member_delete_ind = TRUE
                            WHERE member_id = %s
                        """
                        db.modifydatabase(sql_soft_delete, [memberid])

                        feedbackmessage = "Member has been marked for deletion."
                        okay_href = '/members/members_home'
                        modal_open = True

                    feedbackmessage = "Member information has been updated."
                    okay_href = '/members/members_home'
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
        Output('memberprofile_sex', 'options'),
        Output('memberprofile_civilstatus', 'options'),
        Output('memberprofile_membertypeid', 'options'),
        Output('memberprofile_toload', 'data'),
        Output('memberprofile_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def memberprofile_loaddropdown(pathname, search):

    if pathname == '/members/members_profile':
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
        civilstatus_options = df.to_dict('records')

        sql = """
            SELECT membership as label, typeid as value from membershiptype
        """
        values =[]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        membertype_options = df.to_dict('records')

        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        removerecord_div = None if to_load else {'display': 'none'}

    else:
        raise PreventUpdate
    
    return [sex_options, civilstatus_options, membertype_options, to_load, removerecord_div]

@app.callback(
    [
        Output('memberprofile_fname', 'value'),
        Output('memberprofile_mname', 'value'),
        Output('memberprofile_lname', 'value'),
        Output('memberprofile_address', 'value'),
        Output('memberprofile_contactnumber', 'value'),
        Output('memberprofile_birthdate', 'date'),
        Output('memberprofile_email', 'value'),
        Output('memberprofile_medicaldetails', 'value'),
        Output('memberprofile_emergencycontact', 'value'),
        Output('memberprofile_emergencycontactnumber', 'value'),
        Output('memberprofile_sex', 'value'),
        Output('memberprofile_civilstatus', 'value'),
        Output('memberprofile_membertypeid', 'value'),
        Output('memberprofile_subscription_amount_paid', 'value'),
        Output('memberprofile_date_added', 'date'),
    ],
    [
        Input('memberprofile_toload', 'modified_timestamp'),
    ],
    [
        State('memberprofile_toload', 'data'),
        State('url', 'search'),
    ]
)
def memberprofile_loadmemberdetails(timestamp, to_load, search):
    if to_load == 1:        

        parsed = urlparse(search)
        memberid = parse_qs(parsed.query)['id'][0]

        sql = """
            SELECT member_fname, member_mname, member_lname, member_address, member_contactnumber, 
            member_birthdate, member_email, member_medicaldetails, member_emergencycontact, 
            member_emergencycontactnumber, sex_id, civilstatus_id, typeid, subscription_amount_paid, date_added
            FROM member_info
            WHERE member_id = %s
        """
        values = [memberid]
        col = ['First Name','Middle Name', 'Last Name', 'Address', 'Contact Number', 'Date of Birth', 'Email', 'Medical Details', 'Emergency Contact',
                'Emergency Contact Number', 'Sex', 'Civil Status', 'Membership Type', 'Subscription Amount Paid', 'Date Added']
        
        df = db.querydatafromdatabase(sql, values, col)

        
        firstname = df['First Name'][0]
        middlename = df['Middle Name'][0]
        lastname = df['Last Name'][0]
        address = df['Address'][0]
        contactnumber = df['Contact Number'][0]
        dateofbirth = df['Date of Birth'][0]
        email = df['Email'][0]
        medicaldetails = df['Medical Details'][0]
        emergencycontact = df['Emergency Contact'][0]
        emergencycontactnumber = df['Emergency Contact Number'][0]
        sexid = int(df['Sex'][0])
        civilstatusid = int(df['Civil Status'][0])
        typeid = int(df['Membership Type'][0])
        subscriptionamountpaid = df['Subscription Amount Paid'][0]
        dateadded = df['Date Added'][0]

        
        return [firstname, middlename, lastname, address, contactnumber, dateofbirth, email, medicaldetails, emergencycontact,
                emergencycontactnumber, sexid, civilstatusid, typeid, subscriptionamountpaid, dateadded]
    
    else:
        raise PreventUpdate

