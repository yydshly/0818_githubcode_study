document.documentElement.classList.add("js");

const walkthroughs = {
  browse: {
    title: "拖动墙面，滚轮缩放。",
    copy: "相机在逻辑墙面坐标中移动，远处的卡片也能被发现。",
  },
  inspect: {
    title: "悬停卡片，再点击聚焦。",
    copy: "Raycaster 选中纸张后，镜头移动到目标，其他卡片逐渐变暗，DOM 详情面板同时打开。",
  },
  create: {
    title: "点击墙上的发光加号。",
    copy: "填写内容、分类、纸张和标签后进入放置模式；卡片跟随指针，并在点击墙面时完成 3D 落位。",
  },
};

const capabilities = {
  data: {
    label: "LAYER 01 · DATA",
    title: "一份数据，同时驱动纸面与空间。",
    description: "分类、作者、正文、纸张、附件、位置、旋转和互动数值保存在统一对象中。页面内置八个分类和八种纸张。",
    points: ["统一 P() 默认值工厂", "约二十条固定内容样例", "wallStateJSON() 后端适配钩子"],
    source: "https://github.com/thebuggeddev/promise-wall/blob/0cb1b20c3952e4c4184b7e0e33fe5acfac2b4447/index.html#L1482-L1874",
    sourceLabel: "查看固定源码 1482–1874 ↗",
  },
  texture: {
    label: "LAYER 02 · CANVAS TEXTURE",
    title: "纸张不是素材包，而是现场绘制。",
    description: "Canvas 负责撕边、Alpha、纸纤维、色斑、横线、方格、手写字和涂鸦；生成结果再成为 Three.js CanvasTexture。",
    points: ["512px 独立纹理", "自动换行与字号收敛", "照片、墙面与木纹同样程序化生成"],
    source: "https://github.com/thebuggeddev/promise-wall/blob/0cb1b20c3952e4c4184b7e0e33fe5acfac2b4447/index.html#L2017-L2456",
    sourceLabel: "查看固定源码 2017–2456 ↗",
  },
  scene: {
    label: "LAYER 03 · THREE.JS SCENE",
    title: "一间延伸到镜头之外的房间。",
    description: "大墙面、木地板、踢脚线、接触阴影、环境灰尘和暖色光源共同建立空间。纸张顶点被轻微弯曲，并可叠放。",
    points: ["PerspectiveCamera + 多光源", "PCF 软阴影 + ACES Tone Mapping", "图钉、胶带与夹子为真实几何"],
    source: "https://github.com/thebuggeddev/promise-wall/blob/0cb1b20c3952e4c4184b7e0e33fe5acfac2b4447/index.html#L2458-L2810",
    sourceLabel: "查看固定源码 2458–2810 ↗",
  },
  interaction: {
    label: "LAYER 04 · SPATIAL INPUT",
    title: "指针先进入射线，再回到墙面。",
    description: "Raycaster 负责卡片命中和墙面交点；拖动改变相机目标，滚轮改变距离，放置模式让新纸张跟随指针并在边缘自动平移。",
    points: ["悬停抬升与轻微音效", "选中聚焦并压暗背景", "GSAP 完成落纸、回弹和按钉时间线"],
    source: "https://github.com/thebuggeddev/promise-wall/blob/0cb1b20c3952e4c4184b7e0e33fe5acfac2b4447/index.html#L2835-L3358",
    sourceLabel: "查看固定源码 2835–3358 ↗",
  },
  product: {
    label: "LAYER 05 · DOM PRODUCT UI",
    title: "WebGL 负责记忆，DOM 负责理解。",
    description: "搜索、导航、详情、表单和反馈保留在语义 HTML 中；少量 DOM 控件通过 3D 向量投影获得空间锚点。",
    points: ["搜索作者、正文、分类和标签", "详情、最近添加与创建弹窗", "支持/收藏/举报只是内存模拟"],
    source: "https://github.com/thebuggeddev/promise-wall/blob/0cb1b20c3952e4c4184b7e0e33fe5acfac2b4447/index.html#L3088-L3581",
    sourceLabel: "查看固定源码 3088–3581 ↗",
  },
};

const sceneOrder = ["newyear", "graduation", "wedding", "goals", "recognition", "publicgood", "anonymous", "family", "travel", "brand", "city", "game"];
const scenes = {
  newyear: {
    counter: "01 / 12", toolbar: "新年愿望墙", eyebrow: "SCENE 01 · NEW YEAR", title: "新年愿望墙",
    description: "用户写下明年的目标与愿望，完成一次郑重封存。跨年倒计时让等待成为体验，零点时整面墙共同开启。",
    who: "跨年活动参与者、朋友、家人和未来的自己", write: "明年的目标、愿望、约定和想改变的一件事",
    change: "纸条折成信封，显示封蜡、倒计时和跨年开启状态", memory: "零点钟声后，整面墙从暗处亮起并同时开封",
    caption: "倒计时归零时，所有愿望一起迎来新年的第一次开启。",
    cards: [["明年去看更大的世界", "开启倒计时 · 135 天"], ["把身体照顾好", "封存至 2027.01.01"], ["认真完成那件小事", "跨年统一开启"]],
  },
  graduation: {
    counter: "02 / 12", toolbar: "毕业留言墙", eyebrow: "SCENE 02 · GRADUATION", title: "毕业留言墙",
    description: "班级不只留下一串名字。照片卡、同学寄语和未来计划被放进校园墙面，并按班级与年份形成清晰分区。",
    who: "毕业生、同学、老师和多年后回来探望的人", write: "同学寄语、校园照片、未来计划和最舍不得的一刻",
    change: "墙面出现班级分区、拍立得照片、校色胶带和毕业年份", memory: "每个班拥有一块共同照片墙，多年后仍能按年份回来查看",
    caption: "离开校园之前，把我们共同度过的时间留在同一面墙上。",
    cards: [["别忘了操场边的晚风", "高三（2）班 · 留言 38"], ["十年后还要再见", "未来计划 · 2036"], ["最后一张班级合照", "毕业影像 · 06.18"]],
  },
  wedding: {
    counter: "03 / 12", toolbar: "婚礼祝福墙", eyebrow: "SCENE 03 · WEDDING", title: "婚礼祝福墙",
    description: "来宾写下祝福和共同回忆，卡片像邀请函一样被装入信封。花瓣与暖光回应现场情绪，并保留周年重新开启的约定。",
    who: "新人、亲友、无法到场的人和未来周年纪念时的两个人", write: "来宾祝福、共同回忆、婚后愿望和想留到周年的话",
    change: "信封出现姓名蜡印，花瓣缓慢落下，祝福在暖光中聚拢", memory: "第一周年时，封存的祝福再次开启并组成一封共同的长信",
    caption: "祝福在今天被送达，也为未来的周年留下一次重新开启。",
    cards: [["愿你们一直有话可说", "来自大学同学"], ["记得第一次旅行吗", "共同回忆 · 已珍藏"], ["留给一周年的你们", "开启于 2027.05.20"]],
  },
  goals: {
    counter: "04 / 12", toolbar: "企业目标墙", eyebrow: "SCENE 04 · TEAM GOALS", title: "企业目标墙",
    description: "团队承诺和季度目标按部门进入不同区域。完成不是简单勾选，而是盖下日期印章，并让部门植物从种子继续生长。",
    who: "项目团队、部门负责人和季度复盘参与者", write: "团队承诺、季度目标、关键行动和需要协作的事项",
    change: "部门颜色形成分区，完成项获得印章，进度推动对应植物生长", memory: "季度结束时，一眼看见哪些目标开花、哪些仍需要共同照料",
    caption: "目标不再堆在表格里，而是成为一面看得见团队状态的墙。",
    cards: [["产品组 · 完成首轮验证", "Q3 · 已盖完成印章"], ["市场组 · 找到核心叙事", "进度 72% · 长出新叶"], ["支持组 · 缩短响应时间", "需要跨部门协作"]],
  },
  recognition: {
    counter: "05 / 12", toolbar: "员工感谢墙", eyebrow: "SCENE 05 · RECOGNITION", title: "员工感谢墙",
    description: "每一条具体认可都通过金线连接到被感谢的人。人物卡自动聚合，月底时整面墙形成一份关系与贡献的共同回顾。",
    who: "团队成员、跨部门伙伴和管理者", write: "对同事的具体认可、被帮助的时刻和不应被遗漏的贡献",
    change: "感谢卡获得暖光并连向人物聚合区，月底生成金色关系网络", memory: "月度回顾不是排行榜，而是看到团队怎样彼此托住",
    caption: "一句具体的感谢，会让看不见的协作在墙上留下连接。",
    cards: [["谢谢你接住那次发布", "连接：林岚 · 产品组"], ["你让新人更快融入", "本月收到 6 段感谢"], ["最难的时候你没有离开", "月度回顾 · 已收录"]],
  },
  publicgood: {
    counter: "06 / 12", toolbar: "公益承诺墙", eyebrow: "SCENE 06 · PUBLIC GOOD", title: "公益承诺墙",
    description: "环保、志愿和社会行动被转化成可累积的花园。行动计数推动群体图案生长，让参与者看见微小行动如何成为公共变化。",
    who: "公益组织、志愿者、社区居民和校园行动参与者", write: "具体行动承诺、志愿时长、环保目标和已经完成的贡献",
    change: "每次行动增加叶片和计数，相同主题聚成树木或群体图案", memory: "活动结束时，所有人的行动共同长成一幅可投屏的公共景观",
    caption: "不是说过什么，而是完成了多少行动，决定花园最终长成什么样。",
    cards: [["本月步行代替开车 8 次", "绿色出行 · 8/12"], ["周末参加河岸清理", "志愿行动 · 4 小时"], ["为社区种下一棵树", "群体图案 · 第 286 片叶"]],
  },
  anonymous: {
    counter: "07 / 12", toolbar: "匿名心声墙", eyebrow: "SCENE 07 · INNER VOICE", title: "匿名心声墙",
    description: "身份退到背景，压力、困惑和希望先以折叠纸条出现。隐私模式保持克制，回应不是点赞，而是一圈温和的光。",
    who: "校园心理支持、员工心声、社区互助和私人情绪记录", write: "压力、困惑、无法当面说出口的需求和微小希望",
    change: "文字安静展开，敏感信息保持遮蔽，理解与陪伴化作非竞争性光圈", memory: "最重要的瞬间不是爆发，而是发现自己并不孤单",
    caption: "这里不评判谁更重要，只让一句真话得到安静的回应。",
    cards: [["最近真的有点累", "2 人回应：我理解你"], ["我害怕让大家失望", "隐私模式 · 刚刚展开"], ["希望明天轻一点", "一圈暖光正在靠近"]],
  },
  family: {
    counter: "08 / 12", toolbar: "家庭记忆墙", eyebrow: "SCENE 08 · FAMILY", title: "家庭记忆墙",
    description: "老照片、家庭故事和语音按年代进入旧纸与相框。墙像一条可以走近的家庭时间线，声音让照片重新拥有现场感。",
    who: "家庭成员、长辈、孩子和未来整理家族档案的人", write: "老照片背后的故事、人物关系、重要日期和口述语音",
    change: "相框与旧纸按年代分区，点击卡片出现语音播放提示和人物关系", memory: "听见熟悉声音时，一张静态照片重新变成共同经历",
    caption: "照片保存样子，声音保存一个人当时怎样讲述这段生活。",
    cards: [["外婆第一次进城", "1968 · 语音 01:24"], ["全家搬进新家", "1997 · 家庭相册"], ["小满学会走路", "2025 · 三代人共同记录"]],
  },
  travel: {
    counter: "09 / 12", toolbar: "旅行记忆墙", eyebrow: "SCENE 09 · JOURNEY", title: "旅行记忆墙",
    description: "地点、照片、车票和故事以明信片方式落在地图区域中。路线将零散片段连接起来，让一次旅行重新获得方向。",
    who: "旅行者、伴侣、朋友和记录长期旅程的人", write: "地点、照片、车票、途中故事和下一次想去的地方",
    change: "明信片落在地图分区，路线连接车站、城市和重要片段", memory: "沿着一条线重新走完整段旅程，并发现当时遗漏的故事",
    caption: "每张明信片是一个停靠点，路线让回忆重新开始移动。",
    cards: [["清晨抵达青森", "AOMORI · 08:42"], ["海边那班慢车", "路线 02 · 车票已保存"], ["下一站去更远的地方", "待完成 · 西北方向"]],
  },
  brand: {
    counter: "10 / 12", toolbar: "品牌故事墙", eyebrow: "SCENE 10 · BRAND STORY", title: "品牌故事墙",
    description: "用户证言和产品故事进入统一品牌空间。舞台自动导览代表性故事，并把最有共鸣的内容带到活动大屏。",
    who: "品牌用户、发布会来宾、社区成员和内容策展团队", write: "真实使用故事、产品时刻、用户证言和共同价值",
    change: "品牌色定义空间，导览光标依次聚焦故事，精选内容进入大屏模式", memory: "观众不是看广告，而是看见真实用户如何共同构成品牌",
    caption: "品牌退到背景，让真实故事成为整个空间的主角。",
    cards: [["它陪我完成第一次远行", "用户故事 · 自动导览 01"], ["这个小改变真的有用", "产品时刻 · 大屏精选"], ["我们为什么一直留下", "社区证言 · 2.4k 共鸣"]],
  },
  city: {
    counter: "11 / 12", toolbar: "城市故事墙", eyebrow: "SCENE 11 · CITY MEMORY", title: "城市故事墙",
    description: "居民记忆和城市变化被放进街区分区与年代层。公共展览同时展示过去、现在和未来，让城市不只剩下地标。",
    who: "居民、城市研究者、地方文化机构和公共展览观众", write: "居民记忆、街区照片、城市变化和对未来生活的愿望",
    change: "墙按街区划分，内容叠入年代层，公共模式轮播不同区域", memory: "同一地点的过去与现在在眼前重叠，形成一座城市的共同时间",
    caption: "城市不是一张地图，而是许多人对同一条街的不同记忆。",
    cards: [["旧影院最后一场电影", "东街区 · 1986"], ["河岸重新开放那天", "南岸 · 2024"], ["希望这里保留一棵树", "未来层 · 居民提案"]],
  },
  game: {
    counter: "12 / 12", toolbar: "游戏线索墙", eyebrow: "SCENE 12 · GAME CLUES", title: "游戏线索墙",
    description: "人物、地点、证据和任务通过连线组成调查空间。部分信息保持隐藏，只有建立正确关系或完成阶段目标后才会解锁。",
    who: "剧情游戏玩家、密室参与者和互动叙事观众", write: "人物关系、地点、证据、推理假设和当前任务",
    change: "红线连接证据，模糊卡片保留隐藏信息，阶段完成后依次解锁", memory: "最后一条关系成立时，整面线索墙重新排列并显露真相",
    caption: "答案不是直接显示出来，而是在玩家建立正确关系后被解锁。",
    cards: [["凌晨离开车站的人", "人物 A · 关系未确认"], ["被撕掉一角的车票", "证据 07 · 已连接"], ["仓库二层的锁门", "阶段 03 · 尚未解锁"]],
  },
};

const demo = document.querySelector("#upstream-demo");
const demoLoading = document.querySelector("#demo-loading");
demo.addEventListener("load", () => demoLoading.classList.add("done"));
document.querySelector("#reload-demo").addEventListener("click", () => {
  demoLoading.classList.remove("done");
  demo.src = demo.src;
});

document.querySelectorAll("[data-walkthrough]").forEach((button) => {
  button.addEventListener("click", () => {
    const item = walkthroughs[button.dataset.walkthrough];
    document.querySelectorAll("[data-walkthrough]").forEach((candidate) => candidate.setAttribute("aria-selected", String(candidate === button)));
    document.querySelector("#walkthrough-copy").innerHTML = `<strong>${item.title}</strong><span>${item.copy}</span>`;
  });
});

document.querySelectorAll("[data-capability]").forEach((button) => {
  button.addEventListener("click", () => {
    const item = capabilities[button.dataset.capability];
    document.querySelectorAll("[data-capability]").forEach((candidate) => candidate.setAttribute("aria-selected", String(candidate === button)));
    document.querySelector("#capability-label").textContent = item.label;
    document.querySelector("#capability-title").textContent = item.title;
    document.querySelector("#capability-description").textContent = item.description;
    document.querySelector("#capability-points").innerHTML = item.points.map((point) => `<li>${point}</li>`).join("");
    const source = document.querySelector("#capability-source");
    source.href = item.source;
    source.textContent = item.sourceLabel;
  });
});

