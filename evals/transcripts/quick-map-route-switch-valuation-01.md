按美股 / `quick_map` / 截止今天看 CRWV：这个问题表面是一句话方向，但诚实回答依赖估值锚，不能在没有 EV、NTM 收入一致预期、RPO 或同业增速对比时直接说贵或便宜。`quote_time`: 未拉取实时行情；`live_freshness_status`: unavailable；`source_boundary`: 本 fixture 只验证 quick_map 输出纪律，不声称当前价格。

核心判断：当前只能写成 `working_view`。如果 CRWV 的 EV/NTM-Sales 已经隐含远高于可验证增长和合同兑现，才可能判断偏贵；如果 RPO 转收入和毛利路径能支撑隐含预期，结论会被削弱。现在缺口是 `calculation_gap` / `source_gap`，不是方向判断本身。

事实 / 推断 / 判断：事实需要来自最新股价和市值、净现金/债务、NTM revenue consensus、RPO、毛利率与可比公司倍数；推断是市场隐含了多高增长；判断只能是低到中置信，直到 calculation_gate 补齐。

刷新条件：`must_refresh_if` CRWV 最新财报、RPO 口径、NTM consensus、当前 EV 或 peer multiple 显著变化；若用于 live 判断，必须先刷新 quote_time。

下一步最有用的问题：你要我用 EV/NTM-Sales 还是 EV/RPO 做 CRWV 的估值锚？回答后进入 `standard` + quant/calculation gate，把“贵不贵”从 quick_map 升级为可复核的估值判断。
