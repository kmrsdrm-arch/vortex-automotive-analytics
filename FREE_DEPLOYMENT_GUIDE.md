# 🚀 Free Deployment Guide - Zero Cost!

Deploy your Automotive Analytics System completely **FREE** using:
- ✅ **Vercel** for FastAPI backend (already configured!)
- ✅ **Neon.tech** for PostgreSQL database
- ✅ **Streamlit Cloud** for dashboard

**Total Cost: $0/month** 🎉

---

## 📋 Prerequisites

- GitHub account (free)
- Vercel account (free - sign up with GitHub)
- Streamlit Cloud account (free - sign up with GitHub)
- Neon.tech account (free - sign up with GitHub/Google)
- OpenAI API key (you already have this)

---

## 🗄️ Step 1: Setup Free PostgreSQL Database (Neon.tech)

### Why Neon.tech?
- ✅ Free tier includes PostgreSQL database
- ✅ 512 MB storage (sufficient for this app)
- ✅ Automatic backups
- ✅ No credit card required

### Setup Instructions:

1. **Go to** https://neon.tech
2. **Click** "Sign Up" (use your GitHub account)
3. **Create New Project:**
   - Project Name: `automotive-analytics`
   - PostgreSQL Version: `15` (latest)
   - Region: Choose closest to you

4. **Get Your Connection String:**
   ```
   Click "Dashboard" → Your Project → "Connection Details"
   
   Copy the connection string (looks like):
   postgresql://username:password@ep-something.region.aws.neon.tech/dbname?sslmode=require
   ```

5. **Save this connection string** - you'll need it for Vercel!

---

## 🚀 Step 2: Deploy FastAPI Backend to Vercel (FREE)

### Why Vercel?
- ✅ Your project is ALREADY configured for Vercel!
- ✅ Automatic deployments from GitHub
- ✅ Free SSL certificate
- ✅ Generous free tier (100GB bandwidth)
- ✅ No credit card required

### Setup Instructions:

1. **Push your code to GitHub** (if not already done):
   ```bash
   # Already done! Your repo is at:
   # https://github.com/kmrsdrm-arch/vortex-automotive-analytics
   ```

2. **Go to** https://vercel.com

3. **Sign up with GitHub** (if not already signed up)

4. **Import Your Repository:**
   - Click "Add New" → "Project"
   - Select your GitHub repository: `vortex-automotive-analytics`
   - Click "Import"

5. **Configure Environment Variables:**
   
   Click "Environment Variables" and add these:
   
   | Name | Value | Where to get it |
   |------|-------|-----------------|
   | `DATABASE_URL` | `postgresql://...` | From Neon.tech (Step 1) |
   | `OPENAI_API_KEY` | `sk-proj-...` | Your OpenAI API key |
   | `API_HOST` | `0.0.0.0` | Default value |
   | `API_PORT` | `8000` | Default value |
   | `LOG_LEVEL` | `INFO` | Default value |
   | `DEBUG` | `False` | Production mode |

6. **Configure Build Settings:**
   - Framework Preset: **Other**
   - Root Directory: `.` (leave as is)
   - Build Command: (leave empty - not needed)
   - Output Directory: (leave empty)

7. **Click "Deploy"** 🚀

   Vercel will:
   - Build your project
   - Deploy to serverless functions
   - Give you a URL like: `https://your-project.vercel.app`

8. **Test Your API:**
   ```
   Open: https://your-project.vercel.app/docs
   
   You should see FastAPI interactive documentation!
   ```

9. **Copy Your Vercel API URL** - you'll need it for Streamlit!
   ```
   Example: https://vortex-automotive-analytics.vercel.app
   ```

---

## 📊 Step 3: Deploy Streamlit Dashboard (FREE)

### Why Streamlit Cloud?
- ✅ Built specifically for Streamlit apps
- ✅ Free for public GitHub repos
- ✅ Automatic deployments from GitHub
- ✅ No credit card required

### Setup Instructions:

1. **Go to** https://streamlit.io/cloud

2. **Sign in with GitHub**

3. **Create New App:**
   - Click "New app"
   - Repository: `kmrsdrm-arch/vortex-automotive-analytics`
   - Branch: `main`
   - Main file path: `src/dashboard/app.py`
   - App URL: Choose a custom URL (e.g., `vortex-analytics`)

