# Usual Dash dependencies
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate

# Let us import the app object in case we need to define
# callbacks here
from app import app

Gulods_Logo = "https://scontent.fmnl17-2.fna.fbcdn.net/v/t39.30808-6/279677672_5065406360192429_6832309912774742020_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=efb6e6&_nc_eui2=AeFkiw8FNl5lBlgWqJdizwVbLRSGFCvJOG4tFIYUK8k4bmVVzD0QWPirQnPT9iowFUCGnn1k0ywXagy4kE32MEUO&_nc_ohc=VZGd94TSqXMAX_z7Gqk&_nc_ht=scontent.fmnl17-2.fna&oh=00_AfCvOUX-AoWar9GhZBxS2z1EHNwP-9RfN6rvoZYGISgp6Q&oe=65A5E336"

# CSS Styling for the NavLink components
navlink_style = {
    'color': '#fff'
}
navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=Gulods_Logo, height="75px")),
                    dbc.Col(dbc.NavbarBrand("Gulod's Gym", className="ms-2")),
                ],
                align="center",
            ),
            href="/home",
            style={"textDecoration": "none", 'margin-left': '1.5em'}
        ),
        dbc.NavLink("Home", href="/home", style=navlink_style),
        dbc.NavLink("Members", href="/members/members_home", style=navlink_style),
        dbc.NavLink("Attendance", href="/attendance/attendance_home", style=navlink_style),
        dbc.NavLink("Classes", href="/classes/classes_home", style=navlink_style),
        dbc.NavLink("Instructors", href="/instructors/instructors_home", style=navlink_style),
        dbc.NavLink("Reports", href="/reports/report", style=navlink_style),
        dbc.NavLink("About Us", href="/about_us", style=navlink_style),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(id="navbar-collapse", navbar=True),
        dbc.NavItem(dbc.Button("Logout", color="warning", href="/logout", id="logout_button", style={'margin-left': '0.5em', 'margin-right': '30px'})),
    ],
    dark=True,
    color='dark',
    className="navbar-expand-lg",
    style={"margin-right": "auto"},  # This will move the items to the right
)
