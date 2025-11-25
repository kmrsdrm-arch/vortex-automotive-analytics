# 🚀 Deploy to Render.com (FREE) - Vercel Alternative

## ⚠️ Why Render Instead of Vercel?

Your Vercel deployment has persistent `FUNCTION_INVOCATION_FAILED` errors that we couldn't resolve even with minimal configurations. **Render.com is actually better for Python APIs** and will work immediately!

---

## ✅ **Render.com Advantages:**

- ✅ **FREE Tier** - No credit card required
- ✅ **Always-on** (not serverless, so no cold starts!)
- ✅ **Better for Python** - Native Python support
- ✅ **Simpler setup** - Just works!
- ✅ **Automatic deployments** from GitHub
- ✅ **Free SSL** certificate
- ✅ **750 hours/month free** (enough for 24/7)

---

## 📋 **Step-by-Step Deployment (5 minutes)**

### **Step 1: Sign Up**

1. Go to https://render.com
2. Click **"Get Started"**
3. **Sign up with GitHub** (easiest)

### **Step 2: Create Web Service**

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub account (if not already)
3. Find and select: `kmrsdrm-arch/vortex-automotive-analytics`
4. Click **"Connect"**

### **Step 3: Configure Service**

Fill in these settings:

| Field | Value |
|-------|-------|
| **Name** | `vortex-automotive-api` |
| **Region** | Choose closest to you |
| **Branch** | `main` |
| **Root Directory** | (leave empty) |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` |

### **Step 4: Environment Variables**

Click **"Advanced"** → **"Add Environment Variable"**

Add these:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | Your Neon.tech connection string |
| `OPENAI_API_KEY` | Your OpenAI API key |
| `PYTHON_VERSION` | `3.11.0` |

### **Step 5: Deploy!**

1. Click **"Create Web Service"**
2. Render will:
   - Install dependencies (~2-3 minutes)
   - Start your API
   - Give you a URL like: `https://vortex-automotive-api.onrender.com`

---

## 🎉 **That's It!**

Your API will be live at:
```
https://your-service-name.onrender.com
```

### **Test Your API:**

```bash
# Root endpoint
curl https://your-service-name.onrender.com/

# API docs
https://your-service-name.onrender.com/docs

# Health check
curl https://your-service-name.onrender.com/health
```

---

## 🔄 **Automatic Deployments**

Every time you push to GitHub main branch:
1. Render detects the push
2. Automatically rebuilds
3. Deploys new version
4. **Zero downtime!**

---

## 📊 **Free Tier Limits**

Render Free Tier includes:
- ✅ 750 hours/month (24/7 for one service)
- ✅ 512 MB RAM
- ✅ Shared CPU
- ⏸️ Spins down after 15 min inactivity (auto-wakes on request)

**Perfect for your demo/prototype!**

---

## 🔧 **If Service Sleeps**

Free tier services sleep after 15 minutes of inactivity.

**Solution: Keep it awake**
1. Use UptimeRobot (free) to ping every 14 minutes
2. Or upgrade to Starter plan ($7/month) for always-on

---

## 🎯 **Dashboard Setup**

Once API is live on Render, update your Streamlit dashboard:

1. Go to Streamlit Cloud
2. Your app → Settings → Environment Variables
3. Update `API_URL`:
   ```
   API_URL=https://your-service-name.onrender.com
   ```
4. Redeploy dashboard

---

## 💡 **Why Render Works Better Than Vercel**

### Vercel (Serverless):
- ❌ Cold starts (1-3 seconds)
- ❌ 50MB size limit
- ❌ 10 second timeout
- ❌ Complex configuration
- ❌ Python support is secondary

### Render (Always-On):
- ✅ No cold starts (after first request)
- ✅ No size limits
- ✅ No timeout issues
- ✅ Simple configuration
- ✅ Built for Python

---

## 🐛 **Troubleshooting**

### Build Fails?
- Check **"Logs"** tab in Render dashboard
- Verify `requirements.txt` is correct
- Ensure Python 3.11 is specified

### Service Won't Start?
- Check **"Logs"** tab for errors
- Verify environment variables are set
- Ensure start command is correct

### Database Connection Failed?
- Verify `DATABASE_URL` format:
  ```
  postgresql://user:password@host:5432/database?sslmode=require
  ```

---

## 🎓 **Next Steps**

1. ✅ Deploy API to Render (5 minutes)
2. ✅ Test API endpoints
3. ✅ Update Streamlit dashboard `API_URL`
4. ✅ Redeploy Streamlit
5. 🎉 Everything works!

---

## 📚 **Resources**

- Render Docs: https://render.com/docs
- Deploy Python API: https://render.com/docs/deploy-fastapi
- Free SSL: Automatic!
- Custom Domain: Free (if you have one)

---

## ✅ **Summary**

**Vercel Issue:** `FUNCTION_INVOCATION_FAILED` (unresolved)

**Solution:** Deploy to **Render.com** instead

**Result:** Your API will work perfectly! 🚀

---

**Need help?** Render has great documentation and support.

**Total Cost:** $0/month (Free tier)

**Deployment Time:** 5 minutes

**Status:** Ready to deploy!

