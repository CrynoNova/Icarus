# 🆓 Free Betting API Quick Setup Guide

## Overview
This app now supports **3 completely free betting APIs** to get real DraftKings, FanDuel, and other sportsbook odds. All have generous free tiers requiring NO credit card.

---

## 🎯 Option 1: The Odds API (RECOMMENDED)

### Why Use This?
- ⭐ **Best coverage** - DraftKings, FanDuel, BetMGM, Caesars, and 30+ books
- 📊 **Player props included** - Points, rebounds, assists, passing yards, etc.
- 🆓 **500 free requests/month** - Plenty for personal use
- 📖 **Best documentation** - Easy to integrate

### Setup Steps:
1. Visit https://the-odds-api.com/
2. Click "Get Started" or "Sign Up"
3. Create free account (email + password)
4. Dashboard will show your API key
5. Copy your API key

### Enable in App:
```python
# Open app.py, find line 20, replace:
ODDS_API_KEY = None

# With:
ODDS_API_KEY = "your_actual_api_key_here"
```

### What You Get:
- Real-time odds from multiple sportsbooks
- Player prop lines (Over/Under points, assists, etc.)
- Spread, moneyline, totals for all games
- Live odds updates

### API Usage:
- **500 requests/month** = ~16 requests/day
- Each sport check = 1 request
- Recommended: Enable for special events or when building parlays
- App caches responses for 5 minutes to save requests

---

## 🔄 Option 2: Odds-API.com (Alternative)

### Why Use This?
- 🆓 **100 free requests/day** - Daily limit instead of monthly
- 📊 Game odds coverage
- 🔄 Good backup option if The Odds API hits limit

### Setup Steps:
1. Visit https://odds-api.com/
2. Sign up for free account
3. Verify email
4. Go to dashboard → Copy API key

### Enable in App:
```python
# Open app.py, find line 24, replace:
ODDS_API_COM_KEY = None

# With:
ODDS_API_COM_KEY = "your_actual_api_key_here"
```

### What You Get:
- Game odds from multiple books
- Spreads, moneylines, totals
- Good for team-based betting

### API Usage:
- **100 requests/day** (resets daily at midnight UTC)
- Each sport/league check = 1 request

---

## ⚡ Option 3: RapidAPI Sports Odds (Backup)

### Why Use This?
- 🆓 **100 requests/day** on free tier
- 🔄 Third backup option
- 🌐 Part of RapidAPI ecosystem (access to 1000s of APIs)

### Setup Steps:
1. Visit https://rapidapi.com/
2. Sign up for free account
3. Search for "sports odds" or "american football odds"
4. Subscribe to FREE plan
5. Copy your RapidAPI key from dashboard

### Enable in App:
```python
# Open app.py, find line 28, replace:
RAPIDAPI_KEY = None

# With:
RAPIDAPI_KEY = "your_rapidapi_key_here"
```

### What You Get:
- Basic odds data
- Multiple sports coverage
- Good tertiary fallback

---

## 🔄 API Priority Order

The app tries APIs in this order:

```
1. The Odds API (if key set) → Best quality, player props
2. Odds-API.com (if key set) → Good game odds
3. RapidAPI (if key set) → Basic backup
4. ESPN APIs (always free) → Season stats, live data
5. Database (always available) → Curated season averages
6. None → Shows "data unavailable" (NO FAKE DATA)
```

**You only need ONE API** - The Odds API is recommended.

---

## 💡 Recommended Setup

### For Most Users:
Just enable **The Odds API** (500/month is plenty)

### For Heavy Users:
Enable all 3 APIs for redundancy:
- The Odds API: 500/month
- Odds-API.com: 100/day = 3,000/month
- RapidAPI: 100/day = 3,000/month
- **Total: 6,500 free requests/month!**

---

## 🧪 Testing Your Setup

### After adding API keys:

