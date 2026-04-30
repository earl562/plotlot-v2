export default function ConnectorsPage() {
  return (
    <main style={{ padding: 24 }}>
      <h1 style={{ fontSize: 20, fontWeight: 600 }}>Connectors</h1>
      <p style={{ marginTop: 8, color: "#666" }}>
        Connector readiness and OAuth status will show up here. Run <code>make auth-readiness</code>{" "}
        locally to see which live lanes are configured.
      </p>
    </main>
  );
}

