document.addEventListener("DOMContentLoaded", function () {
  if (typeof mermaid === "undefined") {
    return;
  }

  const isDark = document.body.classList.contains("dark");
  
  mermaid.initialize({
    startOnLoad: true,
    theme: isDark ? "dark" : "default",
    themeVariables: {
      lineColor: isDark ? "#ffffff" : "#333333",
      textColor: isDark ? "#ffffff" : "#333333",
      mainBkg: isDark ? "#2e2e33" : "#f8f9fa",
      nodeBorder: isDark ? "#ffffff" : "#333333",
    },
    securityLevel: 'loose',
  });
});
