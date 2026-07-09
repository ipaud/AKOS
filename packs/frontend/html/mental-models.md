# Mental Models — HTML Pack

- **The element-first ladder:** native element → native element + ARIA attribute → full custom ARIA widget. Descend only as far as needed.
- **Document outline as a landmark map:** `header`/`nav`/`main`/`aside`/`footer` + heading hierarchy form the structure assistive tech and search engines both navigate by.
- **Forms as contracts:** every input's label, type, and validation state is part of the contract with the browser (autofill, validation UI) and with assistive tech — bypassing native form semantics forfeits both.
