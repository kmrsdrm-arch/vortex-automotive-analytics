# Changelog

All notable changes to the VORTEX Automotive Intelligence Platform.

## [3.0.0] - 2024-11-25

### 🚀 Major Refactoring for Vercel Deployment

#### Added
- Consolidated comprehensive `README.md` with all deployment instructions
- Optimized `vercel.json` for serverless deployment
- Clean `api/index.py` entry point for Vercel functions
- `.vercelignore` for optimized deployments

#### Changed
- **Simplified documentation structure**: Single README instead of 12+ separate .md files
- **Removed platform-specific configs**: Focused on Vercel deployment
- **Optimized dependencies**: Streamlined `requirements.txt`
- **Updated project structure**: Clean, production-ready codebase

#### Removed
- ❌ Redundant deployment guides (12 files consolidated into README.md)
- ❌ Windows-specific `.bat` files (start.bat, test_api.bat, push-to-github.bat)
- ❌ Alternative platform configs (render.yaml, railway.json)
- ❌ Empty/unused Dockerfiles
- ❌ Temporary troubleshooting files

#### Migration Notes
- All deployment instructions now in `README.md`
- Vercel deployment is primary focus
- Dashboard still deploys to Streamlit Cloud
- Database uses Neon (serverless PostgreSQL)

---

## [2.0.0] - 2024-11-24

### Added
- Multiple deployment options (Vercel, Render, Railway)
- Comprehensive deployment guides
- Natural language query interface
- AI-powered insights generation
- Automated report generation

### Changed
- Migrated to FastAPI from Flask
- Added Streamlit dashboard
- Integrated OpenAI GPT-4

---

## [1.0.0] - 2024-11-01

### Initial Release
- FastAPI backend
- PostgreSQL database
- Basic analytics endpoints
- SQLAlchemy ORM
- Alembic migrations

---

**Semantic Versioning**: MAJOR.MINOR.PATCH
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes
