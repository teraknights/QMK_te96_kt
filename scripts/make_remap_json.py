#!/usr/bin/env python3
"""Generate the Remap/VIA definition for the custom te96 (rev1_inverted) layout.

Physical positions measured from photos (1 = one key pitch); matrix positions
confirmed with the mapcheck firmware (2026-09-27).
"""
import json, sys
from itertools import groupby

keys = []  # (x, y, "row,col")

# ---- Left half: columns outer -> inner, x = 0..6
L_TOP = [1.0, 1.0, 0.25, 0.0, 0.25, 0.5]           # top offset of alpha columns 1..6
L_THUMB = [None, 4.0, 3.25, 3.0, 3.25, 3.5]        # thumb-row y per alpha column
L_THUMB_COL = [None, 4, 3, 2, 1, 0]                 # matrix col of thumb key (row 2)
for i in range(6):
    mcol = 5 - i
    for k, mrow in enumerate((5, 4, 3)):
        keys.append((i, L_TOP[i] + k, f"{mrow},{mcol}"))
    if L_THUMB[i] is not None:
        keys.append((i, L_THUMB[i], f"2,{L_THUMB_COL[i]}"))
keys.append((6, 3.5, "2,6"))                        # innermost thumb key

# ---- Right half: columns inner -> outer
RX = 8.0
keys.append((RX, 3.5, "9,6"))                       # innermost thumb key
R_TOP = [0.5, 0.25, 0.0, 0.25, 0.75]                # alpha columns 2..6 (matrix col 0..4)
R_THUMB = [3.5, 3.25, 3.0, 3.25, 3.75]
for j in range(5):
    x = RX + 1 + j
    for k, mrow in enumerate((6, 7, 8)):
        keys.append((x, R_TOP[j] + k, f"{mrow},{j}"))
    keys.append((x, R_THUMB[j], f"9,{j}"))

# ---- Serialize as KLE rows (each row: keys sharing the same y)
rows, cur_y = [], None
for y, grp in groupby(sorted(keys, key=lambda k: (k[1], k[0])), key=lambda k: k[1]):
    row_start = 0.0 if cur_y is None else cur_y + 1
    row, x_cursor = [], 0.0
    for idx, (x, _, label) in enumerate(grp):
        props = {}
        if idx == 0 and y != row_start:
            props["y"] = y - row_start
        if x != x_cursor:
            props["x"] = x - x_cursor
        if props:
            row.append(props)
        row.append(label)
        x_cursor = x + 1
    rows.append(row)
    cur_y = y

definition = {
    "name": "te96 custom",
    "vendorId": "0x1209",
    "productId": "0x7E96",
    "lighting": "qmk_rgblight",
    "matrix": {"rows": 12, "cols": 8},
    "layouts": {"keymap": rows},
}
out = sys.argv[1] if len(sys.argv) > 1 else "remap/te96_custom.json"
with open(out, "w") as f:
    json.dump(definition, f, indent=1)
print(f"{len(keys)} keys -> {out}")
