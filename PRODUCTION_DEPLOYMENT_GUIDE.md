# 🚀 Production Deployment Guide - Vortex Automotive Analytics

## Overview

This guide will help you deploy the Vortex Automotive Analytics platform to production on Render.com (free tier).

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PRODUCTION STACK                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────┐  │
│  │   FastAPI    │◄────►│  PostgreSQL  │◄────►│ Render   │  │
│  │   Backend    │      │   Database   │      │ Platform │  │
│  └──────────────┘      └──────────────┘      └──────────┘  │
│         ▲                                                    │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐                                           │
│  │  Streamlit   │                                           │
│  │  Dashboard   │                                           │
│  └──────────────┘                                           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Prerequisites

1. **GitHub Account** (free)
2. **Render Account** (free) - https://render.com
3. **OpenAI API Key** - https://platform.openai.com/api-keys
4. **Git** installed locally

## 📋 Step-by-Step Deployment

### Step 1: Prepare Your Code

1. **Push code to GitHub**:
```bash
cd c:\Users\admin\Documents\Development\LLM\cursor
git add .
git commit -m "Production ready deployment"
git push origin main
```

### Step 2: Deploy Database on Render

1. Go to https://dashboard.render.com
2. Click **"New"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `vortex-db`
   - **Database**: `vortex_analytics`
   - **User**: `vortex_user`
   - **Region**: `Oregon (US West)`
   - **Plan**: `Free`
4. Click **"Create Database"**
5. Wait for database to be created (~2 minutes)
6. **Copy the "Internal Database URL"** - you'll need this!

### Step 3: Deploy FastAPI Backend on Render

1. Click **"New"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   
   **Basic Settings**:
   - **Name**: `vortex-api`
   - **Region**: `Oregon (US West)`
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     pip install --upgrade pip && pip install -r requirements.txt && python init_production_db.py
     ```
   - **Start Command**:
     ```bash
     uvicorn src.api.main:app --host 0.0.0.0 --port $PORT --workers 2
     ```
   - **Plan**: `Free`

   **Environment Variables** (click "Add Environment Variable"):
   - `DATABASE_URL` = (paste the Internal Database URL from Step 2)
   - `OPENAI_API_KEY` = (paste your OpenAI API key)
   - `PYTHON_VERSION` = `3.11.0`
   - `DEBUG` = `false`
   - `LOG_LEVEL` = `INFO`
   - `ENABLE_RAG` = `true`
   - `API_CORS_ORIGINS` = `["*"]`

4. Click **"Create Web Service"**
5. Wait for deployment (~5-10 minutes)
6. Your API will be available at: `https://vortex-api.onrender.com`

### Step 4: Verify API Deployment

1. Once deployed, visit: `https://vortex-api.onrender.com/health`
2. You should see:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-11-26T..."
}
```

3. Visit API documentation: `https://vortex-api.onrender.com/docs`

### Step 5: Seed the Database

**Method 1: Using PowerShell (Recommended)**

```powershell
# Replace YOUR-API-URL with your actual Render API URL
$apiUrl = "https://vortex-api.onrender.com"

# Test connection first
Invoke-RestMethod -Uri "$apiUrl/health" -Method Get

# Seed database with sample data
$body = @{
    num_vehicles = 100
    num_sales = 10000
    months_back = 24
} | ConvertTo-Json

Invoke-RestMethod -Uri "$apiUrl/api/v1/data/seed" -Method Post -ContentType "application/json" -Body $body
```

**Method 2: Using API Docs (Alternative)**

1. Go to: `https://vortex-api.onrender.com/docs`
2. Find `/api/v1/data/seed` endpoint
3. Click **"Try it out"**
4. Use these parameters:
   ```json
   {
     "num_vehicles": 100,
     "num_sales": 10000,
     "months_back": 24
   }
   ```
5. Click **"Execute"**
6. Wait for completion (~30-60 seconds)
7. Should return:
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

### Step 6: Deploy Streamlit Dashboard (Optional)

1. Click **"New"** → **"Web Service"**
2. Connect same GitHub repository
3. Configure:
   - **Name**: `vortex-dashboard`
   - **Region**: `Oregon (US West)`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run src/dashboard/app.py --server.port=$PORT --server.address=0.0.0.0`
   - **Plan**: `Free`

   **Environment Variables**:
   - `API_URL` = `https://vortex-api.onrender.com`

4. Click **"Create Web Service"**

