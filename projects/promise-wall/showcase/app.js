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
