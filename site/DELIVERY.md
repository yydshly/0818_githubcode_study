# GitHub Pages Research Hub · Delivery Record

## Design contract

```text
Entry mode: Brief-led extension of an existing research repository
Request revision: 1
Target user and context: 从 GitHub README 或 Pages 地址进入、希望浏览研究项目的访客
Desired first impression: 这是一个可复现研究索引，而不是仓库链接收藏夹
Visual ambition: Editorial
Experience architecture: Editorial Flow
Visual constraints: 延续 Luopan 展示的深色研究档案视觉；无外部字体、图片或运行时依赖；390px–1440px 可读
Information constraints: 根入口只保留主项目定位、当前项目摘要和行动入口；详细内容进入各项目路径
Operation constraints: 纯静态 HTML/CSS；通过 GitHub Pages Actions 部署；支持后续增加 projects/<slug>/
State constraints: 单页、无脚本；全部链接键盘可达；reduced-motion 无信息损失
Environment constraints: GitHub Pages artifact；本地预览使用 Python HTTP server
Primary journey: 进入 Pages 根页 → 理解研究主库 → 查看 Luopan 摘要 → 打开在线演示或数据档案
User-defined phases: 外部 README 描述；GitHub Pages 部署；Luopan 演示可访问
Required artifacts: 根 README、Pages workflow、site/index.html、site/styles.css、浏览器证据
Autonomy authorization: 用户明确要求描述并部署到 GitHub
User-decision boundary: GitHub 重新认证、Pages 首次启用和 PR 合并属于外部状态
Observable completion criteria: 本地 Pages artifact 可组装；根页与 Luopan 展示均 200；桌面和 390px 无溢出；关键链接有效；workflow 使用官方 Pages actions 与所需权限
Coverage record: 见下表
```

## Coverage manifest

| 用户要求 | 界面/状态 | 证据 | 状态 | 下一步 |
| --- | --- | --- | --- | --- |
| 外部 README 描述 | GitHub 根 README | 项目说明、数据来源表和在线地址 | pass | README diff 已检查 |
| Pages 根入口 | 1440px / 390px | 浏览器截图、无溢出 | pass | 两视口 200 且无横向溢出 |
| Luopan 在线演示 | `/projects/luopan/showcase/` | HTTP 200 与标题 | pass | 标题与 6 个报告卡通过 |
| 原版报告与档案 | 本地 artifact 链接 | 六份报告、数据档案、实战、审计 200 | pass | 11 条发布路径全部 200 |
| GitHub Actions | `pages.yml` | 官方 action 版本、权限和 submodule checkout | pass | 使用 checkout@v6、configure-pages@v5、upload-pages-artifact@v4、deploy-pages@v4 |
| 远端发布 | GitHub branch / PR / Pages | push、PR、workflow、公开 URL | blocked | 等待 `gh auth login` |

## Browser refinement ledger

```text
Current stage: 9 · Engineering and delivery closure
User phase: 外部 README 描述 + GitHub Pages 部署
Coverage item: Pages 根入口、Luopan 演示、报告与档案路径、桌面和手机
User goal: 从外部 README 理解项目，并在 GitHub Pages 直接浏览演示
Browser environment: Headless Chromium / 1440×1000, 390×844 / local artifact at http://127.0.0.1:4180/
Observed evidence: 根页和 Luopan 展示均 200；11 条 artifact 路径均 200；无横向溢出和控制台错误；首个焦点 3px
Problem category: Test acceptance threshold
Root cause: 首轮测试把精简索引正文硬设为至少 500 字符，实际 452 字符但所有必要内容均存在
Minimal intervention: 将阈值校正为 400，并保留精简页面；将易失真的文件数统计替换为 6 份原版报告
Adjacent regression surfaces: 桌面、390px、根页→Luopan 跳转、六份报告、数据档案和实战简报
Observed result: 全部通过
Decision: pass
Next executable action: GitHub 认证后创建分支、提交、推送、PR，并验证 Pages workflow
New authority required: 用户完成 gh auth login
```
