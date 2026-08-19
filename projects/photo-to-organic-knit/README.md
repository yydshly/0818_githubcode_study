# Photo to Organic Knit 项目研究

本子项目研究 [NalaZhang27/photo-to-organic-knit](https://github.com/NalaZhang27/photo-to-organic-knit)。上游不是新的图像模型，而是一套面向 Codex ImageGen 的视觉再创作 Skill：它先从照片中选择辨识锚点，再通过概念、构图、材质和质检约束，把照片重构为留白充足的手工针织艺术海报。

## 当前状态

- 研究分支：`codex/photo-to-organic-knit-research`
- 固定上游 commit：`b84efe522e758649e46fe59f34d700eb60bedc12`
- 状态：已获取上游、已完成独立 ImageGen 实演、已安装目标驱动 Skill，已实现四类确定性发布模板和 localhost Publication Studio
- 上游许可证：MIT，完整文本保留在 `upstream/LICENSE`

## 本研究新增了什么

上游代码通过 Git submodule 原样保存在 `upstream/`，研究层没有修改其中的 Skill。本目录新增：

1. 一组无外部版权依赖的独立 before/after：横版独木舟照片与按照上游 Skill 规则生成的针织海报。
2. 一个“同一意境、六种材料”的效果实验室：针织、剪纸、陶瓷浮雕、彩色玻璃、木刻和微缩场景。
3. 四组以目标交付驱动的场景案例：家庭成长册×针织、旅行纪念×木刻、公益报告×彩色玻璃、独立品牌活动×剪纸。
4. 四个代码原生交付 Mockup：家庭相册、旅行日志、公益报告和品牌活动海报；准确文字由 HTML/CSS 排版而不是交给图像模型。
5. 一座静态研究展厅：可拖动比较输入与输出、切换材料效果、阅读实际场景与成品案例，并查看上游两组原始案例。
6. 一个可运行的 `photo-to-conceptual-art` 扩展 Skill：意境 Schema、六种效果、四类场景、四种交付 Profile、自动路由与 Prompt 编译器。
7. 一次未见照片前向测试：自动木刻与人工剪纸覆盖共享同一 Essence 和交付门禁，记录第一轮失败、针对性修正与 25/24 目标适配评分。
8. 一个跨人物、产品与建筑交通的 `n=3` Pilot，三条自动路线均在首次生成中通过，但明确不外推为生产成功率。
9. 追加式研究台账与确定性 Review 记录器：原始样例被测试锁定，人工门禁证据可验证、可汇总但不伪装成自动视觉评分。
10. 正式安装副本的中文端到端调用：中文请求与 Essence 自动路由为剪纸活动海报，首次生成通过七项门禁并得到 34/35。
11. 同一中文 Key Art 的 4:5 活动海报与 16:9 社媒横幅，准确中文文案由 HTML/CSS 设计层完成。
12. 三组新增效果验证，网页逐组并列完整原图和结果：针织家庭宠物、彩玻璃雨水花园、陶瓷浮雕蜂蜜产品。
13. 首个真正由 Skill 执行的确定性发布闭环：一份中文 `copy.json`、一个 `campaign-poster` 模板、4:5 与 16:9 PNG 导出，以及精确文案、溢出、对比度、安全区、声明和尺寸门禁。
14. 三类目标专用发布模板：家庭针织 Key Art → 3:4 纪念册封面，社区彩玻璃 → A4 影响力报告，灯塔木刻 → 4:5 旅行日志；三张主版均由独立 `copy.json` 生成并通过门禁。
15. 一个可操作的本地 Publication Studio：四模板表单、准确文案、单模板渲染、门禁反馈、PNG/报告/copy.json 下载，以及四模板批量 ZIP。只绑定 `127.0.0.1`，运行产物位于临时目录。
16. 蜂蜜跨图片发布验证：完整展示原始产品图、陶瓷浮雕 Key Art、蜂蜜专用 `copy.json`、4:5 海报和 16:9 横幅；与茶案例共享同一活动模板且无需修改渲染器。
17. 正式发布模式示例：对比 `sample` 与 `approved`，展示如何取消系统样例声明、恢复“官方商城”渠道字段，并明确品牌、文案、法务、资产和渠道五类外部审批。
18. Release Manifest V1：approved 输出必须绑定文案/图片 SHA-256 和五类完整审批；缺包、待审批或哈希不一致都会在输出前失败。
19. Release Security V1：Ed25519 离线签名、可信公钥验证和输出哈希审计链；Demo 私钥仅在临时目录使用并在签名后删除。
20. Non-Production Action Runbook：把目标锁定、Key Art、Review、Sample/Approved、失败处理、证据保留和停止规则写成明确动作。
21. 能力、原理、意义、限制与实际价值分析。
22. 后期使用场景、产品化扩展和研究验证路线。
23. 验证脚本，检查上游固定版本、图片尺寸、页面资源、扩展路由、发布报告、Studio API、索引与 Pages 发布配置。

## 核心结论

该仓库的真实贡献是“可复用的艺术指导协议”：

```text
照片语义
  -> retain / transform / discard
  -> 单一视觉隐喻
  -> 至少三项结构重构
  -> 参考图条件下的 ImageGen
  -> 视觉质检与单问题迭代
```

它比一句“变成毛线风格”更稳定、更有创作意图，但没有模型权重、训练数据或自动视觉评价系统。概念图像素仍由宿主的 ImageGen 完成；目前新增的确定性渲染器只负责把已接受的 Key Art 与准确文案组合为四类受支持的发布模板。

## 查看与验证

直接打开：

- `showcase/index.html`：研究展厅
- `docs/analysis.md`：能力、原理、意义与边界
- `docs/use-cases-and-roadmap.md`：使用场景、扩展方向与实际价值
- `showcase/assets/generated/PROMPTS.md`：本次演示的生成记录
- `extension/photo-to-conceptual-art/SKILL.md`：目标驱动型扩展 Skill
- `extension/photo-to-conceptual-art/scripts/build_prompt.py`：场景、效果和交付 Prompt 编译器
- `extension/photo-to-conceptual-art/forward-tests/lighthouse-travel/RESULT.md`：未见照片前向测试
- `extension/photo-to-conceptual-art/forward-tests/pilot-n3/RESULT.md`：跨题材 Pilot
- `extension/photo-to-conceptual-art/scripts/score_review.py`：人工证据记录验证与确定性汇总
- `research/chinese-invocation/RESULT.md`：正式安装副本的中文调用记录
- `research/additional-validation-v2/RESULT.md`：三效果新增验证及原图对照
- `extension/photo-to-conceptual-art/scripts/render_layout.py`：活动海报确定性排版与检查
- `research/publishing-pipeline-v1/RESULT.md`：4:5 与 16:9 发布文件、门禁和边界
- `research/publishing-pipeline-v2/RESULT.md`：纪念册、影响力报告和旅行日志三类目标主版
- `studio/README.md`：本地发布工作台运行与安全说明
- `research/publication-studio-v1/RESULT.md`：工作台 HTTP、单模板与批量 ZIP 验证
- `research/honey-publication-validation/RESULT.md`：蜂蜜原图、陶瓷 Key Art 与双尺寸发布成品
- `research/honey-formal-publication-demo/RESULT.md`：Sample 与 approved 模式差异和正式发布审批清单
- `research/release-manifest-v1/RESULT.md`：审批包、双哈希绑定和 approved 强制门禁验证
- `research/release-security-v1/RESULT.md`：Ed25519 签名、可信公钥、审计链和私钥清理证据
- `extension/photo-to-conceptual-art/references/action-runbook.md`：非生产操作、失败响应与停止规则

运行验证：

```powershell
python projects/photo-to-organic-knit/tests/verify_project.py
```

## 目录

```text
projects/photo-to-organic-knit/
├── README.md
├── docs/
│   ├── analysis.md
│   └── use-cases-and-roadmap.md
├── showcase/
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── assets/generated/
├── tests/verify_project.py
├── extension/photo-to-conceptual-art/
│   ├── SKILL.md
│   ├── profiles/
│   ├── assets/templates/campaign-poster.json
│   ├── scripts/build_prompt.py
│   ├── scripts/render_layout.py
│   └── tests/
├── research/publishing-pipeline-v1/
├── research/publishing-pipeline-v2/
├── studio/
│   ├── server.py
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── tests/
└── upstream/                 # 固定上游 submodule
```

## 边界

- 独立演示图片由本研究使用 Codex 内置 ImageGen 生成，不是上游作者提供的输出。
- 上游的 `train-before-after.png` 与 `forest-before-after.png` 仅作为原始能力证据展示。
- 页面中的产品场景和扩展路线是研究建议，不代表上游已经实现。
- 生成式图像存在随机性；本次结果不能证明所有输入都能达到相同质量。
