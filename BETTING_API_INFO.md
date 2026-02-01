# Betting API Integration Guide

## Overview
This document explains betting API options for DraftKings, FanDuel, and other sportsbooks.

## Important Notes

### ⚠️ Legal & Access Limitations

1. **No Public Free APIs**: DraftKings, FanDuel, and major sportsbooks DO NOT offer public APIs for odds/lines
2. **Paid Data Providers Required**: You must use licensed sports data providers
3. **Costs**: Most providers charge $500-$5000+/month for real-time odds data

## Recommended Betting Data Providers

### 1. **The Odds API** ⭐ (Best for Parlay Pro)
- Website: https://the-odds-api.com/
- **Pricing**: 
  - Free tier: 500 requests/month
  - Starter: $50/month (10,000 requests)
  - Professional: $500/month (100,000 requests)
- **Coverage**: 
  - DraftKings, FanDuel, BetMGM, Caesars, and 30+ sportsbooks
  - NBA, NFL, MLB, NHL, Soccer, UFC, Tennis
  - Pre-game odds, live odds, player props
- **Advantages**:
  - Easy REST API
  - Real-time odds across multiple books
  - Player prop odds available
  - Good documentation

### 2. **Sportradar**
- Website: https://developer.sportradar.com/
- **Pricing**: Custom enterprise pricing (typically $10k+/year)
- **Coverage**: Official data partner for NFL, NBA, NHL
- **Advantages**: 
  - Most accurate and official data
  - Real-time stats and odds
  - Injury reports included
- **Disadvantages**: Very expensive

### 3. **BetData.io**
- Website: https://betdata.io/
- **Pricing**: Starting at $99/month
- **Coverage**: 20+ sportsbooks, multiple sports
- **Advantages**: Mid-tier pricing, good coverage

### 4. **RapidAPI Sports Odds**
- Website: https://rapidapi.com/theoddsapi/api/live-sports-odds
- **Pricing**: $0-$30/month (limited requests)
- **Coverage**: Basic odds data
- **Advantages**: Cheapest option

## Implementation Example (The Odds API)

```python
import requests

# Get your API key from https://the-odds-api.com/
ODDS_API_KEY = "your_api_key_here"
ODDS_API_BASE = "https://api.the-odds-api.com/v4"

@st.cache_data(ttl=60)
def get_player_props_from_odds_api(sport="basketball_nba", market="player_points"):
    """
    Fetch real player prop odds from multiple sportsbooks
    
    Args:
        sport: basketball_nba, americanfootball_nfl, baseball_mlb, icehockey_nhl
        market: player_points, player_rebounds, player_assists, player_pass_tds, etc.
    """
    try:
        url = f"{ODDS_API_BASE}/sports/{sport}/events"
        params = {
            "apiKey": ODDS_API_KEY,
            "regions": "us",
            "markets": market,
            "oddsFormat": "american",
            "bookmakers": "draftkings,fanduel,betmgm"
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Odds API Error: {str(e)}")
        return None

# Usage
nba_props = get_player_props_from_odds_api("basketball_nba", "player_points")
if nba_props:
    for game in nba_props:
        bookmakers = game.get("bookmakers", [])
        for book in bookmakers:
            if book["key"] == "draftkings":
                markets = book.get("markets", [])
                for market in markets:
                    for outcome in market["outcomes"]:
                        player_name = outcome["description"]
                        line = outcome["point"]
                        over_odds = outcome["price"]
                        
                        st.write(f"{player_name}: {line} O/U ({over_odds})")
```

## Current Parlay Pro Implementation

### What We Use Now:
1. **ESPN API** (Free): Game schedules, live scores, rosters, injury reports
2. **Hardcoded Lines**: Season averages and typical betting lines in `BETTING_LINES` dictionary
3. **Advanced Modeling**: Our AI calculates probabilities using:
   - Historical performance
   - Usage rates
   - Injury status
   - Home/away splits
   - Back-to-back games
   - Matchup difficulty
   - Game pace
   - Recent trends

### Why This Works:
- ESPN provides accurate game data, rosters, and injury status
- Our probability model is more sophisticated than simple odds conversion
- We calculate true win probability, not just market odds
- Users can input actual sportsbook odds for their specific bets

## Upgrade Path

### Phase 1 (Current): ✅ DONE
- ESPN API for games, rosters, injuries
- Advanced probability modeling
- Real-time score tracking

### Phase 2 (Optional): Real Odds Integration
**If you want to integrate betting APIs:**

1. **Sign up** for The Odds API (free tier to start)
2. **Replace** hardcoded lines with real-time odds from multiple sportsbooks
3. **Compare** odds across DraftKings, FanDuel, BetMGM to find best value
4. **Show** line movement and trends

**Code Changes Required:**
```python
# Replace get_betting_line() function to call Odds API
@st.cache_data(ttl=60)
def get_betting_line(player_name, stat_type):
    # Call The Odds API instead of returning hardcoded values
    real_odds = get_player_props_from_odds_api()
    # Parse and return actual sportsbook lines
    return line, current_performance
```

### Phase 3 (Advanced): Arbitrage & Line Shopping
- Compare odds across 20+ sportsbooks
- Alert users to arbitrage opportunities
- Track line movements for betting edges
- Show public betting percentages

## Cost Analysis

### Current (Free):
- ESPN API: $0
- Total: **$0/month**

### With Betting APIs:
- ESPN API: $0
- The Odds API (Starter): $50/month
- Total: **$50/month**

### Professional Setup:
- Sportradar: $1,000+/month
- Total: **$1,000+/month**

## Legal Disclaimer

⚠️ **Important**: 
- Betting APIs require compliance with gambling regulations
- Must verify user age and location
- Some states prohibit sports betting
- DraftKings/FanDuel terms prohibit scraping
- Always use licensed data providers

## Recommendation

**For Parlay Pro:**
1. **Keep current setup** for MVP - it's free and sophisticated
2. **Add The Odds API** only when:
   - You have 1000+ daily users
   - Users request real-time odds
   - Revenue justifies $50-500/month cost
3. **Focus on** improving probability model and UX first
4. **Monitor** ESPN API for any rate limiting

## Contact Information

- The Odds API Support: support@the-odds-api.com
- Sportradar: https://sportradar.com/contact/
- Questions: Add to GitHub issues
