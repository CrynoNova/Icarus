import streamlit as st

# 1. Setup
st.set_page_config(page_title="Global Parlay Pro - Master", layout="wide")
st.title("🌎 Global Multi-Sport Parlay Audit")

# 2. Sidebar Navigation
mode = st.sidebar.radio("Navigation", ["Single Game Audit", "Head-to-Head Comparison", "Live Stat Tracker"])
sport = st.sidebar.selectbox("Select Sport", ["NBA", "NFL", "Soccer"])
bankroll = st.sidebar.number_input("Bankroll ($)", value=1000)

# 3. Comprehensive Data Lists
if sport == "NBA":
    teams = ["Lakers", "Warriors", "Celtics", "Nuggets", "Suns", "Knicks", "Bucks", "76ers"]
    stats = ["Points", "Rebounds", "Assists", "3PM", "Steals", "Blocks"]
elif sport == "NFL":
    teams = ["Chiefs", "Eagles", "49ers", "Bengals", "Cowboys", "Ravens", "Bills"]
    stats = ["Passing Yards", "Passing TDs", "Rushing Yards", "Receiving Yards", "Receptions"]
else: # Soccer
    teams = ["Man City", "Arsenal", "Liverpool", "Real Madrid", "Barcelona", "Bayern Munich"]
    stats = ["Goals", "Assists", "Shots on Target", "Corners", "Yellow Cards"]

# --- MODE 1: SINGLE GAME AUDIT ---
if mode == "Single Game Audit":
    col1, col2 = st.columns(2)
    with col1:
        st.header("📋 Selection")
        team = st.selectbox("Select Team", teams)
        selected_props = st.multiselect("Market Props", [f"{s} Over" for s in stats] + [f"{s} Under" for s in stats])
    with col2:
        st.header("🚨 Context")
        is_injured = st.toggle("Key Player Out?")
        spread = st.slider("Spread", 0.0, 20.0, 4.5)
    
    # Logic
    risk = (len(selected_props) * 15) + (20 if is_injured else 0)
    conf = max(5, 90 - risk)
    st.metric("Hit Possibility", f"{conf}%", delta=f"-{risk}% Risk")

# --- MODE 2: HEAD-TO-HEAD (H2H) ---
elif mode == "Head-to-Head Comparison":
    st.header("⚔️ Team vs Team Audit")
    h1, h2 = st.columns(2)
    with h1:
        t1 = st.selectbox("Team A (Home)", teams, index=0)
        s1 = st.slider(f"{t1} Strength", 0, 100, 75)
    with h2:
        t2 = st.selectbox("Team B (Away)", teams, index=1)
        s2 = st.slider(f"{t2} Strength", 0, 100, 70)
    
    diff = abs(s1 - s2)
    if s1 > s2:
        st.success(f"Advantage: **{t1}** (By {diff} power points)")
    else:
        st.success(f"Advantage: **{t2}** (By {diff} power points)")

# --- MODE 3: LIVE STAT TRACKER ---
elif mode == "Live Stat Tracker":
    st.header("⏱️ Live Player Performance Tracking")
    st.info("Input live data to see if your parlay leg is still alive.")
    
    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        p_name = st.text_input("Player Name", "LeBron James")
        p_stat = st.selectbox("Tracking Stat", stats)
    with p_col2:
        target = st.number_input("Bet Line (O/U)", value=25.5)
        side = st.radio("Side", ["Over", "Under"])
    with p_col3:
        current = st.number_input("Current Live Stat", value=18.0)
    
    # Progress Calculation
    progress = (current / target) if side == "Over" else (target - current) / target
    st.write(f"**{p_name}** needs {max(0.0, target - current)} more {p_stat} to hit the Over.")
    st.progress(min(1.0, progress))
    
    if side == "Over":
        if current >= target: st.success("🎯 LEG HIT!")
        elif current > (target * 0.75): st.warning("🔥 Heating Up - Close to hitting")
        else: st.error("❄️ Cold - Needs a big run")
    else: # Under
        if current >= target: st.error("❌ LEG BUSTED (Went Over)")
        else: st.success("✅ Leg Safe (Still Under)")
