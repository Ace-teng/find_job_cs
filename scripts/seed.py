import json
from pathlib import Path
roles=[('frontend','前端实习','浏览器 · JavaScript · React / Vue','01'),('java','Java 后端','Java · Spring · 数据库 · 并发','02'),('go','Go 后端','Go · 服务开发 · 并发 · 存储','03'),('python','Python 后端','Python · API · 异步 · 数据库','04'),('fullstack','全栈实习','前后端交互 · 认证 · 部署','05'),('ai','AI 应用 / Agent','RAG · 工具调用 · 工作流 · 评测','06'),('ml','机器学习实习','训练 · 评估 · 推理 · 项目','07'),('test','测试开发','接口 · 自动化 · 性能 · 排障','08'),('ops','运维 / 云原生','Linux · 容器 · 网络 · 可观测性','09'),('cpp','C++ / 客户端','内存 · 对象生命周期 · 并发','10')]
S={
'web':('MDN Web Docs','https://developer.mozilla.org/zh-CN/docs/Web',None),
'react':('React 官方文档','https://react.dev/learn','2026-10-12'),
'java':('Java 文档','https://docs.oracle.com/en/java/',None),
'go':('Go 官方文档','https://go.dev/doc/',None),
'python':('Python 官方文档','https://docs.python.org/3/',None),
'db':('MySQL 官方文档','https://dev.mysql.com/doc/refman/8.4/en/',None),
'redis':('Redis 官方文档','https://redis.io/docs/latest/',None),
'ops':('Kubernetes 官方文档','https://kubernetes.io/docs/concepts/',None),
'ai':('LangChain Agents','https://docs.langchain.com/oss/python/langchain/agents','2026-10-12'),
'rag':('LangChain Retrieval','https://docs.langchain.com/oss/python/langchain/retrieval','2026-10-12'),
'graph':('LangGraph Overview','https://docs.langchain.com/oss/python/langgraph/overview','2026-10-12'),
'mcp':('MCP 官方文档','https://modelcontextprotocol.io/docs/getting-started/intro','2026-10-12'),
'ml':('PyTorch 官方文档','https://docs.pytorch.org/docs/stable/index.html',None),
'cpp':('C++ 参考资料','https://en.cppreference.com/w/',None),
'qa':('Playwright 官方文档','https://playwright.dev/docs/intro',None)}
# module, roles, source, interview question, ordered follow-up concepts, optional short answer cues
rows=[
('JavaScript','frontend fullstack','web','闭包为什么会保留外部变量？','闭包|词法作用域|作用域链|垃圾回收|内存泄漏','词法作用域决定变量查找；闭包保留对外部绑定的访问；结合事件监听与定时器说明释放时机。'),
('JavaScript','frontend fullstack','web','Promise、async/await 和事件循环是什么关系？','事件循环|调用栈|任务队列|微任务|Promise|async/await','先区分同步执行与异步调度，再解释任务与微任务；await 后续执行与 Promise 有关。'),
('JavaScript','frontend fullstack','web','this 的指向如何确定？','this|调用方式|箭头函数|call/apply/bind|原型链','按调用方式判断 this；箭头函数没有自己的 this；不要与词法作用域混为一谈。'),
('JavaScript','frontend fullstack','web','浅拷贝和深拷贝怎么选？','引用类型|浅拷贝|深拷贝|structuredClone|循环引用|序列化','说明共享嵌套引用的影响，再比较支持的数据类型和性能；JSON 不能完整保留所有 JS 类型。'),
('JavaScript','frontend fullstack','web','防抖和节流分别适合什么场景？','事件处理|防抖|节流|定时器|请求取消','输入搜索用防抖；滚动处理可用节流；同时考虑旧请求覆盖新结果。'),
('浏览器与页面','frontend fullstack','web','输入 URL 到页面出现，中间发生了什么？','URL|DNS|TCP|TLS|HTTP|DOM|CSSOM|渲染树|布局|绘制','按网络请求和渲染两个阶段组织；每一步都能继续追问缓存、连接和渲染阻塞。'),
('浏览器与页面','frontend fullstack','web','浏览器缓存怎么生效？','HTTP 缓存|Cache-Control|强缓存|协商缓存|ETag|Last-Modified','先判断新鲜度，再谈条件请求；区分 no-cache 与 no-store。'),
('浏览器与页面','frontend fullstack','web','跨域为什么发生，怎么处理？','同源策略|CORS|预检请求|凭据请求|反向代理','跨域限制来自浏览器；CORS 由服务端响应头控制；携带凭据时不能使用通配来源。'),
('浏览器与页面','frontend fullstack','web','页面卡顿如何定位？','性能分析|长任务|重排|重绘|requestAnimationFrame|虚拟列表','先测量，再定位主线程工作、布局和数据量；不要只罗列优化手段。'),
('浏览器与页面','frontend fullstack','web','Flex、Grid 和定位有什么区别？','盒模型|Flex|Grid|定位|层叠上下文|响应式布局','从一维与二维布局、文档流和层叠关系回答，用实际布局说明。'),
('React / Vue','frontend fullstack','react','React 状态更新为什么不能直接修改对象？','React|state|不可变更新|重新渲染|批量更新','说明状态快照、引用变化与渲染；不要把更新时序简单概括为总是异步。'),
('React / Vue','frontend fullstack','react','useEffect 和 useMemo 的用途有什么区别？','Hooks|useEffect|依赖数组|清理函数|useMemo|useCallback','Effect 用于与外部系统同步；Memo 用于缓存计算；解释依赖与清理。'),
('React / Vue','frontend fullstack','react','列表 key 为什么不能随便用下标？','虚拟 DOM|协调过程|key|组件身份|组件状态','key 帮助识别同级组件；插入、删除、重排时下标可能让状态对应错误。'),
('React / Vue','frontend fullstack','web','Vue 响应式和组件通信如何理解？','Vue|Proxy|响应式依赖|computed|watch|props|emit|Pinia','从依赖收集与触发更新展开；区分派生状态、副作用与跨组件共享状态。'),
('前端工程','frontend fullstack','web','首屏慢，你会按什么顺序优化？','首屏性能|LCP|代码分割|懒加载|资源压缩|CDN|SSR|水合','先测 LCP 与资源瀑布；结合网络、脚本执行和渲染定位瓶颈。'),
('前端工程','frontend fullstack','web','TypeScript 能避免所有运行时类型问题吗？','TypeScript|类型收窄|泛型|结构类型|运行时校验','TS 主要做静态检查；外部输入仍需运行时校验；用接口数据举例。'),
('前端工程','frontend fullstack','web','前端项目如何组织构建和测试？','模块化|ES Modules|构建工具|Tree Shaking|单元测试|端到端测试','区分模块依赖、打包优化和测试层次；说明自己的项目取舍。'),
('网络与接口','frontend java go python fullstack ai test ops cpp','web','HTTP 和 HTTPS 有什么区别？','HTTP|HTTPS|TLS|证书|对称加密|非对称加密','HTTPS 使用 TLS；说明身份验证与会话加密，避免说所有数据都用非对称加密。'),
('网络与接口','java go python fullstack test ops cpp','web','TCP 为什么需要握手和重传？','TCP|三次握手|序列号|确认应答|重传|流量控制|拥塞控制','区分可靠传输、连接状态和两类控制；结合丢包场景。'),
('网络与接口','frontend java go python fullstack ai test','web','接口如何设计，重复请求怎么处理？','REST API|HTTP 方法|状态码|幂等性|幂等键|重试','幂等不等于只执行一次；对支付、下单说明去重和状态判断。'),
('安全与认证','frontend java go python fullstack ai test','web','Cookie、Session、JWT 有什么关系？','Cookie|Session|JWT|认证|授权|Token 过期|刷新令牌','区分存储载体、会话机制和令牌格式；讨论撤销、过期和泄漏风险。'),
('安全与认证','frontend java go python fullstack ai test','web','XSS、CSRF 和 SQL 注入如何防？','XSS|输出编码|CSP|CSRF|SameSite|SQL 注入|参数化查询','三个攻击机制分别回答；不能把 CORS 当作通用 CSRF 防护。'),
('Java 基础','java','java','equals 和 hashCode 为什么要一起重写？','Java|equals|hashCode|HashMap|哈希冲突|扩容','相等对象须有相同哈希值；从 HashMap 查找流程解释。'),
('Java 基础','java','java','ArrayList 和 LinkedList 怎么选？','集合|ArrayList|LinkedList|随机访问|数组扩容|缓存局部性','结合访问和修改位置；链表插入快以已持有位置为前提。'),
('Java 并发','java','java','synchronized 和 volatile 各解决什么？','Java 内存模型|可见性|原子性|有序性|volatile|synchronized|happens-before','volatile 不保证复合操作原子性；锁同时提供互斥与可见性保证。'),
('Java 并发','java','java','线程池如何配置，任务堆积怎么办？','线程池|核心线程数|工作队列|拒绝策略|CPU 密集|I/O 密集|背压','先描述负载与监控；线程数依赖任务、机器和下游容量。'),
('JVM / Spring','java','java','JVM 内存与 GC 怎么排查？','JVM|堆|栈|GC Roots|垃圾回收|内存泄漏|OOM','区分内存区域与可达性；使用日志和堆分析定位，不凭症状猜。'),
('JVM / Spring','java','java','Spring 依赖注入和 AOP 是怎么回事？','Spring|IoC|依赖注入|Bean 生命周期|AOP|动态代理','容器管理对象依赖；代理承载横切逻辑；联系事务与调用边界。'),
('JVM / Spring','java','db','事务注解为什么可能失效？','Spring 事务|动态代理|自调用|事务传播|回滚规则|数据库事务','检查是否通过代理调用、异常类型及传播配置；注解不等于任何调用都生效。'),
('Go 基础','go','go','goroutine 和线程有什么区别？','Go|goroutine|GMP 调度|线程|栈增长|并发','协程由运行时调度；不等于每个 goroutine 对应一个 OS 线程。'),
('Go 基础','go','go','channel、锁和 context 怎么搭配？','channel|select|互斥锁|context|超时|取消传播|goroutine 泄漏','用通信或共享状态选择机制；明确谁关闭 channel 和如何退出协程。'),
('Go 基础','go','go','slice、map 和 interface 有哪些坑？','slice|底层数组|append|map|并发读写|interface|nil','关注底层数组共享、map 同步，以及带动态类型的 interface 与 nil。'),
('Python 基础','python ai test','python','生成器、装饰器和可变默认参数怎么解释？','Python|迭代器|生成器|装饰器|可变默认参数|对象引用','说明惰性执行与函数包装；默认参数在函数定义时求值。'),
('Python 并发','python ai test','python','asyncio、线程和进程怎么选？','GIL|线程|进程|asyncio|协程|事件循环|阻塞 I/O','先区分 I/O 与 CPU 负载；GIL 与解释器版本、构建方式有关。'),
('Python 服务','python ai fullstack','python','Python API 服务怎么处理并发与参数校验？','ASGI|WSGI|FastAPI|参数校验|连接池|异步驱动','异步端点内阻塞调用仍可能拖慢服务；检查数据库驱动与连接池。'),
('数据库','java go python fullstack ai test ops','db','索引为什么能加速查询，什么时候用不上？','索引|B+ 树|联合索引|最左前缀|覆盖索引|回表|执行计划','从访问路径和扫描范围解释；索引选择要看优化器和实际执行计划。'),
('数据库','java go python fullstack test','db','事务隔离级别与 MVCC 是什么关系？','事务|ACID|隔离级别|脏读|不可重复读|幻读|MVCC|快照读','结合数据库实现；不要把不同数据库的同名隔离级别行为视为完全相同。'),
('数据库','java go python fullstack test','db','慢 SQL 怎么查？','慢查询|执行计划|索引|扫描行数|锁等待|连接池','先定位耗时位置，再看执行计划与锁；优化前后用同一负载验证。'),
('数据库','java go python fullstack test','db','死锁是怎么产生的，如何处理？','数据库锁|行锁|间隙锁|死锁|锁顺序|事务重试','分析资源等待环；缩短事务、统一锁顺序并处理可重试错误。'),
('缓存','java go python fullstack ai ops','redis','缓存穿透、击穿、雪崩有什么区别？','缓存|缓存穿透|缓存击穿|缓存雪崩|空值缓存|布隆过滤器|互斥重建|TTL 抖动','按不存在、热点失效和批量失效区分；不同场景采用不同机制。'),
('缓存','java go python fullstack','redis','缓存和数据库怎么保持一致？','Cache Aside|数据库更新|缓存删除|并发竞争|最终一致性|CDC','画出并发时序；先明确允许的陈旧窗口，再讨论失败补偿。'),
('缓存','java go python fullstack','redis','Redis 分布式锁有什么风险？','Redis|分布式锁|租约|原子释放|锁续期|fencing token','注意锁过期后的旧持有者；释放须校验身份，下游可用 fencing 拒绝旧操作。'),
('并发与服务','java go python fullstack ops cpp','ops','进程、线程与死锁怎么串起来？','进程|线程|上下文切换|共享内存|互斥锁|死锁','资源与调度单位分开回答；用多个锁的获取顺序说明死锁。'),
('并发与服务','java go python fullstack ai ops','ops','服务突然变慢，你从哪里查？','可观测性|指标|日志|链路追踪|P99|CPU|内存|I/O|连接池','从影响范围、时间线与延迟分位数开始；用链路定位下游。'),
('系统设计','java go python fullstack ai ops','ops','高并发接口怎么保护下游？','限流|令牌桶|熔断|降级|超时|重试|背压','重试可能放大流量；限制重试次数并配合退避、抖动和总超时。'),
('系统设计','java go python fullstack ops','ops','消息队列如何处理重复和丢失？','消息队列|生产确认|消费确认|重复投递|幂等性|死信队列|Outbox','说明交付保证边界；业务副作用仍需幂等与持久化设计。'),
('系统设计','java go python fullstack ops','ops','单机到分布式，哪些问题会出现？','负载均衡|复制|分片|一致性|网络分区|共识|CAP','从失败模型和一致性要求展开；CAP 讨论网络分区时的取舍。'),
('AI 应用基础','ai','ai','大模型 API 调用怎么做成稳定服务？','LLM API|Token|上下文窗口|流式输出|结构化输出|超时|重试|限流','从输入输出约束、错误处理、延迟和成本说明；API 密钥留在服务端。'),
('AI 应用基础','ai','ai','Prompt 和上下文工程有什么区别？','Prompt|系统指令|上下文工程|历史消息|上下文压缩|Token 预算','不仅是写指令，还要选择、组织和裁剪输入；说明信息丢失与成本取舍。'),
('RAG','ai','rag','RAG 的完整链路是什么？','RAG|文档解析|Chunking|Embedding|向量数据库|检索|Rerank|上下文构建|引用','分开离线入库和在线问答；每个阶段都可单独评估。'),
('RAG','ai','rag','关键词检索、向量检索和重排怎么配合？','检索|BM25|向量检索|混合检索|Rerank|Top K|召回率','召回侧扩大候选，重排侧提高排序质量；同时测准确率、延迟和成本。'),
('RAG','ai','rag','RAG 答错了，如何定位？','RAG 评测|检索命中|上下文相关性|忠实度|回答正确性|测试集','先确认正确资料是否被检索，再判断模型是否依据资料回答。'),
('RAG','ai','rag','什么时候选 RAG，什么时候考虑微调？','RAG|微调|知识更新|行为适配|训练数据|评测','知识获取与行为适配是不同目标；微调并不保证事实更新与可追溯引用。'),
('Agent','ai','ai','Agent 和固定工作流有什么区别？','Agent|工作流|模型决策|工具调用|状态|终止条件','模型决定下一步与固定流程的控制方式不同；结合可预测性和成本比较。'),
('Agent','ai','ai','工具调用一定会执行成功吗？','工具调用|JSON Schema|参数校验|工具执行|异常处理|幂等性','模型生成调用请求，应用负责执行；必须校验参数、权限和返回结果。'),
('Agent','ai','graph','Agent 的记忆和状态如何管理？','Agent|短期记忆|长期记忆|状态|检查点|持久化|恢复执行','会话状态与长期信息分开；持久化不等于模型自动记住所有内容。'),
('Agent','ai','graph','LangChain 和 LangGraph 各做什么？','LangChain|Agent|LangGraph|状态图|持久化|人工介入','前者提供模型、工具与 agent 抽象；后者侧重有状态编排运行时；以当前文档为准。'),
('Agent','ai','mcp','MCP 和 Function Calling 是什么关系？','MCP|Host|Client|Server|Tools|Resources|Prompts|工具调用','MCP 规范应用与外部系统的连接；工具调用是模型与应用之间的调用机制，层次不同。'),
('Agent','ai','ai','多 Agent 一定比单 Agent 更好吗？','多 Agent|任务拆分|协调|上下文隔离|延迟|成本|评测','只有拆分带来收益才引入；测量通信开销、错误传播与端到端成功率。'),
('AI 工程','ai test','ai','Agent 怎么防越权和提示词注入？','提示词注入|不可信输入|权限边界|最小权限|沙箱|人工确认','模型输出不能替代权限校验；把文档、网页等内容当不可信数据。'),
('AI 工程','ai test','graph','怎么证明 Agent 项目有效，而不只是 Demo？','Agent 评测|任务成功率|工具正确率|回归集|链路追踪|延迟|成本','固定可复现任务集；评估工具执行与最终结果，记录失败类别。'),
('机器学习','ml','ml','训练集、验证集、测试集为什么要分开？','数据划分|数据泄漏|验证集|测试集|交叉验证|泛化','测试集不用于调参；时间和用户维度分组要符合真实使用场景。'),
('机器学习','ml','ml','过拟合怎么发现，怎么处理？','过拟合|训练误差|验证误差|正则化|Dropout|早停|数据增强','观察训练与验证趋势；根据数据量和模型容量选择干预。'),
('机器学习','ml','ml','分类模型该选哪些评估指标？','混淆矩阵|Precision|Recall|F1|ROC-AUC|PR-AUC|类别不平衡','结合业务误判代价；不要只用准确率衡量不平衡任务。'),
('机器学习','ml','ml','Transformer 和模型微调有哪些核心概念？','Transformer|Attention|位置编码|预训练|微调|LoRA|量化','围绕信息交互、适配目标和资源开销解释，不必从数学课程开始。'),
('机器学习','ml ai','ml','模型推理为什么慢，如何优化？','模型推理|批处理|KV Cache|量化|显存|吞吐|延迟','区分预填充与逐 token 生成；用基准测延迟、吞吐和质量变化。'),
('测试开发','test','qa','接口测试用例怎么设计？','接口测试|等价类|边界值|异常输入|鉴权|幂等性|数据库断言','覆盖正常与失败路径；验证响应以及副作用，不只检查状态码。'),
('测试开发','test frontend fullstack','qa','自动化测试为什么会不稳定？','端到端测试|选择器|自动等待|测试隔离|Mock|Flaky Test','定位共享状态、时序和环境；避免靠固定 sleep 掩盖问题。'),
('测试开发','test ops','qa','压力测试怎么判断系统瓶颈？','压力测试|并发数|吞吐|P99|错误率|资源饱和|容量','先明确负载模型；同时看吞吐拐点、尾延迟和错误率。'),
('部署与运维','ops java go python fullstack ai','ops','容器和虚拟机有什么区别？','容器|虚拟机|Namespace|cgroups|镜像|容器网络','容器隔离进程并共享宿主内核；说明资源限制和隔离边界。'),
('部署与运维','ops','ops','Kubernetes 怎么发布与恢复服务？','Kubernetes|Pod|Deployment|Service|Ingress|健康检查|滚动更新','区分资源职责；结合 readiness、liveness 和回滚说明故障处理。'),
('部署与运维','ops java go python fullstack ai','ops','Linux 服务出问题，常用哪些排查方向？','Linux|进程|文件描述符|端口|权限|磁盘|日志|信号','先从进程、监听、资源和日志确认现象；避免直接重启丢失证据。'),
('部署与运维','ops frontend java go python fullstack ai test','ops','CI/CD 怎么保证发布质量？','Git|分支|代码审查|CI/CD|自动测试|制品|回滚','每次提交自动验证；构建制品可追溯，发布失败有回退路径。'),
('C++ / 客户端','cpp','cpp','指针、引用与智能指针怎么选？','C++|指针|引用|RAII|unique_ptr|shared_ptr|weak_ptr','从所有权和生命周期回答；用 weak_ptr 解释循环引用。'),
('C++ / 客户端','cpp','cpp','拷贝、移动与对象生命周期是什么关系？','对象生命周期|拷贝构造|移动语义|右值引用|析构|悬空引用','移动不等于总是没有拷贝；说明资源所有权转移与有效但未指定状态。'),
('C++ / 客户端','cpp','cpp','虚函数、STL 容器和迭代器有哪些追问？','虚函数|多态|虚析构|vector|unordered_map|迭代器失效','结合基类删除和容器修改场景；注意重分配导致的失效。'),
('手写与算法','frontend java go python fullstack ai ml test cpp','web','笔试和手写题应该优先准备什么？','数组|哈希表|双指针|滑动窗口|栈|队列|二分查找|链表|树|DFS|BFS|动态规划|复杂度','从题目约束选择结构与方法；说明时间空间开销并检查边界。'),
('项目追问','frontend java go python fullstack ai ml test ops cpp','ops','介绍项目时，面试官会沿着什么追问？','项目背景|个人贡献|技术选型|实现链路|性能瓶颈|失败案例|指标验证|改进方案','用自己真实做过的链路回答；准备为什么这样选、遇到什么问题和如何验证。'),
]
previous=json.loads(Path('data.json').read_text()) if Path('data.json').exists() else {}
old_nodes={n['name']:n['id'] for n in previous.get('nodes',[])}
old_questions={q['title']:q['id'] for q in previous.get('questions',[])}
next_node=max([int(v[1:]) for v in old_nodes.values() if v.startswith('n') and v[1:].isdigit()]+[0])+1
next_question=max([int(v[1:]) for v in old_questions.values() if v.startswith('q') and v[1:].isdigit()]+[0])+1
nodes={}; edges={}; questions=[]
for i,(module,rs,src,title,chain,cue) in enumerate(rows):
    names=chain.split('|'); ids=[]
    for name in names:
        if name not in nodes:
            nid=old_nodes.get(name)
            if not nid: nid=f'n{next_node}'; next_node+=1
            nodes[name]={'id':nid,'name':name,'roles':[],'modules':[],'sources':[]}
        n=nodes[name]; ids.append(n['id'])
        for key,vals in [('roles',rs.split()),('modules',[module]),('sources',[src])]: n[key]=list(dict.fromkeys(n[key]+vals))
    qid=old_questions.get(title)
    if not qid: qid=f'q{next_question}'; next_question+=1
    extension=any(word in title for word in ['Flex','首屏','构建和测试','JVM','注解','分布式锁','分布式，','多 Agent','微调有哪些','Kubernetes','虚函数'])
    questions.append({'id':qid,'title':title,'module':module,'roles':rs.split(),'nodes':ids,'cue':cue,'source':src,'priority':'再拓展' if extension else '先准备'})
    # These are interview follow-up edges, not asserted causal/implementation edges.
    for a,b in zip(ids,ids[1:]): edges[(a,b,'追问') ]={'from':a,'to':b,'type':'追问'}
