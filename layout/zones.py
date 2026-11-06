"""Named 3x3 layout zones for the 1920x1080 canvas (PRD v1.2 §7.2).

Zones:
    top_left     top_center     top_right
    mid_left     center         mid_right
    bottom_left  bottom_center  bottom_right
"""

# TODO: implement Zone enum / dataclass and zone_name -> (x, y, w, h) rect
# mapping computed from config.CANVAS_WIDTH / CANVAS_HEIGHT.
