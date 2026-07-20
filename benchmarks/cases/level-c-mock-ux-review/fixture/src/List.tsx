export function List({ items }) {
  return (
    <ul>
      {items.map(i => <li key={i.id}>{i.name}</li>)}
    </ul>
  );
}
// No empty state, no loading state, no error state handled anywhere in this component.
