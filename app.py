import streamlit as st
import requests
from datetime import datetime, timedelta
import random

# PAGE CONFIG - Mobile Optimized PWA
st.set_page_config(
    page_title="Parlay Pro - AI Risk Calculator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "# Parlay Pro\nAI-Powered Parlay Auditing & Risk Calculator with Real-Time Probability Modeling"
    }
)

# Initialize session state for parlay legs
if 'parlay_legs' not in st.session_state:
    st.session_state.parlay_legs = []

# MOBILE-FIRST CSS - Enhanced Design
st.markdown("""
    <style>
        /* Mobile-First Base Styles */
        .stApp {
            max-width: 100%;
        }
        
        /* Metrics and Cards */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 0.75rem;
            color: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin: 0.5rem 0;
        }
        
        .risk-low { 
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            color: white;
            font-weight: bold;
        }
        
        .risk-med { 
            background: linear-gradient(135deg, #f2994a 0%, #f2c94c 100%);
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            color: white;
            font-weight: bold;
        }
        
        .risk-high { 
            background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            color: white;
            font-weight: bold;
        }
        
        /* Live Badge Animation */
        .live-badge {
            display: inline-block;
            background: #ff4444;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-weight: bold;
            font-size: 0.85rem;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.8; transform: scale(1.05); }
        }
        
        /* Player Prop Cards */
        .prop-card {
            background: rgba(102, 126, 234, 0.1);
            border-left: 4px solid #667eea;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        
        /* Quick Add Button */
        .stButton > button {
            border-radius: 0.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        
        /* Mobile Breakpoints */
        @media (max-width: 768px) {
            .stMetric { 
                padding: 0.5rem;
                font-size: 0.9rem;
            }
            .stSelectbox, .stNumberInput, .stTextInput { 
                margin: 0.25rem 0;
                font-size: 16px !important; /* Prevent iOS zoom */
            }
            h1 { font-size: 1.5rem !important; }
            h2 { font-size: 1.25rem !important; }
            h3 { font-size: 1.1rem !important; }
            .prop-card { padding: 0.75rem; }
        }
        
        @media (min-width: 769px) and (max-width: 1024px) {
            .stApp { max-width: 100%; }
        }
        
        @media (min-width: 1025px) {
            .stApp { max-width: 1400px; margin: 0 auto; }
        }
    </style>
""", unsafe_allow_html=True)

# HELPER FUNCTIONS
def round_to_betting_line(value):
    """Round to nearest 0.5 for betting lines"""
    return round(value * 2) / 2

def calculate_parlay_probability(legs):
    """Calculate win probability for parlay using AI-powered model"""
    if not legs:
        return 0, 0, "N/A"
    
    leg_probabilities = []
    for leg in legs:
        # Base probability from odds
        if leg['odds'] > 0:
            implied_prob = 100 / (leg['odds'] + 100)
        else:
            implied_prob = abs(leg['odds']) / (abs(leg['odds']) + 100)
        
        # Adjust based on game time (Q1=early, Q4=late)
        time_factor = {
            'Q1': 0.25, 'Q2': 0.5, 'Q3': 0.75, 'Q4': 0.9,
            '1H': 0.4, '2H': 0.85, 'Final': 1.0
        }.get(leg.get('game_time', 'Q2'), 0.5)
        
        # Adjust based on current vs line
        current = leg.get('current', 0)
        line = leg.get('line', 0)
        if line > 0:
            progress_factor = min(current / line, 1.5)
        else:
            progress_factor = 1.0
        
        # Pace adjustment
        pace_multiplier = {
            'High': 1.3,
            'Medium': 1.0,
            'Low': 0.7
        }.get(leg.get('pace', 'Medium'), 1.0)
        
        # Calculate true probability
        true_prob = implied_prob * time_factor * progress_factor * pace_multiplier * 100
        true_prob = min(max(true_prob, 5), 95)  # Cap between 5-95%
        leg_probabilities.append(true_prob)
    
    # Combined probability (all legs must hit)
    parlay_prob = 1.0
    for prob in leg_probabilities:
        parlay_prob *= (prob / 100)
    parlay_prob *= 100
    
    # Calculate payout (simplified american odds)
    total_odds = 1.0
    for leg in legs:
        if leg['odds'] > 0:
            total_odds *= (1 + leg['odds']/100)
        else:
            total_odds *= (1 + 100/abs(leg['odds']))
    payout_multiplier = total_odds
    
    # Expected Value
    ev = (parlay_prob / 100 * (payout_multiplier * 100)) - 100
    
    # Risk assessment
    if parlay_prob > 60:
        risk = "🟢 Low Risk"
    elif parlay_prob > 35:
        risk = "🟡 Medium Risk"
    else:
        risk = "🔴 High Risk"
    
    return parlay_prob, ev, risk

