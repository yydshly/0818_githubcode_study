# luopan 项目研究

- 上游：[https://github.com/zhangxiaoqiang1991/luopan](https://github.com/zhangxiaoqiang1991/luopan)
- 研究版本：`499eb43b4ecb35ba0653c6d51d18a950efef160a`
- 许可证：MIT
- 研究日期：2026-08-18

## 30 秒结论

- **能力：** luopan 是一套运行在 AI 编程/助手宿主中的商业研究 Skill，而不是独立金融应用：它把请求路由到行业研究或公司研究，再以证据规则和报告模板约束输出。
- **作用：** 它解决的不是“搜到资料”，而是快速建立钱、权力、竞争与决策边界的结构化地图，减少百科式堆料和无依据判断。
- **原理：** 核心价值来自路由规则、分阶段研究方法、A/B/C 信源分级、对抗验证和 JSON 单一事实源；Python 只承担 SEC 最小抓取与公司报告渲染。
- **适配判断：** 建议改造而非原样复制：保留证据分级、路由、对抗验证和单一事实源，将研究对象从行业/公司替换为 GitHub 仓库，形成当前主仓库的标准收录闭环。

## 能力核验

| 能力 | 状态 | 边界 |
| --- | --- | --- |
| 行业/公司统一路由 | 已验证 | 根 SKILL.md 的职责边界清楚：行业进入 industry 模式，具体公司进入 company 模式；组合研究先行业后公司。这里验证的是规则和文件结构存在，实际路由质量仍取决于宿主 AI。 |

  - 仓库包含根路由器及 industry/company 两个独立子 Skill。
  - 公司用途不明确时，被要求在投资、求职、双线三种模式中选择。
  - 来源：[根路由器 SKILL.md](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/SKILL.md); [公司研究模式](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/company/SKILL.md); [本次确定性仓库扫描快照](../research/evidence/repo-scan.json)
| 九阶段行业研究方法 | 官方宣称 | 上游定义行业类型识别、Day-1 假设、权力分层、竞争格局、深度材料、骨架、双格式报告、对抗验证和质量门禁。仓库包含多个示例产物，但本次未重新执行一份完整行业研究。 |

  - 方法强调按议价能力而非传统产业链位置划分上中下游。
  - 要求至少四类视角、2–6 份深度材料，并保留数据冲突。
  - 来源：[行业研究模式](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/industry/SKILL.md); [行业研究完整方法论](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/industry/references/full-methodology.md); [上游 README 与能力说明](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/README.md)
| 投资/求职双线公司研究 | 官方宣称 | 公司模式共享身份、业务和财务事实底座，但投资判断与求职判断分开；投资强调公司质量与价格分离，求职强调业务、团队和岗位层级。方法与示例齐全，本次未做实时公司研究。 |

  - 支持上市公司与非上市公司的不同证据路线。
  - 求职主视角要求生成 10 条低防御面试反问。
  - 来源：[公司研究模式](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/company/SKILL.md); [上游 README 与能力说明](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/README.md)
| JSON → HTML / Markdown 公司报告 | 已验证 | 仓库提供确定性渲染器：校验报告对象后，从同一 JSON 生成 JSON、Markdown 和自包含 HTML，并支持能力视角折叠、数据健康度、事实表、面试问题和选择题。 |

  - 示例 JSON 已成功生成 3 个格式文件。
  - 渲染器相关 7 项单元测试在 UTF-8 模式下通过。
  - 来源：[公司报告渲染器](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/company/scripts/render_report.py); [统一报告模型](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/company/references/report-model.md); [公司报告渲染测试](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/company/tests/test_render_report.py)
| SEC 标准事实最小抓取 | 已验证 | sec_fetch.py 能将 ticker/公司名映射到 CIK，读取 submissions/companyfacts，并对标准 US-GAAP/IFRS 标签保留申报血缘。验证范围是 fixture 单元测试；本次未做 SEC 实网抓取。 |

  - 6 项 SEC fixture 测试覆盖消歧、表单定位、来源血缘、标签过滤与速率限制。
  - 脚本只提取少量标准概念，明确忽略自定义标签。
  - 来源：[SEC 事实抓取器](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/company/scripts/sec_fetch.py); [SEC 抓取器测试](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/company/tests/test_sec_fetch.py)
| 研究示例与静态报告 | 已验证 | 仓库内含 NVIDIA、字节跳动、腾讯三份公司报告的 HTML/Markdown/JSON，以及多个行业 HTML/Markdown 和截图，可直接用于理解预期交付形态。示例存在不等于其全部实时数字已在本次复核。 |

  - 确定性扫描识别 6 个 HTML、8 个 JSON、21 个 Markdown 和 8 张 PNG。
  - 来源：[上游 README 与能力说明](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/README.md); [本次确定性仓库扫描快照](../research/evidence/repo-scan.json)
| 腾讯自选股结构化金融数据 | 外部依赖 | 方法要求先调用 westock-data 获取行情、三表与一致预期，但该 CLI、安装说明、版本约束和依赖清单不在仓库中，本机也未检测到该命令。它是宿主环境能力，不是仓库自带能力。 |

  - data-routing.md 给出 westock-data 命令，并把聚合结果作为 B 级证据要求回核原始披露。
  - 仓库扫描未发现依赖 manifest。
  - 来源：[公司研究数据路由](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/company/references/data-routing.md); [本次确定性仓库扫描快照](../research/evidence/repo-scan.json); [根路由器 SKILL.md](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/SKILL.md)
| 跨市场自动化覆盖 | 实现缺口 | README 和根 Skill 对结构化金融数据覆盖的表达很强，但仓库自带自动化只有 SEC 最小脚本；A 股、港股、行业研究和 westock-data 没有仓库内执行器。声明能力必须与外部依赖能力分开。 |

  - 自动化路线明确把 A 股、港股列为后续阶段。
  - 扫描仅发现 4 个 Python 文件，未发现依赖 manifest 或 CI。
  - 来源：[上游 README 与能力说明](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/README.md); [根路由器 SKILL.md](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/SKILL.md); [公司研究数据路由](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/company/references/data-routing.md); [数据自动化路线图](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/company/references/automation-roadmap.md); [本次确定性仓库扫描快照](../research/evidence/repo-scan.json)
| Windows 默认编码可移植性 | 实现缺口 | 在 Windows 中文默认编码环境直接运行 unittest 时，渲染器 7 项测试因测试代码 read_text() 未指定 UTF-8 而报错；使用 python -X utf8 后 13/13 通过。 |

  - 失败来自测试夹具读取而不是业务渲染器本身。
  - 当前可复现 workaround 是为测试进程开启 UTF-8 模式。
  - 来源：[公司报告渲染测试](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/company/tests/test_render_report.py)

## 原理：五层工作链

### 1. 触发与输入

用户以自然语言提供行业、公司、股票、岗位或 Offer。根 Skill 先判断对象；公司用途不明确时只追问一次投资/求职/双线。

### 2. 路由与编排

行业进入九阶段流水线；公司按上市市场和用户目的加载数据路线、投资框架或求职框架。组合研究复用事实，但不混合两类结论。

### 3. 核心转换

AI 按方法论把来源转换为判断：行业侧分析权力、集中度、利润池与壁垒；公司侧建立共享事实底座，再分别判断投资交易条件或职业价值。

### 4. 验证与约束

A/B/C 信源、事实/推断/计算分离、反方检查、质量门禁与 JSON schema 共同约束输出。公司渲染器提供部分确定性校验，行业门禁主要依赖宿主 AI 执行。

### 5. 产物与反馈

行业目标产物是 HTML+Markdown；公司以 JSON 为真源生成 HTML+Markdown，并附来源、信息局限和可继续追问方向。仓库示例承担演示与回归样本。

## 实际验证

- 环境：Windows / PowerShell / Python 3.10.11 / upstream commit 499eb43
- 测试：13 通过 / 0 失败

```shell
python -m unittest discover -s projects/luopan/upstream/modes/company/tests -v
python -X utf8 -m unittest discover -s projects/luopan/upstream/modes/company/tests -v
python projects/luopan/upstream/modes/company/scripts/render_report.py projects/luopan/upstream/modes/company/examples/example_report.json --output-dir .tmp/luopan-rendered
```

- 默认 Windows 编码运行时，7 个渲染器测试因 read_text() 未指定 UTF-8 而错误；开启 -X utf8 后全部 13 项通过。
- 示例渲染成功生成 HTML、Markdown、JSON 三个文件。
- 未执行需要真实证券数据、外部 westock-data 或完整 Web 研究的业务流程，因此不把示例与单测外推为生产级准确性。

## 已知边界

- 它不是独立应用：完整行业/公司研究依赖能读取 Skill、浏览网页和调用工具的 AI 宿主。
- westock-data 未随仓库提供，本次环境中也不可用；相关金融数据能力属于外部依赖。
- 行业研究大部分是提示词政策与人工门禁，缺少与公司报告类似的统一 schema、执行器和自动化测试。
- Windows 默认编码会让 7 项测试报错；测试文件应显式使用 encoding="utf-8"。
- SEC 脚本测试基于 fixture，本次没有实网验证；A 股和港股自动化仍在路线图中。
- 行业权力指标中的应收/应付强势特征文字疑似反向：占用供应商资金通常对应较高应付，快速回款通常对应较低应收，需在用于评分前校正。
- 方法文档标题称“10 条红线”但实际列出 16 条且存在重复项，说明方法维护还需要结构化 lint。

## 面向主仓库的扩展

### GitHub 项目研究 Skill

新增 study-github-projects 路由，将输入从行业/公司替换为仓库 URL 或本地 checkout，并强制区分已验证、官方宣称、外部依赖和实现缺口。

**验收：** Skill 通过 quick_validate.py，描述能触发仓库分析场景，方法与 schema 由 SKILL.md 直接路由。

### 确定性仓库快照

inspect_repo.py 固定 remote、commit、文件/语言、manifest、测试、CI、许可证和 Skill 信号，为后续判断提供不会随措辞漂移的证据底座。

**验收：** 对 luopan 扫描得到 52 个有效文件、3 个 Skill、MIT 许可证、测试存在、CI/依赖 manifest 不存在，并记录 commit 499eb43。

### 单一事实源研究展厅

用一份项目研究 JSON 同时生成 Markdown 和响应式 HTML；页面支持研究视角切换与能力状态筛选，明确展示验证结果和边界。

**验收：** JSON 校验通过；HTML/Markdown 同步生成；桌面、平板、390px 手机可读且交互可键盘操作。

### 主索引收录闭环

每个研究项目在主 README 中只保留来源、主题、研究记录、演示和状态，详细证据留在子项目；未来可按相同 schema 自动生成索引。

**验收：** 根 README 与 projects/luopan/README.md 同时链接上游、固定版本、研究报告、展厅与扩展 Skill。

## 来源

- **B 级** [上游 README 与能力说明](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/README.md)
- **A 级** [根路由器 SKILL.md](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/SKILL.md)
- **A 级** [行业研究模式](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/industry/SKILL.md)
- **A 级** [行业研究完整方法论](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/industry/references/full-methodology.md)
- **A 级** [公司研究模式](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/company/SKILL.md)
- **A 级** [公司研究数据路由](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/company/references/data-routing.md)
- **A 级** [数据自动化路线图](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/company/references/automation-roadmap.md)
- **A 级** [统一报告模型](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/company/references/report-model.md)
- **A 级** [公司报告渲染器](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/company/scripts/render_report.py)
- **A 级** [SEC 事实抓取器](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/company/scripts/sec_fetch.py)
- **A 级** [公司报告渲染测试](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/company/tests/test_render_report.py)
- **A 级** [SEC 抓取器测试](https://github.com/zhangxiaoqiang1991/luopan/blob/499eb43b4ecb35ba0653c6d51d18a950efef160a/modes/company/tests/test_sec_fetch.py)
- **A 级** [本次确定性仓库扫描快照](../research/evidence/repo-scan.json)
