import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="Global Parlay Pro", layout="wide")
st.title("🌎 Global Multi-Sport Parlay Audit")

# 2. Sidebar: Global Settings & Bankroll
sport = st.sidebar.selectbox("Select Sport", ["NBA", "NFL", "Soccer"])
bankroll = st.sidebar.number_input("Total Bankroll ($)", min_value=0, value=1000)

# 3. Comprehensive Team Lists
if sport == "NBA":
    teams = [
        "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", "Chicago Bulls", 
        "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons", "Golden State Warriors", 
        "Houston Rockets", "Indiana Pacers", "LA Clippers", "LA Lakers", "Memphis Grizzlies", 
        "Miami Heat", "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks", 
        "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns", "Portland Trail Blazers", 
        "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors", "Utah Jazz", "Washington Wizards"
    ]
    props = ["Points Over", "Points Under", "Rebounds Over", "Assists Over", "Made 3-Pointers", "Double-Double"]
elif sport == "NFL":
    teams = [
        "Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills", "Carolina Panthers", 
        "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns", "Dallas Cowboys", "Denver Broncos", 
        "Detroit Lions", "Green Bay Packers", "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", 
        "Kansas City Chiefs", "Las Vegas Raiders", "Los Angeles Chargers", "Los Angeles Rams", "Miami Dolphins", 
        "Minnesota Vikings", "New England Patriots", "New Orleans Saints", "New York Giants", "New York Jets", 
        "Philadelphia Eagles", "Pittsburgh Steelers", "San Francisco 49ers", "Seattle Seahawks", "Tampa Bay Buccaneers", 
        "Tennessee Titans", "Washington Commanders"
    ]
    props = ["Passing TDs Over", "Rushing Yards Over", "Anytime TD Scorer", "Receiving Yards Over", "Spread Cover"]
else: # Soccer
    teams = [
        "Man City", "Arsenal", "Liverpool", "Real Madrid", "Barcelona", "Bayern Munich", 
        "PSG", "Inter Milan", "AC Milan", "Juventus", "Bayer Leverkusen", "Aston Villa"
    ]
    props = ["Goals Over 2.5", "Goals Under 2.5", "BTTS - Yes", "Player to Score", "Corners Over"]

# 4. Interactive Audit Columns
col1, col2, col3 = st.columns(3)

with col1:
    st.header("📋 Selections")
    selected_team = st.selectbox("Select Team", teams)
    selected_props = st.multiselect("Markets & Props", props)
    odds = st.number_input("Decimal Odds (e.g. 2.00)", value=1.91)

with col2:
    st.header("🚨 Risk Factors")
    is_injured = st.toggle("Key Player Out?")
    is_b2b = st.toggle("Back-to-Back Game?")
    bad_weather = st.toggle("Severe Weather?")
    spread = st.slider("Spread/Handicap", 0.0, 20.0, 3.5)

with col3:
    st.header("🏁 Official Factor")
    ref_style = st.radio("Official Tendency", ["Tight (Foul Heavy)", "Average", "Loose (Plays On)"])

st.markdown("---")

# 5. Logic Engine (Hit Possibility Calculation)
base_conf = 85
# Penalty points
penalties = (len(selected_props) * 12)
if is_injured: penalties += 15
if is_b2b: penalties += 10
if bad_weather: penalties += 10
if spread > 10: penalties += 10
if ref_style == "Tight (Foul Heavy)" and sport == "NBA": penalties += 5

confidence = max(5, base_conf - penalties)

# 6. Results & Bankroll Management
st.subheader("📊 Audit Results")
res1, res2, res3 = st.columns(3)

with res1:
    st.metric("Hit Possibility", f"{confidence}%")
with res2:
    # Simplified stake recommendation
    suggested_stake = (bankroll * (confidence / 100)) * 0.05
    st.metric("Suggested Stake", f"${suggested_stake:.2f}")
with res3:
    risk_status = "🔥 HIGH" if confidence < 45 else "⚠️ MED" if confidence < 75 else "✅ LOW"
    st.metric("Risk Level", risk_status)

# Visual Alerts
if confidence < 45:
    st.error(f"AUDIT FAILED: High risk for **{selected_team}**. Too many negative factors.")
elif confidence < 75:
    st.warning(f"AUDIT CAUTION: Moderate risk detected. Adjust your units.")
else:
    st.success(f"AUDIT PASSED: Strong conditions for **{selected_team}**.")

if selected_props:
    st.write(f"Legs included: {', '.join(selected_props)}")
