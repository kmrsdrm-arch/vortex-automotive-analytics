# 🚀 VORTEX Deployment - Quick Start

**Get your app live in 15 minutes!**

---

## ✅ Pre-Flight Checklist

- [ ] Code pushed to GitHub
- [ ] Render.com account created
- [ ] OpenAI API key ready
- [ ] `.gitignore` includes `.env`, `venv/`, `logs/`

---

## 🎯 5-Step Deployment

### 1️⃣ Push to GitHub

```bash
git add .
git commit -m "Deploy VORTEX to production"
git push origin main
```

### 2️⃣ Deploy on Render.com

1. Go to [render.com](https://render.com)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repo
4. Select your repository
5. Click **"Apply"**

### 3️⃣ Add Environment Variables

When prompted, add:

```
OPENAI_API_KEY = sk-proj-your-actual-api-key-here
```

That's it! Render will automatically:
- Create PostgreSQL database
- Deploy FastAPI backend
- Deploy Streamlit dashboard
- Set up all connections

### 4️⃣ Initialize Database

After deployment completes:

1. Go to `vortex-api` service
2. Click **"Shell"** tab
3. Run:

```bash
python scripts/init_db.py
python scripts/seed_data.py
```

### 5️⃣ Test & Share

- **Dashboard**: `https://vortex-dashboard.onrender.com`
- **API Docs**: `https://vortex-api.onrender.com/docs`

⚠️ **First load takes 50-60 seconds** (free tier wakes up)

---

## 📧 Share with Hiring Manager

```
Subject: Portfolio Demo - VORTEX Automotive Intelligence Platform

Hi [Name],

I'd like to share my latest full-stack AI project:

🔗 Live Demo: https://vortex-dashboard.onrender.com
📚 API Docs: https://vortex-api.onrender.com/docs
💻 GitHub: https://github.com/YOUR_USERNAME/vortex-automotive-analytics

Tech Stack: FastAPI, Streamlit, PostgreSQL, OpenAI GPT-4

Note: First load may take 60 seconds (free tier wake-up).

Best regards,
[Your Name]
```

---

## 🔧 Common Issues

### Dashboard Can't Connect to API

**Fix**: Update CORS in API service

1. Go to `vortex-api` → **Environment**
2. Set: `API_CORS_ORIGINS = ["https://vortex-dashboard.onrender.com"]`
3. Save (auto-redeploys)

### OpenAI Errors

**Fix**: Check your API key

1. Verify at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Update in both services: `vortex-api` and `vortex-dashboard`
3. Ensure you have credits in OpenAI account

### Database Errors

**Fix**: Run initialization

```bash
python scripts/init_db.py
python scripts/seed_data.py
```

---

## 💰 Costs

**Free Tier**: $0/month
- Services sleep after 15 min
- 60s cold start
- Perfect for demos!

**Always-On**: $21/month
- No sleep
- Instant loading
- Professional use

---

## 📚 Full Guide

For detailed instructions, see **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**

---

## 🎉 You're Live!

Your portfolio project is now deployed and ready to impress! 🚀

**Pro Tips**:
- Test all features before sharing
- Take screenshots for your portfolio
- Practice explaining your architecture
- Monitor OpenAI usage to avoid surprise costs

Good luck! 💪

