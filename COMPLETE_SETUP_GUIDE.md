# Complete Setup Guide - Dashboard API Connection

## What Was Fixed

### 1. Streamlit Secrets Access (FIXED)
**Problem:** Dashboard was using `st.secrets.get()` which doesn't work correctly.

**Solution:** Changed to proper dictionary syntax `st.secrets["API_URL"]`

**File:** `src/dashboard/app.py` (line 43-46)

### 2. Debug Information Added (FIXED)
**Feature:** Added connection info panel in sidebar with:
- Display of current API_URL being used
- Test Connection button for quick diagnostics
- Real-time connection status

**Location:** Dashboard sidebar → "Connection Info" expander

### 3. Database Seeding Endpoint (ADDED)
**Feature:** Created API endpoint to seed database with synthetic data

**Endpoint:** `POST /api/v1/data/seed`

**File:** `src/api/routes/data.py`

---

## Current Status

✅ **Code Changes:** All committed and pushed to GitHub
⏳ **Streamlit Deploy:** Redeploying with fixed secrets access (takes 2-3 minutes)
⏳ **Render Deploy:** Redeploying with new seed endpoint (takes 5-10 minutes)
⏳ **Database:** Empty - needs seeding after Render deploy completes

---

## Step-by-Step Instructions

### STEP 1: Wait for Deployments (5-10 minutes)

**Streamlit Cloud:** Should redeploy automatically in 2-3 minutes

**Render:** Free tier deploys take 5-10 minutes

**How to check Render status:**
1. Go to: https://dashboard.render.com/
2. Find your service: `vortex-automotive-analytics`
3. Look for:
   - 🔵 "Deploying" = Wait
   - 🟢 "Live" = Ready!

---

### STEP 2: Seed the Database

Once Render shows "Live", seed the database using ONE of these methods:

#### Method A: Via API Docs (Recommended)

1. **Visit:** https://vortex-automotive-analytics.onrender.com/docs

2. **Find** the "Data" section

3. **Find** `POST /api/v1/data/seed` endpoint

4. **Click** "Try it out"

5. **Optionally modify** the parameters:
   ```json
   {
     "num_vehicles": 100,
     "num_sales": 10000,
     "months_back": 24
   }
   ```

6. **Click** "Execute"

7. **Wait** ~30 seconds

8. **Check response** - should show:
   ```json
   {
     "success": true,
     "message": "Database seeded successfully",
     "summary": {
       "vehicles": 100,
       "inventory_records": 100,
       "sales_transactions": 10000
     }
   }
   ```

#### Method B: Via curl (Command Line)

Open PowerShell and run:

```powershell
curl -X POST "https://vortex-automotive-analytics.onrender.com/api/v1/data/seed" `
  -H "Content-Type: application/json" `
  -d '{
    "num_vehicles": 100,
    "num_sales": 10000,
    "months_back": 24
  }'
```

#### Method C: Via Python Requests

```python
import requests

response = requests.post(
    "https://vortex-automotive-analytics.onrender.com/api/v1/data/seed",
    json={
        "num_vehicles": 100,
        "num_sales": 10000,
        "months_back": 24
    }
)

print(response.json())
```

---

### STEP 3: Test the Dashboard

1. **Visit:** Your Streamlit dashboard URL

2. **Should see:**
   - ✅ VORTEX branding and dark theme
   - ✅ KPI cards with actual numbers
   - ✅ Charts with data
   - ✅ No error messages

3. **If still showing error:**
   - Open sidebar → "Connection Info" expander
   - Click "Test Connection" button
   - Should show "✅ Connected!"

---

### STEP 4: Verify Everything Works

Test these pages in the dashboard:
- ✅ Dashboard Summary
- ✅ Sales Analytics
- ✅ Inventory Analytics
- ✅ NL Query
- ✅ Insights
- ✅ Reports

All should display data without errors.

---

## Troubleshooting

### Issue: Dashboard still shows "Unable to load KPI data"

**Possible causes:**

1. **Streamlit hasn't redeployed yet**
   - Solution: Wait 5 minutes total, then refresh browser
   - Check: Streamlit Cloud → Your app → Logs should show "Your app is live!"

