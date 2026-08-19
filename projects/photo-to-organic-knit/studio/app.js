const elements = {
  tabs: document.querySelector("#template-tabs"),
  route: document.querySelector("#route-copy"),
  form: document.querySelector("#copy-form"),
  preview: document.querySelector("#preview-image"),
  previewLoading: document.querySelector("#preview-loading"),
  dimension: document.querySelector("#dimension-copy"),
  reset: document.querySelector("#reset-button"),
  render: document.querySelector("#render-button"),
  copyDownload: document.querySelector("#copy-download-button"),
  status: document.querySelector("#render-status"),
  statusKicker: document.querySelector("#status-kicker"),
  statusTitle: document.querySelector("#status-title"),
  statusDetail: document.querySelector("#status-detail"),
  gates: document.querySelector("#gate-list"),
  downloadRow: document.querySelector("#download-row"),
  pngDownload: document.querySelector("#png-download"),
  reportDownload: document.querySelector("#report-download"),
  serverCopyDownload: document.querySelector("#server-copy-download"),
  batch: document.querySelector("#batch-button"),
  batchDownload: document.querySelector("#batch-download"),
  batchStatus: document.querySelector("#batch-status"),
  showcaseLink: document.querySelector("[data-showcase-link]"),
};

const gateLabels = {
  dimensions: "输出尺寸",
  "exact-copy": "精确文案",
  overflow: "文字溢出",
  "protected-region": "主体保护区",
  contrast: "颜色对比",
  "sample-disclosure": "样例声明",
};

const studio = {
  templates: new Map(),
  originals: new Map(),
  copies: new Map(),
  results: new Map(),
  currentId: null,
  busy: false,
};

const clone = (value) => JSON.parse(JSON.stringify(value));

const getPath = (root, path) => path.split(".").reduce((value, part) => value?.[Number.isInteger(Number(part)) ? Number(part) : part], root);

const setPath = (root, path, value) => {
  const parts = path.split(".");
  let cursor = root;
  parts.forEach((part, index) => {
    const key = Number.isInteger(Number(part)) ? Number(part) : part;
    if (index === parts.length - 1) cursor[key] = value;
    else cursor = cursor[key];
  });
};

const currentTemplate = () => studio.templates.get(studio.currentId);
const currentCopy = () => studio.copies.get(studio.currentId);

const setBusy = (busy, label = "") => {
  studio.busy = busy;
  elements.render.disabled = busy;
  elements.batch.disabled = busy;
  elements.reset.disabled = busy;
  elements.previewLoading.hidden = !busy;
  if (busy && label) elements.previewLoading.querySelector("b").textContent = label;
};

const setStatus = (state, kicker, title, detail) => {
  elements.status.dataset.state = state;
  elements.statusKicker.textContent = kicker;
  elements.statusTitle.textContent = title;
  elements.statusDetail.textContent = detail;
};

const renderGatePlaceholders = () => {
  elements.gates.replaceChildren();
  Object.entries(gateLabels).forEach(([id, label]) => {
    const item = document.createElement("div");
    item.dataset.status = "PENDING";
    item.innerHTML = `<b>PENDING</b><span>${label}</span>`;
    elements.gates.append(item);
  });
};

const renderGates = (checks) => {
  elements.gates.replaceChildren();
  checks.forEach((check) => {
    const item = document.createElement("div");
    item.dataset.status = check.status;
    const variant = check.variant ? `${check.variant} · ` : "";
    item.innerHTML = `<b>${check.status}</b><span>${variant}${gateLabels[check.id] || check.id}</span>`;
    elements.gates.append(item);
  });
};

const renderTabs = () => {
  elements.tabs.replaceChildren();
  [...studio.templates.values()].forEach((template, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.role = "tab";
    button.dataset.templateId = template.id;
    button.setAttribute("aria-selected", String(template.id === studio.currentId));
    button.innerHTML = `<span>0${index + 1} / ${template.id.toUpperCase()}</span>${template.label}`;
    button.addEventListener("click", () => selectTemplate(template.id));
    elements.tabs.append(button);
  });
};

const renderFields = () => {
  const template = currentTemplate();
  const copy = currentCopy();
  elements.form.replaceChildren();
  template.fields.forEach((field, index) => {
    const wrapper = document.createElement("div");
    wrapper.className = "copy-field";
    const inputId = `copy-field-${index}`;
    const label = document.createElement("label");
    label.htmlFor = inputId;
    label.textContent = field.label;
    const input = document.createElement("input");
    input.id = inputId;
    input.name = field.path;
    input.type = "text";
    input.maxLength = 100;
    input.value = getPath(copy, field.path) ?? "";
    input.addEventListener("input", () => {
      setPath(copy, field.path, input.value);
      input.setAttribute("aria-invalid", String(!input.value.trim()));
      studio.results.delete(studio.currentId);
      elements.downloadRow.hidden = true;
      setStatus("dirty", "UNRENDERED EDIT", "文案已经修改", "当前预览仍是上次成功结果。重新渲染后才会更新 PNG 与门禁。");
    });
    wrapper.append(label, input);
    elements.form.append(wrapper);
  });
};

