const CATEGORIES = {
  editorial: { label: "极简编辑", skill: "muyang-editorial-minimal" },
  colorblock: { label: "撞色时装", skill: "muyang-fashion-colorblock" },
  dream: { label: "柔焦梦幻", skill: "muyang-soft-dream" },
  couture: { label: "纯白高定", skill: "muyang-white-couture" },
  dark: { label: "暗黑时尚", skill: "muyang-dark-fashion" },
  oriental: { label: "东方诗意", skill: "muyang-oriental-poetry" },
  print: { label: "复古印刷", skill: "muyang-print-poster" },
  cinematic: { label: "电影叙事", skill: "muyang-cinematic-narrative" }
};

const STYLES = [
  { id: 1, name: "精致极简插画", group: "editorial", asset: "01-minimal-magazine.png", summary: "中性色、流畅线条、大面积留白与少量亮色焦点。" },
  { id: 2, name: "庭院手绘插画", group: "oriental", asset: "02-courtyard.png", summary: "白墙灰瓦、繁茂绿植、斑驳树影与水彩厚涂。" },
  { id: 3, name: "蓝白时尚插画", group: "colorblock", asset: "03-blue-white-fashion.png", summary: "蓝白骨架、锐利色块、冷蓝硬边阴影和杂志感。" },
  { id: 4, name: "极简现代插画", group: "editorial", asset: "04-modern-editorial.png", summary: "北欧与韩系编辑线描、旧纸颗粒和克制色块。" },
  { id: 5, name: "复古柔焦插画", group: "dream", asset: "05-retro-softfocus.png", summary: "低饱和复古水粉、暖灰雾粉与被漂白的旧画报感。" },
  { id: 6, name: "柔纱纯白插画", group: "couture", asset: "06-white-chiffon.png", summary: "高曝光白色空间、百褶纱与欧根纱的流动曲线。" },
  { id: 7, name: "暗调黑红插画", group: "dark", asset: "07-black-red.png", summary: "黑与暗酒红主调，猩红霓虹硬光切割主体。" },
  { id: 8, name: "韩系蓝白插画", group: "colorblock", asset: "08-korean-colorblock.png", summary: "半写实二次元、高纯色块与韩系商业品牌视觉。" },
  { id: 9, name: "柔焦烟灰插画", group: "dream", asset: "09-smoke-gray.png", summary: "冷灰绿雾化背景、冷白侧逆光与清冷忧郁气氛。" },
  { id: 10, name: "东方青绿插画", group: "oriental", asset: "10-oriental-green.png", summary: "青绿体系、留白、湖面远山与轻雾形成禅意空间。" },
  { id: 11, name: "黄黑撞色插画", group: "colorblock", asset: "11-yellow-black-fashion.png", summary: "明黄与纯黑强对比，硬边阴影和竖版时尚封面。" },
  { id: 12, name: "暗黑韩系插画", group: "dark", asset: "12-dark-korean.png", summary: "黑与冷灰暗部层次、少量暗红及商业精修材质。" },
  { id: 13, name: "梦幻鎏金插画", group: "dream", asset: "13-golden-dream.png", summary: "金色轮廓光与深海蓝阴影形成浪漫蓝橙对比。" },
  { id: 14, name: "极简墨灰插画", group: "oriental", asset: "14-ink-gray.png", summary: "冷灰、米白、浓墨块面与诗集封面式东方留白。" },
  { id: 15, name: "华丽银灰插画", group: "couture", asset: "15-silver-white-couture.png", summary: "冰蓝白、银灰、薄纱、珠链与水晶的冷艳高定感。" },
  { id: 16, name: "暗黑冷光插画", group: "dark", asset: "16-black-coldlight.png", summary: "纯黑背景、大量留黑和局部冷白硬光轮廓。" },
  { id: 17, name: "梦幻彩虹插画", group: "dream", asset: "17-rainbow-dream.png", summary: "粉蓝紫虹彩折射、高曝光柔光与半透明材质。" },
  { id: 18, name: "清冷夏日插画", group: "cinematic", asset: "18-cool-summer.png", summary: "低机位仰视、钴蓝天空、冷白硬光和夏日透明感。" },
  { id: 19, name: "复古剪影插画", group: "print", asset: "19-silhouette.png", summary: "米白、炭黑、暖黄三色和木刻印刷颗粒。" },
  { id: 20, name: "极简冰蓝插画", group: "editorial", asset: "20-ice-blue-editorial.png", summary: "冰蓝冷调、抽象几何、半透明叠层与优雅线条。" },
  { id: 21, name: "童话巨宠插画", group: "cinematic", asset: "21-giant-pet.png", summary: "巨大与渺小的尺度反差、暖灰留白和静默凝视。" },
  { id: 22, name: "复古电影插画", group: "print", asset: "22-retro-film.png", summary: "深青、红橙、奶油白大色块与建筑长投影。" },
  { id: 23, name: "粉蓝撞色插画", group: "colorblock", asset: "23-pink-blue-travel.png", summary: "珊瑚粉天空、海军蓝阴影与复古旅行海报气质。" },
  { id: 24, name: "日式版画插画", group: "print", asset: "24-japanese-print.png", summary: "旧纸、深墨主体、少量亮色和昭和木版画视觉。" },
  { id: 25, name: "柔焦霓虹插画", group: "dream", asset: "25-neon-softfocus.png", summary: "青蓝环境、暖橙粉光、水汽折射和胶片失焦。" }
];

