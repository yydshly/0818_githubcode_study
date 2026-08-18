const STYLES = {
  "1": {
    label: "01 · 极简黑白线条讲解漫画",
    reason: "适合把一个方法拆成 3–4 个步骤，文字结构清楚，视觉噪声低。",
    output: "prompt",
    note: "把内容拆成多格，每格包含准确的小标题和一句说明。"
  },
  "4": {
    label: "04 · 小豆人涂鸦信息图",
    reason: "竖版多格、单一橙色重点和手绘箭头，适合结论摘要与社媒信息卡。",
    output: "prompt",
    note: "从内容中提炼 3–4 个要点，指定每格唯一关键物。"
  },
  "10": {
    label: "10 · 情绪叙事淡彩速写",
    reason: "大片留白与单一橙色焦点，适合把里程碑、失败复盘或人物故事转成情绪场景。",
    output: "prompt",
    note: "只选择一件最能代表故事的橙色关键物，其他部分保持淡彩和留白。"
  },
  "11": {
    label: "11 · 二维水彩风格",
    reason: "复古动画概念稿气质，适合作为研究项目封面或专题主视觉。",
    output: "prompt",
    note: "把项目主题翻译成一个可见人物、动作或场景，而不是只画抽象标志。"
  },
  "17": {
    label: "17 · 墨线绘本",
    reason: "墨线提供结构，淡彩保留叙事感，适合较克制的人物与项目故事。",
    output: "prompt",
    note: "主体占主导，背景只保留理解故事所需的元素。"
  },
  "18": {
    label: "18 · 暖色扁平绘本",
    reason: "蓝橙几何色块、大片留白与清晰轮廓，适合现代项目封面和传播卡。",
    output: "prompt",
    note: "上游要求占位符使用英文；让 Agent 先忠实翻译主体，再交给渲染器。"
  },
  "3.1": {
    label: "3.1 · 蜡笔童涂—潦草自画版",
    reason: "固定锚点和三阶段编辑适合连续的团队或家庭日常故事，但调用成本最高。",
    output: "formal-json",
    note: "每张都附 style-only 锚点并完整执行两个修正阶段；前两张不是 final。"
  }
};

const SCENARIOS = {
  method: {
    label: "研究方法拆解",
    styles: ["1", "4"],
    content: "解释 GitHub 项目研究的四步闭环：固定版本、验证真实能力、阅读关键源码、形成可复现结论",
    title: "一个开源项目，应该怎样研究？",
    aspect: "3:4"
  },
  summary: {
    label: "研究结论摘要卡",
    styles: ["4", "18"],
    content: "Hand-drawn Styles 不是图像模型，而是位于用户需求与图像模型之间的视觉 Prompt 编排层",
    title: "它真正解决了什么？",
    aspect: "3:4"
  },
  cover: {
    label: "项目研究封面",
    styles: ["11", "18"],
    content: "一位研究者把零散提示词卡片整理成有编号的视觉配方档案，旁边连接着一个图像生成窗口",
    title: "Prompt as Visual Contract",
    aspect: "16:9"
  },
  milestone: {
    label: "项目里程碑故事",
    styles: ["10", "17"],
    content: "深夜里，一位开发者终于让全部回归测试通过，桌上只有亮着的屏幕和一只橙色马克杯",
    title: "终于，全部通过",
    aspect: "3:4"
  },
  family: {
    label: "团队 / 家庭日常故事卡",
    styles: ["3.1", "10"],
    content: "两位团队成员站在白板前复盘失败实验，其中一人把错误结果贴回证据墙，另一人认真记录",
    title: "失败样例也要留下",
    aspect: "3:4"
  }
};

const form = document.querySelector("#router-form");
const scenarioSelect = document.querySelector("#scenario");
const styleSelect = document.querySelector("#style");
const contentInput = document.querySelector("#content");
const titleInput = document.querySelector("#title");
const aspectSelect = document.querySelector("#aspect");
const styleReason = document.querySelector("#style-reason");
const output = document.querySelector("#output");
const copyButton = document.querySelector("#copy-output");
const copyStatus = document.querySelector("#copy-status");
const copyUsageButton = document.querySelector("#copy-usage-template");
const usageTemplate = document.querySelector("#usage-template");
const usageCopyStatus = document.querySelector("#usage-copy-status");

function updateStyleOptions(selectedStyle) {
  const scenario = SCENARIOS[scenarioSelect.value];
  styleSelect.replaceChildren();
  scenario.styles.forEach((styleId) => {
    const option = document.createElement("option");
    option.value = styleId;
    option.textContent = STYLES[styleId].label;
    option.selected = styleId === selectedStyle;
    styleSelect.append(option);
  });
  styleReason.textContent = STYLES[styleSelect.value].reason;
}

function loadScenario() {
  const scenario = SCENARIOS[scenarioSelect.value];
  updateStyleOptions(scenario.styles[0]);
  contentInput.value = scenario.content;
  titleInput.value = scenario.title;
  aspectSelect.value = scenario.aspect;
  renderInstruction();
}

