import pandas as pd
import streamlit as st
import plotly.express as px  # Import plotly.express
import plotly.graph_objects as go

#BARCHARTTT
# Corrected set_page_config function
st.set_page_config(page_title="Education Data Visualization", layout="wide")
st.title('Education in Lebanon - Data Visualization')

# Load the dataset
df = pd.read_csv('C:/Users/User/Desktop/Assigment2-Amira/ASSIGMENT 2 - PLOTLYPYTHON/EDUCATIONDATASET-CLEAN.csv')

# Checkbox to show/hide raw data
if st.checkbox('Show raw data'):
    st.subheader('Raw Data')
    st.dataframe(df, height=1200)  # Display the dataframe when the checkbox is checked

st.title("Bar Chart: Comparison of Education Levels in Governorates")

# Group the data by 'refArea' and calculate the mean of the education level percentages
governorate_data = df[df['refArea'].str.contains('Governorate')].groupby('refArea').agg({
  'PercentageofEducationlevelofresidents-vocational': 'mean',
  'PercentageofEducationlevelofresidents-elementary': 'mean',
  'PercentageofEducationlevelofresidents-secondary': 'mean',
  'PercentageofEducationlevelofresidents-intermediate': 'mean',
  'PercentageofEducationlevelofresidents-highereducation': 'mean'
}).reset_index()

# Add a filter to select specific governorates
selected_governorates = st.multiselect(
    "Select Governorates",
    options=governorate_data["refArea"].unique(),
    default=governorate_data["refArea"].unique()
)

# Filter the data based on selected governorates
filtered_data = governorate_data[governorate_data["refArea"].isin(selected_governorates)]
# Add filters for education levels
education_levels = {
    'Elementary': 'PercentageofEducationlevelofresidents-elementary',
    'Secondary': 'PercentageofEducationlevelofresidents-secondary',
    'Intermediate': 'PercentageofEducationlevelofresidents-intermediate',
    'Higher Education': 'PercentageofEducationlevelofresidents-highereducation',
    'Vocational': 'PercentageofEducationlevelofresidents-vocational'
}
# Add a filter to select specific educational level
selected_education_levels = st.multiselect(
    "Select Education Levels",
    options=list(education_levels.keys()),
    default=list(education_levels.keys())
)

# Filter columns based on selected education levels
selected_columns = [education_levels[level] for level in selected_education_levels if education_levels.get(level)]
if selected_columns:
    filtered_data = filtered_data[['refArea'] + selected_columns]
else:
    filtered_data = filtered_data[['refArea']]

# Create a bar chart
fig = go.Figure()

# Add traces for selected education levels
for column in selected_columns:
    fig.add_trace(go.Bar(
        name=column.split('-')[-1],
        x=filtered_data['refArea'],
        y=filtered_data[column]
    ))

# Customize the layout
fig.update_layout(
    title="Comparison of Education Levels in Selected Governorates",
    xaxis_title="Governorate",
    yaxis_title="Percentage of Residents",
    barmode='group'
)

# Display the chart in Streamlit
st.plotly_chart(fig)
st.write("Each governorate has a set of bars representing the mean percentage of residents with different education levels.")




import pandas as pd
import plotly.express as px
import streamlit as st

# Load the data
file_path = r"C:/Users/User/Desktop/Assigment2-Amira/ASSIGMENT 2 - PLOTLYPYTHON/EDUCATIONDATASET-CLEANED.csv"
data = pd.read_csv(file_path)

# Filter rows where 'refArea' contains 'District'
districts_only = data[data['refArea'].str.contains('District', case=False, na=False)]

# Group by 'refArea' and calculate the mean of numeric columns
cleaned_districts = districts_only.dropna()
numeric_columns = cleaned_districts.select_dtypes(include='number')
grouped_means = cleaned_districts.groupby('refArea').mean(numeric_only=True).reset_index()

# Create a new column 'highest_in' that contains the highest value in each row
columns = grouped_means.columns[1:-1]
def get_highest_column(row):
    max_value = row[columns].max()
    max_column = row[columns][row[columns] == max_value].index[0]
    return max_column

