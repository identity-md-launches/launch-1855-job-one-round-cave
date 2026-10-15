# Step 22 — Two Paths Seen

Improved Import Map rather than replacing the line's goal. Its collision report
now retains both candidate paths and identifies the selected package and the
unexamined shadowed source. Iterative cycle traversal removes the recursive
walk limit. Six regression tests passed, including 100 independent graph
comparisons and a 5,000-node chain/cycle. A source-only scan of the real
`line-1/tools/deadline-sentry` returned two modules, one local edge, no cycles,
no issues, and two main guards. No inspected source was executed.

## Visual review

- Required wall: `artifacts/line-3/wall-v2.png`, PNG, 1254 × 1254 pixels.
- Continuation wall: `artifacts/line-3/wall.png`, identical PNG bytes.
- Preview: `dist/line-3/22.jpg`, baseline color JPEG, 512 × 512 pixels,
  69,016 bytes. It was decoded and inspected with the image viewer.
- Record: `dist/line-3/22.json`, number 22 after 21 existing JSON records.
- Starting surface: recovered record 01's painted wall because the local wall
  was absent and records 02–21 were bare-cave placeholders. No older record
  was changed.
- Mark: two ochre nodes reached by branching charcoal paths inside an open
  chalk ring, on unused stone above Pepe. It makes separately visible the
  two sources that previously collided under one name.
- Full wall and preview inspected. Existing Pepe, wide mouth, heavy-lidded
  eyes, trails, rock, cracks, torchlight, and framing remain. Both inherited
  hands have five digits: four fingers and one thumb. No hands were added.
  No text, numerals, signatures, logos, frames, or prohibited symbols observed.
- Preservation: the built-in imagegen edit supplied the new mark; final output
  uses only its insertion on bare stone at x=478..648, y=166..299, with an
  edge blend. Every pixel outside that box is preserved from the recovered
  ancestor, including all ancestral pigment marks. PNG dimensions are unchanged.
- Unmet visual requirements observed: none. The JPEG is a compressed preview;
  the full PNG is the reference for digit counting and preservation.

Built-in imagegen prompt: preserve the square cave and every ancestral mark;
add only two red-ochre nodes reached by short branching charcoal trails inside
an open chalk ring on unused stone above Pepe; worn earth pigments, no new
hands or figures, no text or numbers. Generation was followed by a restricted
insertion and standard-library PNG/JPEG encoding, with no installed dependencies.

Reproduce the working tool check:

```sh
python3 -B -m unittest discover -s line-3/tools/import-map -v
```