## ⚠️ Important Notes for Free Tier

### 1. **Cold Starts**
- Free tier services sleep after 15 minutes of inactivity
- First request after sleep takes ~30-60 seconds
- **Solution**: Visit your API URL to wake it up before using

### 2. **Database Connection Limits**
- Free PostgreSQL allows 100 connections
- Our pool size is set to 10 (safe for free tier)
- If you get "too many connections" error, restart the web service

### 3. **Build Time**
- Initial deployment takes 5-10 minutes
- Database initialization runs during build
- Check build logs for any errors

## 🧪 Testing Your Deployment

### Test 1: Health Check
```powershell
Invoke-RestMethod -Uri "https://YOUR-API.onrender.com/health"
```

Expected output:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### Test 2: Get KPIs
```powershell
Invoke-RestMethod -Uri "https://YOUR-API.onrender.com/api/analytics/kpis?days=30"
```

Expected: JSON with revenue, units sold, conversion rate, etc.

### Test 3: Get Sales Analytics
```powershell
Invoke-RestMethod -Uri "https://YOUR-API.onrender.com/api/analytics/sales?days=30"
```

Expected: JSON with sales trends and top vehicles

## 🐛 Troubleshooting

### Issue: "500 Internal Server Error" on seed endpoint

**Possible Causes**:
1. Database tables not created
2. Database connection lost
3. Not enough memory

**Solution**:
```bash
# Check logs on Render dashboard
# Look for the build logs to see if init_production_db.py ran successfully
# If not, trigger a manual deploy
```

### Issue: "Database connection failed"

**Solution**:
1. Go to Render dashboard
2. Check if PostgreSQL database is running
3. Verify DATABASE_URL environment variable is set correctly
4. Restart the web service

### Issue: "OpenAI API validation failed"

**Solution**:
1. Verify your OpenAI API key is valid
2. Check you have available credits: https://platform.openai.com/usage
3. Update OPENAI_API_KEY environment variable on Render
4. Redeploy the service

### Issue: API is very slow

**Cause**: Free tier service was sleeping

**Solution**:
1. Visit your API URL to wake it up
2. Wait 30-60 seconds
3. Try your request again

### Issue: "Too many connections" error

**Solution**:
```bash
# Restart web service from Render dashboard
# Or reduce DB_POOL_SIZE environment variable to 5
```

## 📊 Monitoring

### View Logs
1. Go to Render dashboard
2. Click on your service (vortex-api)
3. Click "Logs" tab
4. Watch real-time logs

### Check Metrics
1. Click "Metrics" tab
2. Monitor:
   - Response time
   - Memory usage
   - CPU usage
   - Request count

## 🔄 Updating Your Deployment

### Option 1: Auto-deploy (Recommended)
1. Enable "Auto-Deploy" in Render dashboard
2. Every push to `main` branch triggers a new deployment

### Option 2: Manual Deploy
1. Push changes to GitHub
2. Go to Render dashboard
3. Click "Manual Deploy" → "Deploy latest commit"

## 🎨 Accessing Your Application

- **API**: `https://vortex-api.onrender.com`
- **API Docs**: `https://vortex-api.onrender.com/docs`
- **Health Check**: `https://vortex-api.onrender.com/health`
- **Dashboard**: `https://vortex-dashboard.onrender.com` (if deployed)

## ✅ Production Checklist

- [ ] GitHub repository is up to date
- [ ] PostgreSQL database created on Render
- [ ] FastAPI backend deployed successfully
- [ ] DATABASE_URL environment variable set
- [ ] OPENAI_API_KEY environment variable set
- [ ] Health check returns 200 OK
- [ ] Database seeded with sample data
- [ ] API documentation accessible at /docs
- [ ] All KPI endpoints returning data
- [ ] Dashboard connected to API (if deployed)

## 🚀 Next Steps

1. **Test all endpoints** using the API documentation
2. **Monitor logs** for any errors
3. **Set up alerts** (optional, paid feature)
4. **Configure custom domain** (optional)
5. **Enable HTTPS** (automatic on Render)

## 📝 Support

If you encounter any issues:
1. Check the logs on Render dashboard
2. Review this troubleshooting guide
3. Check database connection status
4. Verify all environment variables are set correctly

## 🎉 Success!

Your Vortex Automotive Analytics platform is now live in production! 🚗💨

---

**Built with**: FastAPI • Streamlit • PostgreSQL • OpenAI GPT-4 • Render.com