grouped_means['highest_in'] = grouped_means.apply(get_highest_column, axis=1)

# Load the coordinates data
coordinates_file_path = r"C:/Users/User/Desktop/Assigment2-Amira/ASSIGMENT 2 - PLOTLYPYTHON/points (1) (1).csv"
coordinates_data = pd.read_csv(coordinates_file_path)

# Merge the coordinates with grouped means data
merged_data = pd.merge(coordinates_data, grouped_means, on="refArea")

# Streamlit app layout
st.title("Districts Map")
st.write("The map illustrates the education metrics for each district, highlighting the category where each district excels from the following variables:")
# Interactive Dropdown Menu to select education level
education_level = st.selectbox(
    "Select Education Level:",
    ['PercentageofEducationlevelofresidents-university',
     'PercentageofEducationlevelofresidents-secondary',
     'PercentageofEducationlevelofresidents-intermediate',
     'PercentageofEducationlevelofresidents-vocational',
     'PercentageofEducationlevelofresidents-elementary',
     'PercentageofEducationlevelofresidents-highereducation']
)

# Interactive Slider to filter based on percentage
percentage_range = st.slider(
    f"Filter {education_level} by percentage range:",
    min_value=float(merged_data[education_level].min()),
    max_value=float(merged_data[education_level].max()),
    value=(float(merged_data[education_level].min()), float(merged_data[education_level].max()))
)

# Filter the data based on selected percentage range
filtered_data = merged_data[
    (merged_data[education_level] >= percentage_range[0]) &
    (merged_data[education_level] <= percentage_range[1])
]

# Create the scatter mapbox plot (with points)
fig = px.scatter_mapbox(
    filtered_data,
    lat='lat',
    lon='lon',
    hover_name='refArea',
    hover_data={'highest_in': True, education_level: True},
    size=education_level,  # Use size of points based on the selected education level
    color=education_level,  # Color points based on the selected education level
    color_continuous_scale="Viridis",
    mapbox_style="carto-positron",
    zoom=6,
    center={"lat": filtered_data['lat'].mean(), "lon": filtered_data['lon'].mean()},
)


# Update layout to improve interaction
fig.update_layout(
    title_text=f"{education_level} Distribution by District",
    hovermode="closest"
)

# Display the map using Streamlit
st.plotly_chart(fig)


#CORRELATIONNN
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# Load your dataset (make sure to adjust the path if needed)
file_path = r"C:/Users/User/Desktop/Assigment2-Amira/ASSIGMENT 2 - PLOTLYPYTHON/EDUCATIONDATASET-CLEANED.csv"
df = pd.read_csv(file_path)


# Streamlit app layout
st.title("Bubble Plot: Correlation between Illiteracy and School Dropout Rates")


# Add sliders for bubble size and opacity
bubble_size = st.slider('Select Bubble Size', min_value=5, max_value=20, value=8)
bubble_opacity = st.slider('Select Bubble Opacity', min_value=0.1, max_value=1.0, value=0.5)


# Create the bubble chart
fig = go.Figure(data=[go.Scatter(
    x=df['PercentageofEducationlevelofresidents-illeterate'],
    y=df['PercentageofSchooldropout'],
    mode='markers',
    marker=dict(
        size=bubble_size,  # Dynamic bubble size based on slider
        opacity=bubble_opacity,  # Dynamic opacity based on slider
        color='red'
    ),
    text=df['refArea']  # Optional: Add text labels to the bubbles
)])


# Add annotations (example)
annotations = [
    dict(
        x=df['PercentageofEducationlevelofresidents-illeterate'].median(),
        y=df['PercentageofSchooldropout'].median(),
        text="Median Point",
        showarrow=True,
        arrowhead=2
    )
]


fig.update_layout(
    title="Bubble Chart: Correlation between Illiteracy and School Dropout Rates",
    xaxis_title="Percentage of Illiterate Residents",
    yaxis_title="Percentage of School Dropouts",
    showlegend=False,  # Optional: Hide legend if not needed
    annotations=annotations  # Add annotations to the layout
)

# Display the plot using Streamlit
st.plotly_chart(fig)
st.write("The bubble chart shows that the relationship between illiteracy and school dropout rates is not immediately apparent, suggesting that no clear correlation is evident from the data. This lack of clarity in the correlation could imply that other factors may be influencing dropout rates beyond just the illiteracy rate.")
st.write("To expand more on this insight:")





#NEW PIE CHARTS: 
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load your dataset (adjust the path if needed)
file_path = r"C:/Users/User/Desktop/Assigment2-Amira/ASSIGMENT 2 - PLOTLYPYTHON/EDUCATIONDATASET-CLEANED.csv"
df = pd.read_csv(file_path)

# Streamlit app layout
st.title("Pie Chart: Education Level Proportions Across Districts")

# Filter and group the data
district_data = df[df['refArea'].str.contains('District')].groupby('refArea').agg(
    {'PercentageofSchooldropout': 'mean',
     'PercentageofEducationlevelofresidents-illeterate': 'mean'}
).reset_index()

# Interactive Checkbox to filter certain districts
hide_districts = st.multiselect("Hide Districts", options=district_data['refArea'].unique(), default=[])

# Filter data based on districts to hide
filtered_data = district_data[~district_data['refArea'].isin(hide_districts)]

# Slider to filter based on School Dropout percentage
min_dropout, max_dropout = st.slider(
    "Filter Districts by School Dropout Percentage:",
    min_value=float(filtered_data['PercentageofSchooldropout'].min()),
    max_value=float(filtered_data['PercentageofSchooldropout'].max()),
    value=(float(filtered_data['PercentageofSchooldropout'].min()), float(filtered_data['PercentageofSchooldropout'].max()))
)

# Apply the filter
filtered_data = filtered_data[
    (filtered_data['PercentageofSchooldropout'] >= min_dropout) &
    (filtered_data['PercentageofSchooldropout'] <= max_dropout)
]

# Dropdown for selecting a district to highlight
selected_district = st.selectbox("Select a District to Highlight", options=filtered_data['refArea'].unique())

# Define custom explode values for each district (mimicking the "explode" effect in Matplotlib)
explode_values = [0.1 if x == selected_district else 0.0 for x in filtered_data['refArea']]

# Define custom colors
custom_colors = ['orange', 'cyan', 'brown', 'grey', 'indigo', 'beige']

# Filter the data to get the highlighted district's information
highlight_data = filtered_data[filtered_data['refArea'] == selected_district]

# Pie chart for school dropout rates
fig_dropout = go.Figure(data=[go.Pie(
    labels=filtered_data['refArea'],
    values=filtered_data['PercentageofSchooldropout'],
    title="School Dropout Rates Across Districts",
    pull=explode_values,  # This mimics the explode effect in Plotly
    marker=dict(
        colors=custom_colors,  # Custom colors
        line=dict(color='green', width=1)  # Wedge properties
    ),
    hoverinfo='label+percent+value',  # Display detailed hover info
    sort=True
)])

# Pie chart for illiteracy
fig_illeterate = go.Figure(data=[go.Pie(
    labels=filtered_data['refArea'],
    values=filtered_data['PercentageofEducationlevelofresidents-illeterate'],
    title="Proportion of Illiteracy Across Districts",
    pull=explode_values,  # Explode selected district
    marker=dict(
        colors=custom_colors,  # Custom colors
        line=dict(color='green', width=1)  # Wedge properties
    ),
    hoverinfo='label+percent+value',  # Display detailed hover info
    sort=False
)])

# Display the pie charts in Streamlit
st.subheader("School Dropout Rates")
st.plotly_chart(fig_dropout)

st.subheader("Illiteracy Proportion")
st.plotly_chart(fig_illeterate)

# Display additional information based on the selected district
st.write(f"You have selected: **{selected_district}**. The average dropout rate is **{highlight_data['PercentageofSchooldropout'].values[0]:.2f}%**, and the illiteracy rate is **{highlight_data['PercentageofEducationlevelofresidents-illeterate'].values[0]:.2f}%**.")