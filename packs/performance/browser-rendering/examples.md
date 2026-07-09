# Examples — Browser Rendering Pack

## Composite-only slide-in

Bad:

```css
.drawer { left: -300px; transition: left 300ms; }
.drawer.open { left: 0; }
```

Good:

```css
.drawer { transform: translateX(-300px); transition: transform 300ms; }
.drawer.open { transform: translateX(0); }
```

Identical visual result; the good version never triggers layout.

## Batched reads/writes

Bad:

```js
boxes.forEach(box => {
  box.style.width = getWidth(box) + 'px';
  console.log(box.offsetHeight); // forces layout flush, every iteration
});
```

Good:

```js
const heights = boxes.map(box => box.offsetHeight); // all reads first
boxes.forEach((box, i) => { box.style.width = getWidth(box, heights[i]) + 'px'; }); // all writes after
```

## Scoped will-change

```js
el.addEventListener('mouseenter', () => el.style.willChange = 'transform');
el.addEventListener('transitionend', () => el.style.willChange = 'auto');
```

Applied only around the animation window, not permanently.

## IntersectionObserver instead of scroll listener

Bad: `scroll` listener computing element visibility on every tick.
Good:

```js
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => e.target.classList.toggle('visible', e.isIntersecting));
});
items.forEach(item => observer.observe(item));
```

## Virtualized list (React, via a library)

```jsx
<FixedSizeList height={600} itemCount={items.length} itemSize={48}>
  {({ index, style }) => <Row style={style} item={items[index]} />}
</FixedSizeList>
```

Only visible rows (~15-20) are mounted regardless of `items.length`.
