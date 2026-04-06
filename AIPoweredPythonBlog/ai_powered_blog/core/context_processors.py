from django.conf import settings
from django.templatetags.static import static


def _resolve_intro_image_url(image_value: str) -> str:
    if not image_value:
        return static('images/intro/michal-portrait.png')

    if image_value.startswith(('http://', 'https://', '/')):
        return image_value

    return static(image_value)


def site_ui_settings(request):
    intro_overlay_image = getattr(
        settings,
        'INTRO_OVERLAY_IMAGE',
        'images/intro/michal-portrait.png'
    )

    return {
        'INTRO_OVERLAY_ENABLED': getattr(settings, 'INTRO_OVERLAY_ENABLED', False),
        'INTRO_OVERLAY_DURATION_MS': getattr(settings, 'INTRO_OVERLAY_DURATION_MS', 3200),
        'INTRO_OVERLAY_IMAGE': intro_overlay_image,
        'INTRO_OVERLAY_IMAGE_URL': _resolve_intro_image_url(intro_overlay_image),
        'SHOW_SIDEBAR_ON_HOME_STARTUP': getattr(
            settings,
            'SHOW_SIDEBAR_ON_HOME_STARTUP',
            False
        ),
    }
