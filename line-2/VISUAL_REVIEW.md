# Pepe 01 visual and output review

- Wall: `artifacts/line-2/wall.png`, PNG, RGB, **1254 × 1254 px**. This exactly matches the input cave's dimensions and square framing.
- Preview: `dist/line-2/01.jpg`, JPEG, RGB, **512 × 512 px**, 76,192 bytes.
- Record: `dist/line-2/01.json`; number 1, Cave Ice, Wall Line 2. Its image URL uses the SHA-256 of the finished PNG bytes.
- PNG SHA-256: `91b60180e3c0eae1151aee315645029dda7504a806897e355b083e1df631cae8`.

## Chosen review step

Visually inspected the cave input and both generated renders. The first render's upper hand appeared to have four digits, so a targeted second edit added its missing thumb. Counted the final upper hand as four upward/rightward fingers plus one downward thumb, and the lower hand as four fingers plus one thumb: five each. There are no hand stencils. The finished figure has Pepe's wide mouth and large heavy-lidded eyes. Four white pebble circles in each row pair up; the bottom row has one additional red pebble.

The final image retains the input's ceiling, floor, major cracks, warm illumination and square framing. The new marks use charcoal, red/yellow ochre and chalk-like white, with stone texture visible through them. No letters, numbers, captions, signatures, logos, watermark, border, political or hateful symbols, or real people were observed. This was the first Pepe on this wall, so no ancestral marks were present to preserve.

Unmet visual requirements: **none observed on review**. Limitation: a generative edit preserves the cave visually, but does not guarantee pixel-identical geology or lighting outside the painted area. Review is a human-style visual assessment, not an automated guarantee of artistic quality. PNG/JPEG headers, dimensions, record shape, digest, and file size were checked separately with code.

## Generation provenance and prompt

Used the built-in `image_gen.imagegen` tool in edit mode, with `artifacts/ice/cave.png` as the initial edit target and the first result as the correction target. The image tool's generated PNG was copied into the declared wall path. A temporary Pillow checker in disposable `test/scratch/` converted the final wall to the required JPEG preview; it is not a dependency of any delivered code.

Initial prompt: preserve the exact square cave framing, warm rock, cracks, torchlight, ceiling, floor and shadows; add only a worn prehistoric pigment drawing of recognizable Pepe squatting beside two rows of four paired white pebbles with one extra red pebble in the bottom row. Give him a wide mouth, heavy-lidded eyes, and two open five-digit hands; use charcoal, red/yellow ochre and chalk white only, with no writing, logos, frames, or modern rendering.

Final correction prompt: keep the entire cave, Pepe, pebbles and lower hand unchanged; correct only the upper hand by adding one short downward thumb to the four existing upward/rightward fingers. Exactly five separated digits, primitive worn red-ochre/charcoal pigment; no other changes or text.

## Pepe 22 output review

- Wall: `artifacts/line-2/wall.png` and required `artifacts/line-2/wall-v2.png`; both are PNG, RGB, **1254 × 1254 px**. Their SHA-256 is `b267e67040355641a9dfa0b41c55d96330ad5e237e5dea8b966345fffc58ae40`.
- Preview: `dist/line-2/22.jpg`, JPEG, RGB, **512 × 512 px**, under 100 KB.
- Record: `dist/line-2/22.json`; number 22, Cave Ice, Wall Line 2. Its image URL contains the SHA-256 of the finished wall.
- Parent wall: the exact PNG bytes linked by Pepe 01's record were restored before compositing. The new transparent motif was resized and overlaid in the upper-right open rock. The previous painting and all pixels outside the new motif remain unchanged.

Visually inspected the final wall and its JPEG preview. The new smaller figure reads as Pepe through its wide mouth and heavy-lidded eyes. Its raised open hand has four separated fingers and one thumb. The rows of ochre/white/dark pebbles include one pebble set aside. The earlier large figure and its pebble rows remain in place. Rock, framing, cracks, warm cave light, and foreground are preserved. No letters, numbers, captions, logos, watermarks, borders, political/hateful symbols, or real people were observed.

Unmet visual requirements: **none observed**. Visual inspection is not an automated guarantee. The added motif is a composited transparent image, so its pigment texture is generated rather than physically painted into the source photograph. PNG/JPEG headers, dimensions, SHA-256, JSON shape, and file sizes were separately checked.

Pepe 22 used the built-in image-generation tool to create a transparent cave-painting motif, then composited it over the exact prior PNG. The resulting wall was resized to a 512 px JPEG preview. CSV Reconcile added a `--format text` mode; all 17 standard-library tests passed, and the README command produced the documented synthetic inventory report with the expected difference exit status 1.
