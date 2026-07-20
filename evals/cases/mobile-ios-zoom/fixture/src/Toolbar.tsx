// Icon buttons in a dense row. 28px is under both platform floors and under
// the WCAG 2.2 SC 2.5.8 minimum of 24px once spacing is accounted for.
export function Toolbar() {
  return (
    <div className="flex gap-0">
      <button className="h-7 w-7">✎</button>
      <button className="h-7 w-7">⧉</button>
      <button className="h-7 w-7">🗑</button>
    </div>
  );
}
