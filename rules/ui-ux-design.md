# UI/UX Design Rules

## Principles
1. Simplicity — Remove everything not essential
2. Consistency — Same patterns everywhere
3. Hierarchy — Guide users to what matters
4. Feedback — Always show system status
5. Accessibility — Usable by everyone

## Spacing (8px Grid)
```css
--spacing-xs: 4px;   /* Icons, small gaps */
--spacing-sm: 8px;   /* Inline elements */
--spacing-md: 16px;  /* Between elements */
--spacing-lg: 24px;  /* Sections */
--spacing-xl: 32px;  /* Major sections */
```

## Typography
```css
--text-sm: 0.875rem;  /* 14px - secondary */
--text-base: 1rem;    /* 16px - body */
--text-lg: 1.125rem;  /* 18px - emphasis */
--text-xl: 1.25rem;   /* 20px - subheads */
--text-2xl: 1.5rem;   /* 24px - headings */
```

## Color Usage
| Purpose | Use |
|---------|-----|
| Primary | Main actions, links |
| Success | Confirmations |
| Warning | Caution needed |
| Error | Failures, destructive |

## Accessibility
- [ ] Color contrast ≥ 4.5:1
- [ ] No info by color alone
- [ ] Focus indicators visible
- [ ] Alt text on images
- [ ] Keyboard navigable
- [ ] Touch targets ≥ 44px

## Component Standards
- Labels above inputs
- Clear placeholder text
- Visible focus states
- Error messages below inputs
- Touch targets min 44x44px

## Animation
- Duration: 150-350ms
- Use motion purposefully
- Respect prefers-reduced-motion

## Anti-Patterns
- Walls of text
- Too many font sizes
- Inconsistent spacing
- Tiny click targets
- Carousels for important content

## Full Reference
`reference/v1/template/.claude/rules/ui-ux-design.md`