const GENERATED_SAMPLES = [
  { styleId: 1, asset: "01-editorial-minimal.png", observation: "留白、黑白主体与一处暖橙焦点形成清晰编辑层级。" },
  { styleId: 3, asset: "02-fashion-colorblock.png", observation: "蓝白色块和冷光将同一阅读动作转为时装封面语言。" },
  { styleId: 5, asset: "03-soft-dream.png", observation: "低饱和米白与斑驳柔光呈现复古水粉质感。" },
  { styleId: 6, asset: "04-white-couture.png", observation: "高曝光纱质成立，但模型额外生成杂志文字，属于可见偏差。", status: "模型偏差" },
  { styleId: 7, asset: "05-dark-fashion.png", observation: "黑红硬光、重影与高反差明显改变叙事气质。" },
  { styleId: 2, asset: "06-oriental-poetry.png", observation: "主体缩小为庭院生活片段，空间与树影成为画面主角。" },
  { styleId: 19, asset: "07-print-poster.png", observation: "严格三色、纸张颗粒与剪影把主体压缩为版画符号。" },
  { styleId: 18, asset: "08-cinematic-narrative.png", observation: "钴蓝天空、低机位和冷白硬光建立清冷夏日感。" }
];

function assetPath(style) {
  const skill = CATEGORIES[style.group].skill;
  return `../upstream/skills/${skill}/assets/${style.asset}`;
}

const gallery = document.querySelector("#style-gallery");
const generatedGallery = document.querySelector("#generated-gallery");
const resultCount = document.querySelector("#result-count");
const styleSelect = document.querySelector("#style");
const styleNote = document.querySelector("#style-note");
const subjectInput = document.querySelector("#subject");
const constraintInput = document.querySelector("#constraint");
const callOutput = document.querySelector("#call-output");
const routeSkill = document.querySelector("#route-skill");
const routeDescription = document.querySelector("#route-description");
const copyStatus = document.querySelector("#copy-status");

function renderGeneratedGallery() {
  const fragment = document.createDocumentFragment();
  GENERATED_SAMPLES.forEach((sample, index) => {
    const style = STYLES.find((candidate) => candidate.id === sample.styleId);
    const category = CATEGORIES[style.group];
    const card = document.createElement("article");
    card.className = "generated-card";
    card.innerHTML = `
      <figure>
        <img src="assets/generated/${sample.asset}" alt="本研究生成的${style.name}样例：一个女孩在窗边读书" loading="${index < 2 ? "eager" : "lazy"}" decoding="async">
        <span class="sample-index">OUR ${String(index + 1).padStart(2, "0")}</span>
        ${sample.status ? `<strong class="sample-status">${sample.status}</strong>` : ""}
      </figure>
      <div class="generated-body">
        <span>${category.label} / 本研究生成</span>
        <h3>${style.name}</h3>
        <p>${sample.observation}</p>
        <button class="use-style" type="button" data-style-id="${style.id}">用此风格演示文字入参</button>
      </div>`;
    fragment.append(card);
  });
  generatedGallery.replaceChildren(fragment);
}

