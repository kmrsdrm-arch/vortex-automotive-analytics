# ✅ VORTEX Deployment Checklist

Use this checklist to ensure a smooth deployment to production.

---

## 📋 Pre-Deployment

### Code Preparation

- [ ] All code committed to local Git repository
- [ ] `.gitignore` includes:
  - [ ] `.env`
  - [ ] `venv/`
  - [ ] `__pycache__/`
  - [ ] `logs/`
  - [ ] `data/chromadb/`
- [ ] `requirements.txt` is up-to-date
- [ ] Remove any hardcoded secrets or API keys
- [ ] Test application locally:
  - [ ] API runs on `http://localhost:8000`
  - [ ] Dashboard runs on `http://localhost:8501`
  - [ ] All features work correctly

### Account Setup

- [ ] GitHub account created
- [ ] GitHub repository created (public or private)
- [ ] Render.com account created (free tier OK)
- [ ] OpenAI account with valid API key
- [ ] OpenAI account has credits (check at [platform.openai.com/account/billing](https://platform.openai.com/account/billing))

---

## 🚀 Deployment Steps

### Step 1: Push to GitHub

- [ ] Create GitHub repository
- [ ] Add remote: `git remote add origin https://github.com/YOUR_USERNAME/vortex-automotive-analytics.git`
- [ ] Push code: `git push -u origin main`
- [ ] Verify all files are on GitHub (except `.env` and ignored files)

### Step 2: Deploy to Render

#### Option A: Blueprint (Automated)

- [ ] Log in to Render.com
- [ ] Click "New +" → "Blueprint"
- [ ] Connect GitHub account
- [ ] Select your repository
- [ ] Render detects `render.yaml` ✓
- [ ] Add environment variable: `OPENAI_API_KEY`
- [ ] Click "Apply"
- [ ] Wait for deployment (5-10 minutes)

#### Option B: Manual (If Blueprint Fails)

**Database:**
- [ ] Create PostgreSQL database
- [ ] Name: `vortex-db`
- [ ] Plan: Free
- [ ] Region: Oregon (US West)
- [ ] Save internal database URL

**API Service:**
- [ ] Create Web Service
- [ ] Connect GitHub repo
- [ ] Name: `vortex-api`
- [ ] Runtime: Python 3
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
- [ ] Add environment variables:
  - [ ] `DATABASE_URL` (from database)
  - [ ] `OPENAI_API_KEY`
  - [ ] `DEBUG=false`
  - [ ] `LOG_LEVEL=INFO`
- [ ] Deploy

**Dashboard Service:**
- [ ] Create Web Service
- [ ] Connect GitHub repo
- [ ] Name: `vortex-dashboard`
- [ ] Runtime: Python 3
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `streamlit run src/dashboard/app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true --browser.serverAddress 0.0.0.0 --server.enableCORS false`
- [ ] Add environment variables:
  - [ ] `DATABASE_URL` (from database)
  - [ ] `OPENAI_API_KEY`
  - [ ] `API_URL` (from API service URL)
- [ ] Deploy

### Step 3: Initialize Database

- [ ] Go to `vortex-api` service in Render
- [ ] Click "Shell" tab
- [ ] Run: `python scripts/init_db.py`
- [ ] Run: `python scripts/seed_data.py`
- [ ] Verify success messages

### Step 4: Configure CORS

- [ ] Copy dashboard URL from Render
- [ ] Go to `vortex-api` → Environment
- [ ] Add/Update: `API_CORS_ORIGINS=["https://vortex-dashboard.onrender.com"]`
- [ ] Save changes (auto-redeploys)

---

## 🧪 Testing

### API Testing

- [ ] Visit: `https://vortex-api.onrender.com/docs`
- [ ] Swagger UI loads correctly
- [ ] Test `/health` endpoint
- [ ] Test `/api/v1/analytics/kpis` endpoint
- [ ] Verify data returns successfully

### Dashboard Testing

- [ ] Visit: `https://vortex-dashboard.onrender.com`
- [ ] Wait for cold start (50-60 seconds on first load)
- [ ] VORTEX logo displays
- [ ] KPI metrics load
- [ ] Charts render correctly
- [ ] Test date range filter
- [ ] Navigate to all pages:
  - [ ] Dashboard Summary
  - [ ] Sales Analytics
  - [ ] Inventory Analytics
  - [ ] NL Query
  - [ ] Insights
  - [ ] Reports

### Feature Testing

- [ ] **Sales Analytics**: Charts display with data
- [ ] **Inventory Analytics**: Stock levels show correctly
- [ ] **Natural Language Query**: Try "Show me top 5 selling vehicles"
- [ ] **Insights**: AI generates insights (may take 10-20 seconds)
- [ ] **Reports**: Report generates successfully

---

## 📧 Sharing Preparation

### Documentation

- [ ] Update GitHub README with:
  - [ ] Live demo links
  - [ ] Screenshots
  - [ ] Setup instructions
- [ ] Create a short demo video (optional)
- [ ] Prepare talking points about architecture

### URLs to Share

- [ ] Dashboard URL: `______________________________`
- [ ] API Docs URL: `______________________________`
- [ ] GitHub URL: `______________________________`

### Email Preparation

- [ ] Choose email template from `SHARING_TEMPLATE.md`
- [ ] Customize with your information
- [ ] Replace placeholder URLs
- [ ] Add your contact information
- [ ] Proofread

---

## 🎯 Final Checks

### Performance

- [ ] Dashboard loads within 2-3 seconds (after cold start)
- [ ] API responses < 1 second
- [ ] Charts render smoothly
- [ ] No console errors (F12 in browser)

### Presentation

- [ ] Dashboard looks professional
- [ ] No Lorem Ipsum or placeholder text
- [ ] All features demonstrate value
- [ ] Error messages are user-friendly

### Security

- [ ] No API keys visible in code or logs
- [ ] `.env` not in GitHub repository
- [ ] CORS properly configured
- [ ] API endpoints require authentication (if needed)

### Monitoring

- [ ] Check Render logs for errors
- [ ] Monitor OpenAI usage/costs
- [ ] Set up uptime monitoring (optional)

---

## 📝 Post-Deployment

### Portfolio Updates

- [ ] Add to resume
- [ ] Update LinkedIn profile
- [ ] Create LinkedIn post
- [ ] Add to portfolio website
- [ ] Update GitHub profile README

### Interview Preparation

- [ ] Practice explaining architecture
- [ ] Prepare for technical questions
- [ ] Know your code inside-out
- [ ] Be ready to discuss:
  - [ ] Technology choices
  - [ ] Challenges faced
  - [ ] Lessons learned
  - [ ] Future improvements

### Maintenance

- [ ] Bookmark Render dashboard
- [ ] Monitor OpenAI credit usage
- [ ] Check app weekly to keep database active
- [ ] Respond to any service alerts

---

## ⚠️ Troubleshooting Checklist

If something doesn't work:

### Dashboard Won't Load

- [ ] Check Render service status
- [ ] View service logs in Render dashboard
- [ ] Verify environment variables are set
- [ ] Check API_URL points to correct API service
- [ ] Wait 60 seconds for cold start

### API Errors

- [ ] Verify DATABASE_URL is correct
- [ ] Check OpenAI API key is valid
- [ ] View API service logs
- [ ] Test database connection
- [ ] Verify tables exist (run init script again)

### OpenAI Errors

- [ ] Verify API key at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- [ ] Check account has credits
- [ ] Confirm key starts with `sk-proj-` or `sk-`
- [ ] Test with simple query first

### CORS Errors

- [ ] Verify API_CORS_ORIGINS includes dashboard URL
- [ ] Check both services are in same region (optional)
- [ ] Clear browser cache
- [ ] Test in incognito mode

---

## 🎉 Success Criteria

Your deployment is successful when:

✅ Dashboard loads and displays all KPIs
✅ All charts render with data
✅ Natural language query works
✅ AI insights generate successfully
✅ Reports can be created
✅ API documentation is accessible
✅ No console errors
✅ URLs are shareable and work from any device

---

## 📞 Need Help?

Resources:
- **Full Guide**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Quick Start**: [DEPLOYMENT_QUICKSTART.md](DEPLOYMENT_QUICKSTART.md)
- **Render Docs**: [docs.render.com](https://docs.render.com)
- **Render Community**: [community.render.com](https://community.render.com)

---

## 🚀 You're Ready!

Once all items are checked, you're ready to share your project with hiring managers!

**Estimated Time**: 15-30 minutes
**Cost**: $0 (free tier) or $21/month (always-on)

**Good luck!** 💪

---

*Last Updated: November 2025*

