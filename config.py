"""Global configuration for Simple Canvas Explainer (PRD v1.2 §6, §8)."""

from pathlib import Path

# --- Paths ---------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent
SCHEMA_DIR = ROOT_DIR / "schema"
ASSETS_DIR = ROOT_DIR / "assets"
STICKMAN_DIR = ASSETS_DIR / "stickman"
FONTS_DIR = ASSETS_DIR / "fonts"
OUTPUT_DIR = ROOT_DIR / "output"
LLM_DIR = ROOT_DIR / "llm"

STICKMAN_MAP_PATH = STICKMAN_DIR / "stickman_map.json"
SLIDE_SCHEMA_PATH = SCHEMA_DIR / "slide_schema.json"
ALLOWLISTS_PATH = SCHEMA_DIR / "allowlists.json"
SYSTEM_PROMPT_PATH = LLM_DIR / "system_prompt.txt"

# --- Output / canvas -----------------------------------------------------
CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 1080
FPS = 30

# --- LLM (NVIDIA NIM) ----------------------------------------------------
# Secrets are read from the environment; never hardcode API keys.
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
NVIDIA_API_KEY_ENV = "NVIDIA_API_KEY"
# Open item #2 in PRD §9: confirm model with good guided_json support.
LLM_MODEL = "meta-llama/llama-3.1-70b-instruct"
LLM_TEMPERATURE = 0.4
LLM_MAX_TOKENS = 4096

# --- Slides --------------------------------------------------------------
MIN_SLIDES = 5
MAX_SLIDES = 10

# --- TTS -----------------------------------------------------------------
# Open item #1 in PRD §9: spike Piper vs edge-tts vs Coqui.
TTS_ENGINE = "piper"

# --- Render --------------------------------------------------------------
BACKGROUND_COLOR = (255, 255, 255)  # strict white canvas
BRUSH_FONTS = ("PermanentMarker-Regular.ttf", "CaveatBrush-Regular.ttf", "RockSalt-Regular.ttf")
DEFAULT_TEXT_STYLE = "brush"
