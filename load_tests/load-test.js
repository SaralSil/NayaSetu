import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Trend, Rate, Counter } from 'k6/metrics';
import {
  BASE_URL,
  HEADERS,
  ELIGIBILITY_PROFILES,
  SEARCH_KEYWORDS,
  CATEGORIES,
  SCHEME_SLUGS,
  generateHtmlReport,
} from './config.js';

// Custom metrics to track specific parts of the app
const schemesListDuration = new Trend('schemes_list_duration');
const eligibilityDuration = new Trend('eligibility_wizard_duration');
const successfulFlows = new Rate('successful_citizen_flows');
const totalChecks = new Counter('total_checks_run');

export const options = {
  stages: [
    { duration: '30s', target: 50 }, // Ramp-up to 10 VUs
    { duration: '1m', target: 200 },  // Stay at 10 VUs
    { duration: '30s', target: 10 }, // Ramp-up to 25 VUs
    { duration: '1m', target: 1500},  // Stay at 25 VUs
    { duration: '30s', target: 1},  // Ramp-down to 0
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'], // Global HTTP failure rate < 1%
    http_req_duration: ['p(95)<600', 'p(99)<1200'], // 95% under 600ms, 99% under 1.2s
    schemes_list_duration: ['p(95)<400'], // Scheme list should be fast
    eligibility_wizard_duration: ['p(95)<800'], // Eligibility computation
    successful_citizen_flows: ['rate>0.98'], // 98%+ user sessions must complete cleanly
  },
};

export default function () {
  let flowOk = true;

  // 1. Citizen arrives and visits health / basic app
  group('01_App_Arrival', function () {
    const res = http.get(`${BASE_URL}/api/health/`);
    const passed = check(res, {
      'health check status is 200': (r) => r.status === 200,
    });
    totalChecks.add(1);
    if (!passed) flowOk = false;
  });

  sleep(1);

  // 2. Citizen browses schemes directory
  group('02_Browse_Schemes', function () {
    const start = Date.now();
    const res = http.get(`${BASE_URL}/api/schemes/`);
    schemesListDuration.add(Date.now() - start);

    const passed = check(res, {
      'schemes list status is 200': (r) => r.status === 200,
    });
    totalChecks.add(1);
    if (!passed) flowOk = false;
  });

  sleep(1 + Math.random());

  // 3. Citizen searches or filters by category
  group('03_Search_And_Filter', function () {
    const keyword = SEARCH_KEYWORDS[Math.floor(Math.random() * SEARCH_KEYWORDS.length)];
    const category = CATEGORIES[Math.floor(Math.random() * CATEGORIES.length)];

    const searchRes = http.get(`${BASE_URL}/api/schemes/?search=${encodeURIComponent(keyword)}`);
    const filterRes = http.get(`${BASE_URL}/api/schemes/?category=${encodeURIComponent(category)}`);

    const passed = check(searchRes, { 'search returned 200': (r) => r.status === 200 }) &&
                   check(filterRes, { 'filter returned 200': (r) => r.status === 200 });
    totalChecks.add(2);
    if (!passed) flowOk = false;
  });

  sleep(1.5);

  // 4. Citizen inspects a specific scheme detail
  group('04_Scheme_Detail', function () {
    const slug = SCHEME_SLUGS[Math.floor(Math.random() * SCHEME_SLUGS.length)];
    const res = http.get(`${BASE_URL}/api/schemes/${slug}/`);

    const passed = check(res, {
      'scheme detail is 200': (r) => r.status === 200,
    });
    totalChecks.add(1);
    if (!passed) flowOk = false;
  });

  sleep(2);

  // 5. Citizen fills out and submits the Eligibility Wizard
  group('05_Eligibility_Wizard', function () {
    const randomProfile = ELIGIBILITY_PROFILES[Math.floor(Math.random() * ELIGIBILITY_PROFILES.length)];
    const payload = JSON.stringify(randomProfile);

    const start = Date.now();
    const res = http.post(`${BASE_URL}/api/schemes/check-eligibility/`, payload, { headers: HEADERS });
    eligibilityDuration.add(Date.now() - start);

    const passed = check(res, {
      'eligibility status is 200': (r) => r.status === 200,
    });
    totalChecks.add(1);
    if (!passed) flowOk = false;
  });

  successfulFlows.add(flowOk);
  sleep(1 + Math.random() * 2);
}

export function handleSummary(data) {
  return {
    'load-summary.html': generateHtmlReport(data, 'NyayaSetu AI - General Load Test Report'),
  };
}
