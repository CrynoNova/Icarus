import streamlit as st
import requests # Required for live API info

# 1. Setup
st.set_page_config(page_title="Global Parlay Pro - LIVE", layout="wide")

# Helper Function: Forces lines to .0 or .5 only
def round_to_betting_line(value):
    return round(value * 2) / 2

# 2. Sidebar Navigation
st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("API Key", type="password") # Secure input
mode = st.sidebar.radio("Navigation", ["Live Game Audit", "Head-to-Head", "Stat Tracker"])
sport = st.sidebar.selectbox("Select Sport", ["NBA", "NFL", "Soccer"])

# 3. Dynamic Data Lists
if sport == "NBA":
    teams = ["Lakers", "Warriors", "Celtics", "Nuggets", "Suns", "Knicks", "Bucks", "76ers"]
    stats = ["Points", "Rebounds", "Assists", "3PM"]
elif sport == "NFL":
    teams = ["Chiefs", "Eagles", "49ers", "Bengals", "Cowboys", "Ravens", "Bills"]
    stats = ["Passing Yards", "Passing TDs", "Rushing Yards", "Receiving Yards"]
else: # Soccer
    teams = ["Man City", "Arsenal", "Liverpool", "Real Madrid", "Barcelona", "Bayern Munich"]
    stats = ["Goals", "Assists", "Shots on Target", "Corners"]

# 4. API Logic: Fetching Live Data
def get_live_stats(team_name):
    # This is a template URL; replace with your specific API endpoint
    url = f"https://api.sportsdata.io/v3/{sport}/scores/json/LiveStats/{team_name}"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        # response = requests.get(url, headers=headers) # Uncomment when API is ready
        # data = response.json()
        return {"status": "Live", "current_score": "102-98"} # Mock data for demonstration
    except:
        return None

# --- MODE 1: LIVE GAME AUDIT ---
if mode == "Live Game Audit":
    st.title("🌎 Live Multi-Sport Parlay Audit")
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📋 Selection")
        team = st.selectbox("Select Team", teams)
        live_data = get_live_stats(team)
        
        if live_data:
            st.success(f"Connected to Live API: {team} is currently {live_data['current_score']}")
        
        # User sets the line - function ensures it is .0 or .5
        raw_line = st.number_input("Target Line (Points/Stat)", value=25.0, step=0.5)
        clean_line = round_to_betting_line(raw_line)
        st.caption(f"Betting Line Adjusted to: **{clean_line}**")

    with col2:
        st.header("🚨 Context")
        is_injured = st.toggle("Key Player Out?")
        spread = st.slider("Spread", 0.0, 20.0, 4.5)
    
    st.markdown("---")
    risk = (15 if is_injured else 0) + (10 if spread > 10 else 0)
    conf = max(5, 95 - risk)
    st.metric("Global Hit Possibility", f"{conf}%")

# --- MODE 2: HEAD-TO-HEAD (H2H) ---
elif mode == "Head-to-Head":
    st.header("⚔️ Team vs Team Live Audit")
    h1, h2 = st.columns(2)
    with h1:
        t1 = st.selectbox("Home Team", teams, index=0)
        s1 = st.slider(f"{t1} Strength", 0, 100, 80)
    with h2:
        t2 = st.selectbox("Away Team", teams, index=1)
        s2 = st.slider(f"{t2} Strength", 0, 100, 75)
    
    res = "Home Advantage" if s1 >= s2 else "Away Advantage"
    st.info(f"Analysis: **{res}** detected for this matchup.")

# --- MODE 3: STAT TRACKER ---
elif mode == "Stat Tracker":
    st.header("⏱️ Live Player Tracker (.5 / .0 Lines Only)")
    
    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        p_name = st.text_input("Player Name", "Enter Name")
        p_stat = st.selectbox("Stat Category", stats)
    with p_col2:
        # Ensuring the line is always a betting line (.5 or .0)
        target = st.number_input("Betting Line", value=1.5, step=0.5)
        target = round_to_betting_line(target)
        side = st.radio("Side", ["Over", "Under"])
    with p_col3:
        # This would eventually be filled by your API
        current = st.number_input("Live Current Stat", value=0.0)

    # Progress Calculation
    if target > 0:
        progress = min(1.0, current / target)
        st.progress(progress)
        st.write(f"**{p_name}** is {current}/{target} for the {side}.")