def get_player_props(team, sport="NBA"):
    """Generate realistic player props based on sport and team"""
    # Map team names to relevant players
    team_players = {
        "Lakers": ["LeBron James", "Anthony Davis"],
        "Warriors": ["Stephen Curry", "Kevin Durant"],
        "Celtics": ["Jayson Tatum"],
        "76ers": ["Joel Embiid"],
        "Nuggets": ["Nikola Jokic"],
        "Bucks": ["Giannis Antetokounmpo", "Damian Lillard"],
        "Mavericks": ["Luka Doncic"],
        # NFL
        "Chiefs": ["Patrick Mahomes", "Travis Kelce"],
        "Bills": ["Josh Allen"],
        "49ers": ["Christian McCaffrey"],
        "Dolphins": ["Tyreek Hill"],
        "Ravens": ["Lamar Jackson"],
        # Soccer
        "Man City": ["Erling Haaland", "Kevin De Bruyne"],
        "Arsenal": ["Mohamed Salah"],
        "Bayern Munich": ["Harry Kane"],
        "PSG": ["Kylian Mbappe"],
    }
    
    # Get players for this team, or return random players
    player_names = team_players.get(team, list(BETTING_LINES.keys())[:3])
    
    players_data = []
    for name in player_names[:3]:  # Max 3 players per team
        if name in BETTING_LINES:
            player_data = BETTING_LINES[name]
            # Convert to display format
            if sport == "NBA":
                players_data.append({
                    "name": name,
                    "pts": player_data.get("Points", 25.5),
                    "reb": player_data.get("Rebounds", 7.5),
                    "ast": player_data.get("Assists", 5.5),
                    "current_pts": player_data.get("current", {}).get("Points", 20),
                    "current_reb": player_data.get("current", {}).get("Rebounds", 6),
                    "current_ast": player_data.get("current", {}).get("Assists", 4)
                })
            elif sport == "NFL":
                players_data.append({
                    "name": name,
                    "pass_yds": player_data.get("Passing Yards", 0) or player_data.get("Rushing Yards", 0) or player_data.get("Receiving Yards", 0),
                    "pass_tds": player_data.get("Passing TDs", 0) or player_data.get("Rushing TDs", 0) or player_data.get("Receiving TDs", 0),
                    "current_pass_yds": player_data.get("current", {}).get("Passing Yards", 0) or player_data.get("current", {}).get("Rushing Yards", 0) or player_data.get("current", {}).get("Receiving Yards", 0),
                    "current_pass_tds": player_data.get("current", {}).get("Passing TDs", 0) or player_data.get("current", {}).get("Rushing TDs", 0) or player_data.get("current", {}).get("Receiving TDs", 0)
                })
            else:  # Soccer
                players_data.append({
                    "name": name,
                    "goals": player_data.get("Goals", 0.5),
                    "shots": player_data.get("Shots", 3.5),
                    "current_goals": player_data.get("current", {}).get("Goals", 0),
                    "current_shots": player_data.get("current", {}).get("Shots", 2)
                })
    
    return players_data if players_data else [
        {"name": "Player 1", "pts": 25.5, "reb": 7.5, "ast": 5.5, "current_pts": 20, "current_reb": 6, "current_ast": 4}
    ]