4. **Advanced Settings** - Add Environment Variables:
   
   Click "Advanced settings" and add:
   
   ```
   API_URL=https://your-vercel-app.vercel.app
   ```
   
   Replace `your-vercel-app` with your actual Vercel URL from Step 2!

5. **Click "Deploy"** 🎉

   Streamlit will:
   - Clone your repository
   - Install dependencies
   - Start your dashboard
   - Give you a URL like: `https://vortex-analytics.streamlit.app`

6. **Test Your Dashboard:**
   ```
   Open: https://vortex-analytics.streamlit.app
   
   You should see your beautiful dashboard!
   ```

---

## 🔧 Step 4: Initialize Database

Your database is empty! Let's add some data.

### Option 1: Use the API (Recommended)

1. **Open your Vercel API docs:**
   ```
   https://your-project.vercel.app/docs
   ```

2. **Find the `/api/data/seed` endpoint**

3. **Click "Try it out"** → **Execute**

4. **Wait for seeding to complete** (may take 30-60 seconds)

### Option 2: Run Locally and Push to Neon

1. **Update your local `.env`:**
   ```env
   DATABASE_URL=<your-neon-connection-string>
   OPENAI_API_KEY=<your-openai-key>
   ```

2. **Run seed script:**
   ```bash
   python scripts/seed_data.py --vehicles 100 --sales 5000
   ```

3. **Data is now in Neon database** (accessible by Vercel API)

---

## 🎉 Step 5: You're Live!

### Your Free URLs:

| Service | URL | Purpose |
|---------|-----|---------|
| **Dashboard** | `https://vortex-analytics.streamlit.app` | Main user interface |
| **API** | `https://your-project.vercel.app` | Backend API |
| **API Docs** | `https://your-project.vercel.app/docs` | Interactive API documentation |
| **Database** | Neon.tech Dashboard | View/manage database |

### Test Everything:

1. ✅ **Open Dashboard** - Should load and show data
2. ✅ **Try Sales Analytics** - Should display charts
3. ✅ **Try NL Query** - Type "Show me top selling vehicles"
4. ✅ **Try Insights** - Generate AI insights
5. ✅ **Check API Docs** - Should show all endpoints

---

## 🔄 Automatic Deployments

**Good news!** Both Vercel and Streamlit watch your GitHub repo:

```
You push to GitHub → Automatic deployment!

git add .
git commit -m "Update feature"
git push origin main

↓ Automatic ↓

Vercel rebuilds API ✅
Streamlit rebuilds Dashboard ✅
```

**No manual deployment needed!**

---

## 💰 Free Tier Limits

### Vercel (Free Tier):
- ✅ 100 GB bandwidth/month
- ✅ Unlimited deployments
- ✅ Automatic SSL
- ⚠️ 10 second function timeout
- ⚠️ 1 GB memory per function

**Sufficient for:** Low to medium traffic apps

### Neon.tech (Free Tier):
- ✅ 512 MB storage
- ✅ 1 project
- ✅ Automatic backups
- ⚠️ Database pauses after 5 minutes of inactivity (auto-resumes on query)

**Sufficient for:** This demo app with synthetic data

### Streamlit Cloud (Free Tier):
- ✅ 1 GB RAM
- ✅ 1 CPU core
- ✅ Unlimited apps (public repos)
- ⚠️ Apps sleep after inactivity (auto-wake on visit)

**Sufficient for:** Demo and small production apps

---

## 🐛 Troubleshooting

### API Not Working?

1. **Check Vercel Logs:**
   - Go to Vercel Dashboard
   - Click your project
   - Click "Deployments" → Latest deployment → "View Function Logs"

2. **Common Issues:**
   - ❌ DATABASE_URL not set → Add in Vercel Environment Variables
   - ❌ OPENAI_API_KEY not set → Add in Vercel Environment Variables
   - ❌ Function timeout → Your query takes too long (optimize or upgrade)

### Dashboard Not Connecting to API?

1. **Check API_URL in Streamlit:**
   - Go to Streamlit Cloud
   - Click your app → Settings → Secrets
   - Verify API_URL points to your Vercel URL

