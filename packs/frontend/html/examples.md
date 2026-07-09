# Examples — HTML Pack

Bad: `<div class="btn" onclick="submit()">Submit</div>`
Good: `<button type="submit">Submit</button>`

Bad: `<input placeholder="Email">`
Good: `<label for="email">Email</label><input id="email" type="email">`

Bad: `<div class="h3">Section title</div>` used for visual size only, no heading semantics
Good: `<h3>Section title</h3>` styled via CSS class, semantics preserved
