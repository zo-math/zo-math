# ZO Math Design System — evidence source bundle

## Purpose

This self-contained copy gathers representative source material and existing visual outputs referenced by the P0–P2 research and the eight-file consolidation package. It is intended to let a downstream reviewer inspect the evidence without opening the original workspaces.

It is an evidence bundle, **not** a Design System, source of truth, specification, or record of approved decisions. Copying a file here does not make it current, approved, effective, or suitable for reuse. The source path, evidence class, state, and limitations are recorded in [`00_manifest/SOURCE_BUNDLE_MANIFEST.md`](./00_manifest/SOURCE_BUNDLE_MANIFEST.md).

## How to read the evidence

1. Read the eight copied consolidation reports in [`01_research/zo_design_system/consolidation_01/`](./01_research/zo_design_system/consolidation_01/) for the synthesis and its limits.
2. Read P0.2–P0.4 and P1.0 in [`01_research/zo_design_system/`](./01_research/zo_design_system/) to understand the evidence map and governance context.
3. Read the R1, R2, R6, and P2 research reports before inspecting domain sources.
4. Compare the direct implementation sources and the separately classified outputs in `02_`–`16_`. The location register and missing-evidence register explain what was not inspected or copied.

The consolidation reports are included as copies so this folder can travel independently. Compare their statements against the source files here; do not treat the reports as substitutes for the underlying evidence.

## Evidence classes and status labels

The manifest uses these status labels only: `owner-confirmed`, `research`, `candidate`, `historical`, `implementation`, `output`, and `unknown-provenance`.

- **Historical** identifies an earlier or snapshot source/output; it does not mean obsolete.
- **Implementation** means code/configuration or a project rule was observed in a source tree; it does not prove universal use or approval as a system-wide standard.
- **Output** means an existing rendered/exported artifact; it does not establish its quality or release status.
- **Candidate** is a research candidate or proposal; it is not an adopted direction.
- **Owner-confirmed** records the project owner's current stated intent only. It does not prove educational effectiveness, user demand, external validity, or a Design System decision.
- **Unknown provenance** indicates that the source's authority or lineage was not established.

The P2 images are retained only under `16_visual_outputs/early_experiments/`. They are exploratory outputs, not approved directions. Geometry spike outputs are isolated under `historical/geometry_spike/`; they are audit fixtures, not production dependencies.

## Deliberate exclusions

- No font binaries are included. See [`04_typography/FONT_BINARY_INVENTORY.md`](./04_typography/FONT_BINARY_INVENTORY.md) for the observed filenames and original paths.
- No full website, repository, archive, worktree, or broad Downloads folder is included.
- No audio sample, full narration deliverable, standalone subtitle file, or rendered horizontal video was identified and packaged. Existing video/audio process documentation is included.
- Exact duplicate logo binaries were included once; their duplicate locations are recorded in the manifest and location register.
- Some source documents retain references to their original repository paths. Use this bundle's manifest to locate the corresponding copied files.

## Scope

Files were copied for evidence review. No source file was edited, renamed, moved, deleted, rendered, or rebuilt. No production or `_research` file was changed. No Decision, Principle, or Draft 0.1 was created. No commit or push was made.

See [`00_manifest/SOURCE_LOCATION_REGISTER.md`](./00_manifest/SOURCE_LOCATION_REGISTER.md), [`00_manifest/MISSING_OR_UNAVAILABLE_EVIDENCE.md`](./00_manifest/MISSING_OR_UNAVAILABLE_EVIDENCE.md), and [`00_manifest/SHA256SUMS.txt`](./00_manifest/SHA256SUMS.txt).
