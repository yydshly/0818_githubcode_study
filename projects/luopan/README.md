# Luopan 项目研究

> 第一个研究子项目：验证 [zhangxiaoqiang1991/luopan](https://github.com/zhangxiaoqiang1991/luopan) 的真实能力、工作原理与适用边界，并将其方法扩展为本主仓库的 GitHub 项目研究流程。

## 结论

Luopan 不是独立金融应用，而是一套运行在 Codex、Claude Code 等 AI 宿主中的商业研究 Skill。它的主要价值是把“行业或公司调研”约束为带路由、证据分级、对抗验证和结构化产物的决策流程。本项目先展示它已有的行业、投资与求职报告，再解释原理、数据和判断逻辑。

建议对它进行**方法级改造**：保留“证据分级 + 路由 + 对抗验证 + 单一事实源”，将行业/公司对象替换为 GitHub 仓库，服务本主仓库的长期收录、复现、扩展和展示。

## 研究入口

| 内容 | 入口 |
| --- | --- |
| 原版能力、原理与扩展展厅 | [打开主展示](showcase/index.html) |
| 数据来源与信息获取档案 | [查看完整整理](docs/data-sources-and-acquisition.md) |
| AI 编程 Agent 关联场景实战 | [查看行业研究简报](applied/ai-coding-agents-2026.md) |
| 技术审计附录 | [交互审计](showcase/audit/index.html) · [Markdown](showcase/audit/analysis.md) |
| 结构化研究真源 | [luopan-study.json](research/luopan-study.json) |
| 仓库扫描证据 | [repo-scan.json](research/evidence/repo-scan.json) |
| GitHub 项目研究扩展 | [study-github-projects Skill](extension/study-github-projects/SKILL.md) |
| 固定上游源码 | [upstream submodule](upstream) |

研究固定在上游 commit `499eb43b4ecb35ba0653c6d51d18a950efef160a`（2026-07-18）。上游代码采用 MIT License；本研究与扩展不代表上游维护者观点。

## 已验证能力

- 根路由器以及行业/公司两个子 Skill 的模块结构；
- 公司报告从单一 JSON 生成 HTML、Markdown 和 JSON；
- SEC 最小抓取器的 fixture 测试与证据血缘；
- 上游 13 项自动化测试在 `python -X utf8` 下全部通过；
- 示例报告可生成三种同步格式。

完整的“已验证 / 官方宣称 / 外部依赖 / 实现缺口”能力矩阵见[技术审计附录](showcase/audit/analysis.md)。

## 本地查看

从主仓库根目录运行：

```shell
git submodule update --init --recursive
python -m http.server 4173 --directory projects/luopan
```

然后打开 <http://127.0.0.1:4173/showcase/>。

## 重新生成

```shell
python -X utf8 projects/luopan/extension/study-github-projects/scripts/inspect_repo.py projects/luopan/upstream --output projects/luopan/research/evidence/repo-scan.json
python -X utf8 projects/luopan/extension/study-github-projects/scripts/render_report.py projects/luopan/research/luopan-study.json --output-dir projects/luopan/showcase/audit
```

`research/luopan-study.json` 是技术审计真源。不要直接修改生成的 `showcase/audit/index.html` 或 `showcase/audit/analysis.md`。主展示 `showcase/index.html` 是独立编排页面。

## 扩展闭环

```text
GitHub URL
→ 固定 remote / commit / license
→ 确定性仓库扫描
→ 运行测试与代表性示例
→ 区分能力宣称和实测证据
→ 解释五层工作原理
→ 判断与当前项目的适配方式
→ 生成 Markdown + HTML 展示
→ 更新主 README 索引
```