const selectTemplate = (templateId) => {
  studio.currentId = templateId;
  const template = currentTemplate();
  renderTabs();
  renderFields();
  elements.route.textContent = template.route;
  elements.dimension.textContent = template.dimensions;
  const result = studio.results.get(templateId);
  if (result) applyResult(result);
  else {
    elements.preview.src = template.sample_url;
    elements.preview.alt = `${template.label}样例输出`;
    elements.downloadRow.hidden = true;
    renderGatePlaceholders();
    setStatus("idle", "SAMPLE PREVIEW", `${template.label}样例`, "编辑左侧字段后，点击生成预览并检查。当前图片是项目保留样例。 ");
  }
};

const requestJson = async (url, payload) => {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const result = await response.json();
  if (!response.ok) {
    const error = new Error(result.error || `请求失败：${response.status}`);
    error.result = result;
    throw error;
  }
  return result;
};

const applyResult = (result) => {
  const template = studio.templates.get(result.template_id);
  const preferred = result.outputs.find((item) => item.variant === template.primary_variant) || result.outputs[0];
  if (preferred) {
    elements.preview.src = preferred.url;
    elements.preview.alt = `${template.label}本次确定性渲染结果`;
    elements.pngDownload.href = preferred.url;
  }
  elements.reportDownload.href = result.report_url;
  elements.serverCopyDownload.href = result.copy_url;
  elements.downloadRow.hidden = result.status !== "PASS";
  renderGates(result.checks || []);
  if (result.status === "PASS") {
    setStatus("pass", "PASS / VERIFIED LAYOUT", `${template.label}已经重新生成`, `本次输出通过 ${result.checks.length} 项模板门禁；内容审批仍在工具边界之外。`);
  } else {
    setStatus("fail", "FAIL / LAYOUT GATE", `${template.label}未通过`, "检查失败字段，修改文案后再次生成。上次成功预览不会被删除。 ");
  }
};

const renderCurrent = async () => {
  if (studio.busy) return;
  const copy = currentCopy();
  const emptyInput = [...elements.form.querySelectorAll("input")].find((input) => !input.value.trim());
  if (emptyInput) {
    emptyInput.focus();
    emptyInput.setAttribute("aria-invalid", "true");
    setStatus("fail", "INVALID COPY", "存在空白字段", "所有模板字段都必须有明确内容；不会自动补写。 ");
    return;
  }
  setBusy(true, "正在本地渲染与检查");
  setStatus("rendering", "RENDERING", "正在生成确定性预览", "同一请求会执行文案、溢出、对比、安全区、声明和尺寸检查。 ");
  try {
    const result = await requestJson("/api/render", { template_id: studio.currentId, copy });
    studio.results.set(studio.currentId, result);
    applyResult(result);
  } catch (error) {
    if (error.result?.checks) renderGates(error.result.checks);
    setStatus("fail", "FAIL / REQUEST", "本次生成失败", error.message);
  } finally {
    setBusy(false);
  }
};

const resetCurrent = () => {
  studio.copies.set(studio.currentId, clone(studio.originals.get(studio.currentId)));
  studio.results.delete(studio.currentId);
  selectTemplate(studio.currentId);
};

const downloadCurrentCopy = () => {
  const blob = new Blob([`${JSON.stringify(currentCopy(), null, 2)}\n`], { type: "application/json;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${currentCopy().campaign_id}-copy.json`;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
};

const renderBatch = async () => {
  if (studio.busy) return;
  const copies = Object.fromEntries([...studio.copies.entries()]);
  setBusy(true, "正在生成四类主版与 ZIP");
  elements.batchDownload.hidden = true;
  elements.batchStatus.textContent = "正在生成四种模板、五张主版、检查报告与 ZIP……";
  try {
    const result = await requestJson("/api/render-batch", { copies });
    elements.batchDownload.href = result.zip_url;
    elements.batchDownload.hidden = false;
    elements.batchStatus.textContent = `批量任务 ${result.batch_id} 已通过，可下载临时 ZIP。`;
  } catch (error) {
    elements.batchStatus.textContent = `批量任务失败：${error.message}`;
  } finally {
    setBusy(false);
  }
};

const init = async () => {
  try {
    const response = await fetch("/api/state", { cache: "no-store" });
    if (!response.ok) throw new Error(`状态接口返回 ${response.status}`);
    const payload = await response.json();
    payload.templates.forEach((template) => {
      studio.templates.set(template.id, template);
      studio.originals.set(template.id, clone(template.copy));
      studio.copies.set(template.id, clone(template.copy));
    });
    if (payload.showcase_url) elements.showcaseLink.href = payload.showcase_url;
    studio.currentId = payload.templates[0].id;
    selectTemplate(studio.currentId);
    elements.reset.addEventListener("click", resetCurrent);
    elements.render.addEventListener("click", renderCurrent);
    elements.copyDownload.addEventListener("click", downloadCurrentCopy);
    elements.batch.addEventListener("click", renderBatch);
  } catch (error) {
    setStatus("fail", "SERVER REQUIRED", "无法连接本地发布服务", `请运行 python studio/server.py 后重新打开页面。${error.message}`);
    elements.route.textContent = "本页面不能直接通过 file:// 运行";
    elements.render.disabled = true;
    elements.batch.disabled = true;
  }
};

init();
