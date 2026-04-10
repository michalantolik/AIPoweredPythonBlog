from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


WIDTH_CHOICES = [
    ("narrow", "Narrow"),
    ("content", "Content width"),
    ("wide", "Wide"),
    ("full", "Full width"),
]

ALIGN_CHOICES = [
    ("left", "Left"),
    ("center", "Center"),
    ("right", "Right"),
]


class SectionHeadingBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(required=False, max_length=60)
    title = blocks.CharBlock(required=True, max_length=120)

    class Meta:
        icon = "title"
        label = "Section heading"
        template = "cms/blocks/section_heading.html"


class RichSectionBlock(blocks.RichTextBlock):
    class Meta:
        icon = "doc-full"
        label = "Rich text"
        template = "cms/blocks/rich_section.html"


class CalloutBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, max_length=120)
    text = blocks.TextBlock(required=True)
    tone = blocks.ChoiceBlock(
        choices=[
            ("info", "Info"),
            ("success", "Success"),
            ("warning", "Warning"),
            ("danger", "Danger"),
        ],
        default="info",
    )

    class Meta:
        icon = "warning"
        label = "Callout"
        template = "cms/blocks/callout.html"


class CodeBlock(blocks.StructBlock):
    caption = blocks.CharBlock(required=False, max_length=120)
    language = blocks.ChoiceBlock(
        choices=[
            ("python", "Python"),
            ("django", "Django / HTML+Django"),
            ("csharp", "C#"),
            ("javascript", "JavaScript"),
            ("typescript", "TypeScript"),
            ("json", "JSON"),
            ("yaml", "YAML"),
            ("bash", "Bash"),
            ("sql", "SQL"),
            ("docker", "Dockerfile"),
            ("xml", "XML"),
            ("text", "Plain text"),
        ],
        default="python",
    )
    code = blocks.TextBlock(required=True)
    show_line_numbers = blocks.BooleanBlock(required=False, default=True)
    width = blocks.ChoiceBlock(choices=WIDTH_CHOICES, default="content")

    class Meta:
        icon = "code"
        label = "Code"
        template = "cms/blocks/code.html"


class MermaidBlock(blocks.StructBlock):
    caption = blocks.CharBlock(required=False, max_length=120)
    diagram = blocks.TextBlock(required=True)
    width = blocks.ChoiceBlock(choices=WIDTH_CHOICES, default="wide")

    class Meta:
        icon = "site"
        label = "Mermaid diagram"
        template = "cms/blocks/mermaid.html"


class PlantUMLBlock(blocks.StructBlock):
    caption = blocks.CharBlock(required=False, max_length=120)
    source = blocks.TextBlock(required=True)
    width = blocks.ChoiceBlock(choices=WIDTH_CHOICES, default="wide")

    class Meta:
        icon = "diagram"
        label = "PlantUML diagram"
        template = "cms/blocks/plantuml.html"


class FigureBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    caption = blocks.CharBlock(required=False, max_length=180)
    alt_text = blocks.CharBlock(required=False, max_length=180)
    alignment = blocks.ChoiceBlock(choices=ALIGN_CHOICES, default="center")
    width = blocks.ChoiceBlock(choices=WIDTH_CHOICES, default="wide")

    class Meta:
        icon = "image"
        label = "Image"
        template = "cms/blocks/figure.html"
