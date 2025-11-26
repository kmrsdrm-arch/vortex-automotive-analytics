# 🚀 Production Deployment Guide

## Step-by-Step Deployment to Vercel

### ⚡ Quick Start (5 Minutes)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Vortex Analytics"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/vortex-analytics.git
   git push -u origin main
   ```

2. **Deploy to Vercel**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Click **Import Project**
   - Select your GitHub repository
   - Vercel auto-detects Next.js configuration
   - Click **Deploy**

3. **Add Vercel Postgres** (30 seconds)
   - In your Vercel project dashboard
   - Go to **Storage** tab
   - Click **Create Database**
   - Select **Postgres**
   - Choose **Continue** (Free tier is fine)
   - Database credentials automatically added to your project ✨

4. **Add OpenAI API Key**
   - Go to **Settings** → **Environment Variables**
   - Add new variable:
     - Name: `OPENAI_API_KEY`
     - Value: `sk-your-openai-key`
   - Click **Save**
   - Redeploy (Vercel will prompt you)

5. **Initialize Database** (Important!)

   **Option A: Using API Route (Recommended)**
   
   Create this file in your project:
   
   ```typescript
   // app/api/setup/route.ts
   import { NextResponse } from "next/server";
   import { sql } from "@vercel/postgres";

   export async function GET(request: Request) {
     const { searchParams } = new URL(request.url);
     const secret = searchParams.get('secret');
     
     // Simple security - use a secret parameter
     if (secret !== 'YOUR_SECRET_KEY') {
       return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
     }

     try {
       // Run migrations
       await sql`
         CREATE TABLE IF NOT EXISTS vehicles (
           id SERIAL PRIMARY KEY,
           vin VARCHAR(17) UNIQUE NOT NULL,
           make VARCHAR(50) NOT NULL,
           model VARCHAR(50) NOT NULL,
           year INTEGER NOT NULL,
           category VARCHAR(50) NOT NULL,
           msrp DECIMAL(12, 2) NOT NULL,
           specifications JSONB,
           created_at TIMESTAMP DEFAULT NOW() NOT NULL
         )
       `;

       await sql`
         CREATE TABLE IF NOT EXISTS sales (
           id SERIAL PRIMARY KEY,
           vehicle_id INTEGER REFERENCES vehicles(id) NOT NULL,
           sale_date TIMESTAMP NOT NULL,
           quantity INTEGER DEFAULT 1 NOT NULL,
           total_amount DECIMAL(12, 2) NOT NULL,
           customer_segment VARCHAR(50),
           region VARCHAR(50) NOT NULL,
           dealer_name VARCHAR(100),
           created_at TIMESTAMP DEFAULT NOW() NOT NULL
         )
       `;

       await sql`
         CREATE TABLE IF NOT EXISTS inventory (
           id SERIAL PRIMARY KEY,
           vehicle_id INTEGER REFERENCES vehicles(id) NOT NULL,
           warehouse VARCHAR(100) NOT NULL,
           region VARCHAR(50) NOT NULL,
           quantity_available INTEGER DEFAULT 0 NOT NULL,
           status VARCHAR(20) DEFAULT 'in_stock' NOT NULL,
           last_updated TIMESTAMP DEFAULT NOW() NOT NULL
         )
       `;

       await sql`CREATE INDEX IF NOT EXISTS idx_sale_date ON sales(sale_date)`;
       await sql`CREATE INDEX IF NOT EXISTS idx_region ON sales(region)`;

       return NextResponse.json({ 
         success: true, 
         message: 'Database initialized successfully!' 
       });
     } catch (error: any) {
       return NextResponse.json({ 
         error: error.message 
       }, { status: 500 });
     }
   }
   ```

   Then visit: `https://your-app.vercel.app/api/setup?secret=YOUR_SECRET_KEY`

   **Option B: Using Vercel CLI**
   
   ```bash
   # Install Vercel CLI
   npm i -g vercel

   # Login
   vercel login

   # Link your project
   vercel link

   # Pull environment variables
   vercel env pull .env.local

   # Run migrations locally (connected to production DB)
   npm run db:migrate
   ```

6. **Seed Database** (Generate sample data)

   Create another API route:

   ```typescript
   // app/api/seed/route.ts
   import { NextResponse } from "next/server";
   import { db, vehicles, sales, inventory } from "@/lib/db";
   // Import your seed logic here

   export const maxDuration = 300; // 5 minutes for seeding

   export async function GET(request: Request) {
     const { searchParams } = new URL(request.url);
     const secret = searchParams.get('secret');
     
     if (secret !== 'YOUR_SECRET_KEY') {
       return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
     }

     try {
       // Run your seed logic
       // (Copy from lib/db/seed.ts)
       
       return NextResponse.json({ 
         success: true, 
         message: 'Database seeded successfully!' 
       });
     } catch (error: any) {
       return NextResponse.json({ 
         error: error.message 
       }, { status: 500 });
     }
   }
   ```

   Then visit: `https://your-app.vercel.app/api/seed?secret=YOUR_SECRET_KEY`

