# Seed Database - PowerShell Commands (FIXED)

## Method 1: Simple One-Line Command (EASIEST)

Copy and paste this ENTIRE command as ONE line in PowerShell:

```powershell
Invoke-RestMethod -Uri "https://vortex-automotive-analytics-1.onrender.com/api/v1/data/seed" -Method Post -ContentType "application/json" -Body '{"num_vehicles":100,"num_sales":10000,"months_back":24}'
```

---

## Method 2: Using Here-String (If Method 1 fails)

Copy and paste this in PowerShell:

```powershell
$body = @"
{
  "num_vehicles": 100,
  "num_sales": 10000,
  "months_back": 24
}
"@

Invoke-RestMethod -Uri "https://vortex-automotive-analytics-1.onrender.com/api/v1/data/seed" -Method Post -ContentType "application/json" -Body $body
```

---

## Method 3: Using curl (Windows Built-in)

Copy and paste this in PowerShell:

```powershell
curl.exe -X POST "https://vortex-automotive-analytics-1.onrender.com/api/v1/data/seed" -H "Content-Type: application/json" -d "{\"num_vehicles\":100,\"num_sales\":10000,\"months_back\":24}"
```

**Note:** Use `curl.exe` (not just `curl`) to avoid PowerShell alias issues.

---

## Method 4: Step-by-Step (Most Reliable)

Run these commands ONE AT A TIME:

```powershell
$url = "https://vortex-automotive-analytics-1.onrender.com/api/v1/data/seed"
```

```powershell
$json = '{"num_vehicles":100,"num_sales":10000,"months_back":24}'
```

```powershell
$response = Invoke-RestMethod -Uri $url -Method Post -ContentType "application/json" -Body $json
```

```powershell
$response
```

---

## Method 5: Using Invoke-WebRequest (Alternative)

```powershell
$response = Invoke-WebRequest -Uri "https://vortex-automotive-analytics-1.onrender.com/api/v1/data/seed" -Method Post -ContentType "application/json" -Body '{"num_vehicles":100,"num_sales":10000,"months_back":24}'
$response.Content
```

---

## Expected Success Response

You should see something like:

```
success      : True
message      : Database seeded successfully
summary      : @{vehicles=100; inventory_records=100; sales_transactions=10000}
```

OR in JSON format:

```json
{
  "success": true,
  "message": "Database seeded successfully",
  "summary": {
    "vehicles": 100,
    "inventory_records": 100,
    "sales_transactions": 10000
  }
}
```

---

## Common Errors & Solutions

### Error: "Invoke-RestMethod : The remote name could not be resolved"

**Cause:** Network/DNS issue or API is sleeping

**Solution:** 
1. First wake up the API by visiting in browser: https://vortex-automotive-analytics-1.onrender.com/
2. Wait 60 seconds
3. Try the PowerShell command again

---

### Error: "400 Bad Request" or "Unprocessable Entity"

**Cause:** JSON formatting issue

**Solution:** Use **Method 2** (Here-String) or **Method 4** (Step-by-Step)

---

### Error: "curl : A positional parameter cannot be found"

**Cause:** PowerShell is using alias for curl, not real curl

**Solution:** Use `curl.exe` instead of `curl`, or use Invoke-RestMethod

---

### Error: Takes forever and times out

**Cause:** API is doing a cold start (takes 30-60 seconds)

**Solution:** 
- Be patient, wait up to 2 minutes
- The first request after sleep always takes longer
- You'll see the response once it completes

---

### Error: "ConvertTo-Json : Cannot bind argument to parameter 'InputObject'"

**Cause:** Response is already in correct format

**Solution:** Just run the command without piping to ConvertTo-Json

---

## Quick Test - Check if API is Awake

Run this first to wake up the API:

```powershell
Invoke-RestMethod -Uri "https://vortex-automotive-analytics-1.onrender.com/health"
```

Should return:
```
status
------
healthy
```

Then run the seed command.

---

## Alternative: Use Browser-Based Tool

If PowerShell continues to have issues, you can use:

### Option A: Use Browser Console (F12)

1. Visit: https://vortex-automotive-analytics-1.onrender.com/
2. Press F12 (open Developer Tools)
3. Go to "Console" tab
4. Paste this JavaScript code:

```javascript
fetch('https://vortex-automotive-analytics-1.onrender.com/api/v1/data/seed', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({num_vehicles: 100, num_sales: 10000, months_back: 24})
})
.then(r => r.json())
.then(data => console.log(data))
```

5. Press Enter
6. Wait for response in console

---

### Option B: Use Online API Tester

Visit: https://reqbin.com/

1. Select: **POST**
2. URL: `https://vortex-automotive-analytics-1.onrender.com/api/v1/data/seed`
3. Headers: Add `Content-Type: application/json`
4. Body (select JSON): 
```json
{
  "num_vehicles": 100,
  "num_sales": 10000,
  "months_back": 24
}
```
5. Click **Send**

---

## Recommended Approach

**TRY IN THIS ORDER:**

1. ✅ **Method 1** (Simple one-line) - Try first
2. ✅ **Method 4** (Step-by-step) - If Method 1 fails
3. ✅ **Method 3** (curl.exe) - If both above fail
4. ✅ **Browser Console** (F12) - If PowerShell doesn't work at all

---

## Verification After Seeding

Check if data was created:

```powershell
Invoke-RestMethod -Uri "https://vortex-automotive-analytics-1.onrender.com/api/v1/analytics/kpis"
```

Should return KPI data with actual numbers (not empty).

---

**Start with Method 1 above and let me know what error message you get if it fails!**

