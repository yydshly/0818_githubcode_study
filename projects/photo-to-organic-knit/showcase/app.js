const compare = document.querySelector("[data-compare]");
const range = compare?.querySelector('input[type="range"]');

if (compare && range) {
  const updateReveal = () => compare.style.setProperty("--reveal", `${range.value}%`);
  range.addEventListener("input", updateReveal);
  updateReveal();
}

const effects = {
  knit: {
    image: "assets/generated/canoe-organic-knit.png",
    alt: "有机针织效果：红舟沿编织河流驶向针织山谷",
    material: "CROCHET · KNIT · FELT · MOHAIR",
    caption: "有机针织 / Organic Knit",
    kicker: "EFFECT 01 / TACTILE WARMTH",
    title: "把河流变成一根可以触摸的线",
    description: "编织路径承担视觉动线，山脉拆成有缝隙的织物岛，马海毛雾气让“穿过山门”的意境变得柔软而安静。",
    river: "多股编织毛线，线尾和粗细变化可见",
    mountains: "不对称针织块与毛毡层，留出背景缝隙",
    use: "家庭、旅行、儿童内容、温暖品牌视觉",
    value: "亲和、手作、可收藏，适合需要情感温度的内容",
    prompt: "assets/generated/PROMPTS.md",
  },
  paper: {
    image: "assets/generated/canoe-paper-cut.png",
    alt: "分层剪纸效果：红舟沿蓝灰纸带驶向重叠纸山",
    material: "COTTON PAPER · VELLUM · DECKLED EDGE",
    caption: "分层剪纸 / Layered Paper Cut",
    kicker: "EFFECT 02 / EDITORIAL SPACE",
    title: "用纸的边缘重新决定远近",
    description: "河流被压成一条带毛边的纸带，五层不对称山形依靠遮挡和投影建立空间，摄影细节被换成可读的编辑层级。",
    river: "连续蓝灰纸带，以毛边和抬起的边缘引导视线",
    mountains: "五张重叠纸片，半透明描图纸承担雾气",
    use: "杂志、报告封面、文化活动、现代品牌系统",
    value: "结构清晰、留白稳定，便于和标题及版式继续组合",
    prompt: "assets/generated/MULTI_EFFECT_PROMPTS.md#1-layered-paper-cut",
  },
  ceramic: {
    image: "assets/generated/canoe-ceramic-relief.png",
    alt: "陶瓷浮雕效果：釉色河槽穿过手工陶土山脉",
    material: "STONEWARE · SLIP · CELADON GLAZE",
    caption: "陶瓷浮雕 / Ceramic Bas-relief",
    kicker: "EFFECT 03 / COLLECTIBLE DEPTH",
    title: "让行进路线成为一条有深度的釉槽",
    description: "水路由釉料积聚形成真实凹槽，山脉成为手塑陶板，侧光把‘穿越’从平面路径变成可以感知的高低关系。",
    river: "青瓷釉色的深槽，釉料积聚和手工刻痕可见",
    mountains: "不规则石陶浮雕，白色泥浆脊线表现雾气",
    use: "文创、纪念品、展陈概念、包装与空间艺术",
    value: "强化实体收藏感，适合从视觉提案延伸到实物打样",
    prompt: "assets/generated/MULTI_EFFECT_PROMPTS.md#2-ceramic-bas-relief",
  },
  glass: {
    image: "assets/generated/canoe-stained-glass.png",
    alt: "彩色玻璃效果：蓝色玻璃河流由铅线贯穿山谷",
    material: "HAND-CUT GLASS · LEAD CAME · OPAL",
    caption: "彩色玻璃 / Stained Glass",
    kicker: "EFFECT 04 / LUMINOUS SYMBOL",
    title: "把山谷变成由光穿过的符号",
    description: "铅线承担原来由透视完成的结构，蓝色玻璃河流成为最亮的连续路径，红舟与黄衣被压缩成清晰的小型色彩锚点。",
    river: "蓝宝石玻璃带，由深色铅线分段并保持连续",
    mountains: "半透明玻璃切片构成门形，乳白玻璃表现雾",
    use: "文化空间、节庆视觉、音乐封面、仪式性品牌内容",
    value: "高识别、高色彩张力，适合需要象征感和远距离识别的场景",
    prompt: "assets/generated/MULTI_EFFECT_PROMPTS.md#3-stained-glass",
  },
  woodcut: {
    image: "assets/generated/canoe-woodcut.png",
    alt: "木刻版画效果：高对比刻线组成蜿蜒河流和山谷",
    material: "RELIEF INK · GOUGE MARKS · FIBER PAPER",
    caption: "木刻版画 / Reduction Woodcut",
    kicker: "EFFECT 05 / GRAPHIC RHYTHM",
    title: "用刀痕把流动压缩成黑白节奏",
    description: "河流由方向一致的刻线组成，山体退化为高对比块面，大面积纸白承担雾和距离，让故事从柔软转向坚定。",
    river: "深靛刻线形成高速而清晰的 S 形节奏",
    mountains: "粗重块面与轮廓刀痕，纸白直接成为空气",
    use: "出版、海报、音乐、户外品牌与历史主题内容",
    value: "缩小后仍有强轮廓，双色体系也更接近可控印刷",
    prompt: "assets/generated/MULTI_EFFECT_PROMPTS.md#4-reduction-woodcut",
  },
  diorama: {
    image: "assets/generated/canoe-miniature-diorama.png",
    alt: "微缩场景效果：树脂河流穿过软木和石膏山脉模型",
    material: "RESIN · CORK · PLASTER · COTTON MIST",
    caption: "微缩场景 / Miniature Diorama",
    kicker: "EFFECT 06 / NARRATIVE SPACE",
    title: "把意境变成可以绕着观看的小世界",
    description: "透明树脂水道建立真正的空间深度，软木与石膏山体形成可进入的山门，微型红舟把抽象隐喻重新拉回故事现场。",
    river: "半透明树脂槽，利用真实反光和微缩阴影制造深度",
    mountains: "软木、石膏和棉絮组成可见手工痕迹的模型层",
    use: "展览、游戏概念、博物馆教育、空间与产品提案",
    value: "叙事和空间关系最强，适合继续发展为动画或交互场景",
    prompt: "assets/generated/MULTI_EFFECT_PROMPTS.md#5-miniature-diorama",
  },
};

