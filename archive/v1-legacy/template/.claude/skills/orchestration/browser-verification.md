---
name: browser-verification
description: Use browser automation to verify UI changes, test workflows, and validate visual output
version: 2.0.0
triggers:
  - "verify in browser"
  - "check in browser"
  - "visual verification"
  - "test UI"
  - "screenshot"
  - "check responsive"
  - "visual diff"
model: sonnet
tags: [verification, UI, testing, browser]
context: inherit
---

# Browser Verification

Use browser automation to verify UI changes, test workflows, and validate visual output during development.

---

## When to Use Browser Verification

| Situation | Browser Action |
|-----------|----------------|
| UI component created/modified | Screenshot at multiple viewports |
| Form implementation | Test submission flow |
| Responsive changes | Check breakpoints |
| Accessibility work | Run accessibility audit |
| User flow implementation | End-to-end walkthrough |
| Visual regression check | Compare to baseline |
| Debug visual issue | Inspect live page |

---

## Verification Workflows

### 1. Quick Visual Check

After UI changes, verify the result:

```
1. Start local dev server (if not running)
2. Navigate to affected page
3. Take screenshot
4. Report what you see
```

**Command:** "Verify this UI change in browser"

### 2. Responsive Verification

Check all breakpoints:

```
Viewport sizes:
├── Mobile:  375 x 667
├── Tablet:  768 x 1024
├── Desktop: 1280 x 800
└── Wide:    1920 x 1080

For each viewport:
├── Resize browser window
├── Take screenshot
├── Note any layout issues
└── Report findings
```

**Command:** "Check responsive design in browser"

### 3. Accessibility Audit

Run accessibility checks:

```
1. Navigate to page
2. Read accessibility tree (read_page tool)
3. Check for:
   ├── Missing alt text
   ├── Poor color contrast
   ├── Missing form labels
   ├── Keyboard navigation issues
   └── Missing ARIA labels
4. Report findings by severity
```

**Command:** "Run accessibility audit in browser"

### 4. Form Testing

Verify form behavior:

```
1. Navigate to form
2. Find form elements (find tool)
3. Fill form fields (form_input tool)
4. Submit form
5. Verify:
   ├── Validation messages appear
   ├── Success/error states work
   ├── Data submitted correctly
   └── Redirect happens (if expected)
```

**Command:** "Test this form in browser"

### 5. User Flow Walkthrough

Test complete user journey:

```
1. Start at entry point
2. Perform each step:
   ├── Navigate
   ├── Click elements
   ├── Fill forms
   ├── Wait for responses
3. Screenshot key states
4. Verify expected outcomes
5. Report any issues
```

**Command:** "Walk through [user flow] in browser"

### 6. Visual Regression

Compare current state to baseline:

```
1. Take current screenshot
2. Compare to baseline (if exists)
3. Highlight differences
4. Classify changes:
   ├── Expected (intentional change)
   ├── Unexpected (potential bug)
   └── Acceptable (minor variation)
5. Update baseline if approved
```

**Command:** "Check for visual regression"

---

## MCP Browser Tools Reference

### Navigation
```javascript
// Navigate to URL
mcp__claude-in-chrome__navigate({ url: "http://localhost:3000", tabId })

// Go back/forward
mcp__claude-in-chrome__navigate({ url: "back", tabId })
```

### Screenshots
```javascript
// Full page screenshot
mcp__claude-in-chrome__computer({ action: "screenshot", tabId })

// Specific region
mcp__claude-in-chrome__computer({
  action: "zoom",
  region: [x0, y0, x1, y1],
  tabId
})
```

### Interaction
```javascript
// Click element
mcp__claude-in-chrome__computer({
  action: "left_click",
  coordinate: [x, y],
  tabId
})

// Type text
mcp__claude-in-chrome__computer({
  action: "type",
  text: "input text",
  tabId
})

// Fill form field
mcp__claude-in-chrome__form_input({
  ref: "ref_1",
  value: "field value",
  tabId
})
```

### Page Analysis
```javascript
// Get accessibility tree
mcp__claude-in-chrome__read_page({ tabId })

// Find elements by description
mcp__claude-in-chrome__find({
  query: "login button",
  tabId
})

// Extract page text
mcp__claude-in-chrome__get_page_text({ tabId })
```

### Debugging
```javascript
// Read console logs
mcp__claude-in-chrome__read_console_messages({
  tabId,
  pattern: "error"
})

// Read network requests
mcp__claude-in-chrome__read_network_requests({
  tabId,
  urlPattern: "/api/"
})

// Execute JavaScript
mcp__claude-in-chrome__javascript_tool({
  action: "javascript_exec",
  text: "document.title",
  tabId
})
```

---

## Integration with Autonomous Loop

### Browser Verification Phase

In the autonomous loop, browser verification occurs:

```
Phase 4: TEST
├── Run unit tests
├── Run integration tests
└── IF UI changes:
    └── Run browser verification
        ├── Visual check at viewports
        ├── Accessibility audit
        ├── Form testing (if forms)
        └── Report findings

Phase 5: QUALITY
├── Code quality checks
├── Security scan
└── IF UI changes:
    └── Visual regression check
        ├── Compare to baseline
        ├── Flag unexpected changes
        └── Update baseline if approved
```

### Auto-Trigger Conditions

Browser verification auto-triggers when:
- Files in `src/components/` modified
- Files in `src/pages/` or `app/` modified
- CSS/SCSS/style files modified
- `*.tsx` or `*.jsx` files modified
- Changes mention "UI", "visual", "style", "layout"

---

## Verification Checklist

### Before Marking UI Work Complete

- [ ] Visual appearance matches design/expectation
- [ ] Works at mobile viewport (375px)
- [ ] Works at tablet viewport (768px)
- [ ] Works at desktop viewport (1280px)
- [ ] No console errors
- [ ] Forms submit correctly
- [ ] Error states display properly
- [ ] Loading states work
- [ ] Accessibility audit passes
- [ ] Keyboard navigation works
- [ ] Focus states visible

---

## Troubleshooting

### Browser Not Responding

```
1. Check if tab exists: tabs_context_mcp
2. Create new tab if needed: tabs_create_mcp
3. Wait for page load: computer({ action: "wait", duration: 2 })
```

### Element Not Found

```
1. Take screenshot to see current state
2. Use read_page to get accessibility tree
3. Use find tool with broader query
4. Check if element is in viewport (may need scroll)
```

### Screenshots Not Capturing Expected Content

```
1. Wait for page to fully load
2. Wait for async content: computer({ action: "wait", duration: 3 })
3. Scroll to element: computer({ action: "scroll_to", ref: "ref_1" })
4. Check for loading spinners/overlays
```

---

## Example Verification Session

```
Task: Verify new user profile page

1. Get browser context
   → tabs_context_mcp({ createIfEmpty: true })
   → Got tab ID: 12345

2. Navigate to page
   → navigate({ url: "http://localhost:3000/profile", tabId: 12345 })
   → Page loaded

3. Take screenshot
   → computer({ action: "screenshot", tabId: 12345 })
   → [Screenshot shows profile page]

4. Check responsive
   → resize_window({ width: 375, height: 667, tabId: 12345 })
   → computer({ action: "screenshot", tabId: 12345 })
   → [Mobile layout looks good]

5. Check accessibility
   → read_page({ tabId: 12345 })
   → Found issues:
      - Image missing alt text (ref_5)
      - Button has no accessible name (ref_12)

6. Report findings
   → S2: Accessibility issues found
      - Add alt text to profile image
      - Add aria-label to edit button
```

---

## Best Practices

1. **Always screenshot before and after changes** - Creates visual record
2. **Test at multiple viewports** - Don't assume desktop-first
3. **Check console for errors** - JS errors break functionality
4. **Verify actual data flow** - Don't just check visual appearance
5. **Run accessibility checks** - Part of Definition of Done
6. **Document visual decisions** - Screenshots in PR descriptions
