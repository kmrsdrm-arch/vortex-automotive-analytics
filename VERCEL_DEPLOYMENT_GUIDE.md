# 🚀 VORTEX Deployment to Vercel

**Complete Guide to Deploy Your Automotive Intelligence Platform on Vercel**

---

## ⚠️ Important Notice About Vercel Deployment

Vercel is optimized for **serverless functions** and **frontend frameworks**. Your VORTEX app has:

1. **FastAPI Backend** ✅ - Can deploy as serverless functions
2. **Streamlit Dashboard** ⚠️ - Requires separate deployment (Streamlit Cloud recommended)
3. **PostgreSQL Database** ⚠️ - Requires external managed database

### Recommended Architecture:

```
┌─────────────────────┐
│ Vercel (Frontend)   │ → Static files, API routes
│ FastAPI Serverless  │
└──────────┬──────────┘
           │
           ├──→ PostgreSQL (Neon/Supabase)
           │
           └──→ Streamlit Cloud (Dashboard)
```

---

## 🎯 Deployment Strategy

### Option A: Vercel + Streamlit Cloud (Recommended) ⭐

**Best for:** Portfolio projects, easy maintenance

- **API**: Deploy FastAPI to Vercel (serverless)
- **Dashboard**: Deploy Streamlit to Streamlit Cloud (free)
- **Database**: Use Neon or Supabase (free tier)

**Pros:**
- ✅ Both services have free tiers
- ✅ Easy deployment
- ✅ Great for demos/portfolio
- ✅ Separate scaling

**Cons:**
- ⚠️ Two separate deployments
- ⚠️ Need to manage CORS

### Option B: Full Render.com (Alternative)

See `DEPLOYMENT_GUIDE.md` for full Render.com deployment.

**Better for:** All-in-one deployment, always-on services

---

## 🚀 Option A: Vercel + Streamlit Cloud Deployment

### Part 1: Deploy API to Vercel

#### Step 1: Prepare Your Code

Your code is already prepared! I've created:
- ✅ `vercel.json` - Vercel configuration
- ✅ `api/index.py` - Serverless entry point
- ✅ `requirements-vercel.txt` - Optimized dependencies

#### Step 2: Install Vercel CLI (Optional)

```bash
npm install -g vercel
```

Or deploy via GitHub integration (easier).

#### Step 3: Push to GitHub

```bash
# If not already pushed
git add .
git commit -m "Add Vercel deployment configuration"
git push origin master
```

#### Step 4: Deploy to Vercel

**Via Web (Easiest):**

1. Go to: https://vercel.com/new
2. Import your GitHub repository: `kmrsdrm-arch/vortex-automotive-analytics`
3. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty

4. Add Environment Variables:
   ```
   DATABASE_URL = postgresql://user:pass@host/db
   OPENAI_API_KEY = sk-proj-your-key
   API_HOST = 0.0.0.0
   API_PORT = 8000
   ```

5. Click **Deploy**

**Via CLI:**

```bash
vercel login
vercel --prod
```

#### Step 5: Get Your API URL

After deployment, Vercel will give you a URL like:
```
https://vortex-automotive-analytics.vercel.app
```

Your API will be available at:
```
https://vortex-automotive-analytics.vercel.app/docs
```

---

### Part 2: Setup Database (Neon - Free)

#### Why Neon?
- ✅ Free PostgreSQL database
- ✅ Serverless, scales to zero
- ✅ 3GB storage on free tier
- ✅ Perfect for Vercel

#### Steps:

1. **Sign up at Neon**
   - Go to: https://neon.tech
   - Sign up with GitHub

2. **Create Database**
   - Click "Create Project"
   - Name: `vortex-analytics`
   - Region: Choose closest to you
   - Click "Create"

3. **Get Connection String**
   - Copy the connection string shown
   - Format: `postgresql://user:pass@ep-xxx.neon.tech/vortex`

4. **Add to Vercel**
   - Go to Vercel project settings
   - Environment Variables
   - Add: `DATABASE_URL = [your-neon-connection-string]`
   - Redeploy

5. **Initialize Database**
   - You'll need to run migration scripts
   - See "Database Setup" section below

---

### Part 3: Deploy Dashboard to Streamlit Cloud

#### Step 1: Prepare Streamlit App

Create a new file `streamlit_app.py` in project root:

```python
# Redirect to the actual dashboard
import sys
sys.path.insert(0, '.')
from src.dashboard.app import *
```

#### Step 2: Create requirements.txt for Streamlit

The existing `requirements.txt` works fine.

#### Step 3: Deploy to Streamlit Cloud

1. **Sign up**:
   - Go to: https://streamlit.io/cloud
   - Sign in with GitHub

2. **Deploy App**:
   - Click "New app"
   - Repository: `kmrsdrm-arch/vortex-automotive-analytics`
   - Branch: `master`
   - Main file: `src/dashboard/app.py`

3. **Add Secrets** (Environment Variables):
   ```toml
   DATABASE_URL = "postgresql://user:pass@host/db"
   OPENAI_API_KEY = "sk-proj-your-key"
   API_URL = "https://vortex-automotive-analytics.vercel.app"
   ```

4. **Deploy**: Click "Deploy"

