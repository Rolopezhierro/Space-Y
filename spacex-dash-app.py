# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

                                # Dropdown
                                dcc.Dropdown(id='site_dropdown',
                                            options=[{'label': 'All Sites', 'value': 'ALL'}] +
                                                    [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                                            value='ALL',
                                            placeholder='Select a launch site',
                                                    searchable=True),
                                            html.Br(),

                                # Pie chart
                                html.Div(dcc.Graph(id='success_pie_chart')),
                                html.Br(),
                                
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload_slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                        100: '100'},
                                                value=[min_payload, max_payload]),
                                html.Div(dcc.Graph(id='success_payload_scatter_chart')),
                                html.Br()
                                ]
                    )           


# CALLBACK
@app.callback(
    Output('success_pie_chart', 'figure'),
    Input('site_dropdown', 'value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df,
            values='class',
            names='Launch Site',
            title='Total Success Launches by Site'
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(
            filtered_df,
            values='class',
            names='class',
            title=f'Success vs Failed Launches for site {entered_site}'
        )

    return fig

@app.callback(
    Output('success_payload_scatter_chart', 'figure'),
    Input('site_dropdown', 'value'),
    Input('payload_slider', 'value'))

def get_success_payload_scatter_chart(entered_site, payload_slider):
    low, high = payload_slider

    # Filtrar por payload del slider
    df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if entered_site != 'ALL':
        df = df[df['Launch Site'] == entered_site]

    # Crear scatter plot correcto
    fig = px.scatter(
        df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=f"Payload vs Success for site {entered_site}" if entered_site != 'ALL'
              else "Payload vs Success for all sites"
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
