# 🚀 Deploy VORTEX to Vercel - Quick Start

**Get your app live in 20 minutes!**

---

## 🎯 Deployment Strategy

Since VORTEX has both API and Dashboard, we'll use:

1. **Vercel** → FastAPI Backend (Serverless)
2. **Streamlit Cloud** → Dashboard UI (Free)
3. **Neon** → PostgreSQL Database (Free)

**Total Cost: $0/month** 🎉

---

## ⚡ 5-Step Deployment

### Step 1: Push Code to GitHub (2 min)

```bash
git add .
git commit -m "Add Vercel deployment configuration"
git push origin master
```

### Step 2: Deploy API to Vercel (5 min)

1. **Go to**: https://vercel.com
2. **Sign in** with GitHub
3. **Click**: "Add New" → "Project"
4. **Import**: `kmrsdrm-arch/vortex-automotive-analytics`
5. **Configure**:
   - Framework: Other
   - Leave build/output empty
6. **Add Environment Variables**:
   ```
   OPENAI_API_KEY = sk-proj-your-key-here
   DATABASE_URL = (we'll add this in Step 3)
   ```
7. **Deploy**!

**Your API URL**: `https://vortex-automotive-analytics.vercel.app`

### Step 3: Setup Database on Neon (3 min)

1. **Go to**: https://neon.tech
2. **Sign up** with GitHub
3. **Create Project**: `vortex-analytics`
4. **Copy connection string**:
   ```
   postgresql://user:pass@ep-xxx.neon.tech/vortex
   ```
5. **Add to Vercel**:
   - Vercel Dashboard → Settings → Environment Variables
   - Key: `DATABASE_URL`
   - Value: [your connection string]
   - **Save & Redeploy**

### Step 4: Initialize Database (2 min)

Run locally against Neon database:

```bash
# Set environment variable (use your Neon connection string)
$env:DATABASE_URL="postgresql://user:pass@ep-xxx.neon.tech/vortex"

# Initialize
python scripts/init_db.py
python scripts/seed_data.py
```

### Step 5: Deploy Dashboard to Streamlit Cloud (5 min)

1. **Go to**: https://streamlit.io/cloud
2. **Sign in** with GitHub
3. **Click**: "New app"
4. **Configure**:
   - Repository: `kmrsdrm-arch/vortex-automotive-analytics`
   - Branch: `master`
   - Main file: `src/dashboard/app.py`
5. **Add Secrets** (Click "Advanced settings"):
   ```toml
   DATABASE_URL = "postgresql://user:pass@ep-xxx.neon.tech/vortex"
   OPENAI_API_KEY = "sk-proj-your-key"
   API_URL = "https://vortex-automotive-analytics.vercel.app"
   ```
6. **Deploy**!

**Your Dashboard URL**: `https://vortex-dashboard.streamlit.app`

---

## 🎯 Update CORS (Important!)

After dashboard is deployed, update API CORS:

1. **Vercel Dashboard** → Your Project → Settings → Environment Variables
2. **Add**:
   ```
   API_CORS_ORIGINS = ["https://vortex-dashboard.streamlit.app"]
   ```
3. **Redeploy**: Deployments → Click "..." → Redeploy

---

## ✅ Test Your Deployment

1. **Test API**: https://vortex-automotive-analytics.vercel.app/docs
2. **Test Dashboard**: https://vortex-dashboard.streamlit.app
3. **Verify**:
   - ✅ KPIs load
   - ✅ Charts display
   - ✅ Natural language query works

---

## 📧 Share with Hiring Manager

```
Subject: Portfolio Demo - VORTEX on Modern Cloud Stack

Hi [Name],

Live Demo: https://vortex-dashboard.streamlit.app
API Docs: https://vortex-automotive-analytics.vercel.app/docs
GitHub: https://github.com/kmrsdrm-arch/vortex-automotive-analytics

Stack: Vercel + Streamlit Cloud + Neon + OpenAI GPT-4

Best,
[Your Name]
```

---

## 🆘 Troubleshooting

**API not working:**
- Check environment variables in Vercel
- View deployment logs
- Test `/health` endpoint

**Dashboard can't connect:**
- Verify API_URL in Streamlit secrets
- Check CORS settings
- Test API URL directly

**Database errors:**
- Confirm DATABASE_URL is correct
- Check Neon database is active
- Verify tables were created

---

## 📚 Full Guide

For detailed instructions, see: **VERCEL_DEPLOYMENT_GUIDE.md**

---

## 🎉 You're Live!

**Your deployed URLs:**
- 🌐 Dashboard: `https://vortex-dashboard.streamlit.app`
- 📊 API: `https://vortex-automotive-analytics.vercel.app`
- 💻 Code: `https://github.com/kmrsdrm-arch/vortex-automotive-analytics`

**Ready to impress! 🚀**