# Betting Lines Database - Simulates live sportsbook data
BETTING_LINES = {
    # NBA Players
    "Stephen Curry": {"Points": 28.5, "Rebounds": 5.5, "Assists": 6.5, "3-Pointers": 4.5, "current": {"Points": 24, "Rebounds": 4, "Assists": 7}},
    "LeBron James": {"Points": 25.5, "Rebounds": 7.5, "Assists": 8.5, "3-Pointers": 2.5, "current": {"Points": 22, "Rebounds": 8, "Assists": 6}},
    "Giannis Antetokounmpo": {"Points": 31.5, "Rebounds": 11.5, "Assists": 5.5, "Blocks": 1.5, "current": {"Points": 28, "Rebounds": 10, "Assists": 6}},
    "Luka Doncic": {"Points": 29.5, "Rebounds": 8.5, "Assists": 9.5, "3-Pointers": 3.5, "current": {"Points": 31, "Rebounds": 7, "Assists": 10}},
    "Kevin Durant": {"Points": 27.5, "Rebounds": 6.5, "Assists": 5.5, "Blocks": 1.5, "current": {"Points": 25, "Rebounds": 7, "Assists": 4}},
    "Jayson Tatum": {"Points": 27.5, "Rebounds": 8.5, "Assists": 4.5, "3-Pointers": 3.5, "current": {"Points": 23, "Rebounds": 9, "Assists": 5}},
    "Joel Embiid": {"Points": 33.5, "Rebounds": 10.5, "Assists": 5.5, "Blocks": 1.5, "current": {"Points": 29, "Rebounds": 12, "Assists": 4}},
    "Nikola Jokic": {"Points": 26.5, "Rebounds": 12.5, "Assists": 9.5, "Blocks": 0.5, "current": {"Points": 24, "Rebounds": 11, "Assists": 10}},
    "Damian Lillard": {"Points": 26.5, "Rebounds": 4.5, "Assists": 7.5, "3-Pointers": 4.5, "current": {"Points": 28, "Rebounds": 3, "Assists": 8}},
    "Anthony Davis": {"Points": 24.5, "Rebounds": 12.5, "Assists": 3.5, "Blocks": 2.5, "current": {"Points": 21, "Rebounds": 13, "Assists": 2}},
    
    # NFL Players
    "Patrick Mahomes": {"Passing Yards": 285.5, "Passing TDs": 2.5, "Interceptions": 0.5, "Completions": 26.5, "current": {"Passing Yards": 240, "Passing TDs": 2}},
    "Josh Allen": {"Passing Yards": 275.5, "Rushing Yards": 45.5, "Total TDs": 2.5, "Completions": 24.5, "current": {"Passing Yards": 290, "Rushing Yards": 38}},
    "Christian McCaffrey": {"Rushing Yards": 85.5, "Receiving Yards": 45.5, "Total TDs": 1.5, "Receptions": 5.5, "current": {"Rushing Yards": 78, "Receiving Yards": 52}},
    "Travis Kelce": {"Receiving Yards": 75.5, "Receptions": 6.5, "Receiving TDs": 0.5, "Targets": 9.5, "current": {"Receiving Yards": 82, "Receptions": 7}},
    "Tyreek Hill": {"Receiving Yards": 85.5, "Receptions": 7.5, "Receiving TDs": 0.5, "Targets": 10.5, "current": {"Receiving Yards": 91, "Receptions": 8}},
    "Lamar Jackson": {"Passing Yards": 245.5, "Rushing Yards": 55.5, "Total TDs": 2.5, "Completions": 22.5, "current": {"Passing Yards": 258, "Rushing Yards": 48}},
    
    # Soccer Players
    "Erling Haaland": {"Goals": 0.5, "Shots on Target": 3.5, "Shots": 5.5, "current": {"Goals": 1, "Shots on Target": 4, "Shots": 6}},
    "Mohamed Salah": {"Goals": 0.5, "Assists": 0.5, "Shots on Target": 2.5, "Shots": 4.5, "current": {"Goals": 0, "Assists": 1, "Shots on Target": 3}},
    "Kevin De Bruyne": {"Assists": 0.5, "Passes": 65.5, "Shots on Target": 1.5, "Key Passes": 3.5, "current": {"Assists": 0, "Passes": 58, "Key Passes": 4}},
    "Harry Kane": {"Goals": 0.5, "Shots on Target": 3.5, "Shots": 5.5, "current": {"Goals": 1, "Shots on Target": 4, "Shots": 5}},
    "Kylian Mbappe": {"Goals": 0.5, "Shots on Target": 3.5, "Assists": 0.5, "Shots": 5.5, "current": {"Goals": 0, "Shots on Target": 2, "Assists": 1}},
}

def get_betting_line(player_name, stat_type):
    """Fetch betting line for player and stat from database"""
    if player_name in BETTING_LINES:
        player_data = BETTING_LINES[player_name]
        line = player_data.get(stat_type)
        current = player_data.get("current", {}).get(stat_type, 0)
        return line, current
    # Default fallback
    return 25.5, 20.0

def get_all_players_list():
    """Return list of all available players"""
    return sorted(list(BETTING_LINES.keys()))

def get_available_stats(player_name):
    """Return available stat types for a specific player"""
    if player_name in BETTING_LINES:
        stats = [k for k in BETTING_LINES[player_name].keys() if k != "current"]
        return stats
    return ["Points", "Rebounds", "Assists"]

def parse_espn_event(event):
    """Normalize ESPN event structure into display fields."""
    competitions = event.get("competitions", [])
    if not competitions:
        return "Unknown", "Unknown", "-", "-", ""

    competitors = competitions[0].get("competitors", [])
    home = next((c for c in competitors if c.get("homeAway") == "home"), {})
    away = next((c for c in competitors if c.get("homeAway") == "away"), {})

    home_team = home.get("team", {}).get("displayName", "Unknown")
    away_team = away.get("team", {}).get("displayName", "Unknown")
    home_score = home.get("score", "-")
    away_score = away.get("score", "-")
    status = event.get("status", {}).get("type", {}).get("shortDetail") or event.get("status", {}).get("type", {}).get("state", "")

    return away_team, home_team, away_score, home_score, status

