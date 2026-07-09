# Examples — React Pack

## Stable keys

Bad: `items.map((item, i) => <Row key={i} {...item} />)`
Good: `items.map(item => <Row key={item.id} {...item} />)`

## Derived state instead of sync effect

Bad:

```jsx
const [fullName, setFullName] = useState('');
useEffect(() => setFullName(`${first} ${last}`), [first, last]);
```

Good: `const fullName = `${first} ${last}`;` (computed inline, or `useMemo` if expensive).

## Server component default

```jsx
// page.tsx (server component, no "use client")
async function ProductPage({ id }) {
  const product = await db.products.findById(id); // direct backend access, zero client JS
  return <ProductView product={product} />;
}
```

`"use client"` added only to the interactive `AddToCartButton` subcomponent.

## Compound component over boolean props

Bad: `<Modal isLarge isCentered hasCloseButton hasFooter isDismissable />`
Good: `<Modal><Modal.Header/><Modal.Body/><Modal.Footer/></Modal>`
