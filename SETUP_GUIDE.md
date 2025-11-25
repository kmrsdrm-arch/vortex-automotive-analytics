# 🚗 Automotive Analytics - Complete Setup Guide

**Version:** 2.0.0  
**Last Updated:** November 2024  
**Difficulty:** Beginner-Friendly

---

## 📋 Table of Contents

1. [Quick Start](#-quick-start-5-minutes)
2. [Prerequisites](#-prerequisites)
3. [Detailed Setup](#-detailed-setup-step-by-step)
4. [OpenAI API Key Setup](#-openai-api-key-setup)
5. [Testing Your Configuration](#-testing-your-configuration)
6. [Running the Application](#-running-the-application)
7. [Troubleshooting](#-troubleshooting)
8. [Command Reference](#-command-reference)

---

## 🚀 Quick Start (5 Minutes)

```bash
# 1. Clone and navigate to project
cd path\to\automotive-analytics

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
venv\Scripts\activate.bat

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment (see below)
# Edit .env file with your credentials

# 6. Test API key
test_api.bat

# 7. Start services
start.bat
```

**Done!** 🎉 Dashboard opens at http://localhost:8501

---

## ✅ Prerequisites

### Required Software

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **PostgreSQL 14+** - [Download](https://www.postgresql.org/download/)
- **Git** (optional) - [Download](https://git-scm.com/downloads)

### Required Accounts

- **OpenAI Account** - [Sign Up](https://platform.openai.com/signup)
  - With billing configured
  - At least $5 in credits recommended

### System Requirements

- **OS:** Windows 10/11, Linux, macOS
- **RAM:** 4GB minimum, 8GB recommended
- **Disk:** 2GB free space

---

## 📖 Detailed Setup (Step by Step)

### Step 1: Install Python

1. Download Python 3.11+ from https://www.python.org/downloads/
2. During installation:
   - ✅ Check "Add Python to PATH"
   - ✅ Check "Install pip"
3. Verify installation:
   ```bash
   python --version  # Should show 3.11+
   pip --version     # Should show pip version
   ```

### Step 2: Install PostgreSQL

1. Download from https://www.postgresql.org/download/
2. During installation, remember:
   - Username (default: `postgres`)
   - Password (you choose)
   - Port (default: `5432`)
3. Create database:
   ```sql
   CREATE DATABASE automotive_analytics;
   CREATE USER automotive_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE automotive_analytics TO automotive_user;
   ```

### Step 3: Create Virtual Environment

```bash
# Navigate to project directory
cd C:\path\to\automotive-analytics

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate.bat

# Activate it (Linux/Mac)
source venv/bin/activate

# Verify activation
which python  # Should point to venv/Scripts/python
```

### Step 4: Install Dependencies

```bash
# Make sure virtual environment is activated!
pip install -r requirements.txt

# This installs ~50 packages, takes 2-3 minutes
# You should see: "Successfully installed ..."
```

### Step 5: Configure Environment Variables

Create a file named `.env` in the project root:

```env
# Database Configuration
DATABASE_URL=postgresql://automotive_user:your_password@localhost:5432/automotive_analytics

# OpenAI Configuration
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL_PRIMARY=gpt-4-turbo-preview
OPENAI_MODEL_SECONDARY=gpt-3.5-turbo
OPENAI_MAX_TOKENS=4000

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_CORS_ORIGINS=["http://localhost:8501"]

# Dashboard Configuration
DASHBOARD_PORT=8501

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Vector Store
CHROMADB_PATH=./data/chromadb

# Feature Flags
ENABLE_RAG=true
ENABLE_CACHING=false

# Application
APP_NAME=Automotive Analytics Pipeline
APP_VERSION=1.0.0
DEBUG=false
```

**⚠️ IMPORTANT:**
- No spaces around `=`
- No quotes around values
- No line breaks in the middle of values
- One variable per line

---

## 🔑 OpenAI API Key Setup

### Why You Need This

The application uses OpenAI's GPT models for:
- Natural language queries
- Automated insights generation
- AI-powered reports
- Data analysis recommendations

### Getting Your API Key

1. **Go to OpenAI Platform**  
   👉 https://platform.openai.com/api-keys

2. **Sign In / Create Account**  
   - Use Google, Microsoft, or email
   - Verify your email

3. **Set Up Billing**  
   👉 https://platform.openai.com/account/billing
   - Click "Add payment method"
   - Enter credit card
   - Add at least $5 (recommended $10-20)
   - ⚠️ **Required**: Free trial has limitations

4. **Create API Key**
   - Go back to API Keys page
   - Click "**+ Create new secret key**"
   - Give it a name: "Automotive Analytics"
   - Click "Create secret key"
   - **COPY IMMEDIATELY** - you'll only see it once!

5. **Key Format**
   - Project keys: `sk-proj-...` (164 characters) ✅ Recommended
   - Legacy keys: `sk-...` (48 characters)

### Estimated Costs

With the application:
- Testing: ~$0.01 per test
- Normal usage: ~$1-5 per month
- Heavy usage: ~$10-20 per month

**Tip:** Set usage limits in OpenAI dashboard to avoid surprises!

### Adding Key to .env

```env
# In your .env file:
OPENAI_API_KEY=sk-proj-abc123def456...xyz789

# ❌ WRONG:
OPENAI_API_KEY = "sk-proj-..."  # No spaces, no quotes
OPENAI_API_KEY='sk-proj-...'    # No quotes!

# ✅ CORRECT:
OPENAI_API_KEY=sk-proj-abc123def456...xyz789
```

---

## 🧪 Testing Your Configuration

### Method 1: Quick Test (Recommended)

```bash
# Run the test script
test_api.bat

# Or directly:
python verify_openai_api.py
```

**Expected Output:**
```
===========================================================================
  🔑 OPENAI API KEY VERIFICATION
===========================================================================

✅ Found: C:\path\to\.env
✅ Loaded: sk-proj-abc123...xyz789
✅ Format looks correct
✅ Testing connection...

  ✨ SUCCESS! YOUR API KEY WORKS! ✨

🎉 VERIFICATION COMPLETE - ALL SYSTEMS GO!
```

### Method 2: Manual Test

```python
# test_manual.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Say OK"}],
    max_tokens=5
)

print(f"✅ Success: {response.choices[0].message.content}")
```

---

## 🎯 Running the Application

### Method 1: One-Command Start (Easiest)

```bash
# Start everything at once
start.bat

# This will:
# 1. Check configuration
# 2. Test API key
# 3. Start API server (port 8000)
# 4. Start Dashboard (port 8501)
# 5. Open browser automatically
```

### Method 2: Manual Start (Two Terminals)

**Terminal 1 - API Server:**
```bash
venv\Scripts\activate.bat
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Dashboard:**
```bash
venv\Scripts\activate.bat
streamlit run src/dashboard/app.py --server.port 8501
```

### Accessing the Application

- **Dashboard:** http://localhost:8501
- **API Documentation:** http://localhost:8000/docs
- **API:** http://localhost:8000

### Stopping Services

```bash
# Easy way
start.bat stop

# Or press Ctrl+C in each terminal
```

---

## 🔧 Troubleshooting

### Problem: "API Key Error" or "401 Unauthorized"

**Symptoms:**
- Test fails with "Invalid API key"
- Dashboard shows API connection error

**Solutions:**

1. **Verify API key is correct**
   ```bash
   # Check what's in your .env
   type .env | findstr OPENAI_API_KEY
   
   # Should show: OPENAI_API_KEY=sk-proj-...
   ```

2. **Check for formatting issues**
   ```env
   # ❌ WRONG - has spaces
   OPENAI_API_KEY = sk-proj-...
   
   # ❌ WRONG - has quotes
   OPENAI_API_KEY="sk-proj-..."
   
   # ✅ CORRECT
   OPENAI_API_KEY=sk-proj-...
   ```

3. **Make sure key is active**
   - Go to https://platform.openai.com/api-keys
   - Check if key shows as "Active"
   - Try creating a new key if needed

4. **Clear environment variables**
   ```bash
   # In PowerShell
   Remove-Item Env:OPENAI_API_KEY
   
   # Then test again
   test_api.bat
   ```

5. **Verify billing is set up**
   - https://platform.openai.com/account/billing
   - Must have payment method AND credits

---

### Problem: "Port Already in Use"

**Symptoms:**
```
Error: [Errno 10048] Address already in use: 0.0.0.0:8000
```

**Solutions:**

```bash
# Option 1: Stop all services
start.bat stop

# Option 2: Kill specific port
netstat -ano | findstr :8000
taskkill /F /PID <PID_NUMBER>

# Option 3: Use different ports
# Edit .env:
API_PORT=8001
DASHBOARD_PORT=8502
```

---

### Problem: "Module Not Found" Errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'openai'
```

**Solutions:**

```bash
# 1. Make sure venv is activated
venv\Scripts\activate.bat

# 2. Reinstall dependencies
pip install -r requirements.txt

# 3. Verify installation
pip list | findstr openai

# 4. If still failing, recreate venv
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

---

### Problem: Database Connection Errors

**Symptoms:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solutions:**

1. **Check PostgreSQL is running**
   ```bash
   # Windows: Check Services
   services.msc
   # Look for "postgresql-x64-14" or similar
   ```

2. **Verify connection string**
   ```env
   # Format:
   DATABASE_URL=postgresql://username:password@host:port/database
   
   # Example:
   DATABASE_URL=postgresql://postgres:mypassword@localhost:5432/automotive_analytics
   ```

3. **Test connection**
   ```bash
   psql -U automotive_user -d automotive_analytics
   # Should connect without errors
   ```

---

### Problem: Dashboard Loads But Features Don't Work

**Symptoms:**
- Dashboard opens but queries fail
- "API connection error" messages
- Features timeout

**Solutions:**

1. **Check API server is running**
   ```bash
   # Open http://localhost:8000/docs
   # Should show FastAPI documentation
   ```

2. **Check CORS settings**
   ```env
   # In .env:
   API_CORS_ORIGINS=["http://localhost:8501"]
   ```

3. **Check logs**
   ```bash
   # API logs
   tail logs/app.log
   
   # Or check console where API is running
   ```

4. **Restart services**
   ```bash
   start.bat restart
   ```

---

### Common Error Messages Explained

| Error | Meaning | Solution |
|-------|---------|----------|
| `401 Unauthorized` | Invalid API key | Get new key from OpenAI |
| `429 Too Many Requests` | Rate limit hit | Wait 60 seconds, try again |
| `Insufficient quota` | No credits | Add billing to OpenAI account |
| `Connection refused` | Service not running | Run `start.bat` |
| `Module not found` | Missing package | Run `pip install -r requirements.txt` |
| `Database does not exist` | DB not created | Create database in PostgreSQL |

---

## 📝 Command Reference

### Batch Files

```bash
# Main startup script
start.bat          # Start all services
start.bat stop     # Stop all services
start.bat restart  # Restart all services
start.bat test     # Run configuration tests
start.bat help     # Show help

# API testing
test_api.bat       # Test OpenAI API key
```

### Python Scripts

```bash
# API verification (recommended)
python verify_openai_api.py

# Database initialization
python scripts/init_db.py

# Seed sample data
python scripts/seed_data.py

# Run ETL pipeline
python scripts/run_pipeline.py
```

### Manual Commands

```bash
# Activate virtual environment
venv\Scripts\activate.bat

# Run API server
uvicorn src.api.main:app --reload

# Run dashboard
streamlit run src/dashboard/app.py

# Run database migrations
alembic upgrade head

# Run tests
pytest tests/
```

---

## 🎓 Next Steps

After successful setup:

1. **Explore the Dashboard**
   - Main Dashboard: Overview of KPIs
   - Sales Analytics: Detailed sales metrics
   - Inventory Analytics: Stock management
   - NL Query: Ask questions in plain English
   - AI Insights: Automated analysis
   - Reports: Generate AI reports

2. **Seed Sample Data** (optional)
   ```bash
   python scripts/seed_data.py
   ```

3. **Read Documentation**
   - API Docs: http://localhost:8000/docs
   - README.md: Project overview
   - CHANGELOG.md: Version history

4. **Customize**
   - Modify prompts in `src/llm/core/prompts.py`
   - Add new analytics in `src/analytics/`
   - Create custom dashboards in `src/dashboard/pages/`

---

## 📞 Getting Help

- **OpenAI Status:** https://status.openai.com/
- **OpenAI Docs:** https://platform.openai.com/docs
- **PostgreSQL Docs:** https://www.postgresql.org/docs/
- **Streamlit Docs:** https://docs.streamlit.io/

---

## 🔐 Security Best Practices

1. **Never commit .env file**
   - Already in `.gitignore`
   - Contains sensitive credentials

2. **Rotate API keys regularly**
   - Every 90 days recommended
   - Immediately if compromised

3. **Set usage limits**
   - In OpenAI dashboard
   - Prevents unexpected charges

4. **Use strong database passwords**
   - 12+ characters
   - Mix of letters, numbers, symbols

5. **Keep dependencies updated**
   ```bash
   pip list --outdated
   pip install --upgrade package-name
   ```

---

## ✅ Setup Checklist

- [ ] Python 3.11+ installed
- [ ] PostgreSQL 14+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] .env file configured
- [ ] OpenAI API key obtained
- [ ] Billing configured on OpenAI
- [ ] Database created
- [ ] API test passed (`test_api.bat`)
- [ ] Services start successfully (`start.bat`)
- [ ] Dashboard accessible at http://localhost:8501
- [ ] API docs accessible at http://localhost:8000/docs

---

**🎉 Congratulations! You're all set up!**

If you run into any issues, refer to the troubleshooting section or check the error messages from `verify_openai_api.py` - they provide detailed, actionable solutions.

---

*Last updated: November 2024*  
*Version: 2.0.0*

