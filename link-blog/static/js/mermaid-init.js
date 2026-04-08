document.addEventListener("DOMContentLoaded", function () {
  if (typeof mermaid === "undefined") {
    return;
  }

  const getTheme = () => document.body.classList.contains("dark") ? "dark" : "default";

  mermaid.initialize({
    startOnLoad: true,
    theme: getTheme(),
    securityLevel: 'loose',
  });
});
