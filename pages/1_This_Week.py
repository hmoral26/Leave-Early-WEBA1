# this week
# pull the forecast and filter it


import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import requests


st.set_page_config(page_title="This Week", page_icon="☔", layout="wide")


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


st.title("This week's drive")
st.caption("Seven-day forecast. The table and charts follow the filters below.")


# PLACES
# real coords. the weather numbers come from the api
PLACES = {
    "NCF campus": (27.3844, -82.5601),
    "Bradenton": (27.4989, -82.5748),
    "Venice": (27.0998, -82.4543),
    "Tampa": (27.9506, -82.4572),
}


# SESSION STATE
# same keys as home
#without these, this page always opens at NCF and 40%
if "place" not in st.session_state:
    st.session_state.place = "NCF campus"
if "rain_cutoff" not in st.session_state:
    st.session_state.rain_cutoff = 40


# LOAD
# one get request, then turn json into two tables
# cache so moving a slider doesnt hit the api again
## cache is the forecast, not the user's choice. 
# slider does not refetch. new city does

@st.cache_data(ttl=3600) #remember the result of load_forecast for one hour.
def load_forecast(place_name):
    lat, lon = PLACES[place_name]
    r = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "daily": "precipitation_probability_max,precipitation_sum,temperature_2m_max,temperature_2m_min",
            "hourly": "precipitation_probability,temperature_2m",
            "forecast_days": 7,
            "timezone": "America/New_York",
            "temperature_unit": "fahrenheit",
            "precipitation_unit": "inch",
        },
        timeout=20,
    )
    r.raise_for_status()
    data = r.json()

    daily = pd.DataFrame(data["daily"])
    daily = daily.rename(columns={
        "time": "date",
        "precipitation_probability_max": "rain_chance",
        "precipitation_sum": "rain_inches",
        "temperature_2m_max": "high_f",
        "temperature_2m_min": "low_f",
    })
    daily["date"] = pd.to_datetime(daily["date"])

    hourly = pd.DataFrame(data["hourly"])
    hourly = hourly.rename(columns={
        "time": "when",
        "precipitation_probability": "rain_chance",
        "temperature_2m": "temp_f",
    })
    hourly["when"] = pd.to_datetime(hourly["when"])
    hourly["date"] = hourly["when"].dt.normalize()
    hourly["hour"] = hourly["when"].dt.hour
    return daily, hourly


# SIDEBAR
# write the number as one string so it doesnt turn into a white box
with st.sidebar:
    st.header("Your settings")
    st.write("Location: " + st.session_state.place)
    st.write("Treat as wet at " + str(st.session_state.rain_cutoff) + "%")
    st.caption("Edit these on the Home page if you want to change them.")


# FILTERS
# place changes which forecast we load
# slider + checkbox cut the table
place_list = list(PLACES.keys())
place_start = place_list.index(st.session_state.place) #puts the save city back into the drop down

st.subheader("Filter the week")
f1, f2, f3 = st.columns(3)
with f1:
    place = st.selectbox("Starting location", place_list, index=place_start)

    #widget changes
    st.session_state.place = place
with f2:
    cutoff = st.slider(
        "Minimum rain chance (%)",
        10,
        90,
        value=int(st.session_state.rain_cutoff),
        step=5,
    )
    st.session_state.rain_cutoff = cutoff
with f3:
    wet_only = st.checkbox("Show only wet days")


#What if API fails?

try:
    daily, hourly = load_forecast(place)
except Exception:
    st.error("The forecast could not be loaded. Wait a moment and try again.")
    st.stop()


# APPLY FILTERS
# checkbox stacks on the slider. charts must use filtered, not daily
filtered = daily.copy()
if wet_only: #second filter. checkbox stacks on the slider. charts must use filtered, not daily
    filtered = filtered[filtered["rain_chance"] >= cutoff]


# METRICS
# first one uses the whole week + cutoff
# other two use whatever is on screen
## counted here. not a column from the API. 
# Uses the day's max rain chance

#counts days at or above slider
leave_early_days = int((daily["rain_chance"] >= cutoff).sum()) 
if len(filtered) > 0:
    worst = int(filtered["rain_chance"].max())
    avg_high = round(filtered["high_f"].mean(), 1)
else:
    worst = 0
    avg_high = 0

m1, m2, m3 = st.columns(3)
m1.metric("Wet days this week", leave_early_days)
m2.metric("Highest rain chance (shown)", str(worst) + "%")
m3.metric("Average high (shown)", str(avg_high) + " °F")


# EMPTY
## stop so an empty filter does not draw a blank chart
if len(filtered) == 0:
    st.warning("No days match. Clear the checkbox or lower the slider.")
    st.stop() #stops the script so an empty filter does not draw a blank chart.


# TABLE
st.subheader("Days that match")
show = filtered.copy()
show["date"] = show["date"].dt.strftime("%a %b %d") #format the date for the table. not a column from the API.
st.dataframe(
    show.rename(columns={
        "date": "Day",
        "rain_chance": "Rain chance %",
        "rain_inches": "Rain (inches)",
        "high_f": "High °F",
        "low_f": "Low °F",
    }),
    hide_index=True,
    width="stretch",
)


# CHARTS
# line chart averages hourly rows by morning
st.subheader("Charts")
c1, c2 = st.columns(2)

with c1:
    st.write("Daily rain chance")
    bar = (
        alt.Chart(filtered)
        .mark_bar()
        .encode(
            x=alt.X("date:T", title="Day"),
            y=alt.Y("rain_chance:Q", title="Rain chance %"),
            color=alt.value(NAVY),
        )
        .properties(title="Rain chance by day")
    )
    st.altair_chart(bar, width="stretch")
    st.caption("One bar per day, using the filtered table.")

with c2:
    st.write("Morning rain chance (6–10 a.m.)")

    # agrregate the hourly rows into one morning number per day. 
    # then filter to the days that are showing in the table.

    # grouped chart: 6-10am hours averaged into one morning number per day
    morning = hourly[(hourly["hour"] >= 6) & (hourly["hour"] <= 10)]
    by_day = morning.groupby("date", as_index=False)["rain_chance"].mean()
    by_day = by_day[by_day["date"].isin(filtered["date"])]
    if len(by_day) == 0:
        st.write("No morning hours to display.")
    else:
        line = px.line(
            by_day,
            x="date",
            y="rain_chance",
            markers=True,
            title="Average 6–10 a.m. rain chance",
        )
        line.update_traces(line_color=NAVY, marker_color=GOLD)
        line.update_layout(yaxis_title="Rain chance %", xaxis_title="Day")
        st.plotly_chart(line, width="stretch")
        st.caption("Hourly readings grouped into one morning average per day.")


# SOURCE
with st.expander("Data source"):
    st.write("Open-Meteo forecast API. No API key.")
    st.write("https://api.open-meteo.com/v1/forecast")
    st.write("Results are cached for one hour.")