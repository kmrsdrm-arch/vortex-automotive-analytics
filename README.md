# 🚗 VORTEX - Automotive Intelligence Platform

**AI-Powered Sales & Inventory Analytics Dashboard**

A production-ready, full-stack analytics platform with FastAPI backend, Streamlit dashboard, PostgreSQL database, and OpenAI GPT-4 integration.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/kmrsdrm-arch/vortex-automotive-analytics)

---

## 🌟 Live Demo

- **Dashboard**: [Deploy to Streamlit Cloud](https://streamlit.io/cloud)
- **API Docs**: `https://your-app.vercel.app/docs`
- **Source Code**: https://github.com/kmrsdrm-arch/vortex-automotive-analytics

---

## ✨ Features

### 📊 Real-Time Analytics Dashboard
- Executive KPI overview with beautiful metrics
- Interactive Plotly charts and visualizations
- Sales trends and performance analysis
- Inventory management with low-stock alerts

### 💬 Natural Language Queries
- Ask questions in plain English
- AI-powered SQL generation (GPT-4)
- Interactive results with data tables
- Query history tracking

### 🤖 AI-Powered Insights
- Automated trend identification
- Smart recommendations
- Predictive analytics
- Historical pattern analysis

### 📄 Report Generation
- Executive summaries
- Detailed performance reports
- AI-generated content
- Export as MD/TXT

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL database (or use Neon free tier)
- OpenAI API key

### Local Development

1. **Clone Repository**
   ```bash
   git clone https://github.com/kmrsdrm-arch/vortex-automotive-analytics.git
   cd vortex-automotive-analytics
   ```

2. **Setup Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   
   Create `.env` file (see `environment.example`):
   ```env
   DATABASE_URL=postgresql://user:pass@localhost:5432/automotive_analytics
   OPENAI_API_KEY=sk-proj-your-key-here
   ```

4. **Initialize Database**
   ```bash
   # Start PostgreSQL (or use Docker)
   docker-compose up -d postgres

   # Initialize database
   python scripts/init_db.py
   python scripts/seed_data.py
   ```

5. **Start Application**
   ```bash
   # Start API and Dashboard together
   start.bat  # Windows
   
   # Or start separately:
   # Terminal 1 - API
   uvicorn src.api.main:app --reload --port 8000
   
   # Terminal 2 - Dashboard
   streamlit run src/dashboard/app.py
   ```

6. **Access Application**
   - Dashboard: http://localhost:8501
   - API Docs: http://localhost:8000/docs

---

## 🌐 Production Deployment

### Deploy to Vercel + Streamlit Cloud (Recommended) ⭐

**Complete guide**: See [DEPLOY_NOW.md](DEPLOY_NOW.md)

**Quick Steps**:

1. **API on Vercel** (5 min)
   - Go to [vercel.com](https://vercel.com)
   - Import this repository
   - Add `OPENAI_API_KEY` environment variable
   - Deploy!

2. **Database on Neon** (3 min)
   - Sign up at [neon.tech](https://neon.tech)
   - Create PostgreSQL database
   - Add `DATABASE_URL` to Vercel
   - Run `python scripts/init_db.py`

3. **Dashboard on Streamlit Cloud** (5 min)
   - Sign up at [streamlit.io/cloud](https://streamlit.io/cloud)
   - Deploy from GitHub
   - Add secrets (API_URL, DATABASE_URL, OPENAI_API_KEY)
   - Done!

**Total Time**: ~20 minutes  
**Cost**: $0/month (free tiers)

📖 **Full deployment guide**: [DEPLOY_NOW.md](DEPLOY_NOW.md)  
⚡ **Quick reference**: [VERCEL_QUICKSTART.md](VERCEL_QUICKSTART.md)

---

## 🏗️ Architecture

```
┌─────────────────────────────┐
│  Streamlit Dashboard        │  Port 8501
│  (Frontend UI)              │
└──────────┬──────────────────┘
           │ HTTP/REST
           ▼
┌─────────────────────────────┐
│  FastAPI Backend            │  Port 8000
│  (REST API)                 │
└──────────┬──────────────────┘
           │
    ┌──────┴────────┬─────────────┐
    ▼               ▼             ▼
┌────────┐     ┌────────┐    ┌────────┐
│PostgreSQL│    │OpenAI  │    │ChromaDB│
│Database  │    │GPT-4   │    │Vectors │
└──────────┘    └────────┘    └────────┘
```

### Tech Stack

**Backend**:
- FastAPI - Modern async Python web framework
- SQLAlchemy - ORM for database interactions
- Pydantic - Data validation and settings

**Frontend**:
- Streamlit - Python-based dashboard framework
- Plotly - Interactive data visualizations
- Pandas - Data manipulation

**Database**:
- PostgreSQL - Relational database
- Alembic - Database migrations

**AI/ML**:
- OpenAI GPT-4 - Natural language processing
- LangChain - LLM application framework
- ChromaDB - Vector database for embeddings

**DevOps**:
- Vercel - Serverless API deployment
- Streamlit Cloud - Dashboard hosting
- Docker - Containerization
- Git - Version control

---

## 📁 Project Structure

```
vortex-automotive-analytics/
├── src/
│   ├── api/                    # FastAPI backend
│   │   ├── main.py            # API entry point
│   │   ├── routes/            # API endpoints
│   │   └── schemas/           # Pydantic models
│   │
│   ├── dashboard/             # Streamlit frontend
│   │   ├── app.py            # Main dashboard
│   │   ├── pages/            # Dashboard pages
│   │   ├── components/       # Reusable UI components
│   │   └── styles/           # Theme and styling
│   │
│   ├── database/              # Database layer
│   │   ├── models/           # SQLAlchemy models
│   │   └── repositories/     # Data access layer
│   │
│   ├── llm/                   # AI/ML integration
│   │   ├── core/             # OpenAI client
│   │   └── services/         # LLM services
│   │
│   ├── analytics/             # Business logic
│   │   ├── kpi_calculator.py
│   │   └── sales_analytics.py
│   │
│   └── utils/                 # Utilities
│
├── scripts/                   # Utility scripts
│   ├── init_db.py           # Database initialization
│   └── seed_data.py         # Sample data generator
│
├── config/                    # Configuration
│   ├── settings.py          # App settings (Pydantic)
│   └── database.py          # Database config
│
├── tests/                     # Test suite
├── api/                       # Vercel serverless entry
├── docs/                      # Additional documentation
│
├── vercel.json               # Vercel deployment config
├── docker-compose.yml        # Docker configuration
├── requirements.txt          # Python dependencies
├── environment.example       # Environment template
├── start.bat                # Local startup script
└── README.md                # This file
```

---

## 🎨 Dashboard Pages

1. **Dashboard Summary** - Executive overview with key metrics
2. **Sales Analytics** - Comprehensive sales performance analysis
3. **Inventory Analytics** - Stock levels and distribution
4. **Natural Language Query** - Ask questions in plain English
5. **AI Insights** - Automated analysis and recommendations
6. **Reports** - Generate and export reports

---

## 🔧 Configuration

### Environment Variables

See `environment.example` for full list. Key variables:

```env
# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# OpenAI
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL_PRIMARY=gpt-4-turbo-preview
OPENAI_MODEL_SECONDARY=gpt-3.5-turbo

# API
API_HOST=0.0.0.0
API_PORT=8000
API_URL=http://localhost:8000  # For dashboard

# Features
ENABLE_RAG=true
ENABLE_CACHING=false

# App
DEBUG=false
LOG_LEVEL=INFO
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_api.py
```

---

## 📊 API Endpoints

### Health & Status
- `GET /health` - Health check
- `GET /` - API info

### Analytics
- `GET /api/v1/analytics/kpis` - Key performance indicators
- `GET /api/v1/analytics/sales/summary` - Sales summary
- `GET /api/v1/analytics/sales/trends` - Sales trends
- `GET /api/v1/analytics/inventory` - Inventory data

### AI Features
- `POST /api/v1/query/natural-language` - NL to SQL query
- `POST /api/v1/insights/generate` - Generate insights
- `POST /api/v1/reports/generate` - Generate reports

**Full API docs**: http://localhost:8000/docs (Swagger UI)

---

## 🎯 Use Cases

### Business Intelligence
- Executive dashboards for decision-making
- Sales performance tracking
- Inventory optimization

### Data Analytics
- Trend analysis and forecasting
- Customer segmentation
- Regional performance comparison

### AI Integration
- Natural language data queries
- Automated insight generation
- Intelligent recommendations

---

## 🚀 Performance

- **API Response Time**: < 100ms for most endpoints
- **Dashboard Load**: < 2 seconds (after cold start)
- **Database Queries**: Optimized with indexes
- **Scalability**: Serverless architecture (auto-scaling)

---

## 🔒 Security

- ✅ Environment variables for secrets (never hardcoded)
- ✅ CORS configuration for API access control
- ✅ SQL injection prevention via SQLAlchemy ORM
- ✅ Input validation with Pydantic schemas
- ✅ HTTPS enabled on all deployments

---

## 📧 Sharing with Hiring Managers

Use this template:

```
Subject: Portfolio Demo - VORTEX Automotive Intelligence Platform

Hi [Name],

I'd like to share my full-stack AI project:

🔗 Live Demo: https://[your-app].streamlit.app
📚 API Docs: https://[your-app].vercel.app/docs
💻 Source: https://github.com/kmrsdrm-arch/vortex-automotive-analytics

Tech Stack: FastAPI | Streamlit | PostgreSQL | OpenAI GPT-4
Architecture: Vercel (API) + Streamlit Cloud (UI) + Neon (DB)

Key Features:
• Real-time analytics dashboard
• Natural language SQL queries (GPT-4)
• AI-generated insights
• Production serverless deployment

This demonstrates my skills in:
✅ Full-stack development
✅ AI/ML integration
✅ Cloud deployment
✅ API design
✅ Database optimization

I'd love to discuss how my experience aligns with your team's needs.

Best regards,
[Your Name]
```

---

## 🆘 Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
docker-compose ps

# Verify connection string
python -c "from config.settings import settings; print(settings.database_url)"
```

### OpenAI API Errors
- Verify API key at https://platform.openai.com/api-keys
- Check account has credits
- Ensure key format: `sk-proj-...` or `sk-...`

### Dashboard Won't Load
- Hard refresh: Ctrl+F5
- Check API is running: http://localhost:8000/docs
- Verify `API_URL` environment variable

### Deployment Issues
- See [DEPLOY_NOW.md](DEPLOY_NOW.md) for detailed troubleshooting
- Check deployment logs in Vercel/Streamlit dashboard
- Verify all environment variables are set

---

## 📚 Documentation

- **Deployment Guide**: [DEPLOY_NOW.md](DEPLOY_NOW.md) - Production deployment
- **Quick Start**: [VERCEL_QUICKSTART.md](VERCEL_QUICKSTART.md) - 5-step deploy
- **Full Guide**: [VERCEL_DEPLOYMENT_GUIDE.md](VERCEL_DEPLOYMENT_GUIDE.md) - Detailed instructions
- **Environment Setup**: [environment.example](environment.example) - Configuration reference
- **Changelog**: [CHANGELOG.md](CHANGELOG.md) - Version history

---

## 🤝 Contributing

This is a portfolio project, but suggestions and feedback are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is open source and available for educational and portfolio purposes.

---

## 👨‍💻 Author

**kmrsdrm-arch**

- GitHub: [@kmrsdrm-arch](https://github.com/kmrsdrm-arch)
- Repository: [vortex-automotive-analytics](https://github.com/kmrsdrm-arch/vortex-automotive-analytics)

---

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [OpenAI](https://openai.com/)
- [LangChain](https://langchain.com/)
- [Plotly](https://plotly.com/)

---

## ⭐ Show Your Support

If you find this project helpful, please consider giving it a star on GitHub!

---

**Happy Analyzing! 📊🚀**
