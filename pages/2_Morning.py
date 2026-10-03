# morning hours
# filtered table for the drive window. settings come from the other pages


import streamlit as st
import pandas as pd
import requests


st.set_page_config(page_title="Morning Hours", page_icon="☔", layout="wide")


# STYLE
NAVY = "#003087"
GOLD = "#FFBF3F"
st.markdown(
    f"""
    <style>
        .stApp {{ background-color: #FFFFFF; }}
        h1, h2, h3 {{ color: {NAVY} !important; }}
        [data-testid="stSidebar"] {{ background-color: {NAVY}; }}
        [data-testid="stSidebar"] * {{ color: #FFFFFF !important; }}
        hr {{ border: none; border-top: 3px solid {GOLD}; }}
        .stCaption, [data-testid="stCaption"] {{ color: {NAVY} !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("Morning Hours")
st.caption("Filtered table. 6–10 a.m. only. City and rain limit carry over from the app page.")


# PLACES
# same four spots as This Week
PLACES = {
    "NCF campus": (27.3844, -82.5601),
    "Bradenton": (27.4989, -82.5748),
    "Venice": (27.0998, -82.4543),
    "Tampa": (27.9506, -82.4572),
}


# SESSION STATE
# if I set these on app, this page opens with the same values
if "place" not in st.session_state:
    st.session_state.place = "NCF campus"
if "rain_cutoff" not in st.session_state:
    st.session_state.rain_cutoff = 40


# LOAD
# hourly only. cached so the slider doesnt hit the API again
@st.cache_data(ttl=3600)
def load_forecast(place_name):
    lat, lon = PLACES[place_name]
    r = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "hourly": "precipitation_probability,temperature_2m",
            "forecast_days": 7,
            "timezone": "America/New_York",
            "temperature_unit": "fahrenheit",
        },
        timeout=20,
    )
    r.raise_for_status()
    data = r.json()

    hourly = pd.DataFrame(data["hourly"])
    hourly = hourly.rename(columns={
        "time": "when",
        "precipitation_probability": "rain_chance",
        "temperature_2m": "temp_f",
    })
    hourly["when"] = pd.to_datetime(hourly["when"])
    hourly["hour"] = hourly["when"].dt.hour
    return hourly


# SIDEBAR
# shows the values that carried over
with st.sidebar:
    st.header("Your settings")
    st.write("Location: " + st.session_state.place)
    st.write("Treat as wet at " + str(st.session_state.rain_cutoff) + "%")
    st.caption("Edit these on the app page if you want to change them.")


# FILTERS
# these always cut the table. I save city and limit again so app stays in sync
place_list = list(PLACES.keys())
place_start = place_list.index(st.session_state.place)

st.subheader("Filter the table")
f1, f2, f3 = st.columns(3)
with f1:
    place = st.selectbox("Starting location", place_list, index=place_start)
    st.session_state.place = place
with f2:
    cutoff = st.slider(
        "Minimum rain chance (%)",
        10, 90, value=int(st.session_state.rain_cutoff), step=5,
    )
    st.session_state.rain_cutoff = cutoff
with f3:
    hour_choice = st.selectbox("Which hour?", ["All morning", "6", "7", "8", "9", "10"])


try:
    hourly = load_forecast(place)
except Exception:
    st.error("The forecast could not be loaded. Wait a moment and try again.")
    st.stop()


# APPLY FILTERS
# commute hours first, then the slider, then one hour if I picked one
# the table below uses filtered, not the full hourly dump
morning = hourly[(hourly["hour"] >= 6) & (hourly["hour"] <= 10)].copy()
filtered = morning[morning["rain_chance"] >= cutoff]
if hour_choice != "All morning":
    filtered = filtered[filtered["hour"] == int(hour_choice)]


st.metric("Rows in the table", len(filtered))


# EMPTY
# if the filters wipe the table I stop instead of showing a blank one
if len(filtered) == 0:
    st.warning("No rows match. Lower the slider or pick All morning.")
    st.stop()


# TABLE
# this is the filtered table. it changes when the widgets change
show = filtered.copy()
show["when"] = show["when"].dt.strftime("%a %b %d, %I %p")
st.subheader("Hours that match")
st.dataframe(
    show.rename(columns={
        "when": "When",
        "hour": "Hour",
        "rain_chance": "Rain chance %",
        "temp_f": "Temp °F",
    })[["When", "Hour", "Rain chance %", "Temp °F"]],
    hide_index=True,
    width="stretch",
)
st.caption("Only morning hours at or above the rain limit. Not the full week.")