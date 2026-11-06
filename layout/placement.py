"""Zone placement + opposite-zone enforcement (PRD v1.2 §7.3).

Rules:
- Text sits opposite the stickman (left<->right, top<->bottom, center->bottom_center).
- Validator enforces; auto-corrects violations to the opposite zone
  (mapping lives in schema/allowlists.json -> "opposite_zone").
- Max text width: 50% canvas (side zones), 80% (top/bottom zones).
"""

# TODO: implement resolve_text_zone(stickman_zone, text_zone) -> str
#       and compute_text_bounds(zone) -> (x, y, w, h) honoring width caps.
