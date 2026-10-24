# Microsoft Rust Guidelines Skill

An agent skill that makes Microsoft's
[Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)
available when writing, reviewing, or refactoring Rust code.

This project is maintained independently and is not affiliated with or endorsed
by Microsoft.

## How it works

[SKILL.md](SKILL.md) is the entry point. It tells the agent how to choose the
rules relevant to a task and how to apply them, then points to the
[rule index](references/index.md), which links to each original rule file:

```text
SKILL.md → references/index.md → references/upstream/<topic>/M-*.md
```

Only the rules a task needs are loaded. The rule texts, illustrations, and
upstream overview are unmodified copies of the upstream sources, pinned to the
commit recorded in [references/snapshot.json](references/snapshot.json)
together with a SHA-256 hash of every bundled file. No network access is
required at use time.

## Installation

Clone the repository into your agent's skills directory, using
`microsoft-rust-guidelines` as the directory name:

```sh
git clone https://github.com/WenliangCao/microsoft-rust-guidelines-skill.git \
  <skills-directory>/microsoft-rust-guidelines
```

Any agent that supports the `SKILL.md` format can load it. Start a new session
after installing.

## Usage

The agent picks up the skill automatically for Rust work. It can also be
requested explicitly, for example:

- "Review this crate against the Microsoft Rust Guidelines, focusing on error
  handling and the public API."
- "Implement this feature following the Microsoft Rust Guidelines."
- "Does M-TYPES-SEND apply to this async API?"

The skill defers to project constraints such as MSRV, API compatibility,
deployment targets, and the repository's own build and test commands.

## Maintenance

The synchronization script requires Python 3.10+ and Git; the tests use only
the standard library.

```sh
# Verify the committed snapshot offline.
python3 scripts/sync_guidelines.py --check

# Run the synchronization tests.
python3 -m unittest discover -s tests -v

# Update to upstream main (or pass a specific commit), then review the result.
python3 scripts/sync_guidelines.py --ref main
git diff
```

Without `--ref`, the script regenerates the snapshot at the currently pinned
commit. An update rewrites `references/upstream/`, `references/index.md`, and
`references/snapshot.json`. Before committing an update, review the upstream
changes and adjust the topic table in `SKILL.md` if sections were added or
renamed. CI runs both checks on every push and pull request.

## License

The skill instructions, script, and tests are released under the
[MIT License](LICENSE). Microsoft's guideline texts and illustrations remain
under the [upstream MIT License](references/upstream/LICENSE.md). See
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for attribution details.
