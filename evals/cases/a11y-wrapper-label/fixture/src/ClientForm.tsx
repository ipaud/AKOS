import { Field } from "./Field";

export function ClientForm() {
  return (
    <form>
      <Field label="Nom comercial" htmlFor="name">
        <input id="name" onChange={(e) => setName(e.target.value)} />
      </Field>

      {/* No Field, no label, no aria-label. */}
      <input type="search" placeholder="Cerca ràpida" />
    </form>
  );
}
