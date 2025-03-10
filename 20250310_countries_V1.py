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

#Upload data frame of dimensions
df_country = pd.read_excel("culture_map.xlsx", sheet_name = "countries")
df_dimensions = pd.read_excel("culture_map.xlsx", sheet_name = "dimensions")
a = np.where(df_country.Country=='Spain')
b=a[0].item(0)
#print(df_country)

v0 = df_country.iloc[0,1:7].to_numpy()
v1 = df_country.iloc[1,1:7].to_numpy()
v86 = df_country.iloc[86,1:7].to_numpy()
vx = df_country.iloc[:,1:7].to_numpy()
vy = df_country.iloc[b,1:7].to_numpy()

cos_th_1 = (np.dot(v0,v1)/(np.linalg.norm(v0*np.linalg.norm(v1))))
#print(math.acos(cos_th_1))
#print(vx)
cos_th_x = []
for i in vx:
    print()
    cos_th_x_i = (np.dot(vy,i)/(np.linalg.norm(vy*np.linalg.norm(i))))
    cos_th_x.append(cos_th_x_i )
cos_th_x=np.array(cos_th_x)
df_country['cos_thetha'] = cos_th_x
print(df_country)
df_country_friendly = df_country[np.where(df_country.cos_thetha==1,True,False)]
df_country_friendly_num = df_country[np.where(df_country.cos_thetha==1,True,False)].shape[0]
print(df_country.cos_thetha)
print(df_country_friendly_num)



# Sort the DataFrame by Grade in descending order (1 to 0)
df_country = df_country.sort_values(by="cos_thetha", ascending=False).reset_index(drop=True)

# Add a new Rank column (starting from 1)
df_country['Rank'] = df_country.index + 1

# Reorder columns so that Rank appears first
df_country = df_country[['Rank', 'Country', 'cos_thetha']]

# Compute colors for each Grade value
grade_colors = [grade_to_color(g) for g in df_country['cos_thetha']]

# Set a default fill color for the Rank and Country columns
default_color = 'lavender'
rank_colors = [default_color] * len(df_country)
country_colors = [default_color] * len(df_country)

# Create a Plotly table with the Rank, Country, and Grade (with a hot-to-cold gradient)
fig = go.Figure(data=[go.Table(
    header=dict(
        values=["<b>Rank</b>", "<b>Country</b>", "<b>cos_thetha</b>"],
        fill_color='paleturquoise',
        align='left'
    ),
    cells=dict(
        values=[df_country["Rank"], df_country["Country"], df_country["cos_thetha"]],
        fill_color=[rank_colors, country_colors, grade_colors],
        align='left'
    )
)])

fig.update_layout(title="Country Grades Sorted with Hot-to-Cold Gradient (Red = Hot, Blue = Cold)")
fig.show()