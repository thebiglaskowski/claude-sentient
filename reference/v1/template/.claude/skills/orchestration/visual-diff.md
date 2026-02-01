---
name: visual-diff
description: Screenshot comparison and visual regression detection
version: 1.0.0
triggers:
  - "visual diff"
  - "compare screenshots"
  - "visual regression"
  - "screenshot baseline"
  - "before after"
model: sonnet
tags: [orchestration, ui, testing, verification]
context: inherit
---

# Visual Diff

<context>
Visual regression catches unintended UI changes that tests might miss.
By comparing screenshots before and after changes, we detect layout shifts,
color changes, missing elements, and other visual issues that automated
testing often overlooks.
</context>

<role>
You are a visual regression analyst who:
- Captures and compares screenshots
- Identifies meaningful visual differences
- Distinguishes intentional changes from regressions
- Provides actionable feedback on UI changes
</role>

---

## Workflow

<instructions>

<step number="1">
**Capture baseline** before making changes:
```
Take screenshot of current state
Save to .claude/screenshots/[feature]-baseline.png
Record viewport: [width]x[height]
Record URL/route: [path]
```
</step>

<step number="2">
**Make changes** to the UI code
</step>

<step number="3">
**Capture current state** after changes:
```
Take screenshot of changed state
Save to .claude/screenshots/[feature]-current.png
Same viewport as baseline
Same URL/route as baseline
```
</step>

<step number="4">
**Compare screenshots** and analyze differences:
- Identify changed regions
- Categorize as intentional or regression
- Flag unexpected changes for review
</step>

<step number="5">
**Report findings** with visual evidence:
- Side-by-side comparison
- Highlighted diff regions
- Severity classification
</step>

</instructions>

---

## Screenshot Capture

### With Browser Automation

Using MCP browser tools:
```
1. Navigate to target URL
2. Wait for page load + animations
3. Capture full viewport screenshot
4. Save with descriptive filename
```

### Standard Viewports

| Viewport | Width | Height | Use Case |
|----------|-------|--------|----------|
| Mobile | 375 | 667 | iPhone SE |
| Tablet | 768 | 1024 | iPad |
| Desktop | 1280 | 800 | Standard |
| Wide | 1920 | 1080 | Large monitor |

### Filename Convention

```
.claude/screenshots/
├── [feature]-[viewport]-baseline.png
├── [feature]-[viewport]-current.png
└── [feature]-[viewport]-diff.png
```

Example:
```
login-form-mobile-baseline.png
login-form-mobile-current.png
login-form-mobile-diff.png
```

---

## Comparison Analysis

<task>
When comparing screenshots, analyze:
</task>

### Layout Changes
- Element positions shifted
- Spacing differences
- Alignment issues
- Overflow/clipping

### Visual Changes
- Color differences
- Font changes
- Image changes
- Border/shadow changes

### Content Changes
- Text differences
- Missing elements
- New elements
- Order changes

### State Changes
- Loading states
- Hover states
- Error states
- Empty states

---

## Severity Classification

<examples>

<example>
<input>Button moved 2px to the right</input>
<thinking>
Small positional change, likely sub-pixel rendering difference.
Not visible to users in normal use.
</thinking>
<output>
**S3 - Minor**
2px positional variance is within acceptable tolerance.
Action: No action needed (render variance)
</output>
</example>

<example>
<input>Navigation menu completely missing</input>
<thinking>
Major UI element missing. Users cannot navigate.
Critical functionality broken.
</thinking>
<output>
**S0 - Critical**
Navigation menu not rendering. Blocks all navigation.
Action: Immediate fix required before deployment
</output>
</example>

<example>
<input>Footer links are now different color</input>
<thinking>
Visual change that may be intentional (new brand colors)
or regression (CSS specificity issue).
Need to verify intent.
</thinking>
<output>
**S2 - Medium**
Footer link color changed from #333 to #666.
Action: Verify if intentional. Check color contrast (accessibility).
</output>
</example>

