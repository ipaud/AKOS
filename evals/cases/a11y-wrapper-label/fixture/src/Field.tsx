// The wrapper that supplies the accessible name. Reviewing the call sites
// without reading this concludes every form in the app is unlabelled.
export function Field({ label, htmlFor, children }) {
  return (
    <div>
      <label htmlFor={htmlFor}>{label}</label>
      {children}
    </div>
  );
}