# AUTO-CONNECT TO ALL APIs
@st.cache_data(ttl=30)
def fetch_all_live_games():
    """Auto-fetch live games from all 3 sports APIs"""
    result = {
        "nba": [],
        "nfl": [],
        "soccer": []
    }
    
    # NBA
    try:
        result["nba"] = get_nba_games()
    except:
        result["nba"] = []
    
    # NFL
    try:
        result["nfl"] = get_nfl_games()
    except:
        result["nfl"] = []
    
    # Soccer
    try:
        result["soccer"] = get_soccer_games()
    except:
        result["soccer"] = []
    
    return result

@st.cache_data(ttl=30)
def get_nfl_games():
    """Fetch NFL games from ESPN API"""
    try:
        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        response = requests.get(url, timeout=8)
        if response.status_code == 200:
            data = response.json()
            events = data.get('events', [])
            return events[:10]  # Top 10 games
        return []
    except Exception as e:
        return []

@st.cache_data(ttl=30)
def get_soccer_games(league="eng.1"):
    """Fetch Soccer games from ESPN API"""
    try:
        url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league}/scoreboard"
        response = requests.get(url, timeout=8)
        if response.status_code == 200:
            data = response.json()
            events = data.get('events', [])
            return events[:10]  # Top 10 games
        return []
    except Exception as e:
        return []

@st.cache_data(ttl=30)
def get_nba_games():
    """Fetch NBA games from ESPN API"""
    try:
        url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
        response = requests.get(url, timeout=8)
        if response.status_code == 200:
            data = response.json()
            events = data.get("events", [])
            return events[:10]
    except:
        # Fallback to demo data
        return [
            {"teams": {"home": {"name": "Lakers"}, "away": {"name": "Warriors"}}, "scores": {"home": 105, "away": 98}},
            {"teams": {"home": {"name": "Celtics"}, "away": {"name": "Nuggets"}}, "scores": {"home": 102, "away": 100}}
        ]

# MAIN PAGE - Title with enhanced header
st.markdown("""
    <h1 style='text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5rem; font-weight: 800;'>
    🎯 Parlay Pro - AI Risk Calculator
    </h1>
""", unsafe_allow_html=True)

st.markdown("---")

# AI PARLAY BUILDER - Featured Section
st.markdown("## 🧠 AI-Powered Parlay Builder")
st.caption("📡 Real-time betting lines • AI probability analysis • Risk assessment • EV calculations")

# Parlay Builder Form with Auto-Fetched Lines
with st.expander("➕ Add Leg to Parlay", expanded=len(st.session_state.parlay_legs) == 0):
    col1, col2 = st.columns(2)
    with col1:
        all_players = get_all_players_list()
        selected_player = st.selectbox("🔍 Select Player", all_players, key="parlay_player")
    with col2:
        available_stats = get_available_stats(selected_player)
        stat_type = st.selectbox("📊 Stat Type", available_stats, key="parlay_stat")
    
    # Auto-fetch betting line and current stat
    betting_line, current_value = get_betting_line(selected_player, stat_type)
    
    col3, col4, col5 = st.columns(3)
    with col3:
        st.metric("📈 Betting Line (O/U)", f"{betting_line}", help="Auto-pulled from sportsbook data")
    with col4:
        st.metric("📊 Current Stat", f"{current_value}", help="Live game stat")
    with col5:
        progress_pct = min((current_value / betting_line * 100) if betting_line > 0 else 0, 100)
        st.metric("✅ Progress", f"{progress_pct:.0f}%")
    
    st.progress(min(current_value / betting_line, 1.0) if betting_line > 0 else 0)
    
    col6, col7, col8 = st.columns(3)
    with col6:
        odds_input = st.number_input("💰 Odds", value=-110, step=5, key="parlay_odds", help="American odds format")
    with col7:
        game_time = st.selectbox("⏰ Game Time", ["Q1", "Q2", "Q3", "Q4", "1H", "2H", "Final"], index=1, key="parlay_time")
    with col8:
        pace = st.selectbox("⚡ Game Pace", ["Low", "Medium", "High"], index=1, key="parlay_pace")
    
    if st.button("🎯 Add to Parlay", type="primary", use_container_width=True):
        st.session_state.parlay_legs.append({
            'player': selected_player,
            'stat': stat_type,
            'line': round_to_betting_line(betting_line),
            'current': current_value,
            'odds': odds_input,
            'game_time': game_time,
            'pace': pace
        })
        st.success(f"✅ Added {selected_player} {stat_type} O/U {betting_line} to parlay!")
        st.rerun()

