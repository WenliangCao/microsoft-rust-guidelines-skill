---
name: microsoft-rust-guidelines
description: Apply Microsoft's Pragmatic Rust Guidelines when writing, reviewing, or refactoring Rust code. Selects the relevant M-* rules by topic or identifier, covering API design, error handling, correctness and unsafe code, async, performance, documentation, FFI, macros, and workspace layout.
---

# Microsoft Rust Guidelines

This skill provides Microsoft's
[Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/) as a
local reference. The full text of every rule is bundled under `references/`, so
no network access is needed. This packaging is independent and not a Microsoft
product.

## Selecting rules

1. Establish the context: the kind of crate affected (application, crate used
   only by an application, or reusable library), its MSRV, targets, async
   runtime, and public compatibility commitments, plus any repository
   instructions.
2. Open the [rule index](references/index.md) and locate the relevant section
   from the table below, or search for a named `M-*` identifier directly. Load
   only the rules the task needs.
3. Read each selected rule in full, including its exceptions and examples, and
   follow cross-references that bear on the decision. Do not apply a rule on the
   strength of its title alone.

| Area of work | Index section |
| --- | --- |
| Naming, `Debug`/`Display`, magic values, lints, static analysis, logging, crate size | Universal Guidelines |
| Application error types, allocator, `target-cpu` | Application Guidelines |
| Panics, `unsafe`, soundness | Correctness Guidelines |
| Rustdoc structure, first sentences, module docs, `#[doc(inline)]` | Documentation |
| FFI crate naming and layering, DLL state | FFI Guidelines |
| Cargo features, out-of-the-box builds, `-sys` crates | Libraries / Building Guidelines |
| `Send`, `AsRef`, I/O and range parameters, foreign types and re-exports | Libraries / Interoperability Guidelines |
| Statics, strong types, mockable I/O, builder validation, tests, telemetry | Libraries / Resilience Guidelines |
| Library errors, builders, abstractions, `async fn`, generics, modules, services | Libraries / UX Guidelines |
| Declarative and procedural macros | Macros Guidelines |
| Allocation, hashing, hot paths, async stack size, yielding, throughput | Performance Guidelines |
| Workspace layout, edition, MSRV | Project Guidelines |
| AI-friendly APIs, ports from other languages, single item paths, meaningful tests | AI Guidelines |

For a broad review or an unfamiliar crate, begin with
[M-UPSTREAM-GUIDELINES](references/upstream/universal/M-UPSTREAM-GUIDELINES.md),
then the sections that apply. For a narrow task, go straight to the relevant
rules. If a requested identifier is not in the index, state that it is absent
from this snapshot; do not reconstruct its content.

## Applying rules

- **Precedence.** Explicit user requirements and repository conventions take
  precedence. The guidelines are a team-adopted standard, not Rust language
  requirements.
- **Strength.** Preserve the wording of each rule: _must_ rules are meant to
  always hold; _should_ rules allow more flexibility; _may_ rules grant a
  permission.
- **Intent.** Follow the spirit of a rule, not only its letter. Understand why a
  rule exists before departing from it, and do not apply it where doing so would
  defeat its purpose (see the
  [upstream applicability notes](references/upstream/README.md)). Flexibility
  never justifies unsound code.
- **Crate kind.** Apply application and library rules to the right crates. For
  example, [M-APP-ERROR](references/upstream/apps/M-APP-ERROR.md) allows
  application-level error crates, whereas libraries follow
  [M-ERRORS-CANONICAL-STRUCTS](references/upstream/libs/ux/M-ERRORS-CANONICAL-STRUCTS.md).
- **Scope.** Keep changes within the task. Allocator changes, `target-cpu`
  flags, MSRV or edition bumps, dependency replacements, and public API
  redesigns need a project-level reason; a matching rule alone does not justify
  adding them to an unrelated change. Keep existing compatibility commitments
  unless the task includes a migration.
- **Currency.** Rule examples may name crate versions or tools that have since
  changed. Check current documentation when versions, language features, or
  tool availability matter.
- **Verification.** Validate behavior with the project's existing build, test,
  and lint commands, through its own task runner where it has one. Add tools
  such as Miri or feature-combination checks only when the change warrants
  them. Report any check that was not run or could not be run.

## Reporting

- In a review, tie each finding to a code location, its concrete effect, and the
  rule ID. Separate correctness defects from optional design recommendations.
- When implementing, explain significant decisions briefly. Do not add
  guideline-compliance tables or design narratives to product documentation
  ([M-NO-META-DESIGN-DOCUMENTATION](references/upstream/ai/M-NO-META-DESIGN-DOCUMENTATION.md)).

## Source and updates

Rule texts and illustrations are byte-for-byte copies from
[microsoft/rust-guidelines](https://github.com/microsoft/rust-guidelines) under
[Microsoft's MIT license](references/upstream/LICENSE.md).
[snapshot.json](references/snapshot.json) records the pinned upstream commit and
a SHA-256 hash of each bundled file.

Resolve `M-*` cross-references through the local index. Relative links inside
rules are preserved as published; resolve any that do not map to a local file
against the [upstream website](https://microsoft.github.io/rust-guidelines/).

Use the pinned snapshot unless the task is to update it. To update, run
`python3 scripts/sync_guidelines.py --ref main` from the skill directory and
review the diff; `--check` verifies the snapshot offline. Do not edit generated
files under `references/` by hand.
