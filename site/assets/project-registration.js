"use strict";
(() => {
  const form = document.getElementById("demo-form");
  if (!form) return;
  const fields = ["demo-name", "demo-email", "demo-session"].map(id => document.getElementById(id));
  const summary = document.getElementById("demo-errors");
  const list = document.getElementById("demo-error-list");
  const result = document.getElementById("demo-result");
  const errors = new Map();
  function validate(field) {
    if (field.id === "demo-name") {
      field.setCustomValidity(field.value.trim() ? "" : "Enter a fictional practice name.");
    }
    if (field.validity.valid) return "";
    if (field.id === "demo-name") return "Enter a fictional practice name.";
    if (field.id === "demo-email") return field.validity.valueMissing
      ? "Enter a practice email address."
      : "Use one syntactically valid email address, such as reader@example.invalid.";
    return "Choose a practice session.";
  }
  function showField(field, message) {
    const node = document.getElementById(field.id + "-error");
    node.textContent = message;
    node.hidden = !message;
    if (message) field.setAttribute("aria-invalid", "true");
    else field.removeAttribute("aria-invalid");
  }
  function showSummary() {
    list.replaceChildren();
    for (const field of fields) {
      const message = errors.get(field.id);
      if (!message) continue;
      const item = document.createElement("li");
      const link = document.createElement("a");
      link.href = "#" + field.id;
      link.textContent = message;
      link.addEventListener("click", event => {
        event.preventDefault();
        field.focus();
      });
      item.append(link);
      list.append(item);
    }
    summary.hidden = errors.size === 0;
  }
  form.addEventListener("submit", event => {
    event.preventDefault();
    errors.clear();
    result.textContent = "";
    for (const field of fields) {
      const message = validate(field);
      showField(field, message);
      if (message) errors.set(field.id, message);
    }
    showSummary();
    if (errors.size) summary.focus();
    else result.textContent = "The fields passed the browser checks. No application was sent or saved by this demonstration.";
  });
  for (const field of fields) {
    const update = () => {
      result.textContent = "";
      if (!errors.has(field.id)) return;
      const message = validate(field);
      showField(field, message);
      if (message) errors.set(field.id, message);
      else errors.delete(field.id);
      showSummary();
    };
    field.addEventListener("input", update);
    field.addEventListener("change", update);
  }
  form.addEventListener("reset", () => {
    errors.clear();
    for (const field of fields) {
      field.setCustomValidity("");
      showField(field, "");
    }
    showSummary();
    result.textContent = "Example fields reset. No application was sent.";
  });
  // Enable the custom-summary path only after its handlers exist.
  form.noValidate = true;
  document.getElementById("demo-fields").disabled = false;
})();
