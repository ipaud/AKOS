// Shape from a real design-system codebase. `<Input>` is a React component;
// its label comes from the `<Field label=…>` wrapper that renders it. JSX
// capitalises components precisely to distinguish them from HTML elements.
export function ClientForm() {
  return (
    <form>
      <Field label="Nom comercial" required>
        <Input placeholder="Ex: Tech Solutions" {...register("name")} />
      </Field>
      <Field label="Web">
        <Input placeholder="www.empresa.cat" {...register("web")} />
      </Field>
    </form>
  );
}