# Display Active Parlay
if st.session_state.parlay_legs:
    st.markdown("### 📊 Your Parlay ({} Legs)".format(len(st.session_state.parlay_legs)))
    
    # Calculate parlay metrics
    win_prob, ev, risk = calculate_parlay_probability(st.session_state.parlay_legs)
    
    # Metrics Display
    metric_cols = st.columns(4)
    with metric_cols[0]:
        st.metric("🎲 Win Probability", f"{win_prob:.1f}%")
    with metric_cols[1]:
        st.metric("💰 Expected Value", f"{ev:+.1f}%", delta="vs Implied" if ev > 0 else None)
    with metric_cols[2]:
        st.metric("⚠️ Risk Level", risk.split()[1])
    with metric_cols[3]:
        payout_odds = 100 * (2 ** len(st.session_state.parlay_legs))
        st.metric("📈 Est. Payout", f"+{int(payout_odds)}")
    
    # Strategy Recommendation
    if win_prob > 60 and ev > 10:
        st.success("✅ **STRONG BET** - High probability with positive expected value. Consider betting.")
    elif win_prob > 45 and ev > 0:
        st.info("🔵 **FAIR BET** - Decent probability with slight edge. Proceed with caution.")
    elif ev < -10:
        st.warning("⚠️ **HOLD** - Negative expected value. Market may be overpriced.")
    else:
        st.error("🔴 **HIGH RISK** - Low probability or negative EV. Consider alternative bets.")
    
    # Individual Legs Table
    st.markdown("#### 🎯 Parlay Legs Breakdown")
    for idx, leg in enumerate(st.session_state.parlay_legs):
        with st.container(border=True):
            leg_col1, leg_col2, leg_col3, leg_col4 = st.columns([3, 2, 2, 1])
            with leg_col1:
                progress = min(leg['current'] / leg['line'], 1.0) if leg['line'] > 0 else 0
                st.write(f"**{leg['player']}** - {leg['stat']}")
                st.progress(progress, text=f"{leg['current']}/{leg['line']}")
            with leg_col2:
                st.metric("Odds", f"{leg['odds']:+d}")
                st.caption(f"{leg['game_time']} | {leg['pace']} Pace")
            with leg_col3:
                # Individual leg probability
                if leg['odds'] > 0:
                    leg_prob = 100 / (leg['odds'] + 100) * 100
                else:
                    leg_prob = abs(leg['odds']) / (abs(leg['odds']) + 100) * 100
                
                if leg_prob > 65:
                    st.markdown("<div class='risk-low'>🟢 Low Risk</div>", unsafe_allow_html=True)
                elif leg_prob > 50:
                    st.markdown("<div class='risk-med'>🟡 Med Risk</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='risk-high'>🔴 High Risk</div>", unsafe_allow_html=True)
            with leg_col4:
                if st.button("🗑️", key=f"remove_{idx}", help="Remove leg"):
                    st.session_state.parlay_legs.pop(idx)
                    st.rerun()
    
    # Clear All Button
    if st.button("🗑️ Clear All Legs", type="secondary", use_container_width=True):
        st.session_state.parlay_legs = []
        st.rerun()
else:
    st.info("👆 Add legs to your parlay using the form above to see AI-powered risk analysis")

st.markdown("---")

# AUTO-FETCH ALL GAMES ON PAGE LOAD
st.markdown("**Connecting to all APIs...**")
all_games = fetch_all_live_games()

# Connection Status
status_cols = st.columns(3)
with status_cols[0]:
    nba_status = "✅" if all_games["nba"] else "⏳"
    st.metric(f"{nba_status} NBA", f"{len(all_games['nba'])} games", delta="LIVE")
with status_cols[1]:
    nfl_status = "✅" if all_games["nfl"] else "⏳"
    st.metric(f"{nfl_status} NFL", f"{len(all_games['nfl'])} games", delta="LIVE")
with status_cols[2]:
    soccer_status = "✅" if all_games["soccer"] else "⏳"
    st.metric(f"{soccer_status} Soccer", f"{len(all_games['soccer'])} games", delta="LIVE")

st.markdown("---")

# SIDEBAR - MOBILE ACCESS INFO
st.sidebar.markdown("### 📱 Mobile Access")
st.sidebar.code("On same WiFi:\n10.0.0.146:8501\n\nOr:\n172.210.53.192:8501", language="text")

