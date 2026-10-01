# about
# why I split the pages and where the numbers come from


import streamlit as st


st.set_page_config(page_title="About", page_icon="☔", layout="centered")


# STYLE
# ncf navy + white, gold only for small accents
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
st.subheader("Why three pages")
st.write(
    "Home states the problem and stores the two settings. "
    "This Week shows the live forecast. "
    "About holds the source notes so the forecast page stays short."
)


# STATE
st.subheader("What carries across pages")
st.write(
    "Starting location and the rain limit are stored in session state."
    "Values set on Home are the starting values on This Week."
)


# API
st.subheader("The data")
st.write(
    "The forecast comes from Open-Meteo: one GET request, no login. "
    "The response is converted from JSON into two tables, one daily and one hourly."
)
st.write("Documentation: https://open-meteo.com/")


# LIMIT
st.subheader("What this app does not do")
st.write(
    "It does not report parking. "
    "It only shows whether the week looks wet enough to leave a little sooner."


)


with st.expander("Credits"):
    st.write("Weather data: Open-Meteo (CC BY 4.0)")
    st.write("Campus coordinates: New College of Florida, Sarasota")
    st.caption("CEN 3352 · Front-End Development and Design")