function buildInstruction() {
  const scenario = SCENARIOS[scenarioSelect.value];
  const styleId = styleSelect.value;
  const style = STYLES[styleId];
  const content = contentInput.value.trim();
  const title = titleInput.value.trim();
  const aspect = aspectSelect.value;
  const lines = [
    "请使用固定在本项目 upstream/ 的 hand-drawn-styles 配方完成以下任务。",
    "",
    `日常用途：${scenario.label}`,
    `采用风格：${style.label}`,
    `画面内容：${content || "（请补充核心内容）"}`,
    `准确标题：${title || "不加任何文字"}`,
    `画幅比例：${aspect || "不硬锁比例，遵守上游协议"}`,
    "",
    "执行要求：",
    "1. 从 upstream/STYLES.md 原样提取该编号的完整代码块配方，不得缩写、同义改写或与其他风格混配。",
    "2. 只把内容、准确文字和比例填入上游占位符；不得追加第二套线条、五官、色板、材质或纸面规则。",
    `3. 场景路由提示：${style.note}`,
    "4. 若模型不能可靠生成准确中文，保留明确文字区域并报告需要后期排字，不要伪造乱码。"
  ];

  if (["1", "4"].includes(styleId)) {
    lines.push("5. 将核心内容拆成 3–4 格，每格只表达一个步骤或要点；先确保信息顺序，再填【N】和【分镜列表】。");
  }

  if (styleId === "10") {
    lines.push("5. 从内容中选择一件唯一的橙色关键物；标题过长时宁可留白后期排字，不要增加第二个强调色。");
  }

  if (styleId === "18") {
    lines.push("5. 按上游要求把【主体】【构图】【文字】填成英文；准确中文标题建议留白后期排字。");
  }

  if (styleId === "3.1") {
    lines.push(
      "5. 这是正式生产调用：必须输出 family-crayon-card-v3 JSON，而不是只返回 Prompt。",
      "6. 每张请求都附 upstream/assets/style-3.1/anchor-family.png，role=style-only；角色参考图只能作为另一份输入，不能替代锚点。",
      "7. 完整执行 base-generation → scribble-correction → scribble-chaos-correction；前两阶段均为 intermediate-only。",
      "8. 任一锚点校验或编辑阶段不可用时停止生产并明确报错，不得静默退回文本版。",
      "",
      "建议渲染器参数：",
      JSON.stringify({
        style: "3.1",
        subject: content,
        title: title || null,
        text: title ? null : "不加任何文字",
        aspect: aspect || null,
        format: "json"
      }, null, 2)
    );
  } else {
    lines.push("最终交付：只输出一段可直接交给图像模型的完整 Prompt，并注明采用的风格编号和是否注入比例。");
  }

  return lines.join("\n");
}

function renderInstruction() {
  output.textContent = buildInstruction();
  copyStatus.textContent = "";
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  renderInstruction();
  output.focus();
});

scenarioSelect.addEventListener("change", loadScenario);
styleSelect.addEventListener("change", () => {
  styleReason.textContent = STYLES[styleSelect.value].reason;
  renderInstruction();
});
[contentInput, titleInput, aspectSelect].forEach((control) => {
  control.addEventListener("change", renderInstruction);
});

async function copyText(text) {
  let copied = false;
  try {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(text);
      copied = true;
    }
  } catch (error) {
    copied = false;
  }

  if (!copied) {
    try {
      const helper = document.createElement("textarea");
      helper.value = text;
      helper.setAttribute("readonly", "");
      helper.style.position = "fixed";
      helper.style.opacity = "0";
      document.body.append(helper);
      helper.select();
      copied = typeof document.execCommand === "function" && document.execCommand("copy");
      helper.remove();
    } catch (error) {
      copied = false;
    }
  }

  return copied;
}

async function copyOutput() {
  const copied = await copyText(output.textContent);
  copyStatus.textContent = copied ? "已复制完整调用指令。" : "浏览器未允许复制，请在结果区手动选择。";
}

copyButton.addEventListener("click", copyOutput);

copyUsageButton?.addEventListener("click", async () => {
  const copied = await copyText(usageTemplate.textContent);
  usageCopyStatus.textContent = copied ? "已复制标准请求模板。" : "浏览器未允许复制，请在模板区手动选择。";
});

document.querySelectorAll(".filter").forEach((button) => {
  button.addEventListener("click", () => {
    const filter = button.dataset.filter;
    document.querySelectorAll(".filter").forEach((candidate) => {
      const active = candidate === button;
      candidate.classList.toggle("is-active", active);
      candidate.setAttribute("aria-pressed", String(active));
    });
    document.querySelectorAll(".style-card").forEach((card) => {
      card.hidden = filter !== "all" && card.dataset.group !== filter;
    });
  });
});

loadScenario();
