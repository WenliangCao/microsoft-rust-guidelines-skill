# Microsoft Rust Guidelines Skill

An agent skill that packages Microsoft's
[Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)
for on-demand use when writing, reviewing, and refactoring Rust code.

This skill is independently maintained and is not affiliated with or endorsed by Microsoft.

## Design

The concise [SKILL.md](SKILL.md) entrypoint directs the agent to load rules relevant to the task:

```text
SKILL.md → references/index.md → relevant original M-*.md rule files
```

Rule texts and illustrations are copied byte for byte from upstream, preserving
examples, exceptions, copyright notices, and rule IDs. The entrypoint uses
selective loading to keep context focused. Microsoft's original guidance remains
separate from other sources, and its design preferences are distinguished from
Rust language requirements. Supplementary sources, such as the Rust API Guidelines,
are available through the original links.

See [references/snapshot.json](references/snapshot.json) for the pinned upstream
commit, rule count, and file SHA-256 hashes. Browse all rules in the
[rule index](references/index.md). Normal use requires no network access.

## Install in Codex

Clone this repository into Codex's skills directory, using the skill name as the directory name:

```sh
git clone https://github.com/WenliangCao/microsoft-rust-guidelines-skill.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/microsoft-rust-guidelines"
```

If the directory already exists, update the existing installation or choose another
location to avoid overwriting it. Start a new session after installation.
Other agents that support `SKILL.md` can use the same directory in their respective
skills locations; `agents/openai.yaml` provides Codex display metadata only.

## Usage

```text
Use $microsoft-rust-guidelines to review this Rust crate, focusing on error handling and public APIs.
```

```text
Use $microsoft-rust-guidelines to implement this feature, reading only the rules relevant to the change.
```

```text
Use $microsoft-rust-guidelines to check whether M-TYPES-SEND applies to this async API.
```

The skill supports automatic discovery. It respects project constraints, including
MSRV, existing API compatibility, deployment targets, and required command runners
such as `mbx`.

## Maintenance and validation

The synchronization tool requires Python 3.10+ and Git. Tests use only the Python standard library.

```sh
# Verify the integrity of the committed snapshot offline.
python3 scripts/sync_guidelines.py --check

# Run behavior tests for the synchronization tool.
python3 -m unittest discover -s tests -v

# Explicitly update to upstream main, or replace main with a specific commit.
python3 scripts/sync_guidelines.py --ref main
git diff
```

Running synchronization without `--ref` preserves the currently pinned commit.
Updates regenerate `references/upstream/`, `references/index.md`, and
`references/snapshot.json`. Before publishing an update, review the upstream changes
and the entrypoint's topic mapping. Validation checks consistency with the recorded
snapshot; assessing a Rust project's behavior still requires a separate review.

## License

The skill instructions and synchronization tool use the [MIT License](LICENSE).
Microsoft's original texts and illustrations retain the
[upstream MIT License](references/upstream/LICENSE.md). See
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for attribution and packaging details.
