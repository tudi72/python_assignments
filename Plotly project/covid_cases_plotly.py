# import libraries
import numpy as np
import csv
import plotly
import plotly.graph_objects as go
from scipy.optimize import curve_fit
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import pandas as pd

# The url with data about each country with a report about covid cases per day
url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series" \
      "/time_series_covid19_confirmed_global.csv "

# Import CSV data and read one row
data = pd.read_csv(url)
data_time_series = data.iloc[244, 4:-1]

# Extract the last 14 dates and Covid cases
data_time_series = data_time_series.iloc[-14:]

# Extract an array of the last 14 days
date_time_axis = np.array(data_time_series.index)

# Extract an array of the last 14 covid cases
values_axis = np.array(data_time_series.values, dtype=float)

# Plot for an axis xOy where x represents the date and y represents the values of covid cases
figure = make_subplots(rows=1, cols=1)
figure.add_trace(go.Scatter(x=date_time_axis, y=values_axis, name="Line infections", showlegend=True), row=1, col=1)

# Predefined constants
a0 = 2.5
a1 = 0.5


# Define function for approximating data to fit and predict
def function(x, b):
    return a0 * np.exp(-b * x) + a1


# Evaluate and Plot Function
function_values_axis = function(values_axis, 0.5)

# Add the dates to be predicted by the model
figure.add_trace(go.Scatter(x=date_time_axis, y=function_values_axis, name="Figure infections", showlegend=True), row=1,col=1)

# Export data html
plotly.offline.plot(figure, filename="data_fitting_example.html")

# TODO prediction for the next 14 days