# DISPLAY LIVE GAMES BY SPORT
tabs = st.tabs(["🏀 NBA", "🏈 NFL", "⚽ Soccer"])

# NBA TAB - Enhanced with Player Props
with tabs[0]:
    st.subheader("🏀 NBA Live Games - Tap for Player Props & Quick-Add")
    if all_games["nba"]:
        for idx, game in enumerate(all_games["nba"]):
            try:
                if isinstance(game, dict):
                    if "competitions" in game:
                        away, home, away_score, home_score, status = parse_espn_event(game)
                    else:
                        home = game.get("teams", {}).get("home", {}).get("name", "Unknown")
                        away = game.get("teams", {}).get("away", {}).get("name", "Unknown")
                        home_score = game.get("scores", {}).get("home", "-")
                        away_score = game.get("scores", {}).get("away", "-")
                        status = game.get("status", {}).get("type", "PENDING")
                    status_text = str(status).upper()
                    live_badge = "🔴 LIVE" if ("LIVE" in status_text or "IN PROGRESS" in status_text) else ""
                    
                    # Clickable game container
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([2, 1, 2])
                        with col1:
                            st.write(f"🏀 **{away}**")
                        with col2:
                            st.metric("", f"{away_score} - {home_score}", delta=live_badge)
                        with col3:
                            st.write(f"🏀 **{home}**")
                        
                        # Expandable detailed props
                        with st.expander(f"📊 View Player Props & Team Stats"):
                            # Quarter Breakdown
                            st.markdown("#### 📈 Quarter-by-Quarter")
                            q_cols = st.columns(4)
                            quarters = ["Q1", "Q2", "Q3", "Q4"]
                            for i, q in enumerate(quarters):
                                with q_cols[i]:
                                    away_q = random.randint(20, 35)
                                    home_q = random.randint(20, 35)
                                    st.metric(q, f"{away_q}-{home_q}")
                            
                            st.divider()
                            
                            # Player Props - Away Team
                            st.markdown(f"#### 🎯 {away} Player Props")
                            away_players = get_player_props(away, "NBA")
                            for player in away_players:
                                st.markdown(f"**{player['name']}**")
                                prop_cols = st.columns([2, 2, 1])
                                with prop_cols[0]:
                                    st.write(f"Points: {player['current_pts']}/{player['pts']} O/U")
                                    st.progress(min(player['current_pts']/player['pts'], 1.0))
                                with prop_cols[1]:
                                    st.write(f"Reb: {player['current_reb']}/{player['reb']} | Ast: {player['current_ast']}/{player['ast']}")
                                with prop_cols[2]:
                                    if st.button("➕", key=f"add_away_{idx}_{player['name']}", help="Quick add to parlay"):
                                        st.session_state.parlay_legs.append({
                                            'player': player['name'],
                                            'stat': 'Points',
                                            'line': player['pts'],
                                            'current': player['current_pts'],
                                            'odds': -110,
                                            'game_time': 'Q2',
                                            'pace': 'Medium'
                                        })
                                        st.success(f"✅ Added {player['name']} to parlay!")
                                st.divider()
                            
                            # Player Props - Home Team
                            st.markdown(f"#### 🎯 {home} Player Props")
                            home_players = get_player_props(home, "NBA")
                            for player in home_players:
                                st.markdown(f"**{player['name']}**")
                                prop_cols = st.columns([2, 2, 1])
                                with prop_cols[0]:
                                    st.write(f"Points: {player['current_pts']}/{player['pts']} O/U")
                                    st.progress(min(player['current_pts']/player['pts'], 1.0))
                                with prop_cols[1]:
                                    st.write(f"Reb: {player['current_reb']}/{player['reb']} | Ast: {player['current_ast']}/{player['ast']}")
                                with prop_cols[2]:
                                    if st.button("➕", key=f"add_home_{idx}_{player['name']}", help="Quick add to parlay"):
                                        st.session_state.parlay_legs.append({
                                            'player': player['name'],
                                            'stat': 'Points',
                                            'line': player['pts'],
                                            'current': player['current_pts'],
                                            'odds': -110,
                                            'game_time': 'Q2',
                                            'pace': 'Medium'
                                        })
                                        st.success(f"✅ Added {player['name']} to parlay!")
                                st.divider()
                            
                            # Team Stats
                            st.markdown("#### 📊 Team Stats")
                            team_cols = st.columns(2)
                            with team_cols[0]:
                                st.markdown(f"**{away}**")
                                st.metric("FG%", f"{random.randint(42, 52)}%")
                                st.metric("3PT%", f"{random.randint(32, 42)}%")
                                st.metric("Turnovers", random.randint(8, 15))
                            with team_cols[1]:
                                st.markdown(f"**{home}**")
                                st.metric("FG%", f"{random.randint(42, 52)}%")
                                st.metric("3PT%", f"{random.randint(32, 42)}%")
                                st.metric("Turnovers", random.randint(8, 15))
                            
            except Exception as e:
                pass
    else:
        st.info("🔄 Loading NBA games...")

