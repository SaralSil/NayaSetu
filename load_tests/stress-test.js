import http from 'k6/http';
import { check, sleep } from 'k6';
import {
  BASE_URL,
  HEADERS,
  ELIGIBILITY_PROFILES,
  generateHtmlReport,
} from './config.js';

export const options = {
  stages: [
    { duration: '30s', target: 20 },  // Baseline ramp
    { duration: '1m', target: 50 },   // Moderate stress
    { duration: '1m', target: 100 },  // High stress: finding saturation point
    { duration: '1m', target: 170 },  // Hold at peak stress
    { duration: '30s', target: 0 },   // Recovery ramp-down
  ],
  thresholds: {
    http_req_failed: ['rate<0.05'], // Allow up to 5% failure under extreme stress
    http_req_duration: ['p(95)<1500'], // 95% of responses under 1.5s
  },
};

export default function () {
  // Rapid requests mix
  const roll = Math.random();

  if (roll < 0.4) {
    // 40% read schemes catalog
    const res = http.get(`${BASE_URL}/api/schemes/`);
    check(res, { 'schemes 200': (r) => r.status === 200 });
  } else if (roll < 0.7) {
    // 30% eligibility calculation
    const profile = ELIGIBILITY_PROFILES[Math.floor(Math.random() * ELIGIBILITY_PROFILES.length)];
    const res = http.post(`${BASE_URL}/api/schemes/check-eligibility/`, JSON.stringify(profile), { headers: HEADERS });
    check(res, { 'eligibility 200': (r) => r.status === 200 });
  } else {
    // 30% health & search queries
    const res = http.get(`${BASE_URL}/api/health/`);
    check(res, { 'health 200': (r) => r.status === 200 });
  }

  sleep(0.5);
}

export function handleSummary(data) {
  return {
    'stress-summary.html': generateHtmlReport(data, 'NyayaSetu AI - Stress Test Report'),
  };
}
