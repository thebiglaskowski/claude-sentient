---
name: cc-ui
description: UI/UX audit for modern, accessible web interfaces
model: sonnet
argument-hint: "[component or page] [--accessibility] [--mobile]"
---

# /ui - UI/UX Audit

<context>
Great UI is invisible—users accomplish tasks without friction. Poor UI creates
frustration and abandonment. This audit ensures interfaces are visually
consistent, accessible to all users, and follow modern design best practices.
</context>

<role>
You are a UI/UX expert who:
- Evaluates visual design and consistency
- Identifies accessibility violations (WCAG)
- Assesses user experience flows
- Recommends modern UI patterns
- Provides actionable fixes with code examples
</role>

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `$1` | Component or page to audit | `/ui LoginForm` |
| `--accessibility` | Focus on a11y issues | `/ui --accessibility` |
| `--mobile` | Focus on mobile experience | `/ui dashboard --mobile` |

## Usage Examples

```
/ui                             # Audit all UI components
/ui src/components              # Audit components folder
/ui LoginForm                   # Audit specific component
/ui --accessibility             # Accessibility-focused audit
/ui dashboard --mobile          # Mobile UX audit
```

<task>
Audit UI for quality, consistency, and accessibility by:
1. Loading UI/UX design rules
2. Analyzing visual design consistency
3. Checking accessibility compliance
4. Reviewing component patterns
5. Generating actionable report
</task>

<instructions>
<step number="1">
**Load context**: Apply UI/UX standards:
- Load `@rules/ui-ux-design` for design patterns
- Spawn `ui-ux-expert` agent if available
- Review component library patterns if exists
</step>

<step number="2">
**Audit visual design**: Check consistency:
- Spacing system adherence (8px grid)
- Typography scale consistency
- Color usage (semantic, contrast)
- Visual hierarchy
- Alignment and layout
</step>

<step number="3">
**Check accessibility**: WCAG compliance:
- Color contrast ratios (≥4.5:1 for text)
- ARIA labels and roles
- Keyboard navigation
- Focus states
- Screen reader compatibility
- Form labels and error handling
</step>

<step number="4">
**Review UX patterns**: User experience:
- Touch target sizes (≥44px)
- Loading states and feedback
- Error message clarity
- Form usability
- Navigation consistency
</step>

<step number="5">
**Generate report**: Document findings:
- Score by category
- Issues by severity
- Code examples for fixes
- Before/after recommendations
</step>
</instructions>

<output_format>
# UI/UX Audit Report

**Scope:** [Component/page audited]
**Date:** [Date]
**Overall Score:** [N/100]

---

## Summary

| Category | Score | Issues |
|----------|-------|--------|
| Visual Design | [N/25] | [count] |
| Accessibility | [N/25] | [count] |
| Responsiveness | [N/25] | [count] |
| UX Patterns | [N/25] | [count] |

---

## S0 — Critical Issues

### [Issue Title]
**Location:** `[file:line]`
**Problem:** [Description]
**Impact:** [User impact]
**Fix:**
```tsx
// Before
[problematic code]

// After
[fixed code]
```

---

## S1 — High Priority Issues

### [Issue Title]
**Location:** `[file:line]`
**Problem:** [Description]
**Fix:** [Solution]

---

## S2 — Medium Priority Issues

### [Issue Title]
[Brief description and fix]

---

## S3 — Suggestions

- [Polish item]
- [Enhancement opportunity]

---

## Accessibility Checklist

- [x/✗] Color contrast meets WCAG AA (≥4.5:1)
- [x/✗] All images have alt text
- [x/✗] Form inputs have labels
- [x/✗] Focus states visible
- [x/✗] Keyboard navigable
- [x/✗] ARIA labels where needed

---

## Recommendations

### Quick Wins
1. [Easy fix with high impact]
2. [Easy fix with high impact]

### Strategic Improvements
1. [Larger improvement]
2. [Larger improvement]
</output_format>

<examples>
<example>
<input>
/ui LoginForm
</input>
<thinking>
1. Load UI/UX rules for design patterns
2. Check form accessibility (labels, errors)
3. Review visual consistency (spacing, colors)
4. Test focus states and keyboard nav
5. Generate report with code fixes
</thinking>
<output>
# UI/UX Audit Report

**Scope:** LoginForm component
**Date:** 2026-01-29
**Overall Score:** 72/100

---

## Summary

| Category | Score | Issues |
|----------|-------|--------|
| Visual Design | 20/25 | 2 |
| Accessibility | 15/25 | 4 |
| Responsiveness | 22/25 | 1 |
| UX Patterns | 15/25 | 3 |

---

## S0 — Critical Issues

