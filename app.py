import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="My webpage", page_icon=":tada", layout="wide")

# ----- Header Section ----
st.subheader("Hi dude!")
st.title("This is the Title")
st.write("I'm AWESOME!")
st.write("I'm AWESOME again!")

df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(df)

df2 = px.data.gapminder()

fig = px.scatter(
    df2.query("year==2007"),
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=60,
)

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
with tab1:
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
with tab2:
    # Use the native Plotly theme.
    st.plotly_chart(fig, theme=None, use_container_width=True)