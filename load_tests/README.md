# NyayaSetu AI - K6 Load Testing Suite

This directory contains automated performance, load, stress, and spike test scripts for the NyayaSetu AI backend using **k6**.

---

## 🚀 Quick Start

### 1. Ensure the Django Backend is Running
Open a separate PowerShell terminal and start the server:

```powershell
cd "c:\Users\anikd\OneDrive\Desktop\SARAL project\NayaSetu\backend"
.\venv\Scripts\Activate.ps1
python manage.py runserver 8001
```
*(Make sure `http://127.0.0.1:8001/api/health/` returns 200 OK)*

---

### 2. Run Tests

Navigate to the `load_tests` directory:

```powershell
cd "c:\Users\anikd\OneDrive\Desktop\SARAL project\NayaSetu\load_tests"
```

#### A. Smoke Test (Quick 15s Verification)
Validates that endpoints are healthy and contracts are working properly before heavy tests:
```powershell
k6 run smoke-test.js
```
*Generates:* `smoke-summary.html`

#### B. Realistic Load Test (3.5 Minutes)
Simulates realistic citizen flows (Browsing schemes, searching, filtering, scheme details, eligibility wizard) ramping from 0 to 25 concurrent virtual users:
```powershell
k6 run load-test.js
```
*Generates:* `load-summary.html`

#### C. Stress Test (4 Minutes)
Tests system limits and breaking points by ramping up to 100 concurrent virtual users:
```powershell
k6 run stress-test.js
```
*Generates:* `stress-summary.html`

#### D. Spike Test (1.5 Minutes)
Simulates a sudden flood of users (e.g. following a viral news announcement or Duare Sarkar camp opening):
```powershell
k6 run spike-test.js
```
*Generates:* `spike-summary.html`

---

## 🛠️ Handy K6 CLI Options

You can override virtual users, duration, or the target URL without modifying scripts:

- **Quick custom run with 10 virtual users for 30 seconds**:
  ```powershell
  k6 run --vus 10 --duration 30s smoke-test.js
  ```

- **Target a staging or remote server**:
  ```powershell
  k6 run -e BASE_URL=https://api.yourdomain.com load-test.js
  ```

- **Output results to JSON for CI/CD or logging**:
  ```powershell
  k6 run --out json=results.json load-test.js
  ```

---

## 📊 Viewing Test Reports

Each test automatically generates an interactive HTML summary file (`smoke-summary.html`, `load-summary.html`, etc.). You can open it in your browser:

```powershell
# Open in default browser on Windows
Start-Process "smoke-summary.html"
Start-Process "load-summary.html"
```

---

## 📈 Key Metrics Guide

| Metric | Meaning | Healthy Target |
| :--- | :--- | :--- |
| `http_req_duration` | Total round-trip time for requests | **p(95) < 500ms** |
| `http_req_failed` | Percentage of failed requests (non-2xx/3xx) | **< 1.00%** |
| `http_reqs` | Total number of HTTP requests processed | Higher = better throughput |
| `vus` | Active concurrent Virtual Users | Monitored according to stage |
| `http_req_waiting` | Time to First Byte (TTFB) / server compute time | Lower = fast Django views/DB |
