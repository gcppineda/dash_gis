import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

sidebar_title = "OPTIONS"

sidebar_header = dbc.Row(
    [
        html.H1(sidebar_title),
        dbc.Col(
            [
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(0,0,0,.5)",
                        "border-color": "rgba(0,0,0,0)",
                        # "margin-top":"5px",
                    },
                    id="navbar-toggle",
                ),
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(0,0,0,.5)",
                        # "margin-top":"5px",
                        "border-color": "rgba(0,0,0,0)",
                    },
                    id="sidebar-toggle",
                ),
            ],
            width="auto",
            align="center",
        ),
        
    ],
    justify = "end"
)

sidebar_content = [
    html.Hr(),
    html.P(
            "A responsive sidebar layout with collapsible navigation "
        "links.",
        className="lead",
    ),
]

sidebar = html.Div(
    [
        sidebar_header,
        # we wrap the horizontal rule and short blurb in a div that can be
        # hidden on a small screen
        html.Div(
                sidebar_content,
            id="blurb",
        ),
        # use the Collapse component to animate hiding / revealing links
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink("Page 1", href="/page-1", id="page-1-link"),
                    dbc.NavLink("Page 2", href="/page-2", id="page-2-link"),
                    dbc.NavLink("Page 3", href="/page-3", id="page-3-link"),
                ],
                vertical=True,
                pills=True,
            ),
            id="collapse",
        ),
    ],
    id="sidebar",
)

# GERARD!! -------------------------------------------------------------------------------------
# streamlit like usage pero a very low-quality bootleg version
sidebar_content.append(html.H6("Choose a keme"))
sidebar_content.append(
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montreal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='NYC'
    ),
)
sidebar_content.append(html.Br()) # line break haha
sidebar_content.append(html.H6("Choose another keme"))
sidebar_content.append(
    dcc.Dropdown(
        id='demo-dropdown-2',
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montreal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='NYC'
    ),
)