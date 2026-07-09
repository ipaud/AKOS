# Philosophy — TypeScript Pack

Types exist to make illegal states unrepresentable, not to satisfy a compiler ritual. `any` is an escape hatch that disables the entire tool for that value's lifetime — every `any` is a spot where a runtime error can't be caught at compile time, silently defeating the purpose of using TypeScript at all. Strictness is cheapest applied from project start; retrofitting strict mode onto a loose codebase is expensive but still worth doing incrementally, because every year of loose typing compounds bugs that strict mode would have caught for free.
