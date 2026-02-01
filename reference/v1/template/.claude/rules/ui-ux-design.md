# UI/UX Design Rules

## Core Principles

1. **Simplicity** — Remove everything that isn't essential
2. **Consistency** — Same patterns everywhere
3. **Hierarchy** — Guide users to what matters
4. **Feedback** — Always show system status
5. **Accessibility** — Usable by everyone

---

## Visual Design Standards

### Spacing System (8px Grid)

```css
--spacing-xs: 4px;    /* Tight: icons, small gaps */
--spacing-sm: 8px;    /* Default: inline elements */
--spacing-md: 16px;   /* Standard: between elements */
--spacing-lg: 24px;   /* Sections */
--spacing-xl: 32px;   /* Major sections */
--spacing-2xl: 48px;  /* Page sections */
```

### Typography Scale

```css
--text-xs: 0.75rem;   /* 12px - captions */
--text-sm: 0.875rem;  /* 14px - secondary */
--text-base: 1rem;    /* 16px - body */
--text-lg: 1.125rem;  /* 18px - emphasized */
--text-xl: 1.25rem;   /* 20px - subheadings */
--text-2xl: 1.5rem;   /* 24px - headings */
--text-3xl: 2rem;     /* 32px - page titles */
```

### Color Usage

| Purpose | Usage |
|---------|-------|
| Primary | Main actions, links |
| Secondary | Supporting actions |
| Success | Confirmations, completed |
| Warning | Caution, attention needed |
| Error | Failures, destructive |
| Neutral | Text, borders, backgrounds |

### Shadows

```css
/* Subtle elevation */
--shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
--shadow-md: 0 4px 6px rgba(0,0,0,0.07);
--shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
```

---

## Component Standards

### Buttons

```css
/* Sizing */
Small: height 32px, padding 8px 12px
Medium: height 40px, padding 10px 16px
Large: height 48px, padding 12px 24px

/* States */
Default → Hover → Active → Disabled
Focus ring on keyboard navigation
```

### Forms

- Labels above inputs (not inline)
- Clear placeholder text
- Visible focus states
- Error messages below inputs
- Required field indicators
- Touch targets min 44x44px

### Cards

- Consistent border radius (8px or 12px)
- Subtle shadow for depth
- Adequate padding (16-24px)
- Clear visual hierarchy inside

---

## Responsive Design

### Breakpoints

```css
--mobile: 320px;
--tablet: 768px;
--desktop: 1024px;
--wide: 1280px;
```

### Mobile First

- Design for mobile first
- Enhance for larger screens
- Touch-friendly by default
- Avoid hover-only interactions

---

## Accessibility Checklist

- [ ] Color contrast ratio ≥ 4.5:1 (text)
- [ ] Color contrast ratio ≥ 3:1 (large text, icons)
- [ ] No information conveyed by color alone
- [ ] Focus indicators visible
- [ ] Skip links for navigation
- [ ] Alt text on images
- [ ] Semantic HTML (nav, main, article)
- [ ] ARIA labels where needed
- [ ] Keyboard navigable

---

## Animation Guidelines

### Timing

```css
--duration-fast: 150ms;    /* Micro-interactions */
--duration-normal: 250ms;  /* Standard transitions */
--duration-slow: 350ms;    /* Complex animations */
```

### Principles

- Use motion purposefully
- Respect prefers-reduced-motion
- Keep under 400ms for UI
- Ease-out for entering
- Ease-in for exiting

---

## Anti-Patterns

### Avoid

- Walls of text
- Too many font sizes
- Inconsistent spacing
- Harsh borders everywhere
- No visual hierarchy
- Tiny click targets
- Mystery meat navigation
- Carousels for important content
- Infinite scroll without position indicator
- Modal abuse

### Prefer

- Scannable content
- Systematic typography
- Consistent spacing
- Subtle depth (shadows)
- Clear visual hierarchy
- Generous touch targets
- Clear navigation labels
- Static, scannable layouts
- Pagination with context
- Inline editing where possible
