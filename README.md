# ⚡ Vortex Automotive Analytics Platform - Next.js Edition

> **AI-Powered Automotive Intelligence Platform** with Real-Time Analytics, Natural Language Queries, and Predictive Insights

[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3-38bdf8)](https://tailwindcss.com/)
[![Vercel](https://img.shields.io/badge/Deploy-Vercel-black)](https://vercel.com)

---

## 🚀 Quick Deploy to Production

### Prerequisites
- [Vercel Account](https://vercel.com/signup) (free tier available)
- [OpenAI API Key](https://platform.openai.com/api-keys)
- GitHub/GitLab account

### 1. Deploy to Vercel (One-Click)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/vortex-analytics-nextjs)

**OR Manual Setup:**

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Vortex Analytics Next.js"
   git branch -M main
   git remote add origin https://github.com/your-username/vortex-analytics-nextjs.git
   git push -u origin main
   ```

2. **Import to Vercel:**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your GitHub repository
   - Vercel will auto-detect Next.js

3. **Add Vercel Postgres:**
   - In your Vercel project dashboard
   - Go to **Storage** tab
   - Click **Create Database** → Select **Postgres**
   - Click **Create** (free tier: 256 MB, 60 hours compute/month)
   - Database credentials are automatically added to your project

4. **Add Environment Variables:**
   - In Vercel project settings → **Environment Variables**
   - Add: `OPENAI_API_KEY` = `sk-your-key-here`
   - Database variables are auto-configured by Vercel Postgres

5. **Deploy:**
   - Click **Deploy**
   - Wait 2-3 minutes for build completion

### 2. Initialize Database

After deployment, run migrations and seed data:

```bash
# Install Vercel CLI (if not installed)
npm i -g vercel

# Link your project
vercel link

# Run migrations
vercel env pull .env.local
npm run db:migrate

# Seed database with sample data
npm run db:seed
```

**OR** use Vercel's built-in shell (recommended):
- Go to your project on Vercel
- Settings → Functions → Node.js Runtime
- Create an API route to run migrations (see below)

### 3. Access Your App

Your app will be live at: `https://your-project.vercel.app`

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    VORTEX PLATFORM                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Next.js 14 (App Router) ──► Server Actions            │
│       │                            │                     │
│       │                            ▼                     │
│       │                    Vercel Postgres              │
│       │                    (Drizzle ORM)                │
│       │                                                  │
│       ▼                            ▼                     │
│  React Components ──────────► OpenAI GPT-4             │
│  (Recharts + Shadcn/ui)      (Vercel AI SDK)           │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Next.js 14 + React | Server components, streaming |
| **Styling** | Tailwind CSS + Shadcn/ui | Executive-level UI/UX |
| **Database** | Vercel Postgres | Serverless PostgreSQL |
| **ORM** | Drizzle ORM | Type-safe database queries |
| **AI** | OpenAI GPT-4 + Vercel AI SDK | Natural language & insights |
| **Charts** | Recharts | Interactive visualizations |
| **Deployment** | Vercel | Zero-config deployment |

---

## 📁 Project Structure

```
vortex-analytics-nextjs/
├── app/                        # Next.js App Router
│   ├── page.tsx               # Dashboard (home)
│   ├── sales/                 # Sales analytics page
│   ├── inventory/             # Inventory page
│   ├── query/                 # NL Query page
│   ├── insights/              # AI Insights page
│   ├── reports/               # Report generation
│   ├── layout.tsx             # Root layout
│   └── globals.css            # Global styles
│
├── components/                 # React Components
│   ├── dashboard/             # Dashboard-specific components
│   ├── sidebar.tsx            # Navigation sidebar
│   ├── header.tsx             # Top header
│   └── ui/                    # Reusable UI components (Shadcn)
│
├── lib/                        # Core Libraries
│   ├── actions/               # Server Actions
│   │   ├── analytics.ts       # Analytics queries
│   │   ├── nlquery.ts         # Natural language queries
│   │   └── insights.ts        # AI insights & reports
│   ├── ai/                    # AI/LLM Integration
│   │   └── openai.ts          # OpenAI client
│   ├── db/                    # Database
│   │   ├── schema.ts          # Drizzle schema
│   │   ├── index.ts           # DB instance
│   │   ├── migrate.ts         # Migrations
│   │   └── seed.ts            # Seed data
│   └── utils.ts               # Utility functions
│
├── package.json               # Dependencies
├── tsconfig.json              # TypeScript config
├── tailwind.config.ts         # Tailwind config
├── drizzle.config.ts          # Drizzle config
├── vercel.json                # Vercel config
└── README.md                  # This file
```

---

## 🎯 Key Features

### 📊 Executive Dashboard
- **Real-time KPIs**: Revenue, units sold, conversion rates, avg deal size
- **Interactive Charts**: Sales trends, top vehicles, regional performance
- **Inventory Status**: Low stock alerts, category breakdown
- **Vortex Theme**: Premium dark UI with cyan-purple-pink gradient

### 💰 Sales Analytics
- **Comprehensive Metrics**: Sales totals, growth rates
- **Time-Series Analysis**: Daily trends over 30/60/90 days
- **Regional Breakdown**: Performance by geography
- **Top Performers**: Best-selling vehicles and categories

### 📦 Inventory Analytics
- **Real-time Tracking**: Stock levels across warehouses
- **Low Stock Alerts**: Automated notifications
- **Value Calculation**: Total inventory value
- **Status Indicators**: In stock, low stock, out of stock

### 💬 Natural Language Queries
- **Ask in Plain English**: "What were sales last month?"
- **AI-Powered SQL**: GPT-4 generates optimized queries
- **Interactive Results**: Table format with execution time
- **Example Queries**: Pre-populated for quick testing

### 🤖 AI-Generated Insights
- **Strategic Analysis**: Pattern detection and trends
- **Recommendations**: Data-driven suggestions
- **Executive Summary**: Key takeaways and action items
- **Real-time Generation**: Fresh insights on demand

### 📄 Report Generation
- **Executive Reports**: Concise one-page summaries
- **Detailed Reports**: Comprehensive analysis
- **AI-Generated**: GPT-4 powered narratives
- **Downloadable**: Export as Markdown

---

## 🛠️ Local Development

### Prerequisites
- Node.js 18+ 
- npm/yarn/pnpm

### Setup

```bash
# 1. Clone repository
git clone <your-repo>
cd vortex-analytics-nextjs

# 2. Install dependencies
npm install

# 3. Setup environment variables
cp .env.example .env.local

# Edit .env.local and add:
# - POSTGRES_URL (from Vercel or local PostgreSQL)
# - OPENAI_API_KEY

# 4. Run migrations
npm run db:migrate

# 5. Seed database
npm run db:seed

# 6. Start development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

---

## 🎨 UI/UX Features

### Vortex Dark Theme
- **Color Palette**: 
  - Cyan: `#00d4ff` 
  - Purple: `#7b2ff7`
  - Pink: `#f026ff`
- **Full-Width Layout**: Utilizes entire viewport
- **Glass-morphism**: Frosted glass card effects with backdrop blur
- **Smooth Animations**: Fade-ins, hover effects, loading states
- **Premium Typography**: Orbitron (headers) + Inter (body)

### Chart Enhancements
- **Modern Design**: Gradient fills and smooth curves
- **Interactive Tooltips**: Formatted values and context
- **Responsive**: Adapts to all screen sizes
- **Color Coordination**: Matches Vortex gradient theme

---

## 🔧 Configuration

### Environment Variables

```bash
# Database (Auto-configured by Vercel Postgres)
POSTGRES_URL=
POSTGRES_PRISMA_URL=
POSTGRES_URL_NON_POOLING=
POSTGRES_USER=
POSTGRES_HOST=
POSTGRES_PASSWORD=
POSTGRES_DATABASE=

# OpenAI API
OPENAI_API_KEY=sk-your-key-here

# App Config (optional)
NEXT_PUBLIC_APP_URL=https://your-domain.vercel.app
```

---

## 📊 Database Schema

### Core Tables

**vehicles**
- id, vin, make, model, year, category, msrp, specifications

**sales**
- id, vehicle_id, sale_date, quantity, total_amount, customer_segment, region

**inventory**
- id, vehicle_id, warehouse, region, quantity_available, status

**insights_history**
- id, insight_type, title, description, confidence, context

**query_history**
- id, user_query, generated_sql, query_results, execution_time

---

## 🚀 Production Deployment Guide

### Option 1: One-Click Deploy (Easiest)

1. Click the "Deploy with Vercel" button at the top
2. Connect your GitHub account
3. Configure environment variables
4. Deploy!

### Option 2: Manual Deploy (Full Control)

1. **Create Vercel Account**: [vercel.com/signup](https://vercel.com/signup)

2. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Add Postgres Database**:
   - Dashboard → Storage → Create Database → Postgres
   - Auto-links to your project

5. **Set Environment Variables**:
   ```bash
   vercel env add OPENAI_API_KEY
   ```

6. **Run Migrations**:
   Create `app/api/migrate/route.ts`:
   ```typescript
   import { NextResponse } from "next/server";
   import { sql } from "@vercel/postgres";

   export async function GET() {
     try {
       // Run your migration SQL here
       return NextResponse.json({ success: true });
     } catch (error) {
       return NextResponse.json({ error }, { status: 500 });
     }
   }
   ```

   Then visit: `https://your-app.vercel.app/api/migrate`

7. **Seed Database**:
   Similar approach - create API route and visit URL

---

## 💡 Best Practices

### Performance
- **Server Components**: Default to server components for better performance
- **Streaming**: Use Suspense for progressive rendering
- **Edge Runtime**: Consider edge functions for global low latency

### Security
- **Environment Variables**: Never commit `.env` files
- **API Keys**: Store in Vercel environment variables
- **SQL Injection**: Use parameterized queries (Drizzle handles this)

### Monitoring
- **Vercel Analytics**: Enable in project settings
- **Error Tracking**: Add Sentry or similar
- **Database Monitoring**: Use Vercel Postgres dashboard

---

## 🐛 Troubleshooting

### Database Connection Issues
- Verify `POSTGRES_URL` is set correctly
- Check Vercel Postgres dashboard for status
- Ensure migrations have run

### OpenAI API Errors
- Verify API key is valid
- Check usage limits on OpenAI dashboard
- Ensure sufficient credits

### Build Failures
- Check build logs in Vercel dashboard
- Verify all dependencies are in `package.json`
- Ensure TypeScript errors are resolved

---

## 📈 Roadmap

- [x] Core analytics dashboard
- [x] Natural language queries
- [x] AI-powered insights
- [x] Report generation
- [x] Executive-level UI/UX
- [x] Vercel deployment ready
- [ ] Real-time WebSocket updates
- [ ] Mobile responsive design
- [ ] PDF export functionality
- [ ] Email report scheduling
- [ ] Multi-tenancy support
- [ ] Advanced forecasting models

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 🆘 Support

### Resources
- **Next.js Docs**: [nextjs.org/docs](https://nextjs.org/docs)
- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **Drizzle ORM**: [orm.drizzle.team](https://orm.drizzle.team)
- **OpenAI API**: [platform.openai.com/docs](https://platform.openai.com/docs)
- **Tailwind CSS**: [tailwindcss.com/docs](https://tailwindcss.com/docs)

---

## 🎉 Success!

Your Vortex Automotive Analytics Platform is ready for production!

```
┌─────────────────────────────────────────────────┐
│  ⚡ VORTEX AUTOMOTIVE ANALYTICS PLATFORM       │
│                                                  │
│  ✅ Next.js 14 with App Router                 │
│  ✅ Executive-Level UI/UX Design               │
│  ✅ AI-Powered Natural Language Queries        │
│  ✅ Real-Time Analytics Dashboard               │
│  ✅ Vercel One-Click Deployment                │
│  ✅ Serverless PostgreSQL Database             │
│                                                  │
│  Transform Automotive Data into Strategic       │
│  Competitive Advantage                          │
└─────────────────────────────────────────────────┘
```

**Built with ❤️ using Next.js, TypeScript, Tailwind CSS, and OpenAI GPT-4**

---

*Version: 3.0.0 (Production)*  
*Last Updated: November 26, 2025*
