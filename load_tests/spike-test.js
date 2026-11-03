import http from 'k6/http';
import { check, sleep } from 'k6';
import { BASE_URL, generateHtmlReport } from './config.js';

export const options = {
  stages: [
    { duration: '15s', target: 2 },   // Idle / low traffic
    { duration: '10s', target: 70 },  // Instant spike!
    { duration: '25s', target: 70 },  // Maintain spike
    { duration: '10s', target: 2 },   // Sudden drop
    { duration: '15s', target: 2 },   // Recovery observation
    { duration: '25s', target: 70 },
    { duration: '10s', target: 2 },
  ],
  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<1200'],
  },
};

export default function () {
  const res = http.get(`${BASE_URL}/api/health/`);
  check(res, {
    'health check status is 200': (r) => r.status === 200,
  });

  const schemesRes = http.get(`${BASE_URL}/api/schemes/`);
  check(schemesRes, {
    'schemes status is 200': (r) => r.status === 200,
  });

  sleep(0.5);
}

export function handleSummary(data) {
  return {
    'spike-summary.html': generateHtmlReport(data, 'NyayaSetu AI - Spike Test Report'),
  };
}