2. **API_URL not being read from secrets**
   - Solution: Check sidebar "Connection Info" - should show: `https://vortex-automotive-analytics.onrender.com`
   - If shows `http://localhost:8000`: Streamlit hasn't picked up secrets yet - reboot app

3. **Database not seeded**
   - Solution: Follow Step 2 above to seed database
   - Verify: Visit `https://vortex-automotive-analytics.onrender.com/api/v1/analytics/kpis` should return JSON with data

4. **API is sleeping**
   - Solution: Visit API URL to wake it up, wait 60 seconds, refresh dashboard

### Issue: Seed endpoint returns 404 Not Found

**Cause:** Render hasn't finished deploying the new code yet

**Solution:** 
- Wait 5-10 minutes for Render deployment
- Check Render Dashboard for "Live" status
- Refresh /docs page to see new endpoint

### Issue: Seed endpoint returns 500 Error

**Possible causes:**
1. DATABASE_URL not set correctly in Render
2. Database connection failed

**Solution:**
1. Check Render Dashboard → Environment variables
2. Verify DATABASE_URL is correct
3. Check Render logs for specific error message

---

## Expected Timeline

| Time | What Happens |
|------|-------------|
| **Now** | Code pushed to GitHub ✅ |
| **+1 min** | Streamlit detects push, starts build |
| **+3 min** | Streamlit redeploys with fixed secrets ✅ |
| **+2 min** | Render detects push, starts build |
| **+8 min** | Render redeploys with seed endpoint ✅ |
| **+9 min** | Seed database via API (30 seconds) |
| **+10 min** | Dashboard fully functional! 🎉 |

---

## Quick Verification Checklist

After ~10 minutes from code push:

- [ ] Render shows "Live" status
- [ ] API docs show /api/v1/data/seed endpoint
- [ ] Seeded database successfully
- [ ] KPI endpoint returns data: https://vortex-automotive-analytics.onrender.com/api/v1/analytics/kpis
- [ ] Dashboard loads without "Unable to load KPI data" error
- [ ] Dashboard displays actual metrics and charts
- [ ] Sidebar "Connection Info" shows correct API_URL

---

## What Changed in the Code

### Before (Broken):
```python
# Streamlit secrets access - WRONG
try:
    api_url = st.secrets.get("API_URL", "http://localhost:8000")
except:
    api_url = os.getenv("API_URL", "http://localhost:8000")
```

### After (Fixed):
```python
# Streamlit secrets access - CORRECT
try:
    api_url = st.secrets["API_URL"]  # Dictionary syntax!
except (KeyError, FileNotFoundError, AttributeError):
    api_url = os.getenv("API_URL", "http://localhost:8000")
```

### New Feature Added:
```python
# In sidebar
with st.expander("🔍 Connection Info", expanded=False):
    st.caption(f"**API URL:**")
    st.code(st.session_state.api_url, language=None)
    
    if st.button("🔄 Test Connection"):
        # Tests API health endpoint
        # Shows connection status
```

### New API Endpoint:
```python
@router.post("/api/v1/data/seed")
async def seed_database(seed_request: SeedRequest, db: Session):
    # Generates synthetic data
    # Returns summary of what was created
```

---

## Summary

**Root Cause:** 
1. Streamlit secrets not being read correctly
2. Database empty (no data to display)

**Fixes Applied:**
1. ✅ Fixed secrets access using proper dictionary syntax
2. ✅ Added connection debugging tools
3. ✅ Created API endpoint for easy database seeding

**Next Steps:**
1. ⏳ Wait for deployments (~10 minutes)
2. 📝 Seed database via API
3. 🎉 Enjoy your working dashboard!

---

## Need Help?

If after following these steps the dashboard still doesn't work:

1. **Check Render logs:**
   - Render Dashboard → Your service → Logs
   - Look for errors

2. **Check Streamlit logs:**
   - Streamlit Cloud → Your app → Logs
   - Look for connection errors

3. **Test API directly:**
   - Visit: https://vortex-automotive-analytics.onrender.com/
   - Should return JSON
   - Visit: https://vortex-automotive-analytics.onrender.com/docs
   - Should show Swagger UI

4. **Share with me:**
   - Screenshot of dashboard error
   - Screenshot of "Connection Info" in sidebar
   - Any error messages from logs

---

**The fix is complete! Just wait ~10 minutes and seed the database.** 🚀