<example>
<input>Form submit button overlaps input field on mobile</input>
<thinking>
Responsive layout issue. Button is covering input,
making the form difficult to use on mobile.
</thinking>
<output>
**S1 - High**
Layout overlap on mobile viewport (375px).
Submit button covers email input field.
Action: Fix responsive styles before merge
</output>
</example>

</examples>

---

## Report Format

<output_format>
# Visual Diff Report

**Feature:** [feature name]
**Date:** [timestamp]
**Viewports Tested:** [list]

---

## Summary

| Viewport | Status | Changes |
|----------|--------|---------|
| Mobile | ⚠️ | 2 issues |
| Tablet | ✓ | No changes |
| Desktop | ✓ | 1 intentional |

---

## Findings

### S1 - High Priority

#### [Issue Title]
**Viewport:** [affected viewport]
**Location:** [area of screen]

**Baseline:**
[baseline screenshot or description]

**Current:**
[current screenshot or description]

**Difference:**
[what changed]

**Recommendation:**
[how to fix]

---

### Intentional Changes

#### [Change Title]
**Viewport:** [affected viewport]
**Description:** [what changed and why it's expected]
**Verified:** [how we know it's intentional]

---

## Action Items

- [ ] Fix [issue 1]
- [ ] Verify [change 1] with design team
- [ ] Update baseline for [intentional changes]
</output_format>

---

## Integration with /ui Command

When `/ui` audit runs:

```
1. Capture screenshots at standard viewports
2. Run accessibility audit
3. Compare to baselines (if exist)
4. Report combined findings
```

---

## Baseline Management

### Creating Baselines
```
"Create visual baseline for [feature]"
→ Captures screenshots at all standard viewports
→ Saves to .claude/screenshots/[feature]-[viewport]-baseline.png
→ Records metadata (date, URL, viewport)
```

### Updating Baselines
```
"Update baseline for [feature]"
→ Moves current to baseline
→ Clears diff files
→ Updates metadata
```

### Baseline Storage
```
.claude/screenshots/
├── baselines/
│   ├── login-mobile.png
│   ├── login-tablet.png
│   └── login-desktop.png
├── current/
│   └── [captured during tests]
└── diffs/
    └── [generated during comparison]
```

---

## CI Integration

### Pre-merge Check
```bash
# In CI pipeline
./scripts/ci/visual-diff.sh

# Script contents
for viewport in mobile tablet desktop; do
  capture_screenshot "$URL" "$viewport" "current.png"
  compare_screenshots "baseline.png" "current.png" "diff.png"

  if [ "$DIFF_PERCENT" -gt "$THRESHOLD" ]; then
    echo "Visual regression detected: $DIFF_PERCENT% changed"
    exit 1
  fi
done
```

### Threshold Configuration
```json
// In .claude/settings.json
{
  "visualDiff": {
    "threshold": 0.1,     // 0.1% change tolerance
    "viewports": ["mobile", "desktop"],
    "routes": ["/", "/login", "/dashboard"]
  }
}
```

---

## Best Practices

<rules>
- Always capture baselines before changes
- Test at multiple viewports
- Wait for animations to complete before capture
- Use consistent browser/device settings
- Store baselines in version control (LFS for large files)
- Review visual changes before updating baselines
- Document intentional visual changes
- Set appropriate diff thresholds per project
</rules>

---

## Commands

```
"Capture visual baseline for [feature]"
→ Screenshots all standard viewports, saves as baselines

"Run visual diff for [feature]"
→ Captures current, compares to baseline, reports differences

"Update visual baseline for [feature]"
→ Promotes current screenshots to baseline

"Show visual diff report"
→ Displays most recent comparison results

"Compare [url1] to [url2]"
→ Cross-URL comparison (e.g., staging vs production)
```

---

## Error Handling

<error_handling>
If no baseline exists: "No baseline found for [feature]. Create one first with 'capture visual baseline'."
If page fails to load: "Could not load [URL]. Check if the dev server is running."
If viewports differ: "Viewport mismatch: baseline was [W]x[H], current is [W]x[H]. Recapture at matching size."
If screenshots identical: "No visual differences detected. Screenshots are identical."
</error_handling>
