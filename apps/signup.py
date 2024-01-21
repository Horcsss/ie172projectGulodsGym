import hashlib
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

import hashlib

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_html_components as html

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2('Create your account', className='text-center'),  # Centered header
                            html.Hr(),
                            dbc.Alert('Please supply details.', color="danger", id='signup_alert', is_open=False),

                            html.Div(
                                [
                                    dbc.FormFloating(
                                        [
                                            dbc.Input(type="text", id="signup_username", placeholder="Enter a username"),
                                            dbc.Label("Username"),
                                        ]
                                    ),
                                ],
                                className="mb-3",
                            ),
                            html.Div(
                                [
                                dbc.FormFloating(
                                    [
                                        dbc.Input(type="password", id="signup_password", placeholder="Enter a password"),
                                        dbc.Label("Password"),
                                        html.Span(
                                            id='toggle_password_btn_signup',
                                            children="View password 👁️‍🗨️",
                                            style={"cursor": "pointer", "margin-left": "2px"},
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                ],
                                className="mb-3",
                            ),
                            html.Div(
                                [
                                    dbc.FormFloating(
                                        [
                                            dbc.Input(type="password", id="signup_passwordconf", placeholder="Re-type the password"),
                                            dbc.Label("Confirm Password"),
                                        ]
                                    ),
                                ],
                                className="mb-3",
                            ),

                            # Button to navigate back to the login page
                            dbc.Button('Sign up', color="warning", id='signup_signupbtn', className="w-100 mb-3"),

                            dbc.Button('Back to Login', color="dark", href='/login', className="w-100", size='sm'),

                            dbc.Modal(
                                [
                                    dbc.ModalHeader(dbc.ModalTitle("User Saved")),
                                    dbc.ModalBody("User has been saved", id='signup_confirmation'),
                                    dbc.ModalFooter(
                                        dbc.Button("Okay", href='/')
                                    ),
                                ],
                                id="signup_modal",
                                is_open=False,
                            ),
                        ]
                    ),
                    style={"width": "25rem", "margin": "auto"},  # Center the card in the middle
                ),
                width=12,  # Take up the full width of the column
                className="my-auto",  # Vertically center the column
            ),
            style={"height": "100vh", "width": "100%", "margin": "auto", 
                   "background-image": "url('https://i.ibb.co/TWv9JQ4/equipment-6.jpg')",  # Set your image URL here
                   "background-size": "cover",  # Ensure the image covers the entire container
                   "background-repeat": "no-repeat",  # Prevent the image from repeating
                   },
            align="center",  # Center the row horizontally
        ),
    ]
)

# Callback to toggle password visibility
@app.callback(
    [
    Output('signup_password', 'type'),
    ],
    [Input('toggle_password_btn_signup', 'n_clicks')],
    prevent_initial_call=True
)
def toggle_password_visibility_signup(n_clicks):
    # Toggle between 'password' and 'text' types
    password_type = ['text'] if n_clicks % 2 == 1 else ['password']
    return password_type


# disable the signup button if passwords do not match
@app.callback(
    [
        Output('signup_signupbtn', 'disabled'),
    ],
    [
        Input('signup_password', 'value'),
        Input('signup_passwordconf', 'value'),
    ]
)
def deactivatesignup(password, passwordconf):
    
    # enable button if password exists and passwordconf exists 
    #  and password = passwordconf
    enablebtn = password and passwordconf and password == passwordconf

    return [not enablebtn]


# To save the user
@app.callback(
    [
        Output('signup_alert', 'is_open'),
        Output('signup_modal', 'is_open')   
    ],
    [
        Input('signup_signupbtn', 'n_clicks')
    ],
    [
        State('signup_username', 'value'),
        State('signup_password', 'value')
    ]
)
def saveuser(loginbtn, username, password):
    openalert = openmodal = False
    if loginbtn:
        if username and password:
            sql = """INSERT INTO users (user_name, user_password)
            VALUES (%s, %s)"""  
            
            # This lambda fcn encrypts the password before saving it
            # for security purposes, not even database admins can see user passwords 
            encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()  
            
            values = [username, encrypt_string(password)]
            db.modifydatabase(sql, values)
            
            openmodal = True
        else:
            openalert = True
    else:
        raise PreventUpdate

    return [openalert, openmodal]