5. **Your Dashboard URL**:
   ```
   https://vortex-dashboard.streamlit.app
   ```

---

### Part 4: Update CORS Settings

Update your API to allow the Streamlit dashboard:

In `src/api/main.py`, update CORS origins:

```python
api_cors_origins: List[str] = [
    "http://localhost:8501",
    "https://vortex-dashboard.streamlit.app",
    "https://*.streamlit.app"  # Allow all Streamlit apps
]
```

Or add as environment variable in Vercel:
```
API_CORS_ORIGINS = ["https://vortex-dashboard.streamlit.app"]
```

Redeploy Vercel for changes to take effect.

---

## 🗄️ Database Setup

After deploying API and database, initialize it:

### Option 1: Run Locally Against Neon

```bash
# Set environment variable
$env:DATABASE_URL="postgresql://user:pass@ep-xxx.neon.tech/vortex"

# Run migrations
python scripts/init_db.py
python scripts/seed_data.py
```

### Option 2: Use Vercel CLI

```bash
# Run command on Vercel
vercel env pull
python scripts/init_db.py
```

---

## 💰 Cost Breakdown

### Free Tier (Perfect for Portfolio)

**Vercel:**
- ✅ 100GB bandwidth/month
- ✅ Serverless function executions
- ✅ Automatic HTTPS
- ✅ Custom domain support

**Streamlit Cloud:**
- ✅ 1 private app (or unlimited public)
- ✅ 1GB RAM
- ✅ Community support

**Neon:**
- ✅ 3GB storage
- ✅ 1 project
- ✅ Scales to zero (no idle cost)

**Total: $0/month** 🎉

---

## 🎯 Deployment Checklist

### API (Vercel)
- [ ] Code pushed to GitHub
- [ ] Vercel account created
- [ ] Project imported from GitHub
- [ ] Environment variables added
- [ ] API deployed successfully
- [ ] Test: `/docs` endpoint works

### Database (Neon)
- [ ] Neon account created
- [ ] Database created
- [ ] Connection string copied
- [ ] Added to Vercel env vars
- [ ] Database initialized
- [ ] Sample data seeded

### Dashboard (Streamlit Cloud)
- [ ] Streamlit Cloud account created
- [ ] App deployed from GitHub
- [ ] Secrets (env vars) added
- [ ] Dashboard loads successfully
- [ ] Can connect to Vercel API

### Final Testing
- [ ] Dashboard loads
- [ ] KPIs display correctly
- [ ] Charts render
- [ ] Natural language query works
- [ ] No CORS errors

---

## 🔧 Troubleshooting

### API Issues

**Error: Module not found**
- Check `vercel.json` configuration
- Ensure all dependencies in `requirements-vercel.txt`

**Error: Database connection failed**
- Verify DATABASE_URL is correct
- Check Neon database is active
- Test connection locally first

**Error: Cold start timeout**
- Vercel serverless has 10s timeout on free tier
- Optimize imports
- Consider caching

### Dashboard Issues

**Error: Can't connect to API**
- Check API_URL in Streamlit secrets
- Verify CORS settings in API
- Test API endpoint directly

**Error: OpenAI API failed**
- Check OPENAI_API_KEY in Streamlit secrets
- Verify account has credits
- Test with simple query first

---

## 📧 Sharing Your Deployed App

Once deployed, share:

```
Subject: Portfolio Demo - VORTEX Automotive Intelligence Platform

Hi [Hiring Manager],

I'd like to share my full-stack AI project deployed on modern cloud platforms:

🔗 Live Dashboard: https://vortex-dashboard.streamlit.app
📚 API Documentation: https://vortex-automotive-analytics.vercel.app/docs
💻 Source Code: https://github.com/kmrsdrm-arch/vortex-automotive-analytics

Architecture:
• Frontend: Streamlit Cloud (Dashboard)
• Backend: Vercel (FastAPI Serverless)
• Database: Neon (PostgreSQL)
• AI: OpenAI GPT-4

Tech Stack: Python | FastAPI | Streamlit | PostgreSQL | OpenAI

Best regards,
[Your Name]
```

---

## 🚀 Quick Start Summary

```bash
# 1. Push code to GitHub
git push origin master

# 2. Deploy API to Vercel
# → https://vercel.com/new
# → Import GitHub repo
# → Add environment variables
# → Deploy

# 3. Setup Database (Neon)
# → https://neon.tech
# → Create project
# → Copy connection string
# → Add to Vercel

# 4. Deploy Dashboard (Streamlit Cloud)
# → https://streamlit.io/cloud
# → New app from GitHub
# → Add secrets
# → Deploy

# 5. Initialize Database
python scripts/init_db.py
python scripts/seed_data.py

# 6. Test and share!
```

---

## 🆘 Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **Streamlit Docs**: https://docs.streamlit.io/streamlit-cloud
- **Neon Docs**: https://neon.tech/docs

---

## 🎉 Success!

Your VORTEX platform is now deployed on modern cloud infrastructure!

**Your URLs:**
- Dashboard: `https://vortex-dashboard.streamlit.app`
- API: `https://vortex-automotive-analytics.vercel.app`
- GitHub: `https://github.com/kmrsdrm-arch/vortex-automotive-analytics`

Ready to impress hiring managers! 🚀

