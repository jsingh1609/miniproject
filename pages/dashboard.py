import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Spotify Dashboard")

st.image("image/AppleCompetition-FTRHeader_V2-1440x733.png", caption="", use_container_width=True)

df = pd.read_csv('spotify-2023.csv', encoding='ISO-8859-1')


st.dataframe(df)



df['streams'] = pd.to_numeric(df['streams'].astype(str).str.replace(',', ''), errors='coerce')

# Optional: Drop any rows where 'streams' couldn't be converted
df = df.dropna(subset=['streams'])

# Convert to integer if you prefer
df['streams'] = df['streams'].astype('int64')

top_10_tracks = df.sort_values(by='streams', ascending=False).head(10)

fig = px.bar(
    top_10_tracks,
    x='track_name',
    y='streams',
    color='artist(s)_name',
    title='Top 10 Most Streamed Songs by Track Name',
    labels={'artist(s)_name': 'Artist', 'streams': 'Number of Streams'},
    height=500,
    width=900
)

fig.update_layout(
    xaxis_tickangle=-45,
    margin=dict(t=50, b=150)
)
st.plotly_chart(fig)

top_10_artists = df.groupby('artist(s)_name')['streams'].sum().sort_values(ascending=False).head(10).reset_index()

fig = px.bar(
    top_10_artists,
    x='artist(s)_name',
    y='streams',
    title='Top 10 Most Streamed Artists',
    labels={'artist(s)_name': 'Artist', 'streams': 'Total Streams'},
    height=500,
    width=900,
    color='artist(s)_name'
)

fig.update_layout(
    showlegend=False,
    xaxis_tickangle=-45,
    margin=dict(t=50, b=150)
)
st.plotly_chart(fig)

top_30_artists = df.groupby('artist(s)_name')['streams'].sum().sort_values(ascending=False).head(30).reset_index()

fig = px.pie(
    top_30_artists,
    names='artist(s)_name',
    values='streams',
    title='Top 10 Most Streamed Artists',
    color_discrete_sequence=px.colors.sequential.RdBu
)

fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig)

top_artists = df.groupby('in_spotify_playlists')['streams'].sum().nlargest(10).reset_index()

fig = px.treemap(
    top_artists,
    path=['in_spotify_playlists'],
    values='streams',
    title='Top 10 in_spotify_playlists by Total Streams',
    color='streams',
    color_continuous_scale='Blues'
)
st.plotly_chart(fig)

streams_by_year = df.groupby('released_year')['streams'].sum().reset_index()

fig = px.line(
    streams_by_year,
    x='released_year',
    y='streams',
    title='Streams by Release Year',
    markers=True,
    labels={'released_year': 'Year', 'streams': 'Total Streams'}
)
st.plotly_chart(fig)

fig = px.scatter(
    df,
    x='energy_%',
    y='danceability_%',
    size='streams',
    color='artist(s)_name',
    title='Energy vs Danceability (Bubble Size = Streams)',
    labels={'energy_%': 'Energy', 'danceability_%': 'Danceability'}
)
st.plotly_chart(fig)

fig = px.histogram(
    df,
    x='bpm',
    nbins=30,
    title='Distribution of BPM in Tracks',
    labels={'bpm': 'Beats Per Minute (BPM)'}
)
st.plotly_chart(fig)

fig = px.box(
    df,
    x='mode',
    y='danceability_%',
    title='Danceability Distribution by Mode (0 = Minor, 1 = Major)',
    labels={'mode': 'Mode', 'danceability_%': 'Danceability'}
)
st.plotly_chart(fig)

top_years = df['released_year'].value_counts().nlargest(3).index
filtered = df[df['released_year'].isin(top_years)]

fig = px.sunburst(
    filtered,
    path=['released_year', 'artist(s)_name', 'track_name'],
    values='streams',
    title='Streams by Year → Artist → Track'
)
st.plotly_chart(fig)

fig = px.violin(
    df,
    x='released_year',
    y='streams',
    color='released_year',  # add this line for color
    title='Violin Plot of Streams by Release Year',
    labels={'released_year': 'Year', 'streams': 'Streams'},
    box=True,
    points='all'
)
st.plotly_chart(fig)

# streamlit run app.py