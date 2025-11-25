# Create Fresh Render Web Service - Step by Step

## Service Configuration

**Service Name:** `vortex-automotive-analytics-1`  
**Region:** Frankfurt  
**Type:** Web Service  
**Language:** Python  

---

## Step-by-Step Instructions

### Step 1: Create New Web Service

1. Go to: https://dashboard.render.com/
2. Click the **"New +"** button (top right)
3. Select **"Web Service"**

---

### Step 2: Connect Repository

1. **Connect your GitHub repository:**
   - Repository: `kmrsdrm-arch/vortex-automotive-analytics`
   - Click **"Connect"**

2. If not connected yet:
   - Click **"Connect GitHub"**
   - Authorize Render to access your repositories
   - Select the repository

---

### Step 3: Basic Configuration

Fill in these fields:

| Field | Value |
|-------|-------|
| **Name** | `vortex-automotive-analytics-1` |
| **Region** | **Frankfurt (Europe)** |
| **Branch** | `main` |
| **Root Directory** | _(leave empty)_ |
| **Environment** | **Python** |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT` |

---

### Step 4: Instance Type

Select:
- **Instance Type:** Free
- **Plan:** Free

---

### Step 5: Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these **REQUIRED** environment variables:

#### 1. DATABASE_URL
```
postgresql://neondb_owner:npg_pxDvgnhcO9WM1@ep-restless-mouse-a9mntxs3-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require
```
**(Use your actual Neon database URL)**

#### 2. OPENAI_API_KEY
```
sk-proj-YOUR_ACTUAL_API_KEY_HERE
```
**(Your OpenAI API key from https://platform.openai.com/api-keys)**

#### 3. SECRET_KEY
```
your-secret-key-here-change-this-in-production-min-32-chars
```
**(Any random string, at least 32 characters)**

#### 4. PYTHON_VERSION
```
3.11.0
```

#### 5. DEBUG
```
false
```

#### 6. LOG_LEVEL
```
INFO
```

#### 7. ENABLE_RAG
```
true
```

---

### Step 6: Advanced Settings (Optional)

**Auto-Deploy:** 
- ✅ Yes (recommended - auto-deploys when you push to GitHub)

**Pull Request Previews:**
- ❌ No (optional, uses more resources)

---

### Step 7: Create Service

1. Review all settings
2. Click **"Create Web Service"**
3. Wait 5-10 minutes for deployment

---

## Configuration Summary

Here's what you should enter in Render:

```yaml
Name: vortex-automotive-analytics-1
Region: Frankfurt (Europe)
Branch: main
Environment: Python

Build Command:
pip install -r requirements.txt

Start Command:
uvicorn src.api.main:app --host 0.0.0.0 --port $PORT

Environment Variables:
  DATABASE_URL: postgresql://neondb_owner:npg_pxDvgnhcO9WM1@ep-restless-mouse-a9mntxs3-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require
  OPENAI_API_KEY: sk-proj-YOUR_KEY_HERE
  SECRET_KEY: your-secret-key-min-32-chars
  PYTHON_VERSION: 3.11.0
  DEBUG: false
  LOG_LEVEL: INFO
  ENABLE_RAG: true
```

---

## Environment Variable Details

### DATABASE_URL
**Format:** `postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require`

**Your Neon URL:** Get this from:
1. Go to: https://console.neon.tech/
2. Select your database: `neondb`
3. Click **"Connection String"**
4. Copy the **"Connection string"** (NOT the psql command)
5. Make sure format is: `postgresql://...` (not `psql ...`)

**Correct format:**
```
postgresql://neondb_owner:npg_pxDvgnhcO9WM1@ep-restless-mouse-a9mntxs3-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### OPENAI_API_KEY
**Format:** `sk-proj-...` or `sk-...`

**Get your key:**
1. Go to: https://platform.openai.com/api-keys
2. Click **"Create new secret key"**
3. Copy the full key (starts with `sk-proj-` or `sk-`)
4. Paste into Render

### SECRET_KEY
**Any random string, minimum 32 characters**

**Example:**
```
my-super-secret-key-for-jwt-tokens-change-in-production-123
```

**Generate secure key:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

---

## After Deployment

### Step 1: Wait for Deployment
- Takes 5-10 minutes
- Watch the logs in Render dashboard
- Status should change to **"Live"** (green)

### Step 2: Verify API is Working

**Test these URLs:**

1. **Root endpoint:**
   ```
   https://vortex-automotive-analytics-1.onrender.com/
   ```
   Should return:
   ```json
   {
     "message": "Automotive Analytics API",
     "version": "2.0.0"
   }
   ```

2. **Health endpoint:**
   ```
   https://vortex-automotive-analytics-1.onrender.com/health
   ```
   Should return:
   ```json
   {
     "status": "healthy"
   }
   ```

3. **API Documentation:**
   ```
   https://vortex-automotive-analytics-1.onrender.com/docs
   ```
   Should show FastAPI Swagger UI

### Step 3: Seed the Database

Once API is live:

1. Visit: https://vortex-automotive-analytics-1.onrender.com/docs
2. Find: `POST /api/v1/data/seed` (under "Data" section)
3. Click: **"Try it out"**
4. Click: **"Execute"**
5. Wait: ~30 seconds
6. Verify: Response shows success with counts

**Or via curl:**
```bash
curl -X POST "https://vortex-automotive-analytics-1.onrender.com/api/v1/data/seed" \
  -H "Content-Type: application/json" \
  -d '{"num_vehicles": 100, "num_sales": 10000, "months_back": 24}'
```

### Step 4: Update Streamlit Dashboard

Update your Streamlit Cloud secrets:

1. Go to: https://streamlit.io/cloud
2. Find your app → **Settings** → **Secrets**
3. Update `API_URL`:
   ```toml
   API_URL = "https://vortex-automotive-analytics-1.onrender.com"
   ```
4. Click **"Save"**
5. **Reboot app**

---

## Troubleshooting

### Issue: Build fails with "No module named 'X'"

**Solution:** Check that `requirements.txt` includes the module

### Issue: "pg_config executable not found"

**Solution:** This shouldn't happen with `psycopg2-binary`. If it does:
- Check PYTHON_VERSION is set to `3.11.0`
- Verify build command uses `requirements.txt` (not a different file)

### Issue: "Database connection failed"

**Solution:** 
1. Verify DATABASE_URL format (should start with `postgresql://`)
2. Remove any `psql ` prefix
3. Remove quotes around the URL
4. Must end with `?sslmode=require`

### Issue: "OpenAI API error"

**Solution:**
1. Verify OPENAI_API_KEY is correct
2. Check API key is active at https://platform.openai.com/api-keys
3. Ensure you have API credits

### Issue: Service keeps "deploying" forever

**Solution:**
1. Check the logs for errors
2. Common issue: Wrong start command
3. Verify: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`

---

## Quick Reference Card

**Copy these values:**

```
SERVICE NAME:
vortex-automotive-analytics-1

REGION:
Frankfurt (Europe)

BUILD COMMAND:
pip install -r requirements.txt

START COMMAND:
uvicorn src.api.main:app --host 0.0.0.0 --port $PORT

ENVIRONMENT VARIABLES:
DATABASE_URL = <your_neon_postgresql_url>
OPENAI_API_KEY = <your_openai_key>
SECRET_KEY = <random_32_char_string>
PYTHON_VERSION = 3.11.0
DEBUG = false
LOG_LEVEL = INFO
ENABLE_RAG = true
```

---

## Final Checklist

Before creating the service:
- [ ] Repository connected to Render
- [ ] Name: `vortex-automotive-analytics-1`
- [ ] Region: Frankfurt
- [ ] Build command correct
- [ ] Start command correct
- [ ] All 7 environment variables added
- [ ] DATABASE_URL in correct format
- [ ] OPENAI_API_KEY is valid
- [ ] Auto-deploy enabled

After deployment:
- [ ] Status shows "Live"
- [ ] Root URL returns JSON
- [ ] /docs shows Swagger UI
- [ ] Database seeded successfully
- [ ] Streamlit dashboard updated with new API_URL
- [ ] Dashboard displays data

---

**You're ready to create the service! Follow the steps above in your Render dashboard.** 🚀

