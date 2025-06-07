document.addEventListener("DOMContentLoaded", () => {
  const themeBtn = document.getElementById("toggleTheme");
  themeBtn.addEventListener("click", () => {
    const html = document.documentElement;
    const current = html.getAttribute("data-theme");
    html.setAttribute("data-theme", current === "dark" ? "light" : "dark");
  });
});

function readMore() {
  alert("This will open the full article soon.");
}