function renderGallery() {
  const fragment = document.createDocumentFragment();
  STYLES.forEach((style) => {
    const category = CATEGORIES[style.group];
    const card = document.createElement("article");
    card.className = "style-card";
    card.dataset.group = style.group;
    card.innerHTML = `
      <figure>
        <img src="${assetPath(style)}" alt="上游 ${style.name} 风格示意图" loading="lazy" decoding="async">
        <span class="style-index">${String(style.id).padStart(2, "0")}</span>
      </figure>
      <div class="style-body">
        <span class="style-meta">${category.label} / 上游示意</span>
        <h3>${style.name}</h3>
        <p>${style.summary}</p>
        <code>$${category.skill}</code>
        <button class="use-style" type="button" data-style-id="${style.id}">用此风格演示文字入参</button>
      </div>`;
    fragment.append(card);
  });
  gallery.replaceChildren(fragment);
}

function populateStyleSelect() {
  const fragment = document.createDocumentFragment();
  STYLES.forEach((style) => {
    const option = document.createElement("option");
    option.value = String(style.id);
    option.textContent = `${String(style.id).padStart(2, "0")} · ${style.name} / ${CATEGORIES[style.group].label}`;
    fragment.append(option);
  });
  styleSelect.replaceChildren(fragment);
  styleSelect.value = "2";
}

function selectedStyle() {
  return STYLES.find((style) => String(style.id) === styleSelect.value) || STYLES[0];
}

function buildCallText() {
  const style = selectedStyle();
  const subject = subjectInput.value.trim();
  const constraint = constraintInput.value.trim();
  const lines = [
    "$muyang-illustration",
    `主体：${subject || "（请填写主体文字）"}`,
    `风格：${style.name}`
  ];
  if (constraint) lines.push(constraint);
  return lines.join("\n");
}

function updateDemo() {
  const style = selectedStyle();
  const category = CATEGORIES[style.group];
  callOutput.textContent = buildCallText();
  styleNote.textContent = `${category.label}分类；总入口会路由到 $${category.skill}。`;
  routeSkill.textContent = `$muyang-illustration → $${category.skill}`;
  routeDescription.textContent = `子 Skill 读取“${style.name}”固定配方，仅替换主体占位符；真实 Codex 任务随后调用图像生成工具并直接返回图片。`;
  copyStatus.textContent = "";
}

document.querySelectorAll(".filter").forEach((button) => {
  button.addEventListener("click", () => {
    const filter = button.dataset.filter;
    document.querySelectorAll(".filter").forEach((candidate) => {
      const active = candidate === button;
      candidate.classList.toggle("is-active", active);
      candidate.setAttribute("aria-pressed", String(active));
    });
    let visible = 0;
    document.querySelectorAll(".style-card").forEach((card) => {
      const show = filter === "all" || card.dataset.group === filter;
      card.hidden = !show;
      if (show) visible += 1;
    });
    resultCount.textContent = `当前显示 ${visible} / 25 种风格`;
  });
});

function selectStyleFromCard(event) {
  const button = event.target.closest("[data-style-id]");
  if (!button) return;
  styleSelect.value = button.dataset.styleId;
  updateDemo();
  document.querySelector("#workbench").scrollIntoView({ behavior: "smooth", block: "start" });
  window.setTimeout(() => subjectInput.focus({ preventScroll: true }), 350);
}

gallery.addEventListener("click", selectStyleFromCard);
generatedGallery.addEventListener("click", selectStyleFromCard);

document.querySelector("#demo-form").addEventListener("submit", (event) => {
  event.preventDefault();
  updateDemo();
  callOutput.focus();
});

[styleSelect, subjectInput, constraintInput].forEach((control) => {
  control.addEventListener("input", updateDemo);
});

async function copyCall() {
  try {
    await navigator.clipboard.writeText(callOutput.textContent);
    copyStatus.textContent = "已复制调用文本。";
  } catch (error) {
    const helper = document.createElement("textarea");
    helper.value = callOutput.textContent;
    helper.setAttribute("readonly", "");
    helper.style.position = "fixed";
    helper.style.opacity = "0";
    document.body.append(helper);
    helper.select();
    const copied = typeof document.execCommand === "function" && document.execCommand("copy");
    helper.remove();
    copyStatus.textContent = copied ? "已复制调用文本。" : "浏览器未允许复制，请在上方手动选择。";
  }
}

document.querySelector("#copy-call").addEventListener("click", copyCall);

renderGallery();
renderGeneratedGallery();
populateStyleSelect();
updateDemo();
