**🌐 在线访问：[面试地图 · GitHub Pages](https://ace-teng.github.io/find_job_cs/)**

# 面试地图 · Internship Atlas

为自己的实习面试准备而做：**选岗位 → 选话题 → 从起问走到深入追问与实战**。

10 个岗位入口 · **59 条话题链 / 278 个问题步骤** · 265 个独立复习标记。部分问题在不同链中复用，掌握状态同步。原有 168 道题与进度 ID 全部保留。

[HTTP 追问链](https://ace-teng.github.io/find_job_cs/#frontend/topic/http) · [MySQL 索引](https://ace-teng.github.io/find_job_cs/#java/topic/index) · [Redis 缓存](https://ace-teng.github.io/find_job_cs/#java/topic/redis-cache) · [RAG](https://ace-teng.github.io/find_job_cs/#ai/topic/rag-flow) · [Agent](https://ace-teng.github.io/find_job_cs/#ai/topic/agent-loop)

## 怎么用

1. 选择目标实习岗位，从话题目录进入 HTTP、SQL、Redis、React、RAG、Agent 等方向。
2. 默认显示完整问题链：起问 → 为什么继续追问 → 下一问 → 场景 / 项目 / 手写。
3. 搜索一个问题时保留整条链，命中问句单独标记。也可按面经公司、薄弱点、收藏筛选。
4. 先口述，再展开“回答抓手与参考”；也可用“逐问自测”逐个揭开后续问题。
5. 标记待复习、不熟、已掌握，收藏薄弱问题；每问都可复制直达链接。

例如索引链：**为什么索引能加速 → 二级索引为什么保存主键 → 联合索引遇到范围条件 → 是否回表 → 怎样用证据证明优化有效**。

进度保存在当前浏览器，不上传。导出 JSON 后可在另一台设备导入；兼容旧版进度文件和旧题链接。手机上的岗位、话题目录均可滚动浏览。

## 内容范围

| 岗位 | 主要话题 |
| --- | --- |
| 前端 / 全栈 | HTTP、缓存、鉴权、SSE、JS 异步与闭包、React、Vue、性能、CSS、TypeScript、手写 |
| Java 后端 | 集合、并发、线程池、JVM、Spring 事务、依赖治理、SQL、Redis、消息队列 |
| Go 后端 | goroutine、channel、取消、slice、interface、竞态、服务工程 |
| Python 后端 | 对象与函数、asyncio、取消、GIL 版本差异、API 服务 |
| AI 应用 / Agent | RAG 切分与更新、混合检索、评测、Agent 循环、工具、记忆、恢复、MCP、安全 |
| 机器学习实习 | 数据划分、评估、微调、LoRA、训练、推理与 KV Cache |
| 测试开发 | 接口场景、自动化、隔离、并发与压力测试 |
| 运维 / 云原生 | Linux、Docker、Kubernetes、探针、发布恢复、容量与服务排障 |
| C++ / 客户端 | 所有权、智能指针、拷贝移动、容器失效、析构、排障与手写 |

没有独立数学或理论课程目录，基础知识跟随面试问题出现。

## 出处与时效

- **追问链**由编辑组织，衔接文字解释“为什么接着问”。它不是某家公司完整面试顺序，也不是频率排名。
- **面经改编**仅在有依据的单问处标记公司，并链接原帖、日期和招聘范围；当前使用 7 篇 2025 / 2026 年公开面经。
- **编辑追问与回答抓手**参考技术文档，并参考小林 coding、JavaGuide 的话题组织。技术标准可能早于两年，面经时效与技术规范发布日期分别处理。
- 当前面经窗口为 **2024-10-12 至 2026-10-12**；这是本次核验窗口，不会自动滚动。更新时须同步检查日期和版本。
- `verified` / `reviewed` 表示编辑核验日期，不能当成资料发布日期。Go、Python、MCP 等版本敏感问题保留版本条件。

来源索引见 [SOURCES.md](SOURCES.md)。问题与来源分开维护，支持后续补充你的面经、文档和项目资料。

## 本地预览与检查

无需安装依赖：

```sh
python3 -m http.server 8080
```

打开 `http://localhost:8080`。不要直接双击 HTML（浏览器会限制读取 JSON）。

```sh
python3 scripts/seed.py
node --check app.js
node scripts/validate.mjs
```

## 持续补充内容

- `content/chains.json`：岗位、话题、顺序、每次追问的原因，以及分支话题。
- `content/drills.json`：具体场景、代码、回答抓手、易错点和面经出处。
- `scripts/seed.py` / `scripts/enrich.py`：合并为网页读取的 `data.json`。
- `scripts/validate.mjs`：检查问题和来源引用、步骤 ID、衔接、分支与岗位覆盖。

在链中复用旧题时，`id` 与 `questionId` 使用同一个旧题 ID。新问句填写固定的 `id`、`title`、`why`、`focus` 与 `stage`，参考资料放在话题的 `references` 中。第一问可以不写 `why`；后续每问都要说明承接上一问的原因。

**已有 ID 对应用户进度，重排或改标题时不要改 ID。** 新增问题使用新 ID。修改源内容后运行生成与校验；不要只改生成的 `data.json`。旧版少数宽口径题保留在题库，可继续通过旧链接访问。

补充资料可提交 [Issue](https://github.com/Ace-teng/find_job_cs/issues)：附来源链接、日期、岗位，以及能确认的实际问句。只把来源明确支持的题标为面经改编。

## GitHub Pages

Settings → Pages → Deploy from a branch → `main` / `/ (root)`。`.nojekyll` 关闭 Jekyll；所有资源使用相对路径。推送后自动更新网页，Actions 检查 JavaScript 与内容结构。

HTML / CSS / 原生 JavaScript / JSON。无构建步骤、无外部 CDN、无账号。MIT License。
