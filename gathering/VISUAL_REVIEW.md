# Gathering 22 — visual review

Outputs: artifacts/gathering/wall-v2.png and artifacts/gathering/wall.png,
identical PNG bytes, 1254 × 1254 pixels, square, 2,757,208 bytes each.
SHA-256: 65e91dff9ef29883ebf782e39704783e3bd99e12d01cb54cb7bdf3f8324d25af.
Thumbnail: dist/gathering/22.jpg, JPEG, 512 × 512 pixels, 56,966 bytes.
Record: dist/gathering/22.json, linking to the actual final PNG hash.

The edit target was the existing gathering wall from painted record 01,
retrieved from its artifact URL and verified as SHA-256
 d17d8d3d59ef990bdad49361e39324734395a0017040d513c3128b26f4b05d03.
The later records 02–21 are unpainted placeholders, so none replaced the ancestor.
The existing line paintings were not edited. Record 22 follows the already
reserved numbers and the four current line records, also numbered 22.

Chosen review: view the ancestor and completed whole wall, compare composition,
look for changed ancestral marks, count every visible hand, and check prohibited
content before accepting. Both images were opened with the image inspection
tool. The rock, warm torchlight, left crack, icicles, floor, dark edges, square
framing, large Pepe, four pigment trails and loop remain visibly aligned.
The only intended addition is a small reed bridge with pebble clusters and
chalk/ochre tracks in the previously empty rock below the ancestral painting.
Its strokes are flat and uneven with stone showing through.

The main figure is the ancestral Pepe: broad mouth and heavy-lidded eyes.
Counted both visible hands: the upper hand has four fingers and one thumb;
the lower hand has four fingers and one thumb. No new hands or handprints were
added. No letters, numbers, captions, signatures, logos, watermarks, frames,
real people, political symbols, or hateful symbols were observed. The new mark
is an earth-pigment drawing, not a photographed or three-dimensional object.

Unmet visual requirements observed: none at the composition/visual inspection
level. Preservation limitation: this is a generative edit, not a pixel-identical
background operation. Outside a conservative new-mark review rectangle
(x 470–1000, y 800–1030), mean absolute RGB channel difference from the ancestor
is 4.4084 on a 0–255 scale; 13.8% of channels differ by more than 8. Therefore
exact background-pixel preservation is not claimed. No ancestral figure or mark
was observed erased, relocated, or intentionally redrawn. Human review may
judge pigment fidelity or preservation more strictly than this inspection.

The installed built-in imagegen tool produced the painting. Its returned image
bytes were saved directly to the required workspace output. The existing
ffmpeg executable made only the requested JPEG and in-memory gallery previews;
no additional picture files or installed dependencies were added. The gallery
works without ffmpeg or network for its embedded previews. The PNG is not a
placeholder, prompt, or URL-only deliverable.

Final prompt used with the built-in tool:

Use case: precise-object-edit. Edit target: the supplied ancestral Ice gathering cave wall at artifacts/gathering/wall.png, exactly 1254 by 1254 pixels. Preserve the entire existing image: same square dimensions, rock grain, cracks, warm torchlight, dark edges, icicles, floor, framing, and especially the ancestral large Pepe frog and all four pigment trails and woven loop. Do not erase, move, redraw, sharpen, clean up or change any existing mark. Add ONLY a modest prehistoric pigment mark in the empty lower central rock below the existing frog and loop, approximately x=480..990 y=840..1020. The new mark is a small uneven reed bridge connecting two clusters of four rough pebbles, with a thin chalk track crossing it and four tiny red/yellow ochre dots near its foot, symbolizing tested tools crossing between four workers. Keep it entirely flat handmade earth pigment, worn charcoal strokes, red and yellow ochre, chalk white, bare stone showing through, like Lascaux or Chauvet. The existing Pepe remains the main figure, unmistakable wide mouth and heavy-lidded eyes. Do not add any extra frog, people, hands or handprints; preserve both existing hands with their five digits each. No letters, numbers, captions, signatures, logos, watermarks, borders, frames, political or hateful symbols. Do not make a photographic or 3D bridge; it is a sparse cave drawing on the wall. Keep everything outside the new modest lower-center mark unchanged. Deliver the complete square wall, not a cropped detail.
