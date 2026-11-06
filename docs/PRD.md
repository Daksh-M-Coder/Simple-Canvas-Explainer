# PRD — Paint Explainer Video Generator (v1.2)

> Repo note: project is set up under the name **simple-canvas-explainer** (formerly "paint-explainer").

## 1. Overview
An automated Python pipeline that takes a topic → generates a scene-by-scene script via an offline LLM (NVIDIA API) with **grammar-constrained JSON output** → composes simple "paint-style" explainer frames (white canvas, stickman actions in engineered layout zones, brush-paint text with basic rich formatting) → adds free TTS voiceover → exports a 16:9 MP4.

## 2. Problem
Simple white-canvas explainer videos (stickman + side text + narration) are effective but slow to produce by hand. Automate the whole pipeline, with **strict separation between what appears on screen and what is spoken**.

## 3. Goals
- Input: a topic/question.
- Output: finished 16:9 MP4 explainer with visuals + brush-paint text + TTS audio.
- Fully automated, minimal manual editing.
- **LLM output forced into valid JSON via grammar constraints** (no parse-retry loop needed).
- **Slide content and slide speech are separate fields** — screen text is concise/stats-driven (≤80% overlap with narration), narration is conversational.

## 4. Non-Goals (v1)
- No image sourcing (deferred to v2 — only if a free stock API exists).
- No 9:16 shorts.
- No manual timeline editor.
- No multi-language / lip-sync.

## 5. Pipeline

```
1. INPUT          User gives topic/question
        ▼
2. SCRIPT GEN     NVIDIA API + guided_json (JSON Schema constraint)
                  → guaranteed-valid JSON: slides[] with
                    { narration, on_screen_text,
                      stickman_tag, stickman_zone, text_zone,
                      text_style, image_query }
        ▼
3. VALIDATE       Schema check (redundant safety) + tag/zone allow-lists
        ▼
4. ASSET PICK     stickman_tag → clip via stickman_map.json
        ▼
5. FRAME BUILD    White canvas → stickman in stickman_zone,
                  rich brush-paint text in text_zone
        ▼
6. TTS            Free open-source TTS: narration → audio per slide
                  audio duration → slide duration
        ▼
7. ASSEMBLY       Stitch slides, sync audio, export MP4 (moviepy/ffmpeg)
        ▼
8. OUTPUT         final.mp4 (16:9)
```

## 6. Decisions Locked

| Item | Decision |
|---|---|
| Language | Python |
| LLM JSON enforcement | **NVIDIA NIM `guided_json`** (xgrammar backend) — grammar-constrained output |
| Stickman source | Pre-made clip library, mapped via `stickman_map.json` with tags |
| Stickman placement | Zone-based layout system (§7.2) |
| Text placement | Zone-based, opposite the stickman (§7.3) |
| Text formatting | Rich markup: bold, italic, bullets, numbered lists, strikethrough, highlight (§7.4) |
| **Content vs. Speech** | **Separated fields**; screen text ≤80% overlap with narration, concise/stats-driven (§7.5) |
| TTS | Free, open-source, human-like; target = mimic famous paint-explainer TTS |
| Visual style | Strict paint look; brush-paint text |
| Images | Deferred to v2 |
| v1 scope | Text + stickman + TTS only |
| Aspect ratio | 16:9 (1920×1080) |

## 7. Component Specs

### 7.1 `stickman_map.json`
Maps stickman clip files → semantic tags → usage context.
```json
{
  "clips": [
    {
      "file": "stickman_explain.mp4",
      "tags": ["explaining", "teaching", "pointing"],
      "use_when": ["after_topic_intro", "mid_explanation"],
      "description": "stickman with pointer, used for explaining"
    }
  ]
}
```
Validator rejects unknown tags before rendering.

### 7.2 Stickman Layout Zones
Screen divided into named zones. **One stickman per slide** (v1).

```
┌─────────────────────────────────────────────┐
│  TOP_LEFT          TOP_CENTER     TOP_RIGHT │
│  MID_LEFT          CENTER         MID_RIGHT │
│  BOTTOM_LEFT       BOTTOM_CENTER  BOTTOM_RIGHT │
└─────────────────────────────────────────────┘
```
- Clip scaled to fit its zone (max ~40% screen width in side zones).

### 7.3 Text Zone Rules
- Text sits **opposite the stickman** (left↔right, top↔bottom, center→bottom-center).
- Validator enforces; auto-corrects violations to opposite zone.
- Max width: 50% canvas (side), 80% (top/bottom).

### 7.4 Rich Text Formatting
`on_screen_text` supports brush-rendered markup:

| Feature | Markup | Render |
|---|---|---|
| Bold | `**text**` | Thicker brush stroke |
| Italic | `*text*` | Slanted brush |
| Bullets | lines starting `- ` | Brush dot + indent |
| Numbered list | lines starting `1. ` | Brush numeral + text |
| Strikethrough | `~~text~~` | Brush strike line |
| Highlight | `==text==` | Translucent marker band |

Fonts: OFL brush set ("Permanent Marker", "Caveat Brush", "Rock Salt"). Per-glyph jitter (±2° rotation, ±1px position).

