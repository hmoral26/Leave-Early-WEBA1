# about
# source notes, so the other pages stay short


import streamlit as st


st.set_page_config(page_title="About", page_icon="☔", layout="centered")


# STYLE
# same navy / white / gold as the other pages
NAVY = "#003087"
GOLD = "#FFBF3F"
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: #FFFFFF;
        }}
        h1, h2, h3 {{
            color: {NAVY} !important;
        }}
        [data-testid="stSidebar"] {{
            background-color: {NAVY};
        }}
        [data-testid="stSidebar"] * {{
            color: #FFFFFF !important;
        }}
        hr {{
            border: none;
            border-top: 3px solid {GOLD};
        }}
        .stCaption, [data-testid="stCaption"] {{
            color: {NAVY} !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("About")


# PAGES
# four pages now. I split them so the forecast page is not one long scroll
st.subheader("Why these pages")
st.write(
    "The app page states the problem and stores the two settings. "
    "This Week is the forecast and the charts. "
    "Morning hours is the filtered table of the 6–10 a.m. rows. "
    "About is the source note, so the other pages stay short."
)


# STATE
# these two keys are why the city and rain limit show up on the other pages
st.subheader("What carries across pages")
st.write(
    "Starting location and the rain limit are stored in session state. "
    "I set them on the app page. This Week and Morning hours open with the same values."
)


# API
# one GET, no login. same pattern as the Week 5 example
st.subheader("The data")
st.write(
    "The forecast comes from Open-Meteo: one GET request, no login. "
    "The response is converted from JSON into tables. "
    "This Week uses a daily table and an hourly table. Morning hours uses the hourly table."
)
st.write("Documentation: https://open-meteo.com/")


# LIMIT
# what I am not trying to answer
st.subheader("What this app does not do")
st.write(
    "This is a rain forecast for the drive. "
    "It is not a campus map."
)


with st.expander("Credits"):
    st.write("Weather data: Open-Meteo (CC BY 4.0)")
    st.write("Campus coordinates: New College of Florida, Sarasota")
    st.caption("CEN 3352 · Front-End Development and Design")

    