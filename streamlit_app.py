import altair as alt
import pandas as pd
import streamlit as st

# Set page config
st.set_page_config(page_title="Movies Dataset", page_icon="🎬", layout="wide")
st.title("🎬 Filmography Dataset")
st.write(
    """
    Welcome to our interactive visualization app featuring data from 
    [The Movie Database (TMDB)](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata). 
    Dive into the world of cinema and discover which movie genres have dominated the box office over the years. 
    Use the widgets below to start your exploration!
    """
)

# Load the data from a CSV
@st.cache_data
def load_data():
    df = pd.read_csv("data/movies_genres_summary.csv")
    return df

df = load_data()

# Multiselect widget for genres
genres = st.multiselect(
    "🎬 Select Genres",
    df.genre.unique(),
    ["Action", "Adventure", "Biography", "Comedy", "Drama", "Horror"],
)

# Slider widget for years
years = st.slider("📅 Select Years", 1986, 2006, (2000, 2016))

# Filter the dataframe based on the widget input
df_filtered = df[(df["genre"].isin(genres)) & (df["year"].between(years[0], years[1]))]
df_reshaped = df_filtered.pivot_table(
    index="year", columns="genre", values="gross", aggfunc="sum", fill_value=0
)
df_reshaped = df_reshaped.sort_values(by="year", ascending=False)

# Display the data as a table
st.dataframe(
    df_reshaped,
    use_container_width=True,
    column_config={"year": st.column_config.TextColumn("Year")},
)

# Display summary statistics
st.subheader("📊 Summary Statistics")
st.write(df_filtered.describe())

# Display the data as an Altair chart
df_chart = pd.melt(
    df_reshaped.reset_index(), id_vars="year", var_name="genre", value_name="gross"
)
line_chart = (
    alt.Chart(df_chart)
    .mark_line()
    .encode(
        x=alt.X("year:N", title="Year"),
        y=alt.Y("gross:Q", title="Gross earnings ($)"),
        color="genre:N",
        tooltip=["year", "genre", "gross"]
    )
    .properties(height=320, title="Gross Earnings by Genre Over Years")
)
st.altair_chart(line_chart, use_container_width=True)

# Additional Visualization: Bar Chart
st.subheader("📊 Bar Chart: Total Gross Earnings by Genre")
bar_chart = (
    alt.Chart(df_chart)
    .mark_bar()
    .encode(
        x=alt.X("sum(gross):Q", title="Total Gross earnings ($)"),
        y=alt.Y("genre:N", title="Genre"),
        color="genre:N",
        tooltip=["genre", "sum(gross)"]
    )
    .properties(height=320)
)
st.altair_chart(bar_chart, use_container_width=True)

# Additional Visualization: Bubble Chart
st.subheader("📊 Bubble Chart: Gross Earnings by Year and Genre")
bubble_chart = (
    alt.Chart(df_chart)
    .mark_circle(size=60)
    .encode(
        x=alt.X("year:N", title="Year"),
        y=alt.Y("gross:Q", title="Gross earnings ($)"),
        color="genre:N",
        size="gross:Q",
        tooltip=["year", "genre", "gross"]
    )
    .properties(height=320)
)
st.altair_chart(bubble_chart, use_container_width=True)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        color: black; /* Change text color to black */
        font-family: 'Roboto', sans-serif;
        text-align: center; /* Center align text */
    }
    .block-container {
        padding: 2rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 1.2rem; /* Increase button font size */
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        border: none;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>div>input {
        font-size: 1rem;
        padding: 0.5rem;
        border-radius: 0.25rem;
        border: 1px solid #ccc;
    }
    .stSelectbox>div>div>select {
        font-size: 1rem;
        padding: 0.5rem;
        border-radius: 0.25rem;
        border: 1px solid #ccc;
    }
    .stSlider>div>div>div>div>div>div {
        font-size: 1rem;
    }
    .stNumberInput>div>div>input {
        font-size: 1rem;
        padding: 0.5rem;
        border-radius: 0.25rem;
        border: 1px solid #ccc;
    }
    .stAlert {
        font-size: 1.2rem;
        padding: 1rem;
        border-radius: 0.25rem;
    }
    h1, h2, h3, h4, h5, h6, p, label, div, span {
        color: black !important; /* Change text color to black */
        font-size: 1.5rem !important; /* Increase font size for all text */
        text-align: center; /* Center align text */
    }
    </style>
    """, unsafe_allow_html=True)