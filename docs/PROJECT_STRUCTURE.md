# 📁 VORTEX - Project Structure

Clean, production-ready file organization.

---

## 🏗️ Directory Structure

```
vortex-automotive-analytics/
│
├── 📄 Core Configuration
│   ├── .env                        # Environment variables (gitignored)
│   ├── environment.example         # Environment template
│   ├── .gitignore                 # Git ignore rules
│   ├── requirements.txt           # Python dependencies
│   ├── requirements-vercel.txt    # Vercel-specific dependencies
│   └── pyproject.toml             # Project metadata
│
├── 🚀 Deployment
│   ├── vercel.json                # Vercel configuration
│   ├── docker-compose.yml         # Docker setup (local dev)
│   ├── Dockerfile                 # Docker image (API)
│   └── api/
│       └── index.py              # Vercel serverless entry point
│
├── 📚 Documentation
│   ├── README.md                  # Main documentation
│   ├── DEPLOY_NOW.md             # Production deployment guide
│   ├── VERCEL_QUICKSTART.md      # Quick deployment steps
│   ├── VERCEL_DEPLOYMENT_GUIDE.md # Detailed deployment
│   ├── CHANGELOG.md              # Version history
│   └── docs/
│       └── PROJECT_STRUCTURE.md  # This file
│
├── 🔧 Scripts
│   ├── scripts/
│   │   ├── init_db.py           # Database initialization
│   │   ├── seed_data.py         # Sample data generator
│   │   └── run_pipeline.py      # Data pipeline runner
│   └── start.bat                # Local development startup (Windows)
│
├── ⚙️ Configuration
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py          # App settings (Pydantic)
│   │   ├── database.py          # Database configuration
│   │   └── logging_config.py    # Logging setup
│   │
│   ├── alembic/                 # Database migrations
│   │   └── env.py
│   └── alembic.ini              # Alembic configuration
│
├── 📦 Source Code
│   └── src/
│       │
│       ├── 🌐 API (FastAPI Backend)
│       │   └── api/
│       │       ├── main.py              # API entry point
│       │       ├── dependencies.py      # Dependency injection
│       │       ├── middleware.py        # Custom middleware
│       │       │
│       │       ├── routes/              # API endpoints
│       │       │   ├── health.py        # Health checks
│       │       │   ├── analytics.py     # Analytics endpoints
│       │       │   ├── data.py          # Data endpoints
│       │       │   ├── insights.py      # AI insights
│       │       │   ├── query.py         # NL query
│       │       │   └── reports.py       # Report generation
│       │       │
│       │       └── schemas/             # Pydantic models
│       │           ├── common.py        # Shared schemas
│       │           ├── requests.py      # Request models
│       │           └── responses.py     # Response models
│       │
│       ├── 📊 Dashboard (Streamlit Frontend)
│       │   └── dashboard/
│       │       ├── app.py               # Main dashboard entry
│       │       │
│       │       ├── pages/               # Dashboard pages
│       │       │   ├── 00_Dashboard_Summary.py
│       │       │   ├── 0_About.py
│       │       │   ├── 1_Sales_Analytics.py
│       │       │   ├── 2_Inventory_Analytics.py
│       │       │   ├── 3_NL_Query.py
│       │       │   ├── 4_Insights.py
│       │       │   └── 5_Reports.py
│       │       │
│       │       ├── components/          # Reusable UI components
│       │       │   ├── charts.py        # Chart components
│       │       │   ├── header.py        # Header component
│       │       │   ├── metrics.py       # Metric displays
│       │       │   └── page_header.py   # Page headers
│       │       │
│       │       ├── styles/              # Styling
│       │       │   └── theme.py         # Dark theme
│       │       │
│       │       ├── utils/               # Dashboard utilities
│       │       │   ├── api_client.py    # API client
│       │       │   └── formatters.py    # Data formatters
│       │       │
│       │       └── assets/              # Static assets
│       │           └── logo.svg         # App logo
│       │
│       ├── 🗄️ Database
│       │   └── database/
│       │       ├── connection.py        # DB connection
│       │       ├── session.py           # Session management
│       │       │
│       │       ├── models/              # SQLAlchemy models
│       │       │   ├── base.py          # Base model
│       │       │   ├── vehicle.py       # Vehicle model
│       │       │   ├── sales.py         # Sales model
│       │       │   ├── inventory.py     # Inventory model
│       │       │   └── analytics.py     # Analytics model
│       │       │
│       │       └── repositories/        # Data access layer
│       │           ├── base.py          # Base repository
│       │           ├── vehicle_repo.py  # Vehicle repository
│       │           ├── sales_repo.py    # Sales repository
│       │           └── inventory_repo.py # Inventory repository
│       │
│       ├── 🤖 AI/ML Integration
│       │   └── llm/
│       │       ├── core/                # Core LLM functionality
│       │       │   ├── client.py        # OpenAI client
│       │       │   ├── embeddings.py    # Embedding generation
│       │       │   └── prompts.py       # Prompt templates
│       │       │
│       │       └── services/            # LLM services
│       │           ├── nl_query_service.py    # Natural language queries
│       │           ├── insights_service.py    # Insight generation
│       │           ├── report_service.py      # Report generation
│       │           └── rag_service.py         # RAG implementation
│       │
│       ├── 📈 Analytics
│       │   └── analytics/
│       │       ├── kpi_calculator.py    # KPI calculations
│       │       ├── sales_analytics.py   # Sales analysis
│       │       ├── inventory_analytics.py # Inventory analysis
│       │       └── trend_analyzer.py    # Trend analysis
│       │
│       ├── 🔄 Data Pipeline
│       │   └── pipeline/
│       │       ├── pipeline_manager.py  # Pipeline orchestration
│       │       │
│       │       ├── extractors/          # Data extraction
│       │       │   └── data_extractor.py
│       │       │
│       │       ├── transformers/        # Data transformation
│       │       │   ├── data_cleaner.py
│       │       │   └── aggregator.py
│       │       │
│       │       └── loaders/             # Data loading
│       │           └── data_loader.py
│       │
│       ├── 🎲 Data Generation
│       │   └── data_generation/
│       │       ├── synthetic_data.py    # Synthetic data generator
│       │       ├── seeder.py           # Database seeder
│       │       └── schemas.py          # Data schemas
│       │
│       └── 🛠️ Utilities
│           └── utils/
│               ├── exceptions.py        # Custom exceptions
│               ├── helpers.py          # Helper functions
│               ├── logger.py           # Logging utilities
│               └── validators.py       # Data validators
│
├── 🧪 Tests
│   └── tests/
│       ├── conftest.py                  # Test configuration
│       └── ...                          # Test files
│
└── 📁 Data & Logs (gitignored)
    ├── data/
    │   └── chromadb/                    # Vector database
    └── logs/
        └── app.log                      # Application logs
```

