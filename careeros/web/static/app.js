"use strict";

const state = {
  snapshot: null,
  tab: "platform",
  query: "",
  status: "all",
  enabledOnly: false,
};

const el = {
  summary: document.getElementById("summary"),
  tabs: document.getElementById("tabs"),
  content: document.getElementById("content"),
  search: document.getElementById("search"),
  statusFilter: document.getElementById("status-filter"),
  enabledOnly: document.getElementById("enabled-only"),
  resultCount: document.getElementById("result-count"),
  generated: document.getElementById("generated"),
  paths: document.getElementById("paths"),
  refresh: document.getElementById("refresh"),
};

const STATUS_ORDER = ["supported", "pending", "disabled", "temporarily_unavailable", "blocked_or_restricted"];

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => {
    switch (char) {
      case "&":
        return "&amp;";
      case "<":
        return "&lt;";
      case ">":
        return "&gt;";
      case '"':
        return "&quot;";
      default:
        return "&#39;";
    }
  });
}

function labelForStatus(status) {
  const labels = (state.snapshot && state.snapshot.status_labels) || {};
  return labels[status] || status;
}

function safeUrl(raw) {
  try {
    const parsed = new URL(raw);
    return parsed.protocol === "http:" || parsed.protocol === "https:" ? parsed.href : null;
  } catch (error) {
    return null;
  }
}

function statusChip(rawStatus) {
  return `<span class="chip ${escapeHtml(rawStatus)}">${escapeHtml(labelForStatus(rawStatus))}</span>`;
}

function renderSummary() {
  const summary = state.snapshot.summary;
  const other = summary.temporarily_unavailable + summary.blocked_or_restricted;
  const cards = [
    { label: "Configured", value: state.snapshot.total, hint: "across all source files", accent: "#818cf8" },
    { label: "Supported", value: summary.supported, hint: "tested, healthy adapter", accent: "#34d399" },
    { label: "Pending", value: summary.pending, hint: "registered, not usable yet", accent: "#fbbf24" },
    { label: "Disabled", value: summary.disabled, hint: "kept, never queried", accent: "#94a3b8" },
    { label: "Unavailable / blocked", value: other, hint: "adapter health issue", accent: "#f87171" },
    { label: "Config issues", value: state.snapshot.issues.length, hint: "rows rejected visibly", accent: "#f472b6" },
  ];

  el.summary.innerHTML = cards
    .map(
      (card) => `
      <div class="card" style="--card-accent: ${card.accent}">
        <div class="label">${escapeHtml(card.label)}</div>
        <div class="value">${Number(card.value) || 0}</div>
        <div class="hint">${escapeHtml(card.hint)}</div>
      </div>`
    )
    .join("");
}

function renderTabs() {
  const tabs = Object.values(state.snapshot.kinds).map((kind) => ({
    id: kind.kind,
    label: kind.label,
    count: kind.record_count,
    issues: kind.issue_count,
  }));
  tabs.push({
    id: "issues",
    label: "Config issues",
    count: state.snapshot.issues.length,
    issues: state.snapshot.issues.length,
  });
  tabs.push({ id: "adapters", label: "Adapters", count: state.snapshot.adapters.length, issues: 0 });

  el.tabs.innerHTML = tabs
    .map(
      (tab) => `
      <button class="tab${tab.issues ? " has-issues" : ""}" role="tab" type="button"
        data-tab="${escapeHtml(tab.id)}" aria-selected="${tab.id === state.tab}">
        ${escapeHtml(tab.label)}<span class="count">${tab.count}</span>
      </button>`
    )
    .join("");
}

function renderStatusFilter() {
  const options = ['<option value="all">All statuses</option>']
    .concat(
      STATUS_ORDER.map(
        (status) =>
          `<option value="${status}">${escapeHtml(labelForStatus(status))} (${state.snapshot.summary[status]})</option>`
      )
    )
    .join("");
  el.statusFilter.innerHTML = options;
  el.statusFilter.value = state.status;
}

function filteredRecords(kind) {
  const query = state.query.trim().toLowerCase();
  return kind.records.filter((record) => {
    if (state.status !== "all" && record.raw_status !== state.status) return false;
    if (state.enabledOnly && !record.enabled) return false;
    if (!query) return true;
    const haystack = [
      record.name,
      record.url,
      record.adapter,
      record.filename,
      record.raw_status,
      ...Object.values(record.details || {}),
    ]
      .join(" ")
      .toLowerCase();
    return haystack.includes(query);
  });
}