relations=[('RAG','Embedding','使用'),('RAG','微调','对比'),('Agent','工具调用','使用'),('Agent','工作流','对比'),('MCP','工具调用','连接机制'),('LangGraph','状态','管理'),('LangGraph','持久化','支持'),('HTTP','TLS','安全层'),('HTTPS','TLS','使用'),('闭包','词法作用域','依赖'),('索引','B+ 树','常见实现'),('线程','共享内存','共享'),('JWT','认证','用于'),('SQL 注入','参数化查询','防护'),('React','state','管理'),('向量检索','Embedding','依赖'),('微调','LoRA','适配方法'),('Redis','缓存','用途'),('数据库事务','ACID','性质'),('多 Agent','Agent','协作组成')]
relations += [('HTTP 缓存','Cache-Control','配置'),('协商缓存','ETag','验证'),('CORS','预检请求','机制'),('Vue','Proxy','响应式基础'),('Vue','props','组件输入'),('Vue','emit','组件事件'),('React','Hooks','使用'),('useEffect','清理函数','支持'),('useMemo','useCallback','对比'),('Flex','Grid','对比'),('浅拷贝','深拷贝','对比'),('Promise','async/await','语法关系'),('this','call/apply/bind','绑定'),('数组','链表','对比'),('树','DFS','遍历'),('树','BFS','遍历'),('哈希表','哈希冲突','处理'),('HashMap','hashCode','使用'),('ArrayList','数组扩容','涉及'),('volatile','可见性','保证'),('synchronized','互斥锁','提供'),('线程池','工作队列','使用'),('Spring','依赖注入','支持'),('AOP','动态代理','常见实现'),('goroutine','GMP 调度','调度机制'),('context','取消传播','支持'),('slice','底层数组','引用'),('map','并发读写','需要同步'),('asyncio','事件循环','运行机制'),('生成器','迭代器','实现协议'),('联合索引','最左前缀','使用规则'),('覆盖索引','回表','避免'),('事务','ACID','性质'),('MVCC','快照读','支持'),('死锁','锁顺序','预防策略'),('缓存穿透','布隆过滤器','缓解'),('缓存击穿','互斥重建','缓解'),('缓存雪崩','TTL 抖动','缓解'),('幂等性','重试','安全前提'),('限流','令牌桶','实现方法'),('可观测性','链路追踪','组成'),('RAG','Chunking','入库处理'),('RAG','Rerank','可选阶段'),('RAG','引用','可追溯输出'),('混合检索','BM25','组成'),('混合检索','向量检索','组成'),('Agent','终止条件','约束'),('工具调用','参数校验','执行前检查'),('Agent','最小权限','权限原则'),('MCP','Server','架构角色'),('MCP','Client','架构角色'),('MCP','Resources','能力'),('LangGraph','检查点','恢复机制'),('Agent 评测','任务成功率','指标'),('数据泄漏','泛化','评估风险'),('过拟合','早停','缓解'),('模型推理','量化','优化方法'),('KV Cache','显存','资源开销'),('shared_ptr','weak_ptr','配合'),('RAII','析构','释放资源'),('容器','Namespace','隔离机制'),('容器','cgroups','资源控制'),('Deployment','Pod','管理'),('Service','Pod','访问目标'),('CI/CD','自动测试','质量检查'),('接口测试','边界值','用例设计')]
for a,b,t in relations:
    if a in nodes and b in nodes:
        x,y=nodes[a]['id'],nodes[b]['id']; edges[(x,y,t)]={'from':x,'to':y,'type':t}
d={'version':1,'updated':'2026-10-12','roles':[dict(zip(['id','name','description','number'],r)) for r in roles],'sources':{k:{'name':v[0],'url':v[1],'verified':v[2]} for k,v in S.items()},'nodes':list(nodes.values()),'edges':list(edges.values()),'questions':questions}
from enrich import enrich
d=enrich(d)
Path('data.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(f"{len(d['nodes'])} concepts, {len(d['questions'])} questions, {len(d['edges'])} edges")
