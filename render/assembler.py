"""Final video assembly (PRD v1.2 §7.9).

moviepy (or raw ffmpeg) composes canvas frames + stickman clips + audio.
1920x1080, H.264 MP4, AAC audio. Slide duration is always derived from
the real TTS audio length (avoid sync drift, PRD §11).
"""

# TODO: implement assemble(slides, frames, audios) -> output/final.mp4