const effectFields = {
  image: document.querySelector("#effect-image"),
  material: document.querySelector("#effect-material"),
  caption: document.querySelector("#effect-caption"),
  kicker: document.querySelector("#effect-kicker"),
  title: document.querySelector("#effect-title"),
  description: document.querySelector("#effect-description"),
  river: document.querySelector("#effect-river"),
  mountains: document.querySelector("#effect-mountains"),
  use: document.querySelector("#effect-use"),
  value: document.querySelector("#effect-value"),
  prompt: document.querySelector("#effect-prompt-link"),
};

const selectEffect = (effectName) => {
  const effect = effects[effectName];
  if (!effect || !effectFields.image) return;
  effectFields.image.src = effect.image;
  effectFields.image.alt = effect.alt;
  effectFields.material.textContent = effect.material;
  effectFields.caption.textContent = effect.caption;
  effectFields.kicker.textContent = effect.kicker;
  effectFields.title.textContent = effect.title;
  effectFields.description.textContent = effect.description;
  effectFields.river.textContent = effect.river;
  effectFields.mountains.textContent = effect.mountains;
  effectFields.use.textContent = effect.use;
  effectFields.value.textContent = effect.value;
  effectFields.prompt.href = effect.prompt;
  document.querySelectorAll("[data-effect]").forEach((control) => {
    const active = control.dataset.effect === effectName;
    control.classList.toggle("is-active", active);
    if (control.getAttribute("role") === "tab") {
      control.setAttribute("aria-selected", String(active));
    }
  });
};

document.querySelectorAll("[data-effect]").forEach((control) => {
  control.addEventListener("click", () => selectEffect(control.dataset.effect));
});

const scenarios = {
  brand: {
    kicker: "BRAND / 品牌主视觉",
    title: "把真实品牌锚点变成可讲述的视觉徽章",
    input: "产品、门店、创始人、地标或活动照片",
    output: "KV、邀请函、社媒头图与无字封面底图",
    value: "快速验证“手作、自然、柔软、可收藏”的品牌方向",
    note: "Logo、价格和长文案应在 Figma 或专业排版软件中后期完成。",
  },
  travel: {
    kicker: "TRAVEL / 旅行纪念",
    title: "把路线、河流与山口编成一张可收藏的旅程",
    input: "旅行人物、铁路、街道、建筑、山川或露营照片",
    output: "纪念海报、明信片、路线封面与收藏卡",
    value: "路径类元素天然适合转成毛线动线和负形符号",
    note: "优先保留地标关系，而不是追求每一处背景都像原照片。",
  },
  family: {
    kicker: "FAMILY / 家庭绘本",
    title: "保留熟悉的轮廓，把成长瞬间变得柔软",
    input: "家庭、儿童、宠物与成长时刻的合法私有照片",
    output: "绘本扉页、成长卡、纪念册封面与节日卡",
    value: "纤维材料自然传递亲近、保护与手作记忆",
    note: "涉及儿童和家庭照片时，应限制上传、存储与公开展示范围。",
  },
  editorial: {
    kicker: "EDITORIAL / 编辑出版",
    title: "让报道照片拥有第二层概念，而不挤占版面",
    input: "文章主题照片、播客人物、专题摄影或历史素材",
    output: "杂志封面、专题首图、播客封面与栏目识别",
    value: "紧凑主体和大面积留白适合标题、导语与品牌系统",
    note: "事实性内容应保留来源说明，避免让艺术重构替代新闻证据。",
  },
  community: {
    kicker: "COMMUNITY / 社区公益",
    title: "用手作气质降低机构传播的距离感",
    input: "志愿者、社区空间、节庆与公益活动现场",
    output: "活动海报、感谢卡、招募视觉与成果封面",
    value: "保留事件锚点，同时获得温暖、共同制作的情绪",
    note: "人物肖像和组织标志需要授权；正式信息仍应后期排版。",
  },
  packaging: {
    kicker: "PACKAGING / 包装提案",
    title: "快速测试产品是否适合一条手作视觉资产线",
    input: "食品、家居、户外和文创产品照片",
    output: "季节限定插画、礼盒概念、标签方向与货架情绪板",
    value: "低成本比较不同隐喻、材质和构图对品牌感知的影响",
    note: "生成图是概念资产；印刷前仍需重绘、分色、打样与版权复核。",
  },
};

const fields = {
  kicker: document.querySelector("#scenario-kicker"),
  title: document.querySelector("#scenario-title"),
  input: document.querySelector("#scenario-input"),
  output: document.querySelector("#scenario-output"),
  value: document.querySelector("#scenario-value"),
  note: document.querySelector("#scenario-note"),
};

document.querySelectorAll("[data-scenario]").forEach((button) => {
  button.addEventListener("click", () => {
    const scenario = scenarios[button.dataset.scenario];
    if (!scenario) return;
    document.querySelectorAll("[data-scenario]").forEach((candidate) => {
      const active = candidate === button;
      candidate.classList.toggle("is-active", active);
      candidate.setAttribute("aria-selected", String(active));
    });
    Object.entries(fields).forEach(([name, element]) => {
      if (element) element.textContent = scenario[name];
    });
  });
});
