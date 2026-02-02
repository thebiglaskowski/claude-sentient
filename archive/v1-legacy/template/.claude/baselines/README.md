# Visual Baselines

Store screenshots and visual references for regression testing.

---

## Purpose

This directory stores baseline screenshots for:
- Visual regression detection
- Before/after comparisons
- UI change verification
- Design system documentation

---

## Structure

```
baselines/
├── README.md           # This file
├── screenshots/        # Page screenshots by route
│   ├── home/
│   │   ├── desktop-1280.png
│   │   ├── tablet-768.png
│   │   └── mobile-375.png
│   ├── login/
│   └── dashboard/
├── components/         # Component screenshots
│   ├── button-primary.png
│   ├── button-secondary.png
│   └── card-default.png
└── diffs/              # Generated diff images
    └── [timestamp]/
```

---

## Naming Convention

```
[page-or-component]-[variant]-[viewport].png

Examples:
- home-default-desktop.png
- login-error-mobile.png
- button-primary-hover.png
- card-loading-tablet.png
```

---

## Viewports

| Name | Width | Height | Use Case |
|------|-------|--------|----------|
| mobile | 375px | 667px | iPhone SE |
| tablet | 768px | 1024px | iPad |
| desktop | 1280px | 800px | Standard |
| wide | 1920px | 1080px | Large monitors |

---

## Workflow

### Capturing Baselines

```
1. Navigate to page/component
2. Set viewport size
3. Take screenshot
4. Save to appropriate folder
5. Name following convention
```

### Comparing to Baseline

```
1. Take new screenshot
2. Load baseline for same view
3. Generate diff image
4. Review differences:
   - Expected: intentional changes
   - Unexpected: potential bugs
4. Update baseline if approved
```

### Updating Baselines

```
When UI intentionally changes:
1. Review the change
2. Confirm it matches design
3. Replace old baseline
4. Commit with message: "baseline: update [component/page] after [change]"
```

---

## Integration with Loop

The autonomous loop uses baselines when:

1. **UI changes detected** → Captures new screenshot
2. **Baseline exists** → Compares to baseline
3. **Differences found** → Reports in quality check
4. **Approved** → Updates baseline

---

## Excluding from Git

For large projects, consider:

```gitignore
# Option 1: Exclude all baselines (regenerate as needed)
.claude/baselines/screenshots/
.claude/baselines/components/

# Option 2: Keep baselines, exclude diffs
.claude/baselines/diffs/
```

---

## Best Practices

1. **Capture at consistent state** - Wait for animations, loading
2. **Use fixed data** - Mock dynamic content for consistency
3. **Document variants** - Capture hover, focus, error states
4. **Regular updates** - Keep baselines current with design
5. **Review diffs carefully** - Small changes can indicate bugs
