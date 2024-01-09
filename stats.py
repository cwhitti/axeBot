import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import pandas as pd
import numpy as np

def get_pie_chart(column_name):

    # grab csv file
    csv_file = "stats.csv"
    data = pd.read_csv(csv_file)

    # Extract the data for the pie chart
    # Replace 'column_name' with the actual column name containing your data
    labels = data[column_name].unique()  # Extract unique values from the specified column
    values = data[column_name].value_counts()  # Count occurrences of each unique value

    # Create a pie chart
    plt.figure(figsize=(6, 6))  # Adjust the figure size as needed
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.rcParams['font.family'] = 'Arial'
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title('AxeBot Users (2023-09-12 ~ Now)')  # Replace with an appropriate title

    # Save the pie chart as a PNG
    output_png = 'pie_chart.png'
    plt.savefig(output_png, bbox_inches='tight')

    return output_png

def get_usage_histogram():

    # Step 2: Read the CSV data
    csv_file = 'stats.csv'  # Replace 'your_data.csv' with the actual CSV file path
    data = pd.read_csv(csv_file)

    # Generate a list of all days in your date range
    # This assumes you have a start_date and end_date defined or replace them accordingly
    start_date = '2023-09-12'
    end_date = pd.Timestamp.now().date()
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')

    # Create a new DataFrame with zeros for all dates in the date_range
    df_reindexed = pd.DataFrame(0, index=date_range, columns=['day'])

    # Update the values for the dates that exist in the original data
    values = data['day'].value_counts()
    df_reindexed.loc[values.index, 'day'] = values.values

    # Create a figure and axis object
    fig, ax = plt.subplots(figsize=(7, 8))

    # Plot the data as a bar chart
    plt.bar(df_reindexed.index, df_reindexed['day'], width=0.5, edgecolor='k')
    plt.rcParams['font.family'] = 'Arial'
    plt.xlabel('Date')
    plt.ylabel('Times Used')
    plt.title('AxeBot Usage History')

    # Set axis settings for major and minor ticks
    plt.xticks(rotation=90)
    ax.xaxis.set_major_locator(MultipleLocator(2))  # Major ticks every 2 days
    ax.xaxis.set_minor_locator(MultipleLocator(1))  # Minor ticks every 1 day
    ax.yaxis.set_minor_locator(MultipleLocator(1))

    # Customize the x-axis labels to show only month and day
    # Change the font size of x-tick labels
    ax.tick_params(axis='x', labelsize=8.5)  # You can adjust the font size as needed


    # Save the pie chart as a PNG
    output_png = 'histogram_chart.png'
    plt.savefig(output_png, bbox_inches='tight')

    return output_png
