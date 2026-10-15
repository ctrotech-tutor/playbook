self.addEventListener("message", event => {
  const values = event.data;
  if (!Array.isArray(values) || values.length > 100 ||
      !values.every(Number.isFinite)) {
    self.postMessage({ kind: "invalid" });
    return;
  }
  const total = values.reduce((sum, value) => sum + value, 0);
  self.postMessage(Number.isFinite(total) ? { kind: "sum", total } : { kind: "invalid" });
});