### 7.5 Content vs. Speech Separation (NEW RULE)
**Two separate fields per slide, two different jobs:**

| Field | Job | Style |
|---|---|---|
| `narration` | What the TTS **speaks** | Conversational, full sentences, 2–4 sentences per slide |
| `on_screen_text` | What appears **on canvas** | Concise, stats-driven, bullet-friendly, ≤80% overlap with narration |

**The 80% rule:** at least 80% of the key information spoken in `narration` must appear (in condensed form) in `on_screen_text`. This prevents the screen from becoming a redundant transcript while ensuring the visuals carry the core message.

**LLM system prompt instructs:**
- `narration`: explain the idea like a teacher talking to a student.
- `on_screen_text`: distil the same idea into the fewest words/stats possible — bullets, key terms, numbers, highlights.
- Do **not** copy narration verbatim into on_screen_text; compress and structure it.

### 7.6 LLM System Prompt + Grammar Enforcement

**Grammar enforcement (NVIDIA NIM):**
- Use `guided_json` parameter (recommended over `response_format: json_object`) — xgrammar backend constrains generation to the schema.
- The schema is **not** injected into the prompt automatically — the system prompt must still describe the expected structure.
- This eliminates malformed JSON entirely; downstream only needs semantic validation (tags, zones).

**Schema:**
```json
{
  "title": "...",
  "slides": [
    {
      "id": 1,
      "narration": "Full conversational explanation (2-4 sentences).",
      "on_screen_text": "- **Key point**\n- ==highlighted== stat\n- ~~wrong idea~~",
      "stickman_tag": "explaining",
      "stickman_zone": "mid_left",
      "text_zone": "mid_right",
      "text_style": "brush",
      "image_query": null
    }
  ]
}
```

**System prompt constraints:**
- 5–10 slides; first = intro, last = conclusion.
- `stickman_tag` from allow-list (injected into prompt text).
- `stickman_zone` / `text_zone` from allow-list; `text_zone` must be opposite `stickman_zone`.
- `narration` ≠ `on_screen_text` — separate jobs, ≤80% overlap rule.
- `on_screen_text` uses allowed markup only.

### 7.7 TTS
- Free, open-source, human-like. Candidates: **Piper** (offline, default), `edge-tts` (free cloud fallback), Coqui TTS (offline, heavy).
- Per-slide audio; duration via `ffprobe` → slide length.

### 7.8 Brush-Paint Text Renderer
- Renders rich markup runs (§7.4) using brush fonts + highlighter bands.
- Zone-aware wrapping and scaling.
- Slight stroke jitter for hand-painted feel (tunable).

### 7.9 Assembly
- `moviepy` (or raw `ffmpeg`) composes canvas frames + stickman clips + audio.
- 1920×1080, H.264 MP4, AAC audio.

## 8. Repo Layout (proposed)
```
simple-canvas-explainer/
├── main.py
├── config.py
├── llm/
│   ├── client.py              # NVIDIA NIM call with guided_json
│   └── system_prompt.txt
├── schema/
│   ├── slide_schema.json      # JSON Schema (for guided_json + validation)
│   └── allowlists.json        # tags, zones, text_styles
├── layout/
│   ├── zones.py
│   └── placement.py
├── assets/
│   ├── stickman/
│   │   ├── stickman_map.json
│   │   └── *.mp4
│   └── fonts/
├── render/
│   ├── canvas.py
│   ├── rich_text.py
│   ├── stickman.py
│   └── assembler.py
├── tts/
│   └── engine.py
└── output/
    └── final.mp4
```

## 9. Open Items (resolve during build)
1. **TTS engine final pick** — spike Piper vs edge-tts vs Coqui.
2. **NVIDIA model choice** — confirm which model supports `guided_json` well; pick one.
3. **Brush font bundle** — finalize 2–3 OFL brush fonts.
4. **Free stock image API** — check once; images stay v2 if none clean.
5. **Slide count control** — fixed range (5–10) vs user-specified.
6. **Highlighter color palette** — pick 3–4 default colors.
7. **80% overlap measurement** — how to verify at validation time (manual prompt instruction vs automated check). Recommend: prompt instruction only for v1; automated check deferred.

## 10. Success Criteria (v1)
- Given a topic, produces valid MP4 without manual steps.
- **LLM output is always valid JSON** (grammar-enforced); zero parse failures.
- Every slide: valid tag + zone, text zone opposite stickman, narration and on_screen_text distinct with ≤80% overlap.
- Output recognizable as a paint explainer.

## 11. Risks
- **Grammar feature limitations** — `guided_json` supports a subset of JSON Schema; keep schema simple (no `anyOf`/`oneOf` mixing, no nested `$ref`).
- **LLM still ignores structure hints** — grammar enforces JSON shape but not semantic correctness; system prompt must clearly describe allow-lists and the 80% rule.
- **Stickman style mismatch** — clips must share consistent art style.
- **Brush-paint authenticity** — tune jitter.
- **TTS naturalness** — spike before committing.
- **Sync drift** — always derive slide duration from real audio length.
