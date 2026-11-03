// Shared configuration & test data for NyayaSetu AI Load Tests
export const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:8001';

export const HEADERS = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
};

// Realistic citizen demographic profiles for testing Eligibility Wizard
export const ELIGIBILITY_PROFILES = [
  {
    age: 29,
    gender: 'female',
    caste: 'SC',
    annual_family_income: 72000,
    has_land: false,
    is_student: false,
  },
  {
    age: 42,
    gender: 'male',
    caste: 'General',
    annual_family_income: 110000,
    has_land: true,
    is_student: false,
  },
  {
    age: 64,
    gender: 'male',
    caste: 'ST',
    annual_family_income: 40000,
    has_land: false,
    is_student: false,
  },
  {
    age: 19,
    gender: 'female',
    caste: 'OBC',
    annual_family_income: 60000,
    has_land: false,
    is_student: true,
  },
  {
    age: 24,
    gender: 'female',
    caste: 'General',
    annual_family_income: 80000,
    has_land: false,
    is_student: false,
  },
];

export const SEARCH_KEYWORDS = ['annapurna', 'women', 'pension', 'student', 'bandhu', 'krishak', 'card'];
export const CATEGORIES = ['women', 'agriculture', 'education', 'tribal_caste', 'health'];
export const SCHEME_SLUGS = ['annapurna-yojana', 'jai-johar', 'sikshashree', 'taposhili-bandhu', 'wb-student-credit-card'];

/**
 * Generates a clean standalone HTML summary report from k6 test results
 */
export function generateHtmlReport(data, testTitle = 'NyayaSetu AI - K6 Load Test Report') {
  const metrics = data.metrics || {};
  const httpReqs = metrics.http_reqs ? metrics.http_reqs.values.count : 0;
  const httpFailed = metrics.http_req_failed ? (metrics.http_req_failed.values.rate * 100).toFixed(2) : '0.00';
  const durationAvg = metrics.http_req_duration ? metrics.http_req_duration.values.avg.toFixed(1) : 0;
  const durationP95 = metrics.http_req_duration ? metrics.http_req_duration.values['p(95)'].toFixed(1) : 0;
  const durationMax = metrics.http_req_duration ? metrics.http_req_duration.values.max.toFixed(1) : 0;
  const vusMax = metrics.vus_max ? metrics.vus_max.values.max : 0;
  const iterations = metrics.iterations ? metrics.iterations.values.count : 0;

  const passedThresholds = Object.entries(data.thresholds || {}).filter(([_, v]) => v.ok).length;
  const totalThresholds = Object.keys(data.thresholds || {}).length;

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>${testTitle}</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 2rem; }
    .container { max-width: 900px; margin: 0 auto; }
    .header { border-bottom: 1px solid #334155; padding-bottom: 1.5rem; margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: center; }
    h1 { margin: 0; font-size: 1.75rem; color: #38bdf8; }
    .badge { padding: 0.35rem 0.8rem; border-radius: 9999px; font-size: 0.85rem; font-weight: 600; }
    .badge-pass { background: #065f46; color: #34d399; }
    .badge-warn { background: #854d0e; color: #facc15; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
    .card { background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 1.25rem; }
    .card-title { color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
    .card-val { font-size: 1.8rem; font-weight: 700; color: #ffffff; }
    .card-sub { font-size: 0.75rem; color: #64748b; margin-top: 0.35rem; }
    table { width: 100%; border-collapse: collapse; background: #1e293b; border-radius: 8px; overflow: hidden; margin-top: 1rem; }
    th, td { text-align: left; padding: 0.85rem 1rem; border-bottom: 1px solid #334155; font-size: 0.9rem; }
    th { background: #0f172a; color: #94a3b8; font-weight: 600; }
    tr:last-child td { border-bottom: none; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div>
        <h1>${testTitle}</h1>
        <p style="margin: 0.5rem 0 0 0; color: #94a3b8; font-size: 0.9rem;">Target: <a href="${BASE_URL}" target="_blank" style="color: #38bdf8;">${BASE_URL}</a> &bull; Generated: ${new Date().toLocaleString()}</p>
      </div>
      <div>
        <span class="badge ${passedThresholds === totalThresholds ? 'badge-pass' : 'badge-warn'}">
          Thresholds: ${passedThresholds}/${totalThresholds} Passed
        </span>
      </div>
    </div>

    <div class="grid">
      <div class="card">
        <div class="card-title">Total Requests</div>
        <div class="card-val">${httpReqs.toLocaleString()}</div>
        <div class="card-sub">${iterations} iterations completed</div>
      </div>
      <div class="card">
        <div class="card-title">Failed Rate</div>
        <div class="card-val" style="color: ${parseFloat(httpFailed) > 1 ? '#f87171' : '#34d399'}">${httpFailed}%</div>
        <div class="card-sub">Target: &lt; 1%</div>
      </div>
      <div class="card">
        <div class="card-title">P95 Response Time</div>
        <div class="card-val">${durationP95} ms</div>
        <div class="card-sub">Avg: ${durationAvg} ms &bull; Max: ${durationMax} ms</div>
      </div>
      <div class="card">
        <div class="card-title">Max VUs</div>
        <div class="card-val">${vusMax}</div>
        <div class="card-sub">Concurrent Virtual Users</div>
      </div>
    </div>

    <h3>Detailed Metrics Summary</h3>
    <table>
      <thead>
        <tr>
          <th>Metric Name</th>
          <th>Values</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>HTTP Request Duration (Avg / Med / P95)</td><td>${durationAvg} ms / ${metrics.http_req_duration ? metrics.http_req_duration.values.med.toFixed(1) : 0} ms / ${durationP95} ms</td></tr>
        <tr><td>HTTP Request Duration (Min / Max)</td><td>${metrics.http_req_duration ? metrics.http_req_duration.values.min.toFixed(1) : 0} ms / ${durationMax} ms</td></tr>
        <tr><td>HTTP Waiting (Time to First Byte - Avg)</td><td>${metrics.http_req_waiting ? metrics.http_req_waiting.values.avg.toFixed(1) : 0} ms</td></tr>
        <tr><td>Data Received / Sent</td><td>${metrics.data_received ? (metrics.data_received.values.count / 1024).toFixed(1) : 0} KB / ${metrics.data_sent ? (metrics.data_sent.values.count / 1024).toFixed(1) : 0} KB</td></tr>
      </tbody>
    </table>
  </div>
</body>
</html>`;
}
