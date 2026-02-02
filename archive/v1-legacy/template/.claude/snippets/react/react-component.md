# Snippet: react-component

## Description

React functional component with TypeScript, proper typing, and common patterns.

## When to Use

- Creating new UI components
- Building reusable components
- Starting component-based features

## Code

### Basic Component

```tsx
import { memo } from 'react';
import { cn } from '@/lib/utils';

interface ComponentNameProps {
  /** Primary content */
  children: React.ReactNode;
  /** Additional CSS classes */
  className?: string;
  /** Component variant */
  variant?: 'default' | 'primary' | 'secondary';
  /** Disabled state */
  disabled?: boolean;
  /** Click handler */
  onClick?: () => void;
}

export const ComponentName = memo(function ComponentName({
  children,
  className,
  variant = 'default',
  disabled = false,
  onClick,
}: ComponentNameProps) {
  return (
    <div
      className={cn(
        'base-styles',
        {
          'variant-default': variant === 'default',
          'variant-primary': variant === 'primary',
          'variant-secondary': variant === 'secondary',
          'opacity-50 cursor-not-allowed': disabled,
        },
        className
      )}
      onClick={disabled ? undefined : onClick}
      role="button"
      tabIndex={disabled ? -1 : 0}
      aria-disabled={disabled}
    >
      {children}
    </div>
  );
});
```

### Component with State

```tsx
import { useState, useCallback, memo } from 'react';

interface CounterProps {
  initialValue?: number;
  min?: number;
  max?: number;
  onChange?: (value: number) => void;
}

export const Counter = memo(function Counter({
  initialValue = 0,
  min = 0,
  max = 100,
  onChange,
}: CounterProps) {
  const [count, setCount] = useState(initialValue);

  const increment = useCallback(() => {
    setCount((prev) => {
      const next = Math.min(prev + 1, max);
      onChange?.(next);
      return next;
    });
  }, [max, onChange]);

  const decrement = useCallback(() => {
    setCount((prev) => {
      const next = Math.max(prev - 1, min);
      onChange?.(next);
      return next;
    });
  }, [min, onChange]);

  return (
    <div className="flex items-center gap-2">
      <button
        onClick={decrement}
        disabled={count <= min}
        aria-label="Decrease"
      >
        -
      </button>
      <span aria-live="polite">{count}</span>
      <button
        onClick={increment}
        disabled={count >= max}
        aria-label="Increase"
      >
        +
      </button>
    </div>
  );
});
```

### Component with Data Fetching

```tsx
import { useQuery } from '@tanstack/react-query';
import { Skeleton } from '@/components/ui/skeleton';
import { Alert } from '@/components/ui/alert';

interface User {
  id: string;
  name: string;
  email: string;
}

interface UserCardProps {
  userId: string;
}

export function UserCard({ userId }: UserCardProps) {
  const {
    data: user,
    isLoading,
    isError,
    error,
  } = useQuery<User>({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  if (isLoading) {
    return (
      <div className="p-4 border rounded-lg">
        <Skeleton className="h-6 w-32 mb-2" />
        <Skeleton className="h-4 w-48" />
      </div>
    );
  }

  if (isError) {
    return (
      <Alert variant="destructive">
        Failed to load user: {error.message}
      </Alert>
    );
  }

  return (
    <div className="p-4 border rounded-lg">
      <h3 className="font-semibold">{user.name}</h3>
      <p className="text-muted-foreground">{user.email}</p>
    </div>
  );
}
```

### Compound Component Pattern

```tsx
import { createContext, useContext, useState, ReactNode } from 'react';

// Context
interface AccordionContextValue {
  openItems: Set<string>;
  toggle: (id: string) => void;
}

const AccordionContext = createContext<AccordionContextValue | null>(null);

function useAccordion() {
  const context = useContext(AccordionContext);
  if (!context) {
    throw new Error('Accordion components must be used within Accordion');
  }
  return context;
}

// Root
interface AccordionProps {
  children: ReactNode;
  defaultOpen?: string[];
}

export function Accordion({ children, defaultOpen = [] }: AccordionProps) {
  const [openItems, setOpenItems] = useState(new Set(defaultOpen));

  const toggle = (id: string) => {
    setOpenItems((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  return (
    <AccordionContext.Provider value={{ openItems, toggle }}>
      <div className="divide-y">{children}</div>
    </AccordionContext.Provider>
  );
}

// Item
interface AccordionItemProps {
  id: string;
  title: string;
  children: ReactNode;
}

Accordion.Item = function AccordionItem({
  id,
  title,
  children,
}: AccordionItemProps) {
  const { openItems, toggle } = useAccordion();
  const isOpen = openItems.has(id);

  return (
    <div>
      <button
        className="w-full p-4 text-left font-medium"
        onClick={() => toggle(id)}
        aria-expanded={isOpen}
      >
        {title}
      </button>
      {isOpen && <div className="p-4 pt-0">{children}</div>}
    </div>
  );
};

// Usage
// <Accordion defaultOpen={['item-1']}>
//   <Accordion.Item id="item-1" title="Section 1">Content 1</Accordion.Item>
//   <Accordion.Item id="item-2" title="Section 2">Content 2</Accordion.Item>
// </Accordion>
```

## Customization Points

- `ComponentName` — Replace with your component name
- Props interface — Add your specific props
- Styling — Adjust classes for your design system
- State logic — Modify for your use case

## Related Snippets

- [react-hook](react-hook.md) — Extract logic to hook
- [react-context](react-context.md) — State management
- [jest-test](../testing/jest-test.md) — Test components
