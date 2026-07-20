/**
 * Capability-based access control for the office roles.
 *
 * UI gating is the fast layer; the real boundary is the RLS in
 * supabase/migrations/0009_roles.sql. This file decides what to render, not
 * what a request is allowed to do.
 */
export type Capability = "financials" | "operations" | "settings";

const MATRIX: Record<string, Capability[]> = {
  owner: ["financials", "operations", "settings"],
  warehouse: ["operations"],
};

export function can(role: string, cap: Capability): boolean {
  return (MATRIX[role] ?? []).includes(cap);
}