const experience = document.querySelector(".experience-shell");
const playButton = document.querySelector("#scene-play");
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
let activeScene = "newyear";
let playbackTimer = null;
let playbackSteps = 0;

function stopScenePlayback() {
  clearInterval(playbackTimer);
  playbackTimer = null;
  playbackSteps = 0;
  playButton.setAttribute("aria-pressed", "false");
  playButton.textContent = reducedMotion.matches ? "降动效：手动切换" : "播放十二幕";
}

function setScene(key, { stopPlayback = true, moveFocus = false } = {}) {
  const item = scenes[key];
  if (!item) return;
  if (stopPlayback) stopScenePlayback();
  activeScene = key;
  experience.dataset.scene = key;
  document.querySelector("#scene-counter").textContent = item.counter;
  document.querySelector("#scene-toolbar-title").textContent = item.toolbar;
  document.querySelector("#scene-eyebrow").textContent = item.eyebrow;
  document.querySelector("#scene-title").textContent = item.title;
  document.querySelector("#scene-description").textContent = item.description;
  document.querySelector("#scene-who").textContent = item.who;
  document.querySelector("#scene-write").textContent = item.write;
  document.querySelector("#scene-change").textContent = item.change;
  document.querySelector("#scene-memory").textContent = item.memory;
  document.querySelector("#scene-stage-caption").textContent = item.caption;
  ["a", "b", "c"].forEach((slot, index) => {
    document.querySelector(`#scene-card-${slot}`).textContent = item.cards[index][0];
    document.querySelector(`#scene-card-${slot}-meta`).textContent = item.cards[index][1];
  });
  document.querySelectorAll("[data-scene-select]").forEach((button) => {
    const selected = button.dataset.sceneSelect === key;
    button.setAttribute("aria-selected", String(selected));
    if (selected && moveFocus) button.focus();
  });
}

