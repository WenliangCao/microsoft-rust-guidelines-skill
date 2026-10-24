---
name: microsoft-rust-guidelines
description: Apply Microsoft's Pragmatic Rust Guidelines when writing, reviewing, or refactoring Rust code. Select original rules by topic and M-* identifier for APIs, correctness, async code, performance, documentation, and workspace design.
---

# Microsoft Rust Guidelines

Use Microsoft's guidelines as a source of concrete Rust design advice. This is an
independent skill packaging, not a Microsoft product. The complete rule texts are
bundled locally; normal use needs no network access.

## Select the relevant rules

1. Inspect the task and repository instructions. Identify whether the affected
   crate is an application, an internal application crate, or a reusable library;
   note its MSRV, targets, runtime, and public compatibility requirements.
2. Open [the rule index](references/index.md), select the relevant topic below,
   then read the linked rule files. For a named `M-*` rule, find that identifier
   directly. Do not load every rule for an ordinary edit.
3. Read a selected rule in full, including its exceptions and examples. Follow
   cross-references when they affect the decision. An index title alone is not
   enough evidence to apply a rule.

| Work being done | Index section |
| --- | --- |
| Naming, common traits, logging, lints | Universal |
| Application errors, allocator, deployment CPU | Application |
| Panics, unsafe, soundness | Correctness |
| Rustdoc, examples, public documentation | Documentation |
| Foreign interfaces, DLL boundaries | FFI |
| Features, dependencies, build experience | Libraries / Building |
| `Send`, conversions, I/O traits, foreign types | Libraries / Interoperability |
| Global state, strong types, mocking, integration tests | Libraries / Resilience |
| Public errors, builders, abstractions, async APIs | Libraries / UX |
| Declarative and procedural macros | Macro |
| Allocation, hot paths, yielding, throughput | Performance |
| Workspace layout, edition, MSRV | Project |
| Agent edits, ports, public paths, meaningful tests | AI |

For an unfamiliar crate or a broad review, start with
[M-UPSTREAM-GUIDELINES](references/upstream/universal/M-UPSTREAM-GUIDELINES.md)
and the applicable topics. For a narrow task, go directly to its rules. If an
identifier is absent from the index, say it is absent from this snapshot rather
than inventing its contents.

## Apply with context

- Follow explicit user requirements and repository conventions. Preserve the
  original distinction between **must**, **should**, and **may**. Microsoft design
  preferences are not automatically Rust language requirements.
- Apply application and library rules to the correct crates. In particular,
  [M-APP-ERROR](references/upstream/apps/M-APP-ERROR.md) permits application error
  crates, while reusable library errors have different guidance in
  [M-ERRORS-CANONICAL-STRUCTS](references/upstream/libs/ux/M-ERRORS-CANONICAL-STRUCTS.md).
- Keep the change within the requested scope. Allocator changes, deployment CPU
  flags, MSRV bumps, dependency swaps, and public API redesigns require relevant
  project context; finding a recommendation is not a reason to add them to an
  unrelated edit. Guideline flexibility never justifies unsound code.
- Retain existing compatibility commitments unless the task includes migration.
  Consult current authoritative documentation when crate versions, language
  features, or tool availability matter; the bundled snapshot is not a promise
  that an example's dependency version is current.
- Validate observable behavior with the project's existing checks. Respect its
  command runner, including `mbx` when required, instead of bypassing it with
  bare Cargo. Select additional tools such as Miri or feature checks only when
  warranted by the change. Report unavailable or unrun checks accurately.

When reviewing, connect each actionable finding to a location, a concrete effect,
and the applicable rule ID. Distinguish correctness problems from optional design
recommendations. When implementing, explain material decisions briefly; do not
add guideline compliance tables or design journals to product documentation.

## Source and maintenance

[Snapshot metadata](references/snapshot.json) pins the upstream commit and hashes
the bundled files. Rule text and illustrations are copied byte for byte from
[microsoft/rust-guidelines](https://github.com/microsoft/rust-guidelines), with
[Microsoft's MIT license](references/upstream/LICENSE.md).

Use the local index to resolve cross-rule IDs. Original relative book links are
preserved; resolve other book links against the corresponding page of the
[upstream website](https://microsoft.github.io/rust-guidelines/).

Use the pinned snapshot by default. Refresh only when the task calls for an
update; run `python3 scripts/sync_guidelines.py --ref main` from this skill's
directory, then inspect the diff. Use `--check` to verify the local snapshot
without network access. Do not edit generated reference files by hand.
