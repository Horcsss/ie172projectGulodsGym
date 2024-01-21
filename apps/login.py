import hashlib
import dash_bootstrap_components as dbc
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from apps import dbconnect as db
import dash_html_components as html

warning_icon = "\u26A0"



carousel = dbc.Carousel(
        items=[
            {"key": "1", "src": "https://i.ibb.co/3hCJb82/1.png", "header": "Transform Your Body", 
             "caption": "Achieve your fitness goals with our personalized training programs and state-of-the-art facilities. Start your fitness journey today!"},
            {"key": "2", "src": "https://i.ibb.co/Df1vPzV/2.png", "header": "Diverse Classes, One Community",
             "caption": "Join our vibrant fitness community with a variety of classes, including boxing, dancing, and taekwondo. Experience the power of collective motivation and reach new heights together"},
            {"key": "3", "src": "https://i.ibb.co/DptTCG0/3.png", "header": "Unlock Your Potential, Unleash Your Power",
             "caption": "It's not just a workout; it's a journey to unlock your full potential and unleash the power within."},
        ],
        controls=False,
        indicators=False,
        interval=2200,  # Change slide every 4 seconds
        ride='carousel',
        style={"height": "20px"}
    ),

card_image = dbc.Card(
    dbc.CardImg(src="https://i.ibb.co/gF6DPhS/302611216-5411221435610918-1042162209739813418-n.jpg", top=True, style={"width": "60%"}),
    style={"width": "45rem", "background-color": "rgba(255, 255, 255, 0)"},
    outline=False,
)

login_card = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                [
                    html.Img(src="https://scontent.fmnl17-2.fna.fbcdn.net/v/t39.30808-6/279677672_5065406360192429_6832309912774742020_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=efb6e6&_nc_eui2=AeFkiw8FNl5lBlgWqJdizwVbLRSGFCvJOG4tFIYUK8k4bmVVzD0QWPirQnPT9iowFUCGnn1k0ywXagy4kE32MEUO&_nc_ohc=VZGd94TSqXMAX_z7Gqk&_nc_ht=scontent.fmnl17-2.fna&oh=00_AfCvOUX-AoWar9GhZBxS2z1EHNwP-9RfN6rvoZYGISgp6Q&oe=65A5E336", alt="Your Image", style={"width": "100%", "max-width": "200px"}),
                    html.H2('Please Log in', className='text-center'),
                ],
                className="d-flex flex-column align-items-center justify-content-center mb-4"
            ),
            
            html.Hr(),
            dbc.Alert(
                [
                    warning_icon,
                    "Username or password is incorrect.",
                ],
                color="danger", id='login_alert', is_open=False,
                className="d-flex align-items-center",
            ),

            dbc.FormFloating(
                [
                    dbc.Input(type="text", id="login_username", placeholder="Enter username", style={"width": "100%"}),
                    dbc.Label("Username", html_for="login_username"),
                ],
                className="mb-3",
            ),

            dbc.FormFloating(
                [
                    dbc.Input(type="password", id="login_password", placeholder="Enter password", style={"width": "100%"}),
                    dbc.Label("Password", html_for="login_password"),
                    html.Span(
                        id='toggle_password_btn',
                        children="View password 👁️‍🗨️",
                        style={"cursor": "pointer", "position": "relative", "left": "2px", "top": "2px"},
                    ),
                ],
                className="mb-3",
            ),

            dbc.Button('Login', color="dark", id='login_loginbtn', style={"width": "100%"}, className="mb-3"),
            html.Hr(),
            dbc.Button('Signup Now!', href='/signup', color="warning", style={"width": "100%"}, className="mr-1"),
            html.Div(
                "If you don't have an account yet, please sign up.",
                style={'color': 'red', 'margin-top': '11px'}
            )
        ],
        className="mx-auto",  # Center the content horizontally
    ),
    style={"width": "400px", "margin": "auto", "marginTop": "100px"},  # Adjust the width and marginTop to your preference
    color="light",
    outline=True,
)



layout = html.Div(
            [
            html.H1([html.Span(style={'margin-right': '0.5em'}), "GULOD'S GYM INFORMATION SYSTEM"], 
            style={'background-color': '#ffc404', 'text-align': 'center'}),
            dbc.Row(carousel),
            login_card])

# Callback to toggle password visibility
@app.callback(
    [
    Output('login_password', 'type'),
    ],
    [Input('toggle_password_btn', 'n_clicks')],
    prevent_initial_call=True
)
def toggle_password_visibility(n_clicks):
    # Toggle between 'password' and 'text' types
    password_type = ['text'] if n_clicks % 2 == 1 else ['password']
    return password_type


@app.callback(
    [
        Output('login_alert', 'is_open'),
        Output('currentuserid', 'data'),
    ],
    [
        Input('login_loginbtn', 'n_clicks'), # begin login query via button click
        Input('sessionlogout', 'modified_timestamp'), # reset session userid to -1 if logged out
    ],
    [
        State('login_username', 'value'),
        State('login_password', 'value'),   
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'), 
        State('url', 'pathname'), 
    ]
)
def loginprocess(loginbtn, sessionlogout_time,
                 username, password,
                 sessionlogout, currentuserid,
                 pathname):

    ctx = callback_context
    
    if ctx.triggered:
        openalert = False
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    else:
        raise PreventUpdate
    
    
    if eventid == 'login_loginbtn': # trigger for login process
        if loginbtn and username and password:
            sql = """SELECT user_id
            FROM users
            WHERE 
                user_name = %s AND
                user_password = %s AND
                NOT user_delete_ind"""
            
            # we match the encrypted input to the encrypted password in the db
            encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest() 
            
            values = [username, encrypt_string(password)]
            cols = ['userid']
            df = db.querydatafromdatabase(sql, values, cols)
            
            if df.shape[0]: # if query returns rows
                currentuserid = df['userid'][0]
            else:
                currentuserid = -1
                openalert = True

    elif eventid == 'sessionlogout' and pathname == '/logout': # reset the userid if logged out
        currentuserid = -1
        
    else:
        raise PreventUpdate
    
    return [openalert, currentuserid]


@app.callback(
    [
        Output('url', 'pathname'),
    ],
    [
        Input('currentuserid', 'modified_timestamp'),
    ],
    [
        State('currentuserid', 'data'), 
    ]
)
def routelogin(logintime, userid):
    ctx = callback_context
    if ctx.triggered:
        if userid > 0:
            url = '/home'
        else:
            url = '/'
    else:
        raise PreventUpdate
    return [url]
