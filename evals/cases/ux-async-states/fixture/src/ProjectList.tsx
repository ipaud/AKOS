import { useQuery } from "@tanstack/react-query";

export function ProjectList() {
  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["projects"],
    queryFn: fetchProjects,
  });

  if (isLoading) return <Spinner />;
  if (isError) return <ErrorState onRetry={refetch} />;
  if (data.length === 0) return <EmptyState action="Crea el primer projecte" />;

  return <ul>{data.map((p) => <li key={p.id}>{p.name}</li>)}</ul>;
}
