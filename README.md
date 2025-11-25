# 🚗 VORTEX - Automotive Intelligence Platform

**AI-Powered Analytics Dashboard | FastAPI + Streamlit + PostgreSQL + OpenAI GPT-4**

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/kmrsdrm-arch/vortex-automotive-analytics)

---

## 📋 Overview

VORTEX is a full-stack automotive analytics platform that combines real-time data visualization, AI-powered insights, and natural language query capabilities. Built with modern cloud-native architecture for serverless deployment.

### Key Features

- 📊 **Real-time Analytics Dashboard** - Interactive visualizations with Plotly
- 💬 **Natural Language Queries** - Ask questions in plain English, get SQL results
- 🤖 **AI-Generated Insights** - Automated trend analysis and recommendations
- 📄 **Report Generation** - Executive summaries with AI assistance
- 🏗️ **Serverless Architecture** - Scales automatically, pay only for what you use

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation and settings management

### Frontend
- **Streamlit** - Interactive dashboard UI
- **Plotly** - Data visualization
- **Pandas** - Data manipulation

### Database & AI
- **PostgreSQL** - Relational database
- **OpenAI GPT-4** - Natural language processing
- **ChromaDB** - Vector database for embeddings

### Deployment
- **Vercel** - API serverless functions
- **Streamlit Cloud** - Dashboard hosting
- **Neon** - Serverless PostgreSQL

---

## 🚀 Quick Start - Local Development

### Prerequisites

- Python 3.11+
- PostgreSQL database
- OpenAI API key

### 1. Clone Repository

```bash
git clone https://github.com/kmrsdrm-arch/vortex-automotive-analytics.git
cd vortex-automotive-analytics
```

### 2. Install Dependencies

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

### 3. Configure Environment

Create `.env` file in project root:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/automotive_analytics

# OpenAI
OPENAI_API_KEY=sk-proj-your-key-here

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
API_URL=http://localhost:8000

# Optional
DEBUG=false
LOG_LEVEL=INFO
```

### 4. Initialize Database

```bash
python scripts/init_db.py
python scripts/seed_data.py
```

### 5. Run Application

**Terminal 1 - API:**
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Dashboard:**
```bash
streamlit run src/dashboard/app.py
```

**Access:**
- Dashboard: http://localhost:8501
- API Docs: http://localhost:8000/docs

---

## ☁️ Production Deployment

### Deploy to Vercel + Streamlit Cloud (Recommended)

**Architecture:**
```
┌─────────────────┐
│ Vercel          │ → FastAPI (Serverless)
│ API Functions   │
└────────┬────────┘
         │
         ├──→ Neon (PostgreSQL)
         └──→ Streamlit Cloud (Dashboard)
```

### Step 1: Deploy API to Vercel

1. **Push to GitHub:**
   ```bash
   git push origin main
   ```

2. **Import to Vercel:**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import: `kmrsdrm-arch/vortex-automotive-analytics`
   - Framework: Other
   - Click **Deploy**

3. **Add Environment Variables:**
   ```
   DATABASE_URL = postgresql://user:pass@host/db
   OPENAI_API_KEY = sk-proj-your-key
   ```

**Result:** `https://vortex-kmrsdrm.vercel.app`

### Step 2: Setup Database (Neon)

1. **Create Database:**
   - Go to [neon.tech](https://neon.tech)
   - Create project: `vortex-analytics`
   - Copy connection string

2. **Add to Vercel:**
   - Vercel → Settings → Environment Variables
   - Update `DATABASE_URL`
   - Redeploy

3. **Initialize Database:**
   ```bash
   # Set environment variables
   export DATABASE_URL="your-neon-connection-string"
   export OPENAI_API_KEY="your-openai-key"
   
   # Run migrations
   python scripts/init_db.py
   python scripts/seed_data.py
   ```

### Step 3: Deploy Dashboard (Streamlit Cloud)

1. **Deploy App:**
   - Go to [streamlit.io/cloud](https://streamlit.io/cloud)
   - New app from GitHub
   - Repository: `kmrsdrm-arch/vortex-automotive-analytics`
   - Main file: `src/dashboard/app.py`

2. **Add Secrets:**
   ```toml
   DATABASE_URL = "your-neon-connection-string"
   OPENAI_API_KEY = "sk-proj-your-key"
   API_URL = "https://vortex-kmrsdrm.vercel.app"
   ```

3. **Deploy**

**Result:** `https://your-app.streamlit.app`

### Step 4: Update CORS

In Vercel, add environment variable:
```
API_CORS_ORIGINS = ["https://your-app.streamlit.app"]
```

Redeploy.

---

## 📁 Project Structure

```
vortex-automotive-analytics/
├── api/
│   └── index.py              # Vercel serverless entry point
├── config/
│   ├── database.py           # Database configuration
│   ├── logging_config.py     # Logging setup
│   └── settings.py           # Environment settings
├── scripts/
│   ├── init_db.py            # Database initialization
│   └── seed_data.py          # Sample data seeding
├── src/
│   ├── analytics/            # Analytics engine
│   ├── api/                  # FastAPI application
│   │   ├── main.py           # API entry point
│   │   ├── routes/           # API endpoints
│   │   └── schemas/          # Pydantic models
│   ├── dashboard/            # Streamlit UI
│   │   ├── app.py            # Dashboard entry point
│   │   ├── components/       # Reusable components
│   │   ├── pages/            # Multi-page app
│   │   └── styles/           # Theme configuration
│   ├── database/             # Database models & repos
│   ├── llm/                  # OpenAI integration
│   └── utils/                # Utilities
├── .gitignore
├── requirements.txt          # Python dependencies
├── vercel.json               # Vercel configuration
└── README.md                 # This file
```

---

## 🔧 API Endpoints

### Analytics
- `GET /api/v1/analytics/kpis` - Key performance indicators
- `GET /api/v1/analytics/sales/summary` - Sales summary
- `GET /api/v1/analytics/sales/trends` - Sales trends
- `GET /api/v1/analytics/inventory` - Inventory status

### AI Features
- `POST /api/v1/query/natural-language` - NL to SQL query
- `POST /api/v1/insights/generate` - Generate insights
- `POST /api/v1/reports/generate` - Generate reports

### Health
- `GET /health` - Health check
- `GET /` - API information

**Full Documentation:** `/docs` (Swagger UI)

---

## 🔑 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | ✅ | - |
| `OPENAI_API_KEY` | OpenAI API key | ✅ | - |
| `API_URL` | API endpoint URL | ✅ | `http://localhost:8000` |
| `API_HOST` | API host | ❌ | `0.0.0.0` |
| `API_PORT` | API port | ❌ | `8000` |
| `DEBUG` | Debug mode | ❌ | `false` |
| `LOG_LEVEL` | Logging level | ❌ | `INFO` |

See `environment.example` for full list.

---

## 💰 Cost (Free Tier)

| Service | Free Tier | Use Case |
|---------|-----------|----------|
| **Vercel** | 100GB bandwidth/month | API hosting |
| **Streamlit Cloud** | 1GB RAM, unlimited public apps | Dashboard |
| **Neon** | 3GB storage | Database |
| **OpenAI** | Pay-as-you-go | AI features |

**Estimated Monthly Cost:** $0-10 (mostly OpenAI usage)

---

## 🧪 Testing

```bash
# Run tests
pytest tests/

# API testing
python test_api.bat  # Windows
# bash test_api.sh   # Linux/Mac

# OpenAI verification
python verify_openai_api.py
```

---

## 🐛 Troubleshooting

### API Issues

**Error: Module not found**
- Check Python path in `api/index.py`
- Verify all dependencies in `requirements.txt`

**Error: Database connection failed**
- Verify `DATABASE_URL` is correct
- Check database is accessible
- Ensure tables are initialized

### Dashboard Issues

**Can't connect to API**
- Check `API_URL` environment variable
- Verify CORS settings in API
- Test API endpoint directly

**OpenAI errors**
- Verify API key is valid
- Check account has credits
- Test with `verify_openai_api.py`

### Deployment Issues

**Vercel build failed**
- Check deployment logs
- Verify `vercel.json` configuration
- Ensure all dependencies are listed

**Cold start timeout**
- Optimize imports
- Consider caching strategies
- Upgrade to paid tier if needed

---

## 📊 Features Demo

### 1. Real-time Dashboard
- KPI metrics with trend indicators
- Interactive charts (sales, inventory, regional)
- Date range filtering
- Responsive design

### 2. Natural Language Queries
```
User: "Show me top 5 selling vehicles this month"
VORTEX: [Generates SQL, executes, returns formatted results]
```

### 3. AI Insights
- Automated trend detection
- Sales forecasting
- Inventory recommendations
- Market analysis

### 4. Report Generation
- Executive summaries
- Detailed analytics reports
- Export as Markdown/PDF
- AI-assisted content

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🔗 Links

- **Live Demo:** [Dashboard](https://your-app.streamlit.app) | [API](https://vortex-kmrsdrm.vercel.app/docs)
- **Repository:** [GitHub](https://github.com/kmrsdrm-arch/vortex-automotive-analytics)
- **Documentation:** [API Docs](https://vortex-kmrsdrm.vercel.app/docs)

---

## 📧 Contact

**Developer:** kmrsdrm-arch  
**Email:** kmrsdrm@gmail.com  
**GitHub:** [@kmrsdrm-arch](https://github.com/kmrsdrm-arch)

---

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Streamlit for the intuitive dashboard framework
- OpenAI for GPT-4 capabilities
- Vercel for serverless deployment
- Neon for serverless PostgreSQL

---

**Built with ❤️ using modern cloud-native technologies**

**Star ⭐ this repo if you find it helpful!**
