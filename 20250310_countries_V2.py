import numpy as np
import plotly.express as plt
import plotly.graph_objects as go
import pandas as pd

#Upload data frame of dimensions
df_country = pd.read_excel("culture_map.xlsx", sheet_name = "countries")
df_dimensions = pd.read_excel("culture_map.xlsx", sheet_name = "dimensions")

print(df_country.iloc[[0]].to_numpy())