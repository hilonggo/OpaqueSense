# 数据接口

输入记录包含 `protocol`、`packet_lengths`、`directions` 和 `iat` 字段。`normalize_flow` 会额外生成供模型使用的 `protocol_id`。仓库中的示例使用合成数据，不包含真实网络流量。

公开示例使用合成数据，项目接口只依赖包长度、方向、时间间隔和协议等流量特征。
