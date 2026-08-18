const scenes = {
  travel: {
    source: "assets/demo/inputs-v2/travel-coast.jpg",
    output: "assets/demo/outputs-v2/travel-coast-stamp.png",
    sourceLabel: "原创旅行摄影",
    outputLabel: "默认透明邮票",
    kicker: "TRAVEL / 3:2 LANDSCAPE",
    description: "高信息量风景最能体现齿孔边缘的“收藏品”语义；默认模式让画面直接延伸到齿孔。",
    sourceAlt: "海岸公路与红色踏板车的旅行照片",
    outputAlt: "旅行照片生成的透明邮票边输出",
  },
  architecture: {
    source: "assets/demo/inputs-v2/architecture-rain.jpg",
    output: "assets/demo/outputs-v2/architecture-rain-stamp.png",
    sourceLabel: "原创建筑摄影",
    outputLabel: "竖向透明邮票",
    kicker: "ARCHITECTURE / VERTICAL",
    description: "混凝土轮廓、树影与湿地反射在规则齿孔中形成强烈边界，适合建筑档案和作品集。",
    sourceAlt: "雨中现代主义混凝土建筑照片",
    outputAlt: "建筑照片生成的竖向透明邮票",
  },
  food: {
    source: "assets/demo/inputs-v2/breakfast-table.jpg",
    output: "assets/demo/outputs-v2/breakfast-table-stamp.png",
    sourceLabel: "原创餐饮静物",
    outputLabel: "方形透明邮票",
    kicker: "FOOD / SQUARE FLAT LAY",
    description: "顶视静物细节密集，邮票边能把普通菜单素材变成可分享的餐饮收藏卡。",
    sourceAlt: "亚麻桌布上的早餐静物照片",
    outputAlt: "早餐静物生成的方形透明邮票",
  },
  botanical: {
    source: "assets/demo/inputs-v2/botanical-glasshouse.jpg",
    output: "assets/demo/outputs-v2/botanical-glasshouse-stamp.png",
    sourceLabel: "原创植物摄影",
    outputLabel: "横向透明邮票",
    kicker: "BOTANICAL / FIELD RESEARCH",
    description: "层叠植物、玻璃与旧木桌提供丰富纹理，适合自然笔记、研究档案和 moodboard。",
    sourceAlt: "历史玻璃温室与植物标本桌照片",
    outputAlt: "植物温室照片生成的透明邮票",
  },
  social: {
    source: "assets/demo/inputs-v2/social-travel-story.png",
    output: "assets/demo/outputs-v2/social-travel-story-stamp.png",
    sourceLabel: "本地组装社交长帖",
    outputLabel: "长截图透明邮票",
    kicker: "SOCIAL POST / LONG CAPTURE",
    description: "这是最接近上游示例的场景：完整内容长帖直接变成带齿孔和投影的可发布素材。",
    sourceAlt: "由旅行、早餐和植物照片组成的社交长帖",
    outputAlt: "社交长帖生成的长图透明邮票",
  },
  poster: {
    source: "assets/demo/inputs-v2/field-notes-poster.png",
    output: "assets/demo/outputs-v2/field-notes-poster-stamp.png",
    sourceLabel: "本地组装编辑海报",
    outputLabel: "海报透明邮票",
    kicker: "EDITORIAL / FIELD NOTES",
    description: "海报本身已有完整信息层级，邮票边只负责增加媒介感，不改变内部排版。",
    sourceAlt: "以雨中建筑为主题的编辑海报",
    outputAlt: "编辑海报生成的透明邮票",
  },
};

const sceneButtons = [...document.querySelectorAll("[data-scene]")];
const sourceImage = document.querySelector("#scene-source");
const outputImage = document.querySelector("#scene-output");
const sourceLabel = document.querySelector("#scene-source-label");
const outputLabel = document.querySelector("#scene-output-label");
const sceneKicker = document.querySelector("#scene-kicker");
const sceneDescription = document.querySelector("#scene-description");

function selectScene(name) {
  const scene = scenes[name];
  sourceImage.src = scene.source;
  sourceImage.alt = scene.sourceAlt;
  outputImage.src = scene.output;
  outputImage.alt = scene.outputAlt;
  sourceLabel.textContent = scene.sourceLabel;
  outputLabel.textContent = scene.outputLabel;
  sceneKicker.textContent = scene.kicker;
  sceneDescription.textContent = scene.description;
  sceneButtons.forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.scene === name)));
}

sceneButtons.forEach((button) => button.addEventListener("click", () => selectScene(button.dataset.scene)));

const backgroundButtons = [...document.querySelectorAll("[data-preview-background]")];
const stampWell = document.querySelector(".stamp-well");

function selectBackground(name) {
  stampWell.dataset.background = name;
  backgroundButtons.forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.previewBackground === name)));
}

backgroundButtons.forEach((button) => button.addEventListener("click", () => selectBackground(button.dataset.previewBackground)));
