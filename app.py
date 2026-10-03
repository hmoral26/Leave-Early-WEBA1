# app page
# problem + the two settings the other page reads


import streamlit as st


st.set_page_config(page_title="Is the drive wet?", page_icon="☔️", layout="wide")


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


st.title("Is the drive wet this week?")
st.caption("Seven-day rain forecast for the drive to New College.")


# SESSION STATE
# these two get used on This Week so they dont reset when I switch pages
# first visit only. these two have to exist before This Week reads them
if "place" not in st.session_state:
    st.session_state.place = "NCF campus"
if "rain_cutoff" not in st.session_state:
    st.session_state.rain_cutoff = 40


# PROBLEM
st.subheader("The problem")
st.write(
    "I drive to New College from off campus. I pick a leave time the night before, "
    "then find out in the morning whether the rain is light or heavy enough to matter. "
    "This page is a seven-day rain forecast for that drive, not a parking guide."
)
st.write(
    "How might we show the week’s rain chance on the drive before the student "
    "sets an alarm without opening a separate weather app?"
)

st.divider()


# PERSONA
st.subheader("Who this is for")
left, right = st.columns(2)
with left:
    st.write("Commuter students at New College.")
    st.write("**Goal:** get to morning class without leaving extra early every day." )
    st.write("**Frustration:** some days are dry and some look like a downpour.")
with right:
    st.write('**Quote:** "If it looks like rain I add 20 minutes, even when I don\'t know if I need to."')
    st.write("This app is only the weather on the drive.")

st.divider()


# SETTINGS
# whatever I pick here should still be selected on This Week
st.subheader("Set when rain is enough to matter")
st.write("These choices stay selected on This Week and Morning hours.")

#This block picks which city the dropdown should open on.
places = ["NCF campus", "Bradenton", "Venice", "Tampa"]
if st.session_state.place in places:
    start = places.index(st.session_state.place)
else:
    start = 0

c1, c2 = st.columns(2)
with c1:
    place = st.selectbox("Starting location", places, index=start)
    st.session_state.place = place # save city so This Week does not reset
with c2:
    cutoff = st.slider(
        "Treat a day as wet when rain chance reaches (%)",
        10,
        90,
        value=int(st.session_state.rain_cutoff),
        step=5,
    )
    st.session_state.rain_cutoff = cutoff # save rain limit across the page jump

st.write("Wet-day limit: " + str(cutoff) + "% · Location: " + place)
st.page_link("pages/1_This_Week.py", label="Open this week's forecast")