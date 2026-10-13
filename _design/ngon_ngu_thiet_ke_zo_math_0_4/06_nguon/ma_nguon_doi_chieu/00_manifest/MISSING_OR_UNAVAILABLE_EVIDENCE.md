# Missing, unavailable, and intentionally excluded evidence

The absence of an item below does not mean it never existed. The bundle is representative and bounded, not a complete archive.

## Missing at the exact P0 locator

- P0.2 lists legacy social-image paths under `E:\zo_math\images\` (including Facebook covers and the YouTube banner). The named image files were not present at those exact paths during the copy check. Files with matching names were found under `E:\zo_math\assets\logo\` and are included as separate evidence; no lineage to the old `images\` paths was established.
- `D:\Downloads\ZO_MATH_ABOUT_HANDOFF_20260829\_research\README.md` was not present at that exact locator. The repository's `E:\zo_math\_research\README.md` is included, but it is not substituted as the Downloads handoff copy.
- Some exact P0-referenced snapshots and folder contents were not independently inventoried, including the contents of `E:\zo_math_ca_nhan\tu_repo_zo_math` and the two personal archives recorded in the location register.

## Not located or not represented by a direct output

- No standalone subtitle (`.srt`/`.ass`) file was confirmed in the bounded media/video survey.
- A genuine rendered vertical 9:16 video was found and included. No rendered horizontal 16:9 video was confirmed; the included horizontal artifact is a design template only.
- No clearly identified final narration/voice-over file was confirmed. No audio sample was copied.
- No website screenshot/rendered webpage was available as a selected visual output. Existing PDFs, SVGs, PNGs, and the vertical MP4 provide other visual evidence.
- No geometry receipt file was located in the selected audit-fixture set. The compiler and existing YAML/SVG/PNG fixtures are included.
- No separate variation schema file was identified in the tool-folder inventory. The README, builder, TeX template, CSS/Lua integration, JSON data, and existing rendered tables are included.
- Only selected published and lesson PDFs are included; this is not a PDF-output archive.

## Intentionally not copied

- Font binaries (`.ttf`, `.otf`, `.woff2`) were not copied. The 26 observed filenames and original paths are listed in [`../04_typography/FONT_BINARY_INVENTORY.md`](../04_typography/FONT_BINARY_INVENTORY.md). This avoids redistributing font binaries without a task-specific need or licensing review.
- WAV/SFX/music files were not copied. Their source/licensing and sonic-brand status were not established, and the text guidance is sufficient for this evidence pass.
- Large or intermediate media, render fragments, caches, broad archive/download directories, complete website trees, and complete repositories/worktrees were excluded.
- Duplicate logo files across repository, media, prelaunch/publish snapshots, and Downloads were included once where SHA-256 matched; exact duplicate relations are listed in the bundle manifest.
- P0 mentions other Downloads snapshots and release/recovery bundles. They were not opened or copied unless an exact named file was directly relevant to the selected evidence set. No lineage was inferred from similar filenames.
- The Downloads Playbook PDF is included as a locator-specific binary, but its pages were not inspected. It must not be used as an authority based on its filename alone.

## Lineage and authority still unresolved

- Logo filenames containing `master` do not establish approval. Matching hashes establish byte identity only for the compared files.
- Current repository, media workspace, prelaunch and published outputs are separate evidence contexts. The bundle does not reconcile all their histories or establish a single current identity system.
- Some copied reports and source files contain references to original paths or uncopied assets. The manifest provides the copied-file location and original source locator; no claim is made that every original relative link remains navigable.
- Copied research reports were preserved without rewriting their original links. A bounded local-link check found references to source files outside the mirrored research-report tree; the corresponding selected sources are mapped to their bundle domain folders in `SOURCE_BUNDLE_MANIFEST.md`. Some linked sources were intentionally not selected (for example, complete social upload packages and unrelated research citations).
- No accessibility, contrast, screen-reader, font-rendering, or cross-medium visual acceptance testing was conducted for this bundle.
