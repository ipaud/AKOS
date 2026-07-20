// The shared input surface for every form in the app.
//
// `text-sm` is 14px. iOS Safari auto-zooms the page whenever a focused field
// renders under 16px, which shoves the layout sideways on every form the
// technicians fill in on site.
export const fieldBase =
  "h-11 w-full rounded-xl border bg-card px-3.5 text-sm transition-colors";

export const Input = (props) => <input className={fieldBase} {...props} />;