7. **Done! 🎉**
   - Visit your app: `https://your-project.vercel.app`
   - Dashboard should show data
   - Try natural language queries
   - Generate AI insights

---

## 📋 Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Project imported to Vercel
- [ ] Vercel Postgres database created
- [ ] `OPENAI_API_KEY` environment variable added
- [ ] Database migrations run
- [ ] Database seeded with sample data
- [ ] App tested in production
- [ ] Custom domain configured (optional)

---

## 🔧 Post-Deployment Configuration

### Custom Domain (Optional)

1. Go to **Settings** → **Domains**
2. Add your custom domain
3. Follow DNS configuration instructions
4. SSL certificate is automatically provisioned

### Environment Variables for Production

```bash
# Required
OPENAI_API_KEY=sk-your-key

# Auto-configured by Vercel Postgres
POSTGRES_URL=postgres://...
POSTGRES_PRISMA_URL=postgres://...
POSTGRES_URL_NON_POOLING=postgres://...

# Optional
NEXT_PUBLIC_APP_URL=https://your-domain.com
```

### Enable Analytics

1. Go to **Analytics** tab in Vercel dashboard
2. Click **Enable Analytics**
3. Free tier: 100k events/month

---

## 🎯 Testing Your Deployment

### 1. Test Dashboard
- Visit homepage
- Check if KPIs load
- Verify charts render
- Test date range selector

### 2. Test Natural Language Query
- Go to `/query`
- Try: "What were total sales last month?"
- Verify SQL generation and results

### 3. Test AI Insights
- Go to `/insights`
- Click "Generate Insights"
- Wait for AI analysis
- Verify insights display

### 4. Test Reports
- Go to `/reports`
- Generate executive or detailed report
- Try downloading

---

## 🐛 Common Issues & Solutions

### Issue: "Database connection failed"
**Solution:**
- Verify Vercel Postgres is linked to your project
- Check environment variables are set
- Redeploy after adding database

### Issue: "OpenAI API error"
**Solution:**
- Verify `OPENAI_API_KEY` is set correctly
- Check API key has credits
- Ensure no extra spaces in the key

### Issue: "No data showing on dashboard"
**Solution:**
- Run database migrations first
- Seed database with sample data
- Check browser console for errors

### Issue: "Build failed"
**Solution:**
- Check build logs in Vercel dashboard
- Ensure all imports are correct
- Verify TypeScript has no errors
- Run `npm run build` locally to test

### Issue: "Function timeout"
**Solution:**
- Add `export const maxDuration = 60;` to slow routes
- For free tier, max is 10s (upgrade for more)

---

## 📊 Monitoring & Maintenance

### View Logs
- Vercel dashboard → **Deployments** → Select deployment → **Logs**
- Real-time function logs available

### Database Management
- Vercel dashboard → **Storage** → Your database
- View usage, connection pool, queries
- Access pgAdmin for direct queries

### Performance Monitoring
- Enable Vercel Analytics for:
  - Page views
  - Core Web Vitals
  - User geography
  - Device breakdown

---

## 🚀 Advanced: Production Optimizations

### 1. Enable Caching

```typescript
// In your server actions
export const revalidate = 60; // Cache for 60 seconds

// Or per-route
export const dynamic = 'force-static'; // Static generation
```

### 2. Image Optimization

Use Next.js Image component:
```typescript
import Image from 'next/image';
```

### 3. Database Connection Pooling

Already configured via Vercel Postgres connection pooling.

### 4. Edge Functions (Optional)

For global low latency:
```typescript
export const runtime = 'edge';
```

---

## 💰 Cost Estimates

### Free Tier (Hobby Plan)
- **Vercel Hosting**: Free
  - 100GB bandwidth/month
  - 100k function invocations/month
  - 100 hours serverless function execution

- **Vercel Postgres**: Free
  - 256 MB storage
  - 60 hours compute/month
  - 256 MB bandwidth/month

- **OpenAI API**: Pay-as-you-go
  - GPT-4 Turbo: ~$0.01/request
  - Estimate: $10-20/month for moderate use

**Total: ~$10-20/month** (mostly OpenAI)

### Pro Plan ($20/month)
- 1TB bandwidth
- Unlimited function invocations
- Better database (512MB storage, 100 hours compute)
- Team collaboration features

---

## 🎓 Next Steps

1. **Customize Branding**
   - Update colors in `tailwind.config.ts`
   - Replace logo in `components/sidebar.tsx`
   - Modify metadata in `app/layout.tsx`

2. **Add Authentication**
   - Use NextAuth.js or Clerk
   - Protect routes with middleware

3. **Add More Features**
   - Export to PDF/Excel
   - Email reports
   - Real-time notifications
   - Advanced forecasting

4. **Scale Up**
   - Upgrade Vercel plan for more resources
   - Add Redis for caching
   - Implement rate limiting

---

## 📞 Support

- **Vercel Support**: [vercel.com/support](https://vercel.com/support)
- **Next.js Docs**: [nextjs.org/docs](https://nextjs.org/docs)
- **Vercel Discord**: [vercel.com/discord](https://vercel.com/discord)

---

**🎉 Congratulations! Your Vortex Analytics Platform is now live in production!**

