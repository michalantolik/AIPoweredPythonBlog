from __future__ import annotations

import hashlib
import urllib.error
import urllib.request
import zlib

from django.conf import settings
from django.core.cache import cache
from django.utils.html import escape
from django.utils.safestring import mark_safe

_PLANTUML_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"


def _encode_6bit(value: int) -> str:
    return _PLANTUML_ALPHABET[value & 0x3F]


def _append_3bytes(b1: int, b2: int, b3: int) -> str:
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    return "".join(_encode_6bit(part) for part in (c1, c2, c3, c4))


def plantuml_encode(source: str) -> str:
    raw = source.encode("utf-8")
    compressed = zlib.compress(raw)
    # PlantUML expects raw DEFLATE bytes (zlib header and checksum removed).
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


def build_plantuml_url(source: str, output_format: str = "svg") -> str:
    base_url = getattr(
        settings,
        "PLANTUML_SERVER_URL",
        "https://www.plantuml.com/plantuml",
    ).rstrip("/")
    encoded = plantuml_encode(source)
    return f"{base_url}/{output_format}/{encoded}"


def render_plantuml_svg(source: str) -> str:
    normalized_source = (source or "").strip()

    if not normalized_source:
        return ""

    cache_timeout = getattr(settings, "PLANTUML_CACHE_TIMEOUT_SECONDS", 3600)
    cache_key = (
        "plantuml-svg:"
        + hashlib.sha256(normalized_source.encode("utf-8")).hexdigest()
    )
    cached_svg = cache.get(cache_key)

    if cached_svg:
        return cached_svg

    request = urllib.request.Request(
        build_plantuml_url(normalized_source, output_format="svg"),
        headers={"User-Agent": "ai-powered-python-blog/plantuml-renderer"},
    )

    timeout = getattr(settings, "PLANTUML_RENDER_TIMEOUT_SECONDS", 10)

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            content_type = response.headers.get("Content-Type", "")
            svg = response.read().decode("utf-8")

            if "svg" not in content_type.lower() and "<svg" not in svg:
                raise ValueError("PlantUML renderer did not return SVG content.")

            cache.set(cache_key, svg, cache_timeout)
            return svg
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        escaped_error = escape(str(exc))
        fallback_source = escape(normalized_source)
        return mark_safe(
            "<div class=\"article-plantuml__error\">"
            "<strong>PlantUML diagram could not be rendered.</strong>"
            f"<div class=\"article-plantuml__error-message\">{escaped_error}</div>"
            "<pre class=\"article-plantuml__fallback-source\">"
            f"{fallback_source}"
            "</pre>"
            "</div>"
        )
