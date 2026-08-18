# Hand-drawn Styles 研究子项目状态

> 状态快照：2026-08-18。用于区分已合并基线、远端待合并增强、验证证据和后续动作。

## 当前结论

研究与本地实现已经完成，远端增强分支与本地同步；基础版已进入 `main`，后续视觉案例和长期使用指南等待新PR合并。

| 项目 | 当前值 |
| --- | --- |
| 上游仓库 | `threerocks/hand-drawn-styles` |
| 固定上游版本 | `9f150d9f4c90f3a4ace78a751d2d8263d818220c` |
| 主仓库 | `yydshly/0818_githubcode_study` |
| 工作分支 | `agent/luopan-data-sources` |
| 最新功能提交 | `893c202`（长期使用指南） |
| 远端分支 | 功能提交已同步到 `origin/agent/luopan-data-sources`；本状态快照随下一提交同步 |
| `main` 当前基线 | PR #2 合并提交 `0c5c105`，包含 `ad73b38` 基础研究展厅 |
| 待合并范围 | `1bd2d18`～`893c202` 共5个功能增强提交，外加本状态快照提交 |
| 研究状态 | 已复现，持续扩展，增强内容待合并 |

## 已进入 main 的内容

PR [#2](https://github.com/yydshly/0818_githubcode_study/pull/2) 已合并：

- 固定上游 Git submodule；
- 能力、原理和工程边界分析；
- 10张上游代表样图；
- 五层实现与普通/3.1合同说明；
- 初版日常场景路由工作台；
- 项目测试、主研究索引和 GitHub Pages 组装。

## 远端分支待合并增强

| 提交 | 内容 |
| --- | --- |
| `1bd2d18` | 直接使用 ChatGPT ImageGen 生成项目封面、原理图和里程碑图 |
| `0d55a96` | 同一研究者贯穿的六幕连续案例 |
| `b5aa164` | 水墨、像素、纸雕和软偶4种任务化项目样例 |
| `3f66345` | 将4种单图升级为问题→处理→结果三幕流程 |
| `893c202` | 长期使用手册、七类场景、标准资产包、SOP和请求模板 |

上述提交已推送，但不在已合并的 PR #2 中。创建新PR后才能进入 `main` 并触发最新 Pages 部署。

## 当前交付物

### 研究与指南

- [`README.md`](README.md)：项目定位、复现方式和主要结论；
- [`docs/analysis.md`](docs/analysis.md)：能力、原理、工程实现、局限和研究价值；
- [`docs/usage-guide.md`](docs/usage-guide.md)：长期使用指南；
- [`showcase/DELIVERY.md`](showcase/DELIVERY.md)：六次修订的设计契约和浏览器证据；
- [`tests/verify_project.py`](tests/verify_project.py)：项目验收脚本。

### 可运行展厅

页面当前包含：

- 19套上游风格能力说明；
- 10张上游代表样图；
- 6幕主案例：混乱→归档→路由→组装→回归→发布；
- 4条多风格三幕流程，共12个场景；
- 3类图片职责：封面、讲解、故事；
- 7类长期使用场景；
- 每项目默认视觉资产包；
- 五步使用SOP和可复制请求模板；
- 5种日常场景路由工作台。

本地入口：`http://127.0.0.1:4174/showcase/`。

### 生成资产

`showcase/assets/generated/` 当前包含：

- 20张 ChatGPT ImageGen 项目图片；
- PNG 总体积约 40 MB；
- `STORY.md`：六幕主案例、角色合同和逐幕Prompt；
- `MULTI-STYLE.md`：多风格适用边界；
- `MULTI-STYLE-FLOWS.md`：4条三幕流程和新增Prompt；
- `PROMPTS.md`：主要内容资产Prompt；
- `README.md`：资产来源、职责和文件索引。

## 验证状态

| 检查 | 结果 |
| --- | --- |
| 项目自动验收 | `python projects/hand-drawn-styles/tests/verify_project.py` 通过 |
| JavaScript语法 | `node --check projects/hand-drawn-styles/showcase/app.js` 通过 |
| Git补丁格式 | `git diff --check` 通过 |
| 浏览器 | 1440×1000、768×1024、390×844 通过 |
| 页面图片 | 32/32 完整滚动后加载 |
| 图片替代文本 | 缺失 0 |
| 移动端横向溢出 | 390px视口内容宽375，无溢出 |
| 控制台与页面错误 | 无 |
| 键盘焦点 | 3px可见轮廓 |
| 使用指南文档 | 本地 HTTP 200 |

## 已知上游问题

固定上游未做修改，研究记录了两项问题：

1. Windows 上游测试为 `18/19`：失败来自路径分隔符字符串断言，不是锚点缺失；
2. 1号配方中的 `【最重要·硬性负向约束】` 与占位符语法冲突，CLI会误判为必填变量。

详见 [`docs/analysis.md`](docs/analysis.md)。

## 下一步

1. 从 `agent/luopan-data-sources` 向 `main` 创建新PR；
2. 复核新PR包含 `1bd2d18`～`893c202` 的5次功能增强和本状态快照；
3. 合并后等待 GitHub Pages workflow；
4. 验证线上路径：`/projects/hand-drawn-styles/showcase/`；
5. 后续新研究项目按 [`docs/usage-guide.md`](docs/usage-guide.md) 的标准资产包执行。
