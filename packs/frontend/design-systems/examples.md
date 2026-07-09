# Examples — Design Systems Pack

## Three-layer tokens

```css
/* reference */
--blue-600: #2563eb;
/* system (semantic) */
--color-action-primary: var(--blue-600);
/* component */
--button-primary-bg: var(--color-action-primary);
```

## Deprecation path

```jsx
// v1: <Button size="big" />  (deprecated, still works)
// v2: <Button size="lg" />   (new canonical prop)
function Button({ size, ...props }) {
  const resolvedSize = size === 'big' ? (warnDeprecated('size="big"', 'size="lg"'), 'lg') : size;
  // ...
}
```

## Composition for high-variance components

```jsx
<Card>
  <Card.Image src="..." />
  <Card.Title>Product name</Card.Title>
  <Card.Actions><Button>Buy</Button></Card.Actions>
</Card>
```
instead of one `Card` with 15 conditional-rendering props.
