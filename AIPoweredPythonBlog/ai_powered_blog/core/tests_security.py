from django.test import TestCase, override_settings
from django.urls import reverse

from core.checks import production_security_checks


class SecurityHeadersTests(TestCase):
    @override_settings(
        APP_CSP_ENABLED=True,
        APP_CSP_DIRECTIVES={
            "default-src": ("'self'",),
            "script-src": ("'self'",),
            "style-src": ("'self'",),
            "img-src": ("'self'", "data:", "https:"),
            "font-src": ("'self'", "data:"),
            "connect-src": ("'self'",),
            "object-src": ("'none'",),
            "base-uri": ("'self'",),
            "frame-ancestors": ("'none'",),
            "form-action": ("'self'",),
        },
        APP_CSP_EXCLUDE_PATH_PREFIXES=("/admin/",),
        APP_PERMISSIONS_POLICY_ENABLED=True,
        APP_PERMISSIONS_POLICY={
            "camera": (),
            "geolocation": (),
            "microphone": (),
        },
        SECURE_CONTENT_TYPE_NOSNIFF=True,
        X_FRAME_OPTIONS="DENY",
        SECURE_REFERRER_POLICY="strict-origin-when-cross-origin",
    )
    def test_public_pages_return_security_headers(self):
        response = self.client.get(reverse("website:home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")
        self.assertEqual(
            response.headers["Referrer-Policy"],
            "strict-origin-when-cross-origin",
        )
        self.assertIn("default-src 'self'", response.headers["Content-Security-Policy"])
        self.assertIn("script-src 'self'", response.headers["Content-Security-Policy"])
        self.assertIn("camera=()", response.headers["Permissions-Policy"])
        self.assertIn("geolocation=()", response.headers["Permissions-Policy"])

    @override_settings(
        APP_CSP_ENABLED=True,
        APP_CSP_DIRECTIVES={
            "default-src": ("'self'",),
            "script-src": ("'self'",),
        },
        APP_CSP_EXCLUDE_PATH_PREFIXES=("/admin/",),
    )
    def test_admin_login_is_excluded_from_csp(self):
        response = self.client.get("/admin/login/")

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Content-Security-Policy", response.headers)


class ProductionSecurityChecksTests(TestCase):
    @override_settings(
        DEBUG=False,
        SECRET_KEY="django-insecure-xoj4nsk4w@+^4&3v6%$jeu3b(iior(4(&wbp25m2oibat#3_q+",
        ALLOWED_HOSTS=["*"],
        SECURE_HSTS_SECONDS=0,
    )
    def test_production_checks_fail_for_default_secret_and_wildcard_hosts(self):
        messages = production_security_checks(None, deploy=True)
        ids = {message.id for message in messages}

        self.assertIn("core.E001", ids)
        self.assertIn("core.E002", ids)
        self.assertIn("core.W001", ids)

    @override_settings(
        DEBUG=False,
        SECRET_KEY="very-long-production-secret-key-that-is-unique-and-safe-123456789",
        ALLOWED_HOSTS=["example.com"],
        SECURE_HSTS_SECONDS=3600,
    )
    def test_production_checks_pass_for_hardened_configuration(self):
        messages = production_security_checks(None, deploy=True)
        ids = {message.id for message in messages}

        self.assertNotIn("core.E001", ids)
        self.assertNotIn("core.E002", ids)
        self.assertNotIn("core.W001", ids)
