window.demoIntegrityRuns = (window.demoIntegrityRuns || 0) + 1;
const integrityStatus = document.getElementById("integrity-status");
if (integrityStatus) integrityStatus.textContent = "The supplied teaching script ran.";
