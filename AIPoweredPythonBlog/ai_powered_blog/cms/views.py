from django.http import HttpResponse
from django.views.decorators.cache import cache_page

from .plantuml import get_plantuml_svg_or_error


@cache_page(60 * 60)
def plantuml_svg(request, diagram_id: str):
    svg, status_code = get_plantuml_svg_or_error(diagram_id)

    response = HttpResponse(
        svg,
        content_type="image/svg+xml; charset=utf-8",
        status=status_code,
    )
    response["Cache-Control"] = "public, max-age=3600"
    response["X-Content-Type-Options"] = "nosniff"
    return response
