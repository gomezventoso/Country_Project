import numpy as np
import plotly.express as plt
import plotly.graph_objects as go
import pandas as pd

# Function to convert a grade (0-1) to a color between blue and red.
def grade_to_color(grade):
    # Blue is (0, 0, 255) for grade 0 and red is (255, 0, 0) for grade 1.
    r = int(grade * 255)
    g = 0
    b = int((1 - grade) * 255)
    return f'rgb({r}, {g}, {b})'

#Promp user input via the command line
country_name = input("Please enter the name of a country: ")

if country_name:
    print(f"Country entered: {country_name}")
else:
    print("No country was entered")

#Upload data frame of dimensions
df_country = pd.read_excel("culture_map.xlsx", sheet_name = "countries")
df_dimensions = pd.read_excel("culture_map.xlsx", sheet_name = "dimensions")
a = np.where(df_country.Country==country_name)
b=a[0].item(0)

A_1= df_country.iloc[b,1:7].to_numpy()
A_x = df_country.iloc[:,1:7].to_numpy()
A_2 = df_country.iloc[1,1:7].to_numpy()

d_A1_A2 = np.sqrt(sum((A_1-A_2) ** 2))
d_A1_A2_2 = np.linalg.norm(A_1 - A_2)

cos_A1_A2 = np.dot(A_1,A_2)/(np.linalg.norm(A_1)*np.linalg.norm(A_2))

print(d_A1_A2)
print(d_A1_A2_2)
print(cos_A1_A2)

eu_d = []

for v in A_x:
    d_A1_v = np.linalg.norm(A_1 - v)
    eu_d.append(d_A1_v)
print(np.array(eu_d))

df_country["Euclidian distance"]=eu_d

# Sort the DataFrame by lower to larger distance
df_country = df_country.sort_values(by="Euclidian distance", ascending=True).reset_index(drop=True)

# Add a new Rank column (starting from 1)
df_country['Rank'] = df_country.index + 1

# Reorder columns so that Rank appears first
df_country = df_country[['Rank', 'Country', 'Euclidian distance']]

# Compute colors for each normalized Euclidean distance value
min_d = df_country["Euclidian distance"].min()
max_d = df_country["Euclidian distance"].max()
df_country["normalized_distance"] = (df_country["Euclidian distance"] - min_d) / (max_d - min_d)

grade_colors = [grade_to_color(g) for g in df_country["normalized_distance"]]

# Set a default fill color for the Rank and Country columns
default_color = 'lavender'
rank_colors = [default_color] * len(df_country)
country_colors = [default_color] * len(df_country)

# Create a Plotly table with the Rank, Country, and Grade (with a hot-to-cold gradient)
fig = go.Figure(data=[go.Table(
    header=dict(
        values=["<b>Rank</b>", "<b>Country</b>", "<b>Euclidian distance</b>"],
        fill_color='paleturquoise',
        align='left',
        font=dict(color='black')
    ),
    cells=dict(
        values=[df_country["Rank"], df_country["Country"], df_country["Euclidian distance"]],
        fill_color=[rank_colors, country_colors, grade_colors],
        align='left',
        # For Rank and Country, we use black; for Euclidian distance, we use white
        font=dict(color=[
            ["black"] * len(df_country), 
            ["black"] * len(df_country), 
            ["white"] * len(df_country)
        ])
    )
)])
fig.update_layout(title="Country Grades Sorted with Hot-to-Cold Gradient (Red = Hot, Blue = Cold)")
fig.show()