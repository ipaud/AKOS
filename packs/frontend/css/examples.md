# Examples — CSS Pack

## Token-based spacing

```css
:root { --space-2: 8px; --space-4: 16px; --space-6: 24px; }
.card { padding: var(--space-4); gap: var(--space-2); }
```

## Container query

```css
.card-grid { container-type: inline-size; }
@container (min-width: 400px) {
  .card { grid-template-columns: 120px 1fr; }
}
```

## Mobile-first breakpoint

```css
.nav { display: block; }
@media (min-width: 768px) { .nav { display: flex; } }
```

## Compositor-only animation

```css
.modal { transform: translateY(20px); opacity: 0; transition: transform 200ms, opacity 200ms; }
.modal.open { transform: translateY(0); opacity: 1; }
```
