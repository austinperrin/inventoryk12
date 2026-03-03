export default function Home() {
  return (
    <section className="hero">
      <p className="eyebrow">Milestone 1</p>
      <h1>InventoryK12 frontend skeleton</h1>
      <p className="hero-copy">
        The app shell, route map, and baseline styling are in place so later
        milestone work can add auth flows and product screens without replacing
        the root structure.
      </p>
      <div className="hero-actions">
        <a className="hero-link" href="/api/v1/common/health/">
          Backend health endpoint
        </a>
        <span className="hero-hint">Next slice: auth and runtime plumbing.</span>
      </div>
    </section>
  );
}
