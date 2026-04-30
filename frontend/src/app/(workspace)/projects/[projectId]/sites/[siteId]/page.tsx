export default async function SitePage({
  params,
}: {
  params: Promise<{ projectId: string; siteId: string }>;
}) {
  const { projectId, siteId } = await params;
  return (
    <main style={{ padding: 24 }}>
      <h1 style={{ fontSize: 20, fontWeight: 600 }}>Site</h1>
      <p style={{ marginTop: 8, color: "#666" }}>projectId: {projectId}</p>
      <p style={{ marginTop: 4, color: "#666" }}>siteId: {siteId}</p>
    </main>
  );
}
