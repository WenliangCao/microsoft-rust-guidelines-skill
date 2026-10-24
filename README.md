# Microsoft Rust Guidelines Skill

把微软的 [Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)
打包成可按需读取的 agent skill，用于编写、审查和重构 Rust 代码。

这是独立维护的 skill，与 Microsoft 无隶属或背书关系。

## 设计

入口是简短的 [SKILL.md](SKILL.md)，规则按任务加载：

```text
SKILL.md → references/index.md → 相关的 M-*.md 原文
```

规则正文和配图均从上游逐字节复制，保留示例、例外、版权声明与规则 ID。
不把全文塞进入口，不混合其他指南后冒充微软原文，也不把微软的设计偏好
当成 Rust 语言的强制要求。Rust API Guidelines 等补充来源仍按原文链接查阅。

上游版本、commit、规则数量和文件 SHA-256 见
[references/snapshot.json](references/snapshot.json)；完整目录见
[规则索引](references/index.md)。日常使用无需联网。

## 安装到 Codex

把本仓库克隆到 Codex 的 skills 目录，目录名使用技能名：

```sh
git clone https://github.com/WenliangCao/microsoft-rust-guidelines-skill.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/microsoft-rust-guidelines"
```

如果该目录已存在，请更新已有安装或选择另一个安装位置，避免覆盖。
安装后在新的会话中使用。其他支持 `SKILL.md` 的 agent 可将同一目录安装到
各自的技能目录；`agents/openai.yaml` 仅提供 Codex 展示信息。

## 使用

```text
用 $microsoft-rust-guidelines 审查这个 Rust crate，优先检查错误处理和公共 API。
```

```text
用 $microsoft-rust-guidelines 实现这个功能，只读取与当前改动相关的规则。
```

```text
按 $microsoft-rust-guidelines 核对 M-TYPES-SEND 在这个异步 API 上是否适用。
```

技能支持自动发现。具体执行仍遵守项目约束，例如 MSRV、已有 API 兼容性、
部署目标，以及项目要求的 `mbx` 等命令入口。

## 维护与校验

同步工具只依赖 Python 3.10+ 和 Git，测试只使用 Python 标准库。

```sh
# 离线核对已提交文件的完整性。
python3 scripts/sync_guidelines.py --check

# 运行同步工具的行为测试。
python3 -m unittest discover -s tests -v

# 显式更新到上游 main，或将 main 换成具体 commit。
python3 scripts/sync_guidelines.py --ref main
git diff
```

不带 `--ref` 同步时沿用当前固定的 commit。更新会重建
`references/upstream/`、`references/index.md` 和 `references/snapshot.json`；
发布前检查原文变动和入口的主题映射。校验只证明文件与记录的快照一致，
不等于已经审查了某个 Rust 项目的全部行为。

## 许可证

技能说明与同步工具使用 [MIT License](LICENSE)。微软原文与配图保留
[上游 MIT License](references/upstream/LICENSE.md)。来源及处理方式见
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
