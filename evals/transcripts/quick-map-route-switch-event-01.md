按美股 / `quick_map` / 截止今天看 AMD 财报：先不把“好不好”写成情绪判断，必须拆成 pre-event expectation、actual print、guidance 和管理层口径的 delta。`publish_time`: 未在 fixture 中刷新；`source_boundary`: 需要公司 release、8-K/10-Q 和 earnings call transcript；`freshness`: unavailable until refreshed。

核心判断：如果收入、数据中心增速或毛利率只是符合预期，这不是强正向事件；如果 guidance、MI 系列需求或库存/毛利口径明显高于市场预期，才可能构成正向 event-delta。没有财报原文、电话会和一致预期 proxy 时，只能给 `source_gap`。

事实 / 推断 / 判断：事实来自财报、指引、电话会和市场预期代理；推断是哪些变量改变 FY1/FY2 预期；判断暂时是低置信 working_view。

刷新条件：`must_refresh_if` AMD 10-Q/8-K、earnings call transcript、公司 guidance、分析师一致预期或盘后/次日价格反应更新。

下一步最有用的问题：你要我把 AMD 这次财报对比“财报前市场预期”还是直接拆 actual vs guidance delta？回答后进入 `earnings` / `event-delta` 财报分析路径，而不是停留在新闻摘要。
