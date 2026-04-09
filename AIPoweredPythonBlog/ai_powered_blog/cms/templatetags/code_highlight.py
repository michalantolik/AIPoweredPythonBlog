from django import template
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name
from pygments.util import ClassNotFound

register = template.Library()


@register.simple_tag
def render_highlighted_code(code: str, language: str = "text", linenos: bool = True):
    try:
        lexer = get_lexer_by_name(language)
    except ClassNotFound:
        lexer = TextLexer()

    formatter = HtmlFormatter(
        cssclass="codehilite",
        linenos="table" if linenos else False,
    )
    return mark_safe(highlight(code, lexer, formatter))