function moveScene(delta, options = {}) {
  const index = sceneOrder.indexOf(activeScene);
  const next = (index + delta + sceneOrder.length) % sceneOrder.length;
  setScene(sceneOrder[next], options);
}

function startScenePlayback() {
  if (reducedMotion.matches) return;
  stopScenePlayback();
  playButton.setAttribute("aria-pressed", "true");
  playButton.textContent = "暂停播放";
  playbackTimer = setInterval(() => {
    moveScene(1, { stopPlayback: false });
    playbackSteps += 1;
    if (playbackSteps >= sceneOrder.length - 1) stopScenePlayback();
  }, 3000);
}

document.querySelectorAll("[data-scene-select]").forEach((button) => {
  button.addEventListener("click", () => setScene(button.dataset.sceneSelect));
  button.addEventListener("keydown", (event) => {
    if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
    event.preventDefault();
    moveScene(event.key === "ArrowRight" ? 1 : -1, { moveFocus: true });
  });
});

document.querySelectorAll("[data-route-scene]").forEach((button) => {
  button.addEventListener("click", () => {
    setScene(button.dataset.routeScene);
    document.querySelector("#scene-lab").scrollIntoView({ behavior: reducedMotion.matches ? "auto" : "smooth", block: "start" });
  });
});

document.querySelector("#scene-prev").addEventListener("click", () => moveScene(-1));
document.querySelector("#scene-next").addEventListener("click", () => moveScene(1));
playButton.addEventListener("click", () => playbackTimer ? stopScenePlayback() : startScenePlayback());

function syncReducedMotion() {
  if (reducedMotion.matches) {
    stopScenePlayback();
    playButton.disabled = true;
    playButton.textContent = "降动效：手动切换";
  } else {
    playButton.disabled = false;
    if (!playbackTimer) playButton.textContent = "播放十二幕";
  }
}

reducedMotion.addEventListener?.("change", syncReducedMotion);
syncReducedMotion();

const navLinks = [...document.querySelectorAll(".topbar nav a")];
const observedSections = navLinks.map((link) => document.querySelector(link.getAttribute("href"))).filter(Boolean);
if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver((entries) => {
    const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (!visible) return;
    navLinks.forEach((link) => link.classList.toggle("active", link.getAttribute("href") === `#${visible.target.id}`));
  }, { rootMargin: "-20% 0px -68%", threshold: [0, .25, .6] });
  observedSections.forEach((section) => observer.observe(section));
}
