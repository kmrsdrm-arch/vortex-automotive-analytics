# 🚀 VORTEX Deployment Guide - Render.com

**Complete Step-by-Step Guide to Deploy Your Automotive Intelligence Platform**

Share your amazing dashboard with hiring managers in just 15 minutes! 🎯

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Deployment Steps](#deployment-steps)
- [Post-Deployment Setup](#post-deployment-setup)
- [Sharing with Hiring Managers](#sharing-with-hiring-managers)
- [Troubleshooting](#troubleshooting)
- [Cost & Free Tier](#cost--free-tier)

---

## ✅ Prerequisites

Before you begin, make sure you have:

1. **GitHub Account** - To host your code repository
2. **Render.com Account** - Sign up for free at [render.com](https://render.com)
3. **OpenAI API Key** - Get from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
4. **Your Code Ready** - Committed and pushed to GitHub

---

## 🚀 Deployment Steps

### Step 1: Prepare Your GitHub Repository

1. **Initialize Git (if not already done)**

```bash
cd c:\Users\admin\Documents\Development\LLM\cursor
git init
```

2. **Create a `.gitignore` file** (if not exists)

```
venv/
__pycache__/
*.pyc
.env
logs/
data/chromadb/
*.log
.DS_Store
```

3. **Commit and Push to GitHub**

```bash
git add .
git commit -m "Prepare VORTEX for production deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/vortex-automotive-analytics.git
git push -u origin main
```

> **Note**: Replace `YOUR_USERNAME` with your actual GitHub username

---

### Step 2: Deploy to Render.com

#### Option A: Deploy via Blueprint (Recommended) ⭐

1. **Log in to Render.com**
   - Go to [render.com](https://render.com)
   - Sign in or create an account

2. **Create New Blueprint**
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Select the repository: `vortex-automotive-analytics`
   - Render will automatically detect `render.yaml`

3. **Configure Environment Variables**
   - Render will prompt you for required environment variables
   - Add your **OPENAI_API_KEY**:
     ```
     OPENAI_API_KEY=sk-proj-your-actual-key-here
     ```

4. **Deploy**
   - Click "Apply"
   - Render will create:
     - PostgreSQL Database (`vortex-db`)
     - FastAPI Backend (`vortex-api`)
     - Streamlit Dashboard (`vortex-dashboard`)
   - Wait 5-10 minutes for deployment to complete

#### Option B: Manual Deployment (Alternative)

If Blueprint doesn't work, deploy services individually:

##### 2.1. Deploy PostgreSQL Database

1. Click "New +" → "PostgreSQL"
2. Configure:
   - **Name**: `vortex-db`
   - **Database**: `vortex_analytics`
   - **User**: `vortex_user`
   - **Region**: `Oregon (US West)`
   - **Plan**: `Free`
3. Click "Create Database"
4. **Save the Internal Database URL** (you'll need it)

##### 2.2. Deploy FastAPI Backend

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `vortex-api`
   - **Region**: `Oregon (US West)`
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free`

4. **Add Environment Variables**:
   ```
   DATABASE_URL = [Use internal database URL from Step 2.1]
   OPENAI_API_KEY = sk-proj-your-actual-key-here
   DEBUG = false
   LOG_LEVEL = INFO
   ENABLE_RAG = true
   ```

5. Click "Create Web Service"

##### 2.3. Deploy Streamlit Dashboard

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `vortex-dashboard`
   - **Region**: `Oregon (US West)`
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: 
     ```
     streamlit run src/dashboard/app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true --browser.serverAddress 0.0.0.0 --server.enableCORS false
     ```
   - **Plan**: `Free`

4. **Add Environment Variables**:
   ```
   DATABASE_URL = [Use internal database URL from Step 2.1]
   OPENAI_API_KEY = sk-proj-your-actual-key-here
   API_URL = https://vortex-api.onrender.com
   ```
   > **Important**: Replace `vortex-api.onrender.com` with your actual API service URL from Step 2.2

5. Click "Create Web Service"

---

### Step 3: Initialize Database

After all services are deployed:

1. **Access the API Service Shell**
   - Go to your `vortex-api` service
   - Click "Shell" tab
   - Run initialization commands:

```bash
python scripts/init_db.py
python scripts/seed_data.py
```

2. **Verify Database**
   - Check that tables are created
   - Sample data should be loaded

---

### Step 4: Update CORS Settings (Important!)

1. **Get Your Dashboard URL**
   - From Render dashboard, copy your `vortex-dashboard` URL
   - Example: `https://vortex-dashboard.onrender.com`

2. **Update API CORS Settings**
   - Go to `vortex-api` service
   - Click "Environment" tab
   - Add/Update:
     ```
     API_CORS_ORIGINS = ["https://vortex-dashboard.onrender.com"]
     ```
   - Click "Save Changes"
   - Service will auto-redeploy

---

## 🎯 Post-Deployment Setup

### Verify Deployment

1. **Test API**
   - Visit: `https://vortex-api.onrender.com/docs`
   - You should see the FastAPI Swagger documentation
   - Try the `/health` endpoint

2. **Test Dashboard**
   - Visit: `https://vortex-dashboard.onrender.com`
   - Dashboard should load with the VORTEX logo
   - Check that KPIs and charts display correctly

### First Time Load

> ⚠️ **Important**: Free tier services sleep after 15 minutes of inactivity
> - First load may take 50-60 seconds to wake up
> - Subsequent loads will be much faster
> - This is normal for Render.com free tier

---

## 📧 Sharing with Hiring Managers

### Professional Email Template

```
Subject: Portfolio Project - VORTEX Automotive Intelligence Platform

Dear [Hiring Manager Name],

I'm excited to share my latest project with you - VORTEX, an AI-powered 
Automotive Analytics & Intelligence Platform.

🔗 Live Dashboard: https://vortex-dashboard.onrender.com
📚 API Documentation: https://vortex-api.onrender.com/docs
💻 Source Code: https://github.com/YOUR_USERNAME/vortex-automotive-analytics

Key Features:
✅ Full-stack application (FastAPI + Streamlit)
✅ PostgreSQL database with SQLAlchemy ORM
✅ OpenAI GPT-4 integration for AI insights
✅ Natural language query interface
✅ Real-time analytics dashboard with interactive charts
✅ Professional dark theme UI/UX
✅ Deployed on Render.com with CI/CD

Tech Stack:
- Backend: FastAPI, Python 3.11, SQLAlchemy
- Frontend: Streamlit, Plotly
- Database: PostgreSQL
- AI/ML: OpenAI GPT-4, ChromaDB, LangChain
- Deployment: Render.com, Docker

Note: First load may take 50-60 seconds as the free-tier services wake up.

I'd love to discuss the project and my approach to building production-ready 
applications.

Best regards,
[Your Name]
```

### What to Highlight

1. **Full-Stack Skills**
   - Backend API development
   - Frontend dashboard creation
   - Database design & management

2. **AI/ML Integration**
   - OpenAI API integration
   - Natural language processing
   - Vector embeddings with ChromaDB

3. **Production Readiness**
   - Environment configuration
   - Error handling & logging
   - API documentation
   - Deployment & DevOps

4. **Best Practices**
   - Clean code architecture
   - Type hints & validation (Pydantic)
   - RESTful API design
   - Responsive UI/UX

---

## 🔧 Troubleshooting

### Issue: Dashboard Can't Connect to API

**Symptoms**: Dashboard shows "Unable to load KPI data" errors

**Solution**:
1. Check that `API_URL` environment variable is set correctly in dashboard service
2. Verify API service is running: visit `https://vortex-api.onrender.com/docs`
3. Check CORS settings in API service include dashboard URL

### Issue: OpenAI API Errors

**Symptoms**: "401 Unauthorized" or API key errors

**Solution**:
1. Verify API key is valid at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Check environment variable `OPENAI_API_KEY` is set in both services
3. Ensure key starts with `sk-proj-` (project key) or `sk-` (legacy)
4. Check you have credits in your OpenAI account

### Issue: Database Connection Errors

**Symptoms**: "Could not connect to database" errors

**Solution**:
1. Check database service is running in Render dashboard
2. Verify `DATABASE_URL` is set correctly in both services
3. Use the **internal** database URL for connections
4. Run initialization scripts if tables don't exist

### Issue: Services Keep Sleeping

**Symptom**: Slow first load every time

**This is Normal**: Free tier services sleep after 15 minutes of inactivity

**Solutions**:
- Upgrade to paid plan ($7/month) for always-on services
- Use a cron job or uptime monitor to ping your service
- Accept the delay as normal for free tier

### Issue: Deployment Failed

**Check these**:
1. Verify `requirements.txt` has all dependencies
2. Check build logs for specific errors
3. Ensure Python version is 3.11+
4. Verify all import paths are correct

---

## 💰 Cost & Free Tier

### Render.com Free Tier Includes:

- ✅ **750 hours/month** of service uptime (enough for 1 service always-on)
- ✅ **PostgreSQL** database (90-day expiration, auto-renewed with activity)
- ✅ **100GB bandwidth/month**
- ⚠️ Services sleep after 15 minutes of inactivity
- ⚠️ 50-60 second cold start time

### For Production/Always-On:

- **Starter Plan**: $7/month per service
  - Always on (no sleeping)
  - 400 build minutes/month
  - 100GB bandwidth
  
**Total for VORTEX**: $14/month (API + Dashboard) + $7/month (Database) = **$21/month**

### OpenAI Costs:

- GPT-3.5-Turbo: ~$0.001 per query
- GPT-4-Turbo: ~$0.01 per query
- Expected: $5-10/month for demo/portfolio use

---

## 🎉 Success!

Your VORTEX platform is now live and ready to impress hiring managers!

### Quick Links:

- 🌐 **Dashboard**: `https://vortex-dashboard.onrender.com`
- 📊 **API Docs**: `https://vortex-api.onrender.com/docs`
- 💾 **Database**: Managed by Render
- 🔑 **API Keys**: Securely stored as environment variables

### Next Steps:

1. ✅ Test all features thoroughly
2. ✅ Take screenshots for your portfolio
3. ✅ Update your resume/LinkedIn
4. ✅ Send the link to hiring managers
5. ✅ Practice explaining your architecture and decisions

---

## 📚 Additional Resources

- **Render.com Docs**: [docs.render.com](https://docs.render.com)
- **Streamlit Deployment**: [docs.streamlit.io/deploy](https://docs.streamlit.io/deploy)
- **FastAPI Deployment**: [fastapi.tiangolo.com/deployment](https://fastapi.tiangolo.com/deployment)
- **OpenAI Best Practices**: [platform.openai.com/docs/guides](https://platform.openai.com/docs/guides)

---

## 🆘 Need Help?

If you encounter issues:

1. Check Render service logs (Logs tab in each service)
2. Review this troubleshooting guide
3. Check GitHub Issues for similar problems
4. Render Community: [community.render.com](https://community.render.com)

---

## 🎊 Congratulations!

You've successfully deployed a production-ready, full-stack AI application!

This demonstrates:
- ✅ Full-stack development skills
- ✅ AI/ML integration expertise
- ✅ DevOps & deployment knowledge
- ✅ Production-ready code practices

**You're ready to impress! 🚀**

---

*Last Updated: November 2025*
*VORTEX - Automotive Intelligence Platform v2.0*

