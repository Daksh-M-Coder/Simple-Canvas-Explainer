"""TTS engine (PRD v1.2 §7.7).

Free, open-source, human-like. Target: mimic the famous paint-explainer TTS.
Candidates: Piper (offline, default), edge-tts (free cloud fallback),
Coqui TTS (offline, heavy). Open item #1 (PRD §9): spike before committing.

Per-slide audio; duration measured via ffprobe -> slide length.
"""

# TODO: implement synthesize(text, out_path) -> wav/mp3 path
#       and get_duration(audio_path) -> float via ffprobe.
