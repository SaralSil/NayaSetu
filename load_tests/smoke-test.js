import http from 'k6/http';
import { check, sleep } from 'k6';
import { BASE_URL, HEADERS, ELIGIBILITY_PROFILES, generateHtmlReport } from './config.js';

export const options = {
  vus: 1, // 1 Virtual User
  duration: '15s', // Quick smoke test
  thresholds: {
    http_req_failed: ['rate<0.01'], // < 1% errors
    http_req_duration: ['p(95)<400'], // 95% of requests must complete below 400ms
  },
};

export default function () {
  // 1. Health Check
  let res = http.get(`${BASE_URL}/api/health/`);
  check(res, {
    'Health Check status is 200': (r) => r.status === 200,
    'Health status is active': (r) => {
      try {
        return JSON.parse(r.body).status === 'active';
      } catch (e) {
        return false;
      }
    },
  });

  sleep(0.5);

  // 2. Get All Schemes
  res = http.get(`${BASE_URL}/api/schemes/`);
  check(res, {
    'Schemes list status is 200': (r) => r.status === 200,
    'Schemes list returns array': (r) => {
      try {
        const body = JSON.parse(r.body);
        return Array.isArray(body.results || body);
      } catch (e) {
        return false;
      }
    },
  });

  sleep(0.5);

  // 3. Search Schemes
  res = http.get(`${BASE_URL}/api/schemes/?search=farmer`);
  check(res, {
    'Search schemes status is 200': (r) => r.status === 200,
  });

  sleep(0.5);

  // 4. Filter by Category
  res = http.get(`${BASE_URL}/api/schemes/?category=women`);
  check(res, {
    'Filter schemes by category status is 200': (r) => r.status === 200,
  });

  sleep(0.5);

  // 5. Get Scheme Detail (Annapurna Yojana)
  res = http.get(`${BASE_URL}/api/schemes/annapurna-yojana/`);
  check(res, {
    'Scheme detail status is 200': (r) => r.status === 200,
  });

  sleep(0.5);

  // 6. Check Eligibility Wizard (POST)
  const payload = JSON.stringify(ELIGIBILITY_PROFILES[0]);
  res = http.post(`${BASE_URL}/api/schemes/check-eligibility/`, payload, { headers: HEADERS });
  check(res, {
    'Eligibility check status is 200': (r) => r.status === 200,
    'Eligibility returns results': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body && (body.eligible_schemes || body.results || body.schemes !== undefined || Array.isArray(body));
      } catch (e) {
        return false;
      }
    },
  });

  sleep(1);
}

export function handleSummary(data) {
  return {
    'smoke-summary.html': generateHtmlReport(data, 'Smoke Test - NyayaSetu API'),
  };
}
