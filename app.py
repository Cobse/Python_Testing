import streamlit as st
import pandas as pd
import numpy as np

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