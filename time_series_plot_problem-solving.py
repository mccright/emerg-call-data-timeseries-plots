import pandas as pd
import matplotlib.pyplot as plt

# Read CSV data into a DataFrame
df = pd.read_csv('data/test_emerg_data2.csv')

# Convert 'incident_date' to datetime format
df['incident_date'] = pd.to_datetime(df['incident_date'], format='%m/%d/%y')
"""
# Either Filter response units ending with '11' or '12'
filtered_df = df[df['response_unit'].str.endswith(('11', '12'))]
"""
# Or Filter response units starting with 'WAVE' or 'SE'
filtered_df = df[df['response_unit'].str.startswith(('WAVE', 'SE'))]

# Plot time series for each 'response_unit'
response_units = filtered_df['response_unit'].unique()

for unit in response_units:
    unit_data = filtered_df[filtered_df['response_unit'] == unit]
    # print(f"unit_data: {unit_data}")

    # Create a time series plot
    plt.figure(figsize=(10, 6))
    plt.plot(unit_data['incident_date'], pd.to_timedelta(unit_data['time_in_service']).dt.total_seconds() / (60 * 60),
             label=unit)

    # Customize the plot
    plt.title(f'Time Series Plot for {unit}')
    plt.xlabel('Incident Date')
    plt.ylabel('Time in Service (hours)')
    plt.legend()
    plt.grid(True)

    # Show the plot or save it to a file
    # plt.show()
    # Alternatively, save the plot to a file if needed:
    plt.savefig(f'plots/{unit}_time_series_plot.png')
