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
                dcc.Store(id='classlist_toload', storage_type='memory', data=0),
            ]
        ),

        dbc.Card(
            [
            dbc.CardHeader(html.H2('Class Details')),  # Card Header
            html.Hr(),
            dbc.CardBody(
                [
                    dbc.Alert(id='classlist_alert', is_open=False), # For feedback purposes
            dbc.Form(
                [
                    dbc.Row(
                        [
                            dbc.Label("Class Name", width=1),
                            dbc.Col(
                                dbc.Input(
                                    type='text',
                                    id='classlist_classname',
                                    placeholder="Class Name"
                                ),
                                width=5
                            )
                        ],
                        className='mb-3'
                    ),
                        dbc.Row(
                            [
                                dbc.Label("Class Description", width=1),
                                dbc.Col(
                                    dbc.Textarea(
                                        id='classlist_classdesc',
                                        placeholder="Description",
                                        style={'height': '100px', 'width': '100%'}  # Adjust the height and width as needed
                                    ),
                                    width=5
                                )
                            ],
                            className='mb-3'
                        ),
                    dbc.Row(
                        [
                            dbc.Label("Instructor", width=1),
                            dbc.Col(
                                dcc.Dropdown(
                                    id='classlist_instructors',
                                    placeholder='Instructor'
                                ),
                                width=5
                            )
                        ],
                        className='mb-3'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Schedule", width=1),
                            dbc.Col(
                                dbc.Input(
                                    type='text',
                                    id='classlist_schedule',
                                    placeholder="Schedule"
                                ),
                                width=5
                            )
                        ],
                        className='mb-3'
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Rates", width=1),
                            dbc.Col(
                                dbc.Input(
                                    type='text',
                                    id='classlist_rates',
                                    placeholder="Rates"
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
                    dbc.Label("Delete Class", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='classlist_removerecord',
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
            id='classlist_removerecord_div'
        ),
                    dbc.Button(
                        'Submit',
                        id='classlist_submit',
                        n_clicks=0  # Initialize number of clicks
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
                        'Class has been saved.'
                    ], id='classlist_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/classes/classes_home',  # Clicking this would lead to a change of pages
                        id='classlist_btn_modal'
                    )
                )
            ],
            centered=True,
            id='classlist_successmodal',
            backdrop='static'  # Dialog box does not go away if you click at the background
        )
    ]
)

@app.callback(
    [
        # dbc.Alert Properties
        Output('classlist_alert', 'color'),
        Output('classlist_alert', 'children'),
        Output('classlist_alert', 'is_open'),
        # dbc.Modal Properties
        Output('classlist_successmodal', 'is_open'),
        Output('classlist_feedback_message', 'children'),
        Output('classlist_btn_modal', 'href'),
    ],
    [
        # for buttons, the property n_clicks
        Input('classlist_submit', 'n_clicks'),
        Input('classlist_btn_modal', 'n_clicks'),
    ],
    [
        State('classlist_classname', 'value'),
        State('classlist_classdesc', 'value'),
        State('classlist_instructors', 'value'),
        State('classlist_schedule', 'value'),
        State('classlist_rates', 'value'),
        State('url', 'search'),
        State('classlist_removerecord', 'value')
    ]
)
def classlistsaveprofile(submitbtn, classid, classname, classdesc, instructorid, schedule, rates, search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    
        if eventid == 'classlist_submit' and submitbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            feedbackmessage = ''
            okay_href = None

            if not classname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the class name.'
            elif not classdesc:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the class description.'
            elif not schedule:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the class schedule.'
            elif not rates:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the class rates.'

            else:
                # Add the data into the db
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]
                
                if create_mode == 'add':
                    sql = """
                        INSERT INTO class_info (class_name, class_description, instructor_id, schedule, rates, class_delete_ind)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    values = [classname, classdesc, instructorid, schedule, rates, False]
                    
                    db.modifydatabase(sql, values)

                    feedbackmessage = "Class has been saved"
                    okay_href = '/classes/classes_home'
                    modal_open = True

                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    classid = parse_qs(parsed.query)['id'][0]

                    sqlcode = """UPDATE class_info
                    SET
                        class_name = %s,
                        class_description = %s,
                        instructor_id = %s,
                        schedule = %s,
                        rates = %s,
                        class_delete_ind = %s
                    WHERE
                        class_id = %s
                    """

                    to_delete = bool(removerecord)

                    values = [classname, classdesc, instructorid, schedule, rates, to_delete, classid]
                    db.modifydatabase(sqlcode, values)

                    if to_delete:
                        sql_soft_delete = """
                            UPDATE class_info
                            SET class_delete_ind = TRUE
                            WHERE class_id = %s
                        """
                        db.modifydatabase(sql_soft_delete, [classid])

                        feedbackmessage = "Class has been marked for deletion."
                        okay_href = '/classes/classes_home'
                        modal_open = True

                    feedbackmessage = "Class information has been updated."
                    okay_href = '/classes/classes_home'
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
        Output('classlist_instructors', 'options'),
        Output('classlist_toload', 'data'),
        Output('classlist_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def classlist_loaddropdown(pathname, search):

    if pathname == '/classes/classes_list':
        sql = """
            SELECT CONCAT(instructor_fname, ' ', instructor_lname) as label, instructor_id as value from instructor_info
        """
        values =[]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        instructors_options = df.to_dict('records')

        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        removerecord_div = None if to_load else {'display': 'none'}

    else:
        raise PreventUpdate
    
    return [instructors_options, to_load, removerecord_div]

@app.callback(
    [
        Output('classlist_classname', 'value'),
        Output('classlist_classdesc', 'value'),
        Output('classlist_instructors', 'value'),
        Output('classlist_schedule', 'value'),
        Output('classlist_rates', 'value'),
    ],
    [
        Input('classlist_toload', 'modified_timestamp'),
    ],
    [
        State('classlist_toload', 'data'),
        State('url', 'search'),
    ]
)

def classprofile_loadclassdetails(timestamp, to_load, search):
    if to_load == 1:        

        parsed = urlparse(search)
        classid = parse_qs(parsed.query)['id'][0]

        sql = """
            SELECT class_name, class_description, instructor_id, schedule, rates
            FROM class_info
            WHERE class_id = %s
        """
        values = [classid]
        col = ['Class Name','Class Description', 'Instructor Name', 'Schedule', 'Rates']
        
        df = db.querydatafromdatabase(sql, values, col)

        
        classname= df['Class Name'][0]
        classdesc= df['Class Description'][0]
        instructor_name_value = df['Instructor Name'][0]
        instructorid = int(instructor_name_value) if instructor_name_value is not None else None
        schedule = df['Schedule'][0]
        rates = df['Rates'][0]

        
        return [classname, classdesc, instructorid, schedule, rates]
    
    else:
        raise PreventUpdate