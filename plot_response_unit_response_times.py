import csv
import dash
from dash import dcc, html
from datetime import datetime
from collections import defaultdict
import argparse

import plotly.graph_objects as go

import plotly.io as pio
pio.renderers.default = "browser"

# Create a Dash application
app = dash.Dash(__name__)


def load_response_times(csv_path):
    records = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['response_time_in_seconds'] = int(row['response_time_in_seconds'])
            records.append(row)
    return records


def plot_scores_interactive_dropdown(records, output_port: int, output_path="scores.svg"):
    # Sort the records so they are alphabetized by response_unit name.
    # This makes it easier to navigate the drop-down list box.
    records = sorted(records, key=lambda x: x['response_unit'])

    # Convert date strings to datetime objects
    for r in records:
        r['incident_date'] = datetime.strptime(r['incident_date'], "%Y-%m-%d")

    # Group by response_unit
    teams = defaultdict(list)
    for r in records:
        teams[r['response_unit']].append(r)

    # Sort each team’s records by date
    for team in teams:
        teams[team] = sorted(teams[team], key=lambda x: x['incident_date'])

    fig = go.Figure()

    # Add one trace per team
    for team, recs in teams.items():
        dates = [r['incident_date'] for r in recs]
        response_time_in_seconds = [r['response_time_in_seconds'] for r in recs]

        fig.add_trace(go.Scatter(
            x=dates,
            y=response_time_in_seconds,
            mode="lines+markers",
            name=team,
            visible=False  # hide initially
        ))

    # Make the first team visible by default
    if fig.data:
        fig.data[0].visible = True

    # Build dropdown menu
    dropdown_buttons = []
    for i, team in enumerate(teams.keys()):
        visibility = [False] * len(teams)
        visibility[i] = True  # show only this team

        dropdown_buttons.append(
            dict(
                label=team,
                method="update",
                args=[{"visible": visibility},
                      {"title": f"Team response_time_in_seconds Over Time — {team}"}]
            )
        )

    fig.update_layout(
        title="Team response_time_in_seconds Over Time",
        xaxis_title="incident_date",
        # yaxis_title="response_time_in_seconds",
        yaxis=dict(
            title='response_time_in_seconds (log scale)',
            type='log',  # Set y-axis to logarithmic
            autorange=True
        ),
        hovermode="x unified",
        updatemenus=[
            dict(
                active=0,
                buttons=dropdown_buttons,
                x=1.15,
                y=1.15
            )
        ]
    )

    # Save as SVG (requires `pip install -U kaleido`)
    #### fig.write_image(output_path)

    # Define the layout of the Dash app
    app.layout = html.Div(children=[
        dcc.Graph(figure=fig)
    ])

    # Run the server on a specific port (e.g., 8050)
    app.run(host='127.0.0.1',port=output_port,threaded=True)



if __name__ == '__main__':
    # Parse command-line arguments  
    parser = argparse.ArgumentParser(description='Run a Dash app with a custom port.')  
    parser.add_argument('--port', type=int, default=8050, help='Port number (default: 8050)')  
    args = parser.parse_args() 
    # Required data columns: 
    # incident_date
    # response_unit
    # response_time_in_seconds
    # time_in_service_in_seconds
    csv_path = './2025-08-02_emerg_data_organized_step_four.csv'
    records = load_response_times(csv_path)
    #
    plot_scores_interactive_dropdown(records, args.port)


