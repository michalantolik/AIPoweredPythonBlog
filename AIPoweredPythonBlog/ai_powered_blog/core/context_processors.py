from django.conf import settings


def intro_overlay_settings(request):
    return {
        'INTRO_OVERLAY_ENABLED': getattr(settings, 'INTRO_OVERLAY_ENABLED', False),
        'INTRO_OVERLAY_DURATION_MS': getattr(settings, 'INTRO_OVERLAY_DURATION_MS', 3200),
        'INTRO_OVERLAY_IMAGE': getattr(
            settings,
            'INTRO_OVERLAY_IMAGE',
            'images/intro/michal-portrait.png'
        ),
    }