2. **Check CORS:**
   - Your API already has CORS enabled
   - Update `API_CORS_ORIGINS` in Vercel if needed

### Database Connection Failed?

1. **Check Neon Database:**
   - Go to Neon.tech Dashboard
   - Verify project is active
   - Copy connection string again (ensure it's complete)

2. **SSL Mode:**
   - Neon requires `?sslmode=require` at end of connection string
   - Example: `postgresql://user:pass@host/db?sslmode=require`

### App Sleeping / Slow First Load?

This is normal on free tiers:
- **Vercel:** Cold start ~1-3 seconds on first request
- **Streamlit:** App wakes from sleep ~5-10 seconds
- **Neon:** Database wakes from sleep ~1-2 seconds

**Solution:** First load is slow, subsequent loads are fast!

---

## 🚀 Performance Tips

### 1. Minimize Cold Starts

**Use a health check ping service (Free):**
- https://uptimerobot.com (Free - pings every 5 minutes)
- Keeps your app warm

**Setup:**
1. Create account at UptimeRobot
2. Add monitors:
   - Monitor 1: `https://your-project.vercel.app/health`
   - Monitor 2: `https://vortex-analytics.streamlit.app`
3. Set interval: 5 minutes

### 2. Optimize API Responses

- ✅ Use date range filters
- ✅ Limit large queries
- ✅ Cache frequently accessed data
- ✅ Use async/await for concurrent operations

### 3. Optimize Streamlit Dashboard

- ✅ Use `@st.cache_data` for expensive computations
- ✅ Lazy load data (only fetch when needed)
- ✅ Show loading spinners for user feedback

---

## 📊 Monitoring Your Free Apps

### Vercel Analytics (Free):
- Go to Vercel Dashboard → Your Project → Analytics
- View:
  - Request count
  - Bandwidth usage
  - Function execution time
  - Error rates

### Streamlit Analytics:
- Go to Streamlit Cloud → Your App → Analytics
- View:
  - Visitor count
  - Session duration
  - Page views

### Neon Database Monitoring:
- Go to Neon Dashboard → Your Project → Monitoring
- View:
  - Storage usage
  - Connection count
  - Query performance

---

## 🎓 Next Steps

### 1. Custom Domain (Optional, Free with Vercel/Streamlit)

**Vercel:**
```
Settings → Domains → Add Domain
Example: api.yourdomain.com
```

**Streamlit:**
```
Settings → Custom Domain
Example: dashboard.yourdomain.com
```

### 2. Upgrade When Needed

When you outgrow free tiers:
- **Vercel Pro:** $20/month (higher limits)
- **Neon.tech Pro:** $19/month (more storage, no sleep)
- **Streamlit Cloud Pro:** $200/month (private apps, more resources)

### 3. Production Optimizations

- Add rate limiting
- Implement caching (Redis)
- Add authentication
- Setup monitoring alerts
- Use CDN for static assets

---

## 📚 Additional Resources

### Documentation:
- **Vercel Docs:** https://vercel.com/docs
- **Streamlit Docs:** https://docs.streamlit.io
- **Neon Docs:** https://neon.tech/docs

### Support:
- **Vercel Support:** https://vercel.com/support
- **Streamlit Community:** https://discuss.streamlit.io
- **Neon Discord:** https://discord.gg/neon

---

## ✅ Deployment Checklist

Before sharing your app publicly:

- [ ] Database seeded with data
- [ ] API responding at `/health` endpoint
- [ ] Dashboard loads without errors
- [ ] Natural language queries work
- [ ] AI insights generate successfully
- [ ] Reports can be generated
- [ ] All environment variables set correctly
- [ ] Tested on mobile (Streamlit is responsive)
- [ ] GitHub repo is up to date
- [ ] README includes deployment links

---

## 🎉 Success!

**Your app is now live and FREE!**

Share your links:
```
Dashboard: https://vortex-analytics.streamlit.app
API: https://your-project.vercel.app
```

**Total Monthly Cost: $0** 💰

Enjoy your free, production-ready analytics platform! 🚀

---

**Need help?** Check the GitHub repository README or open an issue.
**Want to upgrade?** All platforms have easy upgrade paths when you need more resources.


