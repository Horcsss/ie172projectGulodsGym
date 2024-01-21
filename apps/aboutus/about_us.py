# Usual Dash dependencies
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app
from apps import dbconnect as db

carousel = dbc.Carousel(
        items=[
            {"key": "1", "src": "https://i.ibb.co/3hCJb82/1.png", "header": "Transform Your Body", 
             "caption": "Achieve your fitness goals with our personalized training programs and state-of-the-art facilities. Start your fitness journey today!"},
            {"key": "2", "src": "https://i.ibb.co/Df1vPzV/2.png", "header": "Diverse Classes, One Community",
             "caption": "Join our vibrant fitness community with a variety of classes, including boxing, dancing, and taekwondo. Experience the power of collective motivation and reach new heights together"},
            {"key": "3", "src": "https://i.ibb.co/DptTCG0/3.png", "header": "Unlock Your Potential, Unleash Your Power",
             "caption": "It's not just a workout; it's a journey to unlock your full potential and unleash the power within."},
        ],
        controls=True,
        indicators=True,
        interval=2500,  # Change slide every 4 seconds
        ride='carousel',
        style={"height": "100px"}
    ),


card_about = dbc.Card(
    dbc.CardBody(
        [
            html.H2("ABOUT US", className="card-title"),
            html.Hr(),
            html.P(
                "Welcome to Gulod's Gym, where fitness meets streamlined management. Our website empowers you, the manager, with easy member sign-ups, class coordination (boxing, dancing, taekwondo), and efficient payment tracking. Join us in creating a seamless fitness experience for our members. For any questions and concerns about the website, please approach Mr. Ariz Flores, or contact support at 0908-287-8659.",
            ),

            html.Br(),
            html.H2("OUR MISSION & VISION", className="card-title"),
            html.Hr(),
            html.P(
                "At Gulod's Gym, our mission is to empower diverse individuals through affordable fitness facilities and varied sessions. We unlock each member's potential, fostering strength and resilience, and strive to create a supportive community in KNL. Our vision extends to mental and emotional well-being, building camaraderie and guiding members towards holistic health. Together, we envision a thriving community at the intersection of fitness and well-being."
            ),
        ]
    ),
    style={"width": "45rem","margin-left":"5em","opacity":".8"},
    color="light",
    outline=True,
    
)


card_contact = dbc.Card(
    [
        dbc.CardImg(src="https://i.ibb.co/x2DGmPk/gigachad.jpg", top=True),
        dbc.CardBody(
            [
                html.H2("Mr. Ariz Flores", className="card-title text-center"),  # Add text-center class
                html.P('Owner', className="card-text text-center"),  # Add text-center class
            ]
        ),
    ],
    style={"width": "20rem", "margin-left": "15.00em", "margin-right": "2.75em"},
    color="light",
    outline=True,
)

layout = html.Div(
    [
        html.H1([html.Span("\U0001F3CB", style={'margin-right': '0.5em'}), "GULOD'S GYM"], 
                style={'background-color': '#ffc404', 'text-align': 'center'}),
        dbc.Row(carousel),
        dbc.Row(),
        dbc.Row([
            dbc.Col(card_about, width=6),
            dbc.Col(card_contact, width=3),
            # dbc.Col(card_image, className="offset-md-0.5")
        ]), 
    ]
)



if __name__ == "__main__":
    app.run_server(debug=True)