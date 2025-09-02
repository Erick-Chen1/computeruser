"""Load configuration from a .env file."""
from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
VLM_MODEL = os.getenv("VLM_MODEL", "gpt-4o-mini")
