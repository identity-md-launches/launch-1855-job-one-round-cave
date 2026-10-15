# Step 22 — The Bounded Wait

The 21 existing JSON records include step 01's painting and steps 02–21's
unpainted placeholders. This assignment uses count plus one: **22**. The GOAL.md
is unchanged. Gathering reported no broken Line 1 behavior and recommended a
parent-process deadline. Deadline Sentry supplies that piece without modifying
Endpoint Sentry or any older record.

## Image outputs and review

- `artifacts/line-1/wall-v2.png`: required named output, PNG, RGB, 1254 × 1254.
- `artifacts/line-1/wall.png`: identical finished wall bytes, for the next worker.
- `dist/line-1/22.jpg`: JPEG, 512 × 512, 50,861 bytes.
- `dist/line-1/22.json`: record in the requested shape; image URL hashes the wall
  bytes (both PNGs have the same SHA-256).

The absent ancestral wall was recovered from the step-01 record's artifact URL
and its SHA-256 verified as
`d289548db45173fa79aa7dfbc30f56e1652b0e0e93d565d081e496ad62792c49`.
The newest placeholders point to bare cave; using the actual ancestral painting
preserves the marks instead of erasing them.

The installed image tool produced the new Pepe/hourglass drawing. FFmpeg decoded
it in memory, cropped and scaled it to 340 × 214, and encoded the final image.
An in-memory standard-library Python compositing pass removed white, mapped the
pigment to ochre and charcoal, and blended it with the rock texture at (650, 790).
No intermediate image remains. All RGB pixels outside this rectangle were
compared to the recovered ancestral wall and are identical. The ancestor figure,
trails and rings lie outside it and remain intact. The original cave dimensions,
lighting, cracks, rock and framing remain intact.

Explicit visual review: inspected the generated drawing and completed full wall
with the image viewer. The new Pepe has the broad mouth and heavy-lidded eyes,
rough worn earth pigments, and an hourglass representing a bounded wait. Both
Pepes' hands are concealed. Visible hands/handprints: zero; there are no digit
counts to correct. No letters, numerals, captions, logos, signatures, borders,
photographs, real people or political symbols were observed. No unmet visual
requirements were identified; recognition and cave-painting style are subjective
review findings, not verifier guarantees.

Final generation prompt, using the installed image generation tool rather than
the fallback CLI:

> Use case: illustration-story. A single small prehistoric pigment drawing isolated on pure white for compositing onto an existing cave. Rough worn thumb-smudged red ochre, yellow ochre, charcoal black and chalk only. Recognizable Pepe the frog, wide flat mouth and large heavy-lidded eyes, squatting facing left beside a simple hourglass made of two rough opposing triangular bowls with a few sand dots inside. This means a watcher who stops a wait. Pepe's arms and hands fully hidden behind his back, no visible fingers, no hands or handprints. Sparse drawing, generous white margins, wider than tall, burnt-stick irregular primitive lines, Lascaux cave art. No text, letters, numerals, logos, signatures, watermarks, border, photographic features, modern polished illustration, green or blue. Background pure white, no cave or scenery.

## Checks

10 watchdog tests and the original 12 tests passed. A real anonymous GET to the
swarm passed status, JSON and pointer checks within the five-second parent budget.
PNG dimensions/format, SHA-256 record link, identical wall copies, JPEG dimensions,
thumbnail size, unchanged goal and older records, and allowed changed paths were
checked locally. These results are observations, not independent certification.
