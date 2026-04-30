export default async function AnalysisPage({
  params,
}: {
  params: Promise<{ projectId: string; siteId: string; analysisId: string }>;
}) {
  const { projectId, siteId, analysisId } = await params;
  return (
    <main style={{ padding: 24 }}>
      <h1 style={{ fontSize: 20, fontWeight: 600 }}>Analysis</h1>
      <p style={{ marginTop: 8, color: "#666" }}>projectId: {projectId}</p>
      <p style={{ marginTop: 4, color: "#666" }}>siteId: {siteId}</p>
      <p style={{ marginTop: 4, color: "#666" }}>analysisId: {analysisId}</p>
    </main>
  );
}
