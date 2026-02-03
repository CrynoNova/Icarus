# API Guide - Player Data & Betting Odds

## ✅ FIXES APPLIED

### 1. Fixed NBA Player Roster Issue
**Problem:** ESPN v1 roster API was returning empty player lists  
**Solution:** Switched to ESPN v2 Core API which is more reliable

**New API Endpoint:**
```
https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/seasons/2026/teams/{team_id}/athletes?limit=50
```

**Benefits:**
- ✅ Returns complete player lists with positions
- ✅ Includes active status
- ✅ More stable than v1 API
- ✅ Works for all teams

---

## 🎯 AVAILABLE APIS

### 1. ESPN APIs (FREE - Currently Used)

#### ESPN Scoreboard API
- **Endpoint:** `https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard`
- **Data:** Live games, scores, schedules
- **Cost:** FREE ✅
- **Rate Limit:** None (reasonable use)

#### ESPN v2 Core API (NEW - Now Using)
- **Endpoint:** `https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/seasons/2026/teams/{team_id}/athletes`
- **Data:** Team rosters, player details, positions
- **Cost:** FREE ✅
- **Rate Limit:** None (reasonable use)

#### ESPN Box Score API
- **Endpoint:** `https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={game_id}`
- **Data:** Live stats, box scores, player performance
- **Cost:** FREE ✅
- **Rate Limit:** None (reasonable use)

---

### 2. The Odds API (OPTIONAL - Best for Betting Odds)

#### Overview
- **Website:** https://the-odds-api.com/
- **Cost:** 
  - FREE tier: 500 requests/month ✅
  - Paid: Starting at $5/month for 5,000 requests
- **Data:**
  - Live betting odds from 30+ sportsbooks
  - Player props (points, rebounds, assists)
  - Game spreads, totals, moneylines
  - DraftKings, FanDuel, BetMGM, Caesars, etc.

#### Setup Instructions
1. Sign up at https://the-odds-api.com/
2. Get your free API key
3. Add to [app.py](app.py) line 16:
   ```python
   ODDS_API_KEY = "your_api_key_here"
   ```

#### Example API Calls
```python
# Get NBA odds
url = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds"
params = {
    'apiKey': YOUR_KEY,
    'regions': 'us',
    'markets': 'h2h,spreads,totals',
    'oddsFormat': 'american'
}
```

#### Supported Sports
- `basketball_nba` - NBA
- `americanfootball_nfl` - NFL
- `baseball_mlb` - MLB
- `icehockey_nhl` - NHL

---

### 3. Other Betting APIs (Alternative Options)

#### API-SPORTS (RapidAPI)
- **Website:** https://rapidapi.com/api-sports/
- **Cost:** 
  - FREE: 100 requests/day (limited)
  - Basic: $10/month
- **Data:** NBA/NFL stats, odds, standings
- **Pros:** Good documentation
- **Cons:** Rate limits on free tier

#### SportsDataIO
- **Website:** https://sportsdata.io/
- **Cost:** $0-500/month
- **Data:** Comprehensive sports data + odds
- **Pros:** Very detailed player stats
- **Cons:** Expensive for full access

#### OddsJam API
- **Website:** https://oddsjam.com/
- **Cost:** Paid only (~$50/month)
- **Data:** Real-time odds comparison
- **Pros:** Sharp line movements
- **Cons:** No free tier

---

## 📊 CURRENT APP DATA SOURCES

1. **Player Rosters:** ESPN v2 Core API (FREE) ✅
2. **Live Games/Scores:** ESPN Scoreboard API (FREE) ✅
3. **Player Stats:** ESPN Box Score API (FREE) ✅
4. **Betting Odds:** ESPN embedded odds (FREE) ✅
5. **Injury Data:** ESPN injury API (FREE) ✅

---

## 🚀 RECOMMENDED SETUP

### For Personal Use (FREE)
- Current setup is perfect
- ESPN APIs provide all needed data
- No API keys required

### For Enhanced Betting Features
1. Add The Odds API (free tier)
2. Get real-time odds from major sportsbooks
3. 500 requests = ~16 requests/day
4. Perfect for daily use

### For Commercial/High Volume
1. The Odds API paid plan ($5-50/month)
2. SportsDataIO for detailed stats
3. Multiple API keys for redundancy

---

## 🔧 TESTING YOUR APIS

### Test ESPN APIs
```bash
# NBA Scoreboard
curl "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"

# NBA Roster (v2)
curl "https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/seasons/2026/teams/8/athletes?limit=50"
```

### Test The Odds API (if enabled)
```bash
curl "https://api.the-odds-api.com/v4/sports/basketball_nba/odds?apiKey=YOUR_KEY&regions=us&markets=h2h"
```

---

## 📝 NOTES

- ESPN APIs are **free forever** and very reliable
- The Odds API free tier is **plenty for personal use**
- All APIs respect rate limits automatically in the app
- Data is cached (5 minutes) to minimize API calls
- App will work without betting API keys

---

## ✅ CHANGES MADE TODAY

1. ✅ Fixed NBA roster fetching (ESPN v2 Core API)
2. ✅ Added betting API configuration section
3. ✅ Created helper function for The Odds API
4. ✅ Documented all available APIs
5. ✅ App now shows player data correctly

**Your app should now display NBA players in the Build Parlay section!**
