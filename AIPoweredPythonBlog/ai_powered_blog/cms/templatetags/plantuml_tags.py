from django import template
from django.utils.safestring import mark_safe

from cms.plantuml import render_plantuml_svg

register = template.Library()


@register.simple_tag
def render_plantuml(source: str):
    return mark_safe(render_plantuml_svg(source))
