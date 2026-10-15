(() => {
  const form = document.getElementById("local-filter");
  const query = document.getElementById("catalogue-query");
  const list = document.getElementById("catalogue-list");
  const result = document.getElementById("catalogue-result");
  if (!form || !query || !list || !result) return;
  const items = [...list.children];
  form.addEventListener("submit", event => {
    event.preventDefault();
    const term = query.value.trim().toLocaleLowerCase("en");
    let count = 0;
    for (const item of items) {
      item.hidden = !item.textContent.toLocaleLowerCase("en").includes(term);
      if (!item.hidden) count++;
    }
    result.textContent = count === 0 ? "No supplied titles matched."
      : count + (count === 1 ? " supplied title matches." : " supplied titles match.");
  });
  form.addEventListener("reset", () => {
    for (const item of items) item.hidden = false;
    result.textContent = "All three teaching titles are listed below.";
  });
  for (const control of form.elements) control.disabled = false;
})();
