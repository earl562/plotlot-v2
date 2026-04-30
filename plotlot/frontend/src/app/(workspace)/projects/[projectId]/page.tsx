export default async function ProjectPage({
  params,
}: {
  params: Promise<{ projectId: string }>;
}) {
  const { projectId } = await params;
  return (
    <main style={{ padding: 24 }}>
      <h1 style={{ fontSize: 20, fontWeight: 600 }}>Project</h1>
      <p style={{ marginTop: 8, color: "#666" }}>projectId: {projectId}</p>
    </main>
  );
}