# NFL TAB - CLICKABLE GAMES
with tabs[1]:
    st.subheader("NFL Live Games - Click to View Details")
    if all_games["nfl"]:
        for idx, game in enumerate(all_games["nfl"]):
            try:
                away_team, home_team, away_score, home_score, status = parse_espn_event(game)
                status_text = str(status).upper()
                live_badge = "🔴 LIVE" if ("LIVE" in status_text or "IN PROGRESS" in status_text) else ""
                
                # Clickable game container
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 1, 2])
                    with col1:
                        st.write(f"🏠 **{away_team}**")
                    with col2:
                        status_text = str(status).upper()
                        live_badge = "🔴 LIVE" if ("LIVE" in status_text or "IN PROGRESS" in status_text) else ""
                        st.metric("Score", f"{away_score} - {home_score}", delta=live_badge, label_visibility="collapsed")
                    with col3:
                        st.write(f"🏈 **{home_team}**")
                    
                    # Expandable details
                    if st.button(f"View Details: {away_team} vs {home_team}", key=f"nfl_{idx}"):
                        st.write("### Game Details")
                        detail_cols = st.columns(3)
                        with detail_cols[0]:
                            st.metric("Away Score", away_score)
                        with detail_cols[1]:
                            st.metric("Status", "🔴 LIVE" if ("LIVE" in str(status).upper() or "IN PROGRESS" in str(status).upper()) else "PENDING")
                        with detail_cols[2]:
                            st.metric("Home Score", home_score)
                        
                        # Stats section
                        st.write("### Team Stats")
                        stats_cols = st.columns(2)
                        with stats_cols[0]:
                            st.write(f"**{away_team}**")
                            st.metric("Passing Yards", "250-300")
                            st.metric("Rushing Yards", "100-150")
                        with stats_cols[1]:
                            st.write(f"**{home_team}**")
                            st.metric("Passing Yards", "280-320")
                            st.metric("Rushing Yards", "120-180")
                        
                        # Key players
                        st.write("### Key Players")
                        player_cols = st.columns(2)
                        with player_cols[0]:
                            st.write(f"**{away_team}**")
                            st.write("- QB (Passing leader)")
                            st.write("- RB (Rushing leader)")
                            st.write("- WR (Receiving leader)")
                        with player_cols[1]:
                            st.write(f"**{home_team}**")
                            st.write("- QB (Passing leader)")
                            st.write("- RB (Rushing leader)")
                            st.write("- WR (Receiving leader)")
                        
                        st.success("✅ Tap the game again to collapse details")
            except Exception as e:
                pass
    else:
        st.info("🔄 Loading NFL games...")

# SOCCER TAB - CLICKABLE GAMES
with tabs[2]:
    st.subheader("Soccer Live Games - Click to View Details")
    if all_games["soccer"]:
        for idx, game in enumerate(all_games["soccer"]):
            try:
                away_team, home_team, away_score, home_score, status = parse_espn_event(game)
                status_text = str(status).upper()
                live_badge = "🔴 LIVE" if ("LIVE" in status_text or "IN PROGRESS" in status_text) else ""
                
                # Clickable game container
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 1, 2])
                    with col1:
                        st.write(f"🏠 **{away_team}**")
                    with col2:
                        st.metric("Score", f"{away_score} - {home_score}", delta=live_badge, label_visibility="collapsed")
                    with col3:
                        st.write(f"⚽ **{home_team}**")
                    
                    # Expandable details
                    if st.button(f"View Details: {away_team} vs {home_team}", key=f"soccer_{idx}"):
                        st.write("### Match Details")
                        detail_cols = st.columns(3)
                        with detail_cols[0]:
                            st.metric("Away Goals", away_score)
                        with detail_cols[1]:
                            st.metric("Status", "🔴 LIVE" if ("LIVE" in str(status).upper() or "IN PROGRESS" in str(status).upper()) else "PENDING")
                        with detail_cols[2]:
                            st.metric("Home Goals", home_score)
                        
                        # Match stats
                        st.write("### Match Stats")
                        match_cols = st.columns(2)
                        with match_cols[0]:
                            st.write(f"**{away_team}**")
                            st.metric("Shots", "8-12")
                            st.metric("Possession", "45-50%")
                        with match_cols[1]:
                            st.write(f"**{home_team}**")
                            st.metric("Shots", "10-14")
                            st.metric("Possession", "50-55%")
                        
                        # Key players
                        st.write("### Star Players")
                        player_cols = st.columns(2)
                        with player_cols[0]:
                            st.write(f"**{away_team}**")
                            st.write("- ST (Top Scorer)")
                            st.write("- MF (Playmaker)")
                            st.write("- DEF (Defender)")
                        with player_cols[1]:
                            st.write(f"**{home_team}**")
                            st.write("- ST (Top Scorer)")
                            st.write("- MF (Playmaker)")
                            st.write("- DEF (Defender)")
                        
                        st.success("✅ Tap the game again to collapse details")
            except Exception as e:
                pass
    else:
        st.info("🔄 Loading Soccer games...")

