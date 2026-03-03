export default function NotFound() {
  return (
    <section className="hero hero--compact">
      <p className="eyebrow">Route Scaffold</p>
      <h1>Page not found</h1>
      <p className="hero-copy">
        The frontend skeleton includes a fallback route so new pages can be
        added without leaving unmatched URLs undefined.
      </p>
      <a className="hero-link" href="/">
        Return to the home route
      </a>
    </section>
  );
}
