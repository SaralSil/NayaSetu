import http from 'k6/http';
import { check } from 'k6';
import { BASE_URL, generateHtmlReport } from './config.js';

// High-throughput raw capacity test (NO artificial sleep / think-time)
export const options = {
  scenarios: {
    max_throughput: {
      executor: 'constant-vus',
      vus: 20,
      duration: '15s',
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<200'],
  },
};

export default function () {
  // Rapid fire requests to test raw server processing power
  const res = http.get(`${BASE_URL}/api/health/`);
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
}

export function handleSummary(data) {
  return {
    'throughput-summary.html': generateHtmlReport(data, 'Raw Throughput Benchmark'),
  };
}

