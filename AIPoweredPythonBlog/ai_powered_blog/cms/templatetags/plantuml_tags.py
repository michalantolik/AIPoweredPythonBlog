from django import template
from django.urls import reverse

from cms.plantuml import normalize_plantuml_source, plantuml_encode

register = template.Library()


@register.simple_tag
def plantuml_svg_url(source: str):
    normalized = normalize_plantuml_source(source)

    if not normalized:
        return ""

    diagram_id = plantuml_encode(normalized)
    return reverse("cms:plantuml_svg", kwargs={"diagram_id": diagram_id})