function renderSourceTable(kind) {
  const records = filteredRecords(kind);
  el.resultCount.textContent = `${records.length} of ${kind.record_count} shown`;

  if (!kind.record_count) {
    el.content.innerHTML = `<div class="empty"><strong>No sources configured</strong>
      Add rows to ${escapeHtml(kind.filename)} using the format:
      <br /><code>${escapeHtml(kind.format)}</code></div>`;
    return;
  }

  if (!records.length) {
    el.content.innerHTML = `<div class="empty"><strong>Nothing matches</strong>Adjust the search or status filter.</div>`;
    return;
  }

  const rows = records
    .map((record) => {
      const url = safeUrl(record.url);
      const urlCell = url
        ? `<a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(record.url)}</a>`
        : escapeHtml(record.url);
      const detailBits = [];
      if (record.adapter) detailBits.push(`adapter: ${record.adapter}`);
      Object.entries(record.details || {}).forEach(([key, value]) => {
        if (value) detailBits.push(`${key}: ${value}`);
      });
      const reasons = (record.reasons || []).join(" · ");
      const override = record.origin === "override" ? '<span class="override-tag">override</span>' : "";
      return `
        <tr>
          <td class="name">${escapeHtml(record.name)}${override}</td>
          <td class="url">${urlCell}</td>
          <td class="details">${escapeHtml(detailBits.join("  ·  ")) || "—"}</td>
          <td class="status-cell">${statusChip(record.raw_status)}${
            reasons ? `<span class="reason">${escapeHtml(reasons)}</span>` : ""
          }</td>
          <td class="provenance">${escapeHtml(record.filename)}:${Number(record.line) || 0}</td>
        </tr>`;
    })
    .join("");

  el.content.innerHTML = `
    <table>
      <thead>
        <tr>
          <th>Source</th>
          <th>URL</th>
          <th>Details</th>
          <th>Status</th>
          <th>Defined at</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>`;
}

function renderIssues() {
  const issues = state.snapshot.issues;
  el.resultCount.textContent = `${issues.length} issue${issues.length === 1 ? "" : "s"}`;
  if (!issues.length) {
    el.content.innerHTML = `<div class="empty"><strong>All configured rows are valid</strong>
      Comments, blank lines, field counts, URLs, booleans, duplicates and overrides all pass validation.</div>`;
    return;
  }
  el.content.innerHTML = `<div class="issues">${issues
    .map(
      (issue) => `
      <article class="issue">
        <div class="head">
          <span class="code">${escapeHtml(issue.code)}</span>
          <span>${escapeHtml(issue.message)}</span>
          <span class="where">${escapeHtml(issue.filename)}:${Number(issue.line) || 0}</span>
        </div>
        ${issue.raw ? `<div class="raw">${escapeHtml(issue.raw)}</div>` : ""}
      </article>`
    )
    .join("")}</div>`;
}

function renderAdapters() {
  const adapters = state.snapshot.adapters;
  el.resultCount.textContent = `${adapters.length} adapter${adapters.length === 1 ? "" : "s"}`;
  if (!adapters.length) {
    el.content.innerHTML = `<div class="empty"><strong>No adapters registered</strong>
      Every configured source therefore resolves to pending.</div>`;
    return;
  }
  el.content.innerHTML = `<div class="adapters">${adapters
    .map(
      (adapter) => `
      <div class="adapter">
        <div>
          <div class="id">${escapeHtml(adapter.adapter_id)}</div>
          <div class="meta">${escapeHtml(adapter.display_name)} · kinds: ${escapeHtml(
        adapter.kinds.join(", ")
      )}</div>
        </div>
        <div class="notes">${escapeHtml(adapter.notes) || "No notes recorded."}</div>
        <div>${statusChip(adapter.health)}</div>
      </div>`
    )
    .join("")}</div>`;
}

function render() {
  if (!state.snapshot) return;
  renderSummary();
  renderTabs();
  renderStatusFilter();

  const kind = state.snapshot.kinds[state.tab];
  const isSourceTab = Boolean(kind);
  el.search.parentElement.style.display = isSourceTab ? "" : "none";
  el.statusFilter.parentElement.style.display = isSourceTab ? "" : "none";
  el.enabledOnly.parentElement.style.display = isSourceTab ? "" : "none";

  if (isSourceTab) {
    renderSourceTable(kind);
  } else if (state.tab === "issues") {
    renderIssues();
  } else {
    renderAdapters();
  }

  el.generated.textContent = `Loaded ${new Date(state.snapshot.generated_at).toLocaleString()}`;
  el.paths.textContent = `config: ${state.snapshot.config_dir}${
    state.snapshot.override_dir ? ` · overrides: ${state.snapshot.override_dir}` : " · no override layer"
  }`;
}

async function loadSnapshot() {
  el.refresh.disabled = true;
  try {
    const response = await fetch("/api/snapshot", { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload = await response.json();
    if (payload.error) throw new Error(payload.message || payload.error);
    state.snapshot = payload;
    if (!state.snapshot.kinds[state.tab] && state.tab !== "issues" && state.tab !== "adapters") {
      state.tab = Object.keys(state.snapshot.kinds)[0] || "issues";
    }
    render();
  } catch (error) {
    state.snapshot = null;
    el.summary.innerHTML = "";
    el.tabs.innerHTML = "";
    el.resultCount.textContent = "";
    el.content.innerHTML = `<div class="error">Could not load the source snapshot.\n${escapeHtml(
      error.message || error
    )}</div>`;
    el.generated.textContent = "snapshot failed";
  } finally {
    el.refresh.disabled = false;
  }
}

el.tabs.addEventListener("click", (event) => {
  const button = event.target.closest("[data-tab]");
  if (!button) return;
  state.tab = button.dataset.tab;
  render();
});

el.search.addEventListener("input", (event) => {
  state.query = event.target.value;
  render();
});

el.statusFilter.addEventListener("change", (event) => {
  state.status = event.target.value;
  render();
});

el.enabledOnly.addEventListener("change", (event) => {
  state.enabledOnly = event.target.checked;
  render();
});

el.refresh.addEventListener("click", loadSnapshot);

loadSnapshot();