1. **Restart the app** (stop and run again)
2. Go to **Auto-Build tab**
3. Check API status indicators:
   - ✅ Green = API enabled and working
   - ⚪ Gray = API not configured
   - ❌ Red = API configured but failing

4. **Test build a parlay:**
   - Select sports
   - Click "Auto Build Parlay"
   - Props should now use real sportsbook lines

### Verify Real Odds:
Look for these indicators in prop details:
- "DraftKings line: -110"
- "FanDuel Over 25.5"
- Real odds like +150, -120, etc.

---

## 📊 Without APIs (Current State)

**The app still works perfectly without any API keys!**

### What You Get:
- ✅ **ESPN season stats** (real player averages)
- ✅ **ESPN live data** (real-time game stats)
- ✅ **Curated database** (verified season stats)
- ✅ **Probability calculations** (based on real averages)

### What You're Missing:
- ❌ Real sportsbook odds (DraftKings/FanDuel specific lines)
- ❌ Live betting line movements
- ❌ Book-specific props

**BUT:** The app NEVER shows fake data. If data unavailable, it clearly says so.

---

## 🔐 Security Notes

### API Keys Are Safe:
- Stored locally in your `app.py` file
- Not shared or transmitted anywhere except to the API provider
- Free tier keys have limited permissions (read-only odds data)
- Can be revoked/regenerated anytime from provider dashboard

### Best Practices:
1. **Don't commit to GitHub** - Add `app.py` to `.gitignore` if sharing code
2. **Use environment variables** for production:
   ```python
   import os
   ODDS_API_KEY = os.environ.get('ODDS_API_KEY', None)
   ```
3. **Monitor usage** in API provider dashboards
4. **Regenerate keys** if accidentally exposed

---

## 🆘 Troubleshooting

### "API Error" or "Failed to fetch"
- ✅ Double-check API key (no extra spaces)
- ✅ Verify key is within quotes: `"abc123"`
- ✅ Check API provider dashboard - key active?
- ✅ Haven't exceeded free tier limit?

### "No data available" despite API enabled
- ✅ API might not have data for that specific game/player yet
- ✅ Check closer to game time (props posted 24-48h before)
- ✅ Some sports have limited prop coverage

### API Not Showing as Enabled (⚪ instead of ✅)
- ✅ Restart app after adding key
- ✅ Check syntax: `ODDS_API_KEY = "key_here"` not `=None`
- ✅ Make sure you saved app.py

---

## 💰 Cost Comparison

### Free Tier (What You Get):
| Provider | Free Requests | Cost |
|----------|---------------|------|
| The Odds API | 500/month | $0 |
| Odds-API.com | 100/day | $0 |
| RapidAPI | 100/day | $0 |
| ESPN APIs | Unlimited | $0 |
| **TOTAL** | **6,500+/month** | **$0** |

### If You Need More:
| Provider | Paid Plan | Cost |
|----------|-----------|------|
| The Odds API | 10,000/month | $50/mo |
| The Odds API | 100,000/month | $500/mo |
| Odds-API.com | Unlimited | ~$99/mo |

**For personal parlay building, free tiers are more than enough!**

---

## 📈 Monitoring Usage

### The Odds API:
- Dashboard: https://the-odds-api.com/account
- Shows: Requests used, requests remaining, reset date
- Email alerts when approaching limit

### Odds-API.com:
- Dashboard on their website
- Daily usage counter
- Resets at midnight UTC

### RapidAPI:
- Dashboard: https://rapidapi.com/developer/billing
- Shows all API usage across RapidAPI
- Monthly billing cycle

---

## 🎯 Summary

**Recommendation:** Just enable The Odds API first

1. Sign up at https://the-odds-api.com/ (2 minutes)
2. Copy API key
3. Paste into line 20 of app.py
4. Restart app
5. Enjoy real DraftKings/FanDuel odds!

**Free tier = 500 requests/month = plenty for personal use**

If you ever hit the limit, enable the other 2 APIs for 6,500+ free requests/month total.

**Remember:** App works great even without APIs using ESPN data!