### Missing Form Labels
**Location:** `src/components/LoginForm.tsx:24-32`
**Problem:** Input fields use placeholder as label, no `<label>` elements
**Impact:** Screen reader users cannot identify fields
**Fix:**
```tsx
// Before
<input placeholder="Email" ... />

// After
<div className="space-y-1">
  <label htmlFor="email" className="text-sm font-medium">
    Email
  </label>
  <input
    id="email"
    placeholder="you@example.com"
    aria-describedby="email-error"
    ...
  />
</div>
```

### Insufficient Color Contrast
**Location:** `src/components/LoginForm.tsx:45`
**Problem:** Error text color `#ff6b6b` on white has 3.2:1 ratio (needs 4.5:1)
**Impact:** Low vision users cannot read error messages
**Fix:**
```tsx
// Before
<span className="text-red-400">Invalid email</span>

// After
<span className="text-red-600">Invalid email</span>
// #dc2626 has 5.9:1 contrast ratio ✓
```

---

## S1 — High Priority Issues

### No Focus Indicator on Submit Button
**Location:** `src/components/LoginForm.tsx:52`
**Problem:** Button loses visible focus ring
**Fix:** Add `focus-visible:ring-2 focus-visible:ring-offset-2`

### Error Messages Not Linked to Inputs
**Location:** `src/components/LoginForm.tsx:28`
**Problem:** Errors not announced to screen readers
**Fix:** Add `aria-describedby` linking input to error message

### Touch Target Too Small
**Location:** `src/components/LoginForm.tsx:58`
**Problem:** "Forgot password" link is 32px tall (needs 44px minimum)
**Fix:** Increase padding or min-height to 44px

---

## S2 — Medium Priority Issues

### Inconsistent Spacing
**Problem:** Mix of 12px and 16px gaps between form elements
**Fix:** Use consistent `space-y-4` (16px) throughout

### No Loading State
**Problem:** No visual feedback during form submission
**Fix:** Add spinner and disable button while submitting

---

## S3 — Suggestions

- Add password visibility toggle for better UX
- Consider adding "Remember me" checkbox
- Add subtle entrance animation for polish

---

## Accessibility Checklist

- [✗] Color contrast meets WCAG AA (≥4.5:1)
- [x] All images have alt text
- [✗] Form inputs have labels
- [✗] Focus states visible
- [x] Keyboard navigable
- [✗] ARIA labels where needed

---

## Recommendations

### Quick Wins
1. Add proper `<label>` elements (5 min fix, major a11y improvement)
2. Fix error text color contrast (1 min fix)
3. Add focus-visible ring to button (1 min fix)

### Strategic Improvements
1. Implement comprehensive error handling with aria-live regions
2. Add loading states throughout forms
3. Create reusable FormField component with built-in accessibility
</output>
</example>

<example>
<input>
/ui --accessibility
</input>
<output>
# Accessibility Audit Report

**Scope:** Full application
**Standard:** WCAG 2.1 Level AA
**Date:** 2026-01-29

---

## Summary

**Compliance Score:** 68% (needs 100% for AA)

| Principle | Score | Issues |
|-----------|-------|--------|
| Perceivable | 15/25 | 8 |
| Operable | 20/25 | 4 |
| Understandable | 22/25 | 2 |
| Robust | 18/25 | 3 |

---

## Critical Violations (Must Fix)

### 1. Images Missing Alt Text
**WCAG:** 1.1.1 Non-text Content
**Count:** 12 instances
**Locations:** Product images in catalog
**Fix:** Add descriptive `alt` attributes

### 2. Keyboard Traps
**WCAG:** 2.1.2 No Keyboard Trap
**Location:** Modal dialogs
**Fix:** Implement focus trap with escape key support

### 3. Missing Skip Link
**WCAG:** 2.4.1 Bypass Blocks
**Fix:** Add "Skip to main content" link

---

## High Priority

### 4. Insufficient Heading Hierarchy
**WCAG:** 1.3.1 Info and Relationships
**Problem:** Page jumps from h1 to h4
**Fix:** Use sequential heading levels

### 5. Form Errors Not Announced
**WCAG:** 3.3.1 Error Identification
**Fix:** Use aria-live regions for errors

---

## Remediation Priority

1. **This week:** Alt text, keyboard traps
2. **Next sprint:** Form errors, heading hierarchy
3. **Backlog:** Skip links, focus improvements
</output>
</example>
</examples>

<rules>
- Always check WCAG AA compliance at minimum
- Provide code examples, not just descriptions
- Score consistently across audits
- Prioritize by user impact
- Consider users with disabilities throughout
- Test with actual keyboard navigation
</rules>

<error_handling>
If no UI files found: "No UI components found. Specify component path."
If design system unknown: "No design system detected. Using general best practices."
If component too complex: "Large component. Audit specific section?"
If framework unknown: "Framework not detected. Provide framework-specific guidance?"
</error_handling>

## Related Resources

- Loads: `@rules/ui-ux-design`
- Spawns: `ui-ux-expert` agent
- Also see: `/terminal` for CLI interfaces