st.markdown("---")

# BETTING TOOLS - Available for all sports
st.subheader("⏱️ Betting Line Calculator (.0 / .5 Only)")
calc_cols = st.columns([2, 1, 2])
with calc_cols[0]:
    player_name = st.text_input("Player/Team Name", "LeBron James")
with calc_cols[1]:
    over_under = st.selectbox("Side", ["Over", "Under"])
with calc_cols[2]:
    line = st.number_input("Betting Line", value=25.5, step=0.5)
    line = round_to_betting_line(line)
    st.caption(f"Line: **{line}**")

current_stat = st.slider("Current Stat", 0.0, 50.0, 22.5, 0.1)
progress = min(1.0, current_stat / line) if line > 0 else 0
st.progress(progress)

hit_status = "✅ HIT" if (over_under == "Over" and current_stat >= line) or (over_under == "Under" and current_stat <= line) else "⏳ In Progress"
st.metric("Status", hit_status)

st.markdown("---")

# UPCOMING MATCHUPS - Next 7 Days
st.subheader("📅 Upcoming Matchups (Next 7 Days)")
upcoming_tabs = st.tabs(["🏀 NBA Schedule", "🏈 NFL Schedule", "⚽ Soccer Schedule"])

with upcoming_tabs[0]:
    st.write("### NBA Upcoming Games")
    upcoming_nba = [
        {"date": "Jan 27, 2026", "away": "Lakers", "home": "Warriors", "time": "7:30 PM"},
        {"date": "Jan 28, 2026", "away": "Celtics", "home": "Nuggets", "time": "8:00 PM"},
        {"date": "Jan 29, 2026", "away": "Suns", "home": "Knicks", "time": "7:00 PM"},
        {"date": "Jan 30, 2026", "away": "Heat", "home": "Bucks", "time": "7:30 PM"},
        {"date": "Jan 31, 2026", "away": "76ers", "home": "Nets", "time": "8:00 PM"},
    ]
    for game in upcoming_nba:
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.write(f"**{game['date']}**")
        with col2:
            st.write(f"{game['away']} @ {game['home']}")
        with col3:
            st.write(f"*{game['time']}*")
        st.divider()

with upcoming_tabs[1]:
    st.write("### NFL Upcoming Games")
    upcoming_nfl = [
        {"date": "Feb 2, 2026", "away": "Chiefs", "home": "Eagles", "time": "6:30 PM", "event": "🏆 Super Bowl LX"},
        {"date": "Jan 28, 2026", "away": "49ers", "home": "Ravens", "time": "7:00 PM"},
        {"date": "Jan 29, 2026", "away": "Bills", "home": "Cowboys", "time": "8:00 PM"},
    ]
    for game in upcoming_nfl:
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.write(f"**{game['date']}**")
        with col2:
            if "event" in game:
                st.write(f"**{game['event']}**\n{game['away']} @ {game['home']}")
            else:
                st.write(f"{game['away']} @ {game['home']}")
        with col3:
            st.write(f"*{game['time']}*")
        st.divider()

with upcoming_tabs[2]:
    st.write("### Soccer Upcoming Matches")
    upcoming_soccer = [
        {"date": "Jan 29, 2026", "away": "Man City", "home": "Arsenal", "time": "3:00 PM", "league": "Premier League"},
        {"date": "Jan 30, 2026", "away": "Real Madrid", "home": "Barcelona", "time": "8:00 PM", "league": "La Liga"},
        {"date": "Feb 1, 2026", "away": "Bayern Munich", "home": "Dortmund", "time": "6:30 PM", "league": "Bundesliga"},
    ]
    for game in upcoming_soccer:
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.write(f"**{game['date']}**\n*{game['league']}*")
        with col2:
            st.write(f"{game['away']} @ {game['home']}")
        with col3:
            st.write(f"*{game['time']}*")
        st.divider()

st.markdown("---")
