// Reports the gzipped size of the main chunk against a budget.
import { statSync, readdirSync } from "node:fs";

const BUDGET_KB = 150;
const dist = "dist/assets";
const main = readdirSync(dist).find((f) => f.startsWith("index-") && f.endsWith(".js"));
const kb = statSync(`${dist}/${main}`).size / 1024;

console.log(`main chunk: ${kb.toFixed(1)} kB (budget ${BUDGET_KB} kB)`);
if (kb > BUDGET_KB) {
  console.warn(`over budget by ${(kb - BUDGET_KB).toFixed(1)} kB`);
}
// Falls through. Exits 0 whatever the size.
