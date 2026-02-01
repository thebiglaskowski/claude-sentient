# Metrics Tracking

Track quality metrics over time to identify trends and measure improvement.

---

## Purpose

This directory tracks:
- Code quality trends
- Test coverage history
- Security scan results
- Performance metrics
- Session statistics

---

## Structure

```
metrics/
├── README.md           # This file
├── quality.jsonl       # Quality metrics log (JSON Lines)
├── coverage.jsonl      # Test coverage history
├── security.jsonl      # Security scan results
├── performance.jsonl   # Performance benchmarks
└── sessions.jsonl      # Session activity log
```

---

## Metric Formats

### quality.jsonl
```json
{"timestamp": "2026-01-29T10:00:00Z", "complexity": 12, "duplication": 3.2, "issues": {"s0": 0, "s1": 2, "s2": 5, "s3": 8}, "files": 142}
```

### coverage.jsonl
```json
{"timestamp": "2026-01-29T10:00:00Z", "overall": 82.5, "statements": 85.2, "branches": 78.1, "functions": 88.4, "lines": 82.5}
```

### security.jsonl
```json
{"timestamp": "2026-01-29T10:00:00Z", "vulnerabilities": {"critical": 0, "high": 1, "medium": 3, "low": 5}, "dependencies": 145, "outdated": 12}
```

### performance.jsonl
```json
{"timestamp": "2026-01-29T10:00:00Z", "lcp": 2.1, "fid": 45, "cls": 0.05, "ttfb": 0.3, "bundle_size_kb": 245}
```

### sessions.jsonl
```json
{"timestamp": "2026-01-29T10:00:00Z", "duration_min": 45, "iterations": 8, "issues_fixed": 12, "tests_added": 5, "files_changed": 23}
```

---

## Recording Metrics

### Automatic Recording

The autonomous loop records metrics:
- **Start of loop:** Baseline metrics
- **End of iteration:** Progress metrics
- **End of loop:** Final metrics

### Manual Recording

Add metrics manually:
```
"Record current metrics"
→ Runs quality checks
→ Appends to metric files
→ Reports trends
```

---

## Viewing Metrics

### Quick Summary
```
"Show metrics summary"
→ Last 7 days of each metric type
→ Trend indicators (↑↓→)
→ Alerts for degradation
```

### Detailed Report
```
"Show metrics report"
→ Full history with charts (ASCII)
→ Comparison to targets
→ Recommendations
```

### Example Output
```
Quality Metrics (Last 7 Days)
═══════════════════════════════

Coverage: 82.5% → 85.2% ↑ (+2.7%)
Target: 80% ✓

Issues:
  S0: 0 (target: 0) ✓
  S1: 2 → 0 ↓ (target: 0) ✓
  S2: 5 → 3 ↓ (target: <5) ✓
  S3: 8 → 12 ↑ (no target)

Complexity: 12 → 11 ↓ (target: <15) ✓

Trend: ████████████ Improving
```

---

## Targets

Default targets (customize per project):

| Metric | Target | Critical |
|--------|--------|----------|
| Coverage | ≥80% | <60% |
| S0 Issues | 0 | >0 |
| S1 Issues | 0 | >0 |
| S2 Issues | <5 | >10 |
| Complexity | <15 | >20 |
| LCP | <2.5s | >4s |
| Bundle Size | <250KB | >500KB |

---

## Alerting

Alerts trigger when:
- Any S0 or S1 issues exist
- Coverage drops below 60%
- Performance degrades >20%
- Dependencies have critical CVEs

Alert format:
```
⚠️ METRIC ALERT

Coverage dropped from 82% to 71% (-11%)
This is below the critical threshold of 60%.

Recent changes that may have caused this:
- src/api/auth.js (0% coverage, new file)
- src/utils/helpers.js (deleted tests)

Recommended action:
- Run /test to see uncovered files
- Add tests for new auth module
```

---

## Integration with Loop

The autonomous loop uses metrics:

1. **Phase 1 (ASSESS):** Load current metrics as baseline
2. **Phase 5 (QUALITY):** Compare to targets
3. **Phase 6 (EVALUATE):** Record final metrics
4. **Completion:** Update metric files

---

## Retention

- Keep daily summaries for 90 days
- Keep weekly summaries for 1 year
- Archive older data to `metrics/archive/`

---

## Best Practices

1. **Record consistently** - Same conditions each time
2. **Include context** - What changed since last record
3. **Set realistic targets** - Achievable but challenging
4. **Act on trends** - Don't ignore gradual degradation
5. **Celebrate improvements** - Note wins in SESSION_HISTORY
