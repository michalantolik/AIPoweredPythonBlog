from __future__ import annotations

import hashlib
import urllib.error
import urllib.request
import zlib
from xml.sax.saxutils import escape

from django.conf import settings
from django.core.cache import cache

_PLANTUML_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"


PLANTUML_BACKGROUND_COLOR = "#E4EAF4"


def normalize_plantuml_source(source: str) -> str:
    normalized = (source or "").strip()

    if not normalized:
        return ""

    # Ensure @startuml / @enduml
    if "@startuml" not in normalized:
        normalized = f"@startuml\n{normalized}\n@enduml"

    # Inject background color if not already set
    if "skinparam backgroundColor" not in normalized:
        normalized = normalized.replace(
            "@startuml",
            f"@startuml\nskinparam backgroundColor {PLANTUML_BACKGROUND_COLOR}",
            1,
        )

    return normalized


def _encode_6bit(value: int) -> str:
    return _PLANTUML_ALPHABET[value & 0x3F]


def _append_3bytes(b1: int, b2: int, b3: int) -> str:
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    return "".join(_encode_6bit(part) for part in (c1, c2, c3, c4))


def plantuml_encode(source: str) -> str:
    normalized = normalize_plantuml_source(source)
    raw = normalized.encode("utf-8")
    compressed = zlib.compress(raw)
    compressed = compressed[2:-4]

    encoded_parts: list[str] = []
    for index in range(0, len(compressed), 3):
        chunk = compressed[index : index + 3]
        if len(chunk) == 3:
            encoded_parts.append(_append_3bytes(chunk[0], chunk[1], chunk[2]))
        elif len(chunk) == 2:
            encoded_parts.append(_append_3bytes(chunk[0], chunk[1], 0))
        else:
            encoded_parts.append(_append_3bytes(chunk[0], 0, 0))

    return "".join(encoded_parts)


def build_plantuml_remote_url(encoded_diagram: str, output_format: str = "svg") -> str:
    base_url = getattr(
        settings,
        "PLANTUML_SERVER_URL",
        "https://www.plantuml.com/plantuml",
    ).rstrip("/")
    return f"{base_url}/{output_format}/{encoded_diagram}"


def fetch_plantuml_svg(encoded_diagram: str) -> str:
    cache_timeout = getattr(settings, "PLANTUML_CACHE_TIMEOUT_SECONDS", 3600)
    cache_key = f"plantuml-svg:{hashlib.sha256(encoded_diagram.encode('utf-8')).hexdigest()}"
    cached_svg = cache.get(cache_key)

    if cached_svg:
        return cached_svg

    request = urllib.request.Request(
        build_plantuml_remote_url(encoded_diagram, output_format="svg"),
        headers={"User-Agent": "ai-powered-python-blog/plantuml-proxy"},
    )

    timeout = getattr(settings, "PLANTUML_RENDER_TIMEOUT_SECONDS", 10)

    with urllib.request.urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("Content-Type", "")
        svg = response.read().decode("utf-8")

        if "svg" not in content_type.lower() and "<svg" not in svg:
            raise ValueError("PlantUML server did not return valid SVG.")

        cache.set(cache_key, svg, cache_timeout)
        return svg


def build_error_svg(message: str) -> str:
    safe_message = escape(message)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="220" viewBox="0 0 900 220" role="img" aria-label="PlantUML rendering error">
  <rect width="900" height="220" rx="16" fill="#fff7f7" stroke="#fca5a5" stroke-width="2" />
  <text x="32" y="60" font-size="24" font-family="Arial, Helvetica, sans-serif" font-weight="700" fill="#991b1b">
    PlantUML diagram could not be rendered
  </text>
  <text x="32" y="102" font-size="18" font-family="Arial, Helvetica, sans-serif" fill="#7f1d1d">
    {safe_message}
  </text>
  <text x="32" y="150" font-size="16" font-family="Arial, Helvetica, sans-serif" fill="#7f1d1d">
    Check PlantUML syntax or server availability.
  </text>
</svg>"""


def get_plantuml_svg_or_error(encoded_diagram: str) -> tuple[str, int]:
    if not encoded_diagram:
        return build_error_svg("Empty PlantUML diagram."), 400

    try:
        return fetch_plantuml_svg(encoded_diagram), 200
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return build_error_svg(str(exc)), 503
