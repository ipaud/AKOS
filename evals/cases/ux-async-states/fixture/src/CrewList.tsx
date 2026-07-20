import { useQuery } from "@tanstack/react-query";

export function CrewList({ projectId }) {
  const { data, isLoading } = useQuery({
    queryKey: ["crew", projectId],
    queryFn: () => fetchCrew(projectId),
  });

  if (isLoading) return <Spinner />;

  return (
    <ul>
      {data.map((c) => (
        <li key={c.id}>{c.name}</li>
      ))}
    </ul>
  );
}
