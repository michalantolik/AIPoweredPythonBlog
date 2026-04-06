from collections.abc import Iterable

from django.conf import settings


def _normalize_policy_value(value) -> str:
    if isinstance(value, str):
        return value.strip()

    if isinstance(value, Iterable):
        return " ".join(str(item).strip() for item in value if str(item).strip())

    return str(value).strip()


def _serialize_csp_directives(directives: dict[str, object]) -> str:
    parts: list[str] = []

    for directive, value in directives.items():
        if value is None:
            continue

        normalized = _normalize_policy_value(value)

        if normalized:
            parts.append(f"{directive} {normalized}")
        else:
            parts.append(directive)

    return "; ".join(parts)


def _serialize_permissions_policy(policy: dict[str, object]) -> str:
    parts: list[str] = []

    for feature, allowlist in policy.items():
        normalized = _normalize_policy_value(allowlist)
        parts.append(f"{feature}=({normalized})")

    return ", ".join(parts)


class SecurityHeadersMiddleware:
    """
    Adds modern browser security headers for the public site.

    CSP is intentionally skipped for Django admin paths because the admin uses
    inline scripts/styles that would otherwise require a looser policy.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        csp_excluded_prefixes = getattr(
            settings,
            "APP_CSP_EXCLUDE_PATH_PREFIXES",
            (),
        )

        is_csp_excluded = any(
            request.path.startswith(prefix)
            for prefix in csp_excluded_prefixes
        )

        if getattr(settings, "APP_CSP_ENABLED", True) and not is_csp_excluded:
            response.headers.setdefault(
                "Content-Security-Policy",
                _serialize_csp_directives(getattr(settings, "APP_CSP_DIRECTIVES", {})),
            )

        if getattr(settings, "APP_PERMISSIONS_POLICY_ENABLED", True):
            response.headers.setdefault(
                "Permissions-Policy",
                _serialize_permissions_policy(
                    getattr(settings, "APP_PERMISSIONS_POLICY", {})
                ),
            )

        return response
