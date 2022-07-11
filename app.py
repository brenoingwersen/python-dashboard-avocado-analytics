import dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

df = pd.read_csv('avocado.csv')
# df = df.loc[(df['type'] == 'conventional') & (df['region'] == 'Albany')]
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
df.sort_values(by='Date', inplace=True)

external_stylesheets = [
    {
        'href': 'https://fonts.googleapis.com/css2?'
                'family=Lato:wght@400;700&display=swap',
        'rel': 'stylesheet',
    }
]

# Initialize the application
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Avocado Analytics: Understand Your Avocados!'

# define the layout property of your application. This property dictates the look of your app. In this case, you’ll use a heading with a description below it and two graphs.

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(
                    children='🥑',
                    className='header-emoji'
                ),
                html.H1(
                    children='Avocado Analytics',
                    className='header-title'
                ),
                html.P(
                    children="Analyze the behaviour of avocado prices and the number of avocados sold in the US between 2015 and 2018",
                    className='header-description'
                )
            ],
            className='header'
        ),
        # Dropdown menu div wrapper
        html.Div(
            children=[
                # Add dropdown menu for region
                html.Div(
                    children=[
                        html.Div(
                            children='Region',
                            className='menu-title'
                        ),
                        dcc.Dropdown(
                            id='region-filter',
                            options=[
                                region for region in df.region.sort_values().unique()],
                            value='Albany',
                            clearable=False,
                            className='dropdown'
                        )
                    ]
                ),
                # Add dropdown menu for avocado_type
                html.Div(
                    children=[
                        html.Div(
                            children='Type',
                            className='menu-title'
                        ),
                        dcc.Dropdown(
                            id='type-filter',
                            options=[
                                type for type in df.type.sort_values().unique()],
                            value='organic',
                            clearable=False,
                            className='dropdown'
                        )
                    ]
                ),
                # Add dropdown menu for date range
                html.Div(
                    children=[
                        html.Div(
                            children='Date Range',
                            className='menu-title'
                        ),
                        dcc.DatePickerRange(
                            id='date-range',
                            min_date_allowed=df.Date.min().date(),
                            max_date_allowed=df.Date.max().date(),
                            start_date=df.Date.min().date(),
                            end_date=df.Date.max().date()
                        )
                    ]
                )
            ],
            className='menu'
        ),
        html.Div(
            children=[
                # Add price chart
                html.Div(
                    children=dcc.Graph(
                        id='price-chart',
                        # Remove the default floating bar
                        config={'displayModeBar': False},
                        figure={
                            'data': [
                                {
                                    'x': df['Date'],
                                    'y': df['AveragePrice'],
                                    'type': 'lines',
                                    # Specify number format when hovering
                                    'hovertemplate': '$%{y:.2f}<extra></extra>'
                                }
                            ],
                            'layout': {
                                'title': {
                                    'text': 'Average Price of Avocados',
                                    'x': 0.05,
                                    'xanchor': 'left'
                                },
                                'xaxis': {
                                    'fixedrange': True
                                },
                                'yaxis': {
                                    'tickprefix': '$',
                                    'fixedrange': True
                                },
                                'colorway': ['#17B897']
                            }
                        }
                    ),
                    className='card'
                ),
                # Add volume chart
                html.Div(
                    children=dcc.Graph(
                        id='volume-chart',
                        config={'displayModeBar': False},
                        figure={
                            'data': [
                                {
                                    'x': df['Date'],
                                    'y': df['Total Volume'],
                                    'type': 'lines'
                                }
                            ],
                            'layout': {
                                'title': {
                                    'text': 'Avocados Sold',
                                    'x': 0.05,
                                    'xanchor': 'left'
                                },
                                'xaxis': {'fixedrange': True},
                                'yaxis': {'fixedrange': True},
                                'colorway': ['#E12D39']
                            }
                        },
                    ),
                    className='card'
                )
            ],
            className='wrapper'
        )
    ],

)


@app.callback(
    [
        Output('price-chart', 'figure'),
        Output('volume-chart', 'figure')
    ],
    [
        Input('region-filter', 'value'),
        Input('type-filter', 'value'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date')
    ]
)
def update_charts(region, avocado_type, start_date, end_date):
    mask = (
        (df.region == region) &
        (df.type == avocado_type) &
        (df.Date >= start_date) &
        (df.Date <= end_date)
    )
    filterd_data = df.loc[mask, :]

    # Update price chart figure parameter with filtered_data
    price_chart_figure = {
        'data': [
            {
                'x': filterd_data['Date'],
                'y': filterd_data['AveragePrice'],
                'type': 'lines',
                # Specify number format when hovering
                'hovertemplate': '$%{y:.2f}<extra></extra>'
            }
        ],
        'layout': {
            'title': {
                'text': 'Average Price of Avocados',
                'x': 0.05,
                'xanchor': 'left'
            },
            'xaxis': {
                'fixedrange': True
            },
            'yaxis': {
                'tickprefix': '$',
                'fixedrange': True
            },
            'colorway': ['#17B897']
        }
    }

    # Update volume chart figure parameter with filtered_data
    volume_chart_figure = {
        'data': [
            {
                'x': filterd_data['Date'],
                'y': filterd_data['Total Volume'],
                'type': 'lines'
            }
        ],
        'layout': {
            'title': {
                'text': 'Avocados Sold',
                'x': 0.05,
                'xanchor': 'left'
            },
            'xaxis': {'fixedrange': True},
            'yaxis': {'fixedrange': True},
            'colorway': ['#E12D39']
        }
    }

    return price_chart_figure, volume_chart_figure


if __name__ == '__main__':
    app.run_server(debug=True)
