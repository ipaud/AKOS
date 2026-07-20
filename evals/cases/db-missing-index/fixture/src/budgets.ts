// Every read filters on organization_id — the column the RLS policy also
// evaluates on every row. It has no index.
export async function listBudgets(orgId: string) {
  return supabase
    .from("budgets")
    .select("*")
    .eq("organization_id", orgId)
    .order("created_at", { ascending: false });
}