---

## 📄 Key Files Explained

### Configuration Files

| File | Purpose |
|------|---------|
| `environment.example` | Template for environment variables |
| `requirements.txt` | Python dependencies for local/production |
| `requirements-vercel.txt` | Optimized dependencies for Vercel |
| `vercel.json` | Vercel deployment configuration |
| `docker-compose.yml` | Docker services (local development) |

### Entry Points

| File | Purpose |
|------|---------|
| `src/api/main.py` | FastAPI application entry point |
| `src/dashboard/app.py` | Streamlit dashboard entry point |
| `api/index.py` | Vercel serverless function entry |
| `start.bat` | Local development startup script |

### Documentation

| File | Purpose |
|------|---------|
| `README.md` | Main project documentation |
| `DEPLOY_NOW.md` | Production deployment guide |
| `VERCEL_QUICKSTART.md` | Quick deployment steps |
| `VERCEL_DEPLOYMENT_GUIDE.md` | Detailed deployment instructions |
| `CHANGELOG.md` | Version history and changes |

### Scripts

| File | Purpose |
|------|---------|
| `scripts/init_db.py` | Initialize database schema |
| `scripts/seed_data.py` | Generate and load sample data |
| `scripts/run_pipeline.py` | Run data processing pipeline |

---

## 🎯 Clean Architecture Principles

### 1. Separation of Concerns
- **API** (`src/api/`) - REST endpoints and business logic
- **Dashboard** (`src/dashboard/`) - User interface
- **Database** (`src/database/`) - Data persistence
- **LLM** (`src/llm/`) - AI functionality
- **Analytics** (`src/analytics/`) - Business analytics

### 2. Dependency Injection
- `src/api/dependencies.py` - Centralized dependency management
- Repository pattern for data access
- Service layer for business logic

### 3. Configuration Management
- Environment-based configuration (`config/settings.py`)
- Type-safe settings with Pydantic
- Centralized logging configuration

### 4. Modular Design
- Each module has clear responsibilities
- Minimal coupling between modules
- Easy to test and maintain

---

## 🚫 What's NOT in the Repository

These files are gitignored for security and performance:

```
.env                    # Secrets and API keys
venv/                   # Virtual environment
__pycache__/           # Python bytecode
*.pyc                  # Compiled Python
logs/                  # Log files
data/chromadb/         # Vector database
.DS_Store              # Mac OS files
Thumbs.db              # Windows files
```

---

## 📝 File Naming Conventions

- **Python files**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions/variables**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Components**: `descriptive_name.py`
- **Markdown files**: `UPPER_CASE.md` or `Title_Case.md`

---

## 🔄 Development Workflow

1. **Local Development**: `start.bat` or manual startup
2. **Testing**: `pytest` in root directory
3. **Commit Changes**: `git commit -m "message"`
4. **Push to GitHub**: `git push origin main`
5. **Auto-Deploy**: Vercel/Streamlit Cloud auto-deploys

---

## 🎨 Code Organization Best Practices

### ✅ DO
- Keep files focused and single-purpose
- Use meaningful, descriptive names
- Follow Python PEP 8 style guide
- Document complex logic with docstrings
- Keep functions small and testable

### ❌ DON'T
- Mix concerns in single file
- Use abbreviations in names
- Hardcode configuration values
- Create deep nesting (>3 levels)
- Leave commented-out code

---

## 🚀 Adding New Features

### Adding a New API Endpoint

1. Create route in `src/api/routes/`
2. Define schemas in `src/api/schemas/`
3. Add business logic in appropriate service
4. Register route in `src/api/main.py`
5. Update API documentation

### Adding a New Dashboard Page

1. Create page in `src/dashboard/pages/`
2. Use naming: `N_Page_Name.py` (N = order number)
3. Import shared components from `components/`
4. Use `api_client` for API calls
5. Follow existing styling patterns

---

## 📚 Further Reading

- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

---

**Last Updated**: November 2025  
**VORTEX v2.0** - Production-Ready Architecture